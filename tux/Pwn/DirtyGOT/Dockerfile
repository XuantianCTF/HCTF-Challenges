FROM ubuntu:22.04

RUN apt-get update && apt-get install -y xinetd gcc && rm -rf /var/lib/apt/lists/*

RUN useradd -m ctf

COPY chall.c /home/ctf/
RUN gcc -no-pie -fno-stack-protector -o /home/ctf/chall /home/ctf/chall.c && \
    chmod 755 /home/ctf/chall

COPY xinetd.conf /etc/xinetd.d/challenge

EXPOSE 1337

CMD ["/usr/sbin/xinetd", "-dontfork"]
