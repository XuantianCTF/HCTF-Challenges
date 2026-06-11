CC = gcc
CFLAGS = -m64 -fno-stack-protector -fno-pie -no-pie -z noexecstack
LDLIBS = -lseccomp

all: New_World

New_World: New_World.c
	$(CC) $(CFLAGS) $< -o $@ $(LDLIBS)

run:
	./New_World

clean:
	rm -f New_World
