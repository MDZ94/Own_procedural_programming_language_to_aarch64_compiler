# Michal Dziarmaga file generated in AARCH64 assembly

.global _start

.section .text

_start:
  ldr w1, z
  ldr x5, =a
  str w1, [x5]
  ldr w1, g
  ldr x5, =b
  str w1, [x5]

   bl new2

   b new2_jump

#new2

new2:
  stp w2, w3, [sp, #-16]!
  stp w4, w5, [sp, #-16]!

# compare statement 
  ldr w1, a
  ldr w2, b
  cmp w1, w2
  beq if_statement_0_0_0
  b if_statement_0_0_1

# if statement0_0_0
if_statement_0_0_0:

# write system call
   mov x8, #64
   mov x0, #1
   ldr x1, =o
   ldr x2, =olen
   svc 0

   b default_statement_0_0

# if statement0_0_1
if_statement_0_0_1:

# write system call
   mov x8, #64
   mov x0, #1
   ldr x1, =l
   ldr x2, =llen
   svc 0

# default statement0_0
default_statement_0_0:
  ldp w4, w5, [sp], #16
  ldp w2, w3, [sp], #16

   ret

new2_jump:
# System exit

   mov x8, #0x5d
   mov x0, #43
   svc 0


.section .data
z:
    .word 11
g:
    .word 10
a:
    .word 0
b:
    .word 0

# Ascii 

o:
    .ascii "Hello\n"
 olen = . - o
l:
    .ascii "Goodbye\n"
 llen = . - l