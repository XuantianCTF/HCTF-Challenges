FROM ubuntu:22.04 AS builder

RUN apt-get update && apt-get install -y gcc make

WORKDIR /build
COPY vuln.c .
RUN gcc vuln.c -o vuln

# ================= 阶段 2：构建最终运行环境 =================
FROM ubuntu:22.04

RUN apt-get update && apt-get install -y socat vim neovim build-essential && rm -rf /var/lib/apt/lists/*

# 创建真正的 Flag（放在沙盒外面）
RUN echo "HCTF{chroot_escape_is_too_easy}" > /flag

# 创建沙盒目录
WORKDIR /tmp/sandbox
RUN mkdir -p bin lib lib64

RUN cp /bin/sh /tmp/sandbox/bin/sh
RUN cp /lib/x86_64-linux-gnu/libc.so.6 /tmp/sandbox/lib/
RUN cp /lib64/ld-linux-x86-64.so.2 /tmp/sandbox/lib64/

WORKDIR /app
COPY --from=builder /build/vuln .

EXPOSE 10001

CMD ["socat", "TCP-LISTEN:10001,fork,reuseaddr", "EXEC:/app/vuln,stderr"]
