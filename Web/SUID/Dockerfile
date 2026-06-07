FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \
    openssh-server \
    && rm -rf /var/lib/apt/lists/*

# Create player user
RUN useradd -m -s /bin/bash player && echo "ctf:ctf" | chpasswd

# Set SUID bit on find so it runs as root
RUN chmod u+s /usr/bin/find

# Create the flag — only root can read it
RUN mkdir -p /root && \
    echo "HCTF{find_suid_exploit_2026}" > /root/flag.txt && \
    chmod 600 /root/flag.txt && \
    chown root:root /root/flag.txt

# Hint for the player
RUN echo "The flag is in /root/flag.txt, but I don't have permission to read it..." > /home/player/hint.txt && \
    chown player:player /home/player/hint.txt

# SSH configuration
RUN mkdir /var/run/sshd && \
    echo "PermitRootLogin no" >> /etc/ssh/sshd_config && \
    echo "PasswordAuthentication yes" >> /etc/ssh/sshd_config

EXPOSE 22

CMD ["/usr/sbin/sshd", "-D"]
