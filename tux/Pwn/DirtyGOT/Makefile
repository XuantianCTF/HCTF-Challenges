CC = gcc
CFLAGS = -no-pie -fno-stack-protector
TARGET = chall

all: $(TARGET)

$(TARGET): chall.c
	$(CC) $(CFLAGS) -o $@ $^

LIBC   = /usr/lib/x86_64-linux-gnu/libc.so.6
LD     = /lib64/ld-linux-x86-64.so.2

dist: $(TARGET)
	@mkdir -p dist
	@cp $(TARGET) dist/
	@cp $(LIBC) dist/
	@cp $(LD) dist/
	@echo "[+] dist/ 目录:"
	@ls -la dist/

docker:
	docker build -t dirtygot .
	docker run -d --name dirtygot -p 1337:1337 dirtygot

clean:
	rm -f $(TARGET)
	rm -rf dist

.PHONY: all clean docker dist
