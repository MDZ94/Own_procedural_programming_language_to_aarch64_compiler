default: 
	aarch64-linux-gnu-as tommorow.asm -o tommorow.o 
	aarch64-linux-gnu-gcc tommorow.o -o tommorow.elf -nostdlib -static
	qemu-aarch64 ./tommorow.elf  