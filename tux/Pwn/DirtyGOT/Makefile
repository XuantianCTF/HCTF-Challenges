CC = gcc
CFLAGS = -no-pie -fno-stack-protector
TARGET = chall

all: $(TARGET)

$(TARGET): chall.c
	$(CC) $(CFLAGS) -o $@ $^

docker:
	docker build -t dirtygot .
	docker run -d --name dirtygot -p 1337:1337 dirtygot

clean:
	rm -f $(TARGET)

.PHONY: all clean docker
