CC       = gcc
ASM      = nasm
ASMFLAGS = -f elf64
TARGET   = ctf_challenge
OBJS     = start.o logic.o core.o

.PHONY: all clean run

all: $(TARGET)

$(TARGET): $(OBJS)
	ld -o $@ $^ -e _start

start.o: start.asm
	$(ASM) $(ASMFLAGS) -o $@ $<

logic.o: logic.asm
	$(ASM) $(ASMFLAGS) -o $@ $<

core.o: core.asm
	$(ASM) $(ASMFLAGS) -o $@ $<

clean:
	rm -f $(OBJS) $(TARGET)

run: $(TARGET)
	./$(TARGET)
