TARGET := example1

.PHONY: compile asm x86
compile:
	python compiler.py

asm:
	nasm -f elf64 $(TARGET).s

x86:
	gcc -o $(TARGET) $(TARGET).o -no-pie -g

run: compile asm x86
	./$(TARGET)
