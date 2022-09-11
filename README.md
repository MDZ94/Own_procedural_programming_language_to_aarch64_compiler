# Own_procedural_programming_language_to_aarch64_compiler

## The aim of the project:

###New primitive procedural language (similar to C) to aarch64 assembly compiler using Python PLY

The program compiles new structural language to Aarch64 Assembly.

## Technology used in project

Project is written in Python language
with PLY packege: https://www.dabeaz.com/ply/

## Quick tutorial

### Examples of base language syntax

The basic examples of new language syntax are in ./tests folder. The advanced documentation of project is in file DOKUMENTACJA_PROJEKTU in main folder of the project

### Using compilator

In order to use compilator you need to start teminal commad 

```
python myCompiler [filename with program written in new programmming language] [name of file which will be created with assembly code file (the .asm extension will be added to the name)]
```

### Running assembly code

To run generated assembly code you need to start all commands written in MakeFile. You can run MakeFile in after correnting the file name (default tommorow.asm) or use all commands written in MakeFile to run generated code.
