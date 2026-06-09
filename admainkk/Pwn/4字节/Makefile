CC = gcc
CFLAGS = -m32 -fno-stack-protector -fno-pie -no-pie -z noexecstack

all: four_bytes

four_bytes: four_bytes.c
	$(CC) $(CFLAGS) $< -o $@

run:
	./four_bytes

clean:
	rm -f four_bytes
