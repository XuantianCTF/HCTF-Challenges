CC       = gcc
ASM      = nasm
CFLAGS   = -no-pie -Wall -Wextra -O2
ASMFLAGS = -f elf64
TARGET   = ctf_challenge
OBJS     = main.o logic.o

.PHONY: all clean run

all: $(TARGET)

$(TARGET): $(OBJS)
	$(CC) $(CFLAGS) -o $@ $^

main.o: main.c
	$(CC) $(CFLAGS) -c -o $@ $<

logic.o: logic.asm
	$(ASM) $(ASMFLAGS) -o $@ $<

clean:
	rm -f $(OBJS) $(TARGET)

run: $(TARGET)
	./$(TARGET)
