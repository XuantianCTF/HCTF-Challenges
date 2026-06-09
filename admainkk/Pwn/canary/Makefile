CC = gcc
CFLAGS = -m64 -fno-pie -no-pie -z noexecstack

all: canary

canary: canary.c
	$(CC) $(CFLAGS) $< -o $@

run:
	./canary

clean:
	rm -f canary
