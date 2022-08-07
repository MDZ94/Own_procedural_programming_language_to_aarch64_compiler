from myLexer import *
import ply.yacc as yacc
import ply.lex as lex
import sys
 
class MyParser:
 
    # CONSTRUCTOR
    def __init__(self):
        print("Parser called")
        self.parser = yacc.yacc(module=self)
 
    # DESTRUCTOR
    def __del__(self):
        print('Parser destructor called.')
 
    tokens = MyLexer.tokens

    Lines = ''

    output_file = ''

    lines_global_start = [
        '# Michal Dziarmaga file generated in AARCH64 assembly\n',
    '\n',
    '.global _start\n'
    ]

    lines_section_text = [
            '\n',
        '.section .text\n'
    ]

    lines_start = [
        '\n',
        '_start:\n'
    ]

    lines_section_function_definition = [
            '# System exit\n',
        '\n',
        '   mov x8, #0x5d\n'
        '   mov x0, #43\n'
        '   svc 0\n'
        ]

    lines_section_data = [
    '\n',
        '\n',
        '.section .data'
    ]
    lines_section_data_ascii = [
        '\n',
        '\n',
        '# Ascii \n'
    ]

    while_if_condition_flag = -1
    registry_while_if_condition_flag = []

    env = {}
    if_nested_level = -1
    if_instruction_counter = []
    inner_if_counters = []

    while_nested_level = -1
    while_instruction_counter = []

    function_variable_dictionary = {}
    
    

    def file_prepare(self, file_name):
        self.output_file = open(file_name+'.asm', "w")


    def file_closing(self):
        self.Lines = self.lines_global_start + self.lines_section_text + self.lines_start + self.lines_section_function_definition + self.lines_section_data + self.lines_section_data_ascii
        self.output_file.writelines(self.Lines)
        self.output_file.close()



    def fragment(self, p):

        if type(p) == tuple:
            if p[0] == 'main':
                self.fragment(p[1])
                return
            elif p[0] == 'exec':
                self.fragment(p[1])
                return
            elif p[0] == 'sequentional_exec':
                self.fragment(p[1])
                self.fragment(p[2])
                return
            elif p[0] == 'declare':
                if p[1] == '.ascii':
                    self.lines_section_data_ascii = self.lines_section_data_ascii +['\n'+ str(p[2])+':\n    '+ str(self.fragment(p[1]))+' ']
                else:
                    self.lines_section_data = self.lines_section_data +['\n'+ str(p[2])+':\n    '+ str(self.fragment(p[1]))+' ']
                return

            elif p[0] == 'assign':
                if p[2][0] == '+'or p[2][0] =='-' or p[2][0] == '/' or p[2][0] =='*':
                    self.fragment(p[2])
                    self.lines_start = self.lines_start+['  ldr x5, ='+str(p[1])+'\n  str w1, [x5]\n']

                    return

                elif p[1][0] == 'declare':
                    self.fragment(p[1])
                    if p[1][1] == '.ascii':
                        self.lines_section_data_ascii = self.lines_section_data_ascii +[str(self.fragment(p[2]))]
                        self.lines_section_data_ascii = self.lines_section_data_ascii +['\n '+str(p[1][2])+'len = . - '+str(p[1][2])]
                    else:
                        self.lines_section_data = self.lines_section_data +[str(self.fragment(p[2]))]
                    return
                elif p[2][0] == "variable":
                    self.lines_start = self.lines_start+['  ldr w1, '+str(self.fragment(p[2]))+'\n  ldr x5, ='+str(p[1])+'\n  str w1, [x5]\n']
                else:
                    self.lines_start = self.lines_start+['  mov w1, #'+str(self.fragment(p[2]))+'\n  ldr x5, ='+str(p[1])+'\n  str w1, [x5]\n']
                return
            elif p[0] == 'print':
                self.lines_start = self.lines_start+['\n# write system call\n   mov x8, #64\n   mov x0, #1\n   ldr x1, =' + str(self.fragment(p[1]))+ '\n   ldr x2, ='+str(self.fragment(p[1]))+'len\n   svc 0\n']
                return
            elif p[0] == 'if':

                self.registry_while_if_condition_flag = self.registry_while_if_condition_flag + [self.while_if_condition_flag]
                self.while_if_condition_flag = 1

                self.if_nested_level = self.if_nested_level+1

                if(len(self.if_instruction_counter)<self.if_nested_level+1):
                    self.if_instruction_counter.append(0)
                    self.inner_if_counters.append([])
                    self.inner_if_counters[self.if_nested_level].append(0)
                else:
                    self.inner_if_counters.append([])
                    self.if_instruction_counter[self.if_nested_level] = self.if_instruction_counter[self.if_nested_level]+1
                    self.inner_if_counters[self.if_nested_level].append(0)
                    

                self.fragment(p[1])
                self.lines_start = self.lines_start+['\n# if statement'+str(self.if_nested_level)+'_'+str(self.if_instruction_counter[self.if_nested_level])+'_'+str(self.inner_if_counters[self.if_nested_level][self.if_instruction_counter[self.if_nested_level]])+
                                                        '\nif_statement_'+str(self.if_nested_level)+'_'+str(self.if_instruction_counter[self.if_nested_level])+'_'+str(self.inner_if_counters[self.if_nested_level][self.if_instruction_counter[self.if_nested_level]])+':\n']
                self.fragment(p[2])
                self.lines_start = self.lines_start+['\n   b default_statement_'+str(self.if_nested_level)+'_'+str(self.if_instruction_counter[self.if_nested_level])+'\n']

                self.inner_if_counters[self.if_nested_level][self.if_instruction_counter[self.if_nested_level]] = self.inner_if_counters[self.if_nested_level][self.if_instruction_counter[self.if_nested_level]] +1

                self.lines_start = self.lines_start+['\n# if statement'+str(self.if_nested_level)+'_'+str(self.if_instruction_counter[self.if_nested_level])+'_'+str(self.inner_if_counters[self.if_nested_level][self.if_instruction_counter[self.if_nested_level]])+\
                                                        '\nif_statement_'+str(self.if_nested_level)+'_'+str(self.if_instruction_counter[self.if_nested_level])+'_'+str(self.inner_if_counters[self.if_nested_level][self.if_instruction_counter[self.if_nested_level]])+':\n']

                self.inner_if_counters[self.if_nested_level][self.if_instruction_counter[self.if_nested_level]] = self.inner_if_counters[self.if_nested_level][self.if_instruction_counter[self.if_nested_level]] +1

                self.fragment(p[3])
                self.if_nested_level = self.if_nested_level-1
                return
            elif p[0] == 'ifelse':
                self.fragment(p[1])
                self.lines_start = self.lines_start+['\n# if statement'+str(self.if_nested_level)+'_'+str(self.if_instruction_counter[self.if_nested_level])+'_'+str(self.inner_if_counters[self.if_nested_level][self.if_instruction_counter[self.if_nested_level]])+
                                                        '\nif_statement_'+str(self.if_nested_level)+'_'+str(self.if_instruction_counter[self.if_nested_level])+'_'+str(self.inner_if_counters[self.if_nested_level][self.if_instruction_counter[self.if_nested_level]])+':\n']
                self.fragment(p[2])
                self.lines_start = self.lines_start+['\n   b default_statement_'+str(self.if_nested_level)+'_'+str(self.if_instruction_counter[self.if_nested_level])+'\n']

                self.inner_if_counters[self.if_nested_level][self.if_instruction_counter[self.if_nested_level]] = self.inner_if_counters[self.if_nested_level][self.if_instruction_counter[self.if_nested_level]] +1

                self.lines_start = self.lines_start+['\n# if statement'+str(self.if_nested_level)+'_'+str(self.if_instruction_counter[self.if_nested_level])+'_'+str(self.inner_if_counters[self.if_nested_level][self.if_instruction_counter[self.if_nested_level]])+\
                                                        '\nif_statement_'+str(self.if_nested_level)+'_'+str(self.if_instruction_counter[self.if_nested_level])+'_'+str(self.inner_if_counters[self.if_nested_level][self.if_instruction_counter[self.if_nested_level]])+':\n']

                self.inner_if_counters[self.if_nested_level][self.if_instruction_counter[self.if_nested_level]] = self.inner_if_counters[self.if_nested_level][self.if_instruction_counter[self.if_nested_level]] +1
                                                        
                self.fragment(p[3])
                return
            elif p[0] == 'else':
                self.fragment(p[1])
                self.lines_start = self.lines_start+['\n# default statement'+str(self.if_nested_level)+'_'+str(self.if_instruction_counter[self.if_nested_level])+\
                                                        '\ndefault_statement_'+str(self.if_nested_level)+'_'+str(self.if_instruction_counter[self.if_nested_level])+':\n']

                self.while_if_condition_flag = self.registry_while_if_condition_flag[-1]
                self.registry_while_if_condition_flag.pop()
                return
            elif p[0] == '<':
                self.lines_start = self.lines_start+['\n# compare statement \n']
                if p[1][0] == 'digit':
                    self.lines_start = self.lines_start+['  mov w1, #'+str(self.fragment(p[1]))+'\n']
                else:
                    self.lines_start = self.lines_start+['  ldr w1, '+str(self.fragment(p[1]))+'\n']
                
                if p[2][0] == 'digit':
                    self.lines_start = self.lines_start+['  mov w2, #'+str(self.fragment(p[2]))]
                else:
                    self.lines_start = self.lines_start+['  ldr w2, '+str(self.fragment(p[2]))]
                if self.while_if_condition_flag == 1:
                    self.lines_start = self.lines_start+['\n  cmp w1, w2\n  blt if_statement_'+str(self.if_nested_level)+'_'+str(self.if_instruction_counter[self.if_nested_level])+'_'+str(self.inner_if_counters[self.if_nested_level][self.if_instruction_counter[self.if_nested_level]])+\
                                                        '\n  b if_statement_'+str(self.if_nested_level)+'_'+str(self.if_instruction_counter[self.if_nested_level])+'_'+str(self.inner_if_counters[self.if_nested_level][self.if_instruction_counter[self.if_nested_level]]+1)+'\n']
                elif self.while_if_condition_flag == 2:
                    self.lines_start = self.lines_start+['\n  cmp w1, w2\n  blt while_statement_'+str(self.while_nested_level)+'_'+str(self.while_instruction_counter[self.while_nested_level])+\
                                                        '\n  b end_while_statement_'+str(self.while_nested_level)+'_'+str(self.while_instruction_counter[self.while_nested_level])+'\n']
            elif p[0] == '<=':
                self.lines_start = self.lines_start+['\n# compare statement \n']
                if p[1][0] == 'digit':
                    self.lines_start = self.lines_start+['  mov w1, #'+str(self.fragment(p[1]))+'\n']
                else:
                    self.lines_start = self.lines_start+['  ldr w1, '+str(self.fragment(p[1]))+'\n']
                
                if p[2][0] == 'digit':
                    self.lines_start = self.lines_start+['  mov w2, #'+str(self.fragment(p[2]))]
                else:
                    self.lines_start = self.lines_start+['  ldr w2, '+str(self.fragment(p[2]))]
                if self.while_if_condition_flag == 1:
                    self.lines_start = self.lines_start+['\n  cmp w1, w2\n  ble if_statement_'+str(self.if_nested_level)+'_'+str(self.if_instruction_counter[self.if_nested_level])+'_'+str(self.inner_if_counters[self.if_nested_level][self.if_instruction_counter[self.if_nested_level]])+\
                                                        '\n  b if_statement_'+str(self.if_nested_level)+'_'+str(self.if_instruction_counter[self.if_nested_level])+'_'+str(self.inner_if_counters[self.if_nested_level][self.if_instruction_counter[self.if_nested_level]]+1)+'\n']

            elif p[0] == '>':
                self.lines_start = self.lines_start+['\n# compare statement \n']
                if p[1][0] == 'digit':
                    self.lines_start = self.lines_start+['  mov w1, #'+str(self.fragment(p[1]))+'\n']
                else:
                    self.lines_start = self.lines_start+['  ldr w1, '+str(self.fragment(p[1]))+'\n']
                
                if p[2][0] == 'digit':
                    self.lines_start = self.lines_start+['  mov w2, #'+str(self.fragment(p[2]))]
                else:
                    self.lines_start = self.lines_start+['  ldr w2, '+str(self.fragment(p[2]))]
                if self.while_if_condition_flag == 1:
                    self.lines_start = self.lines_start+['\n  cmp w1, w2\n  bgt if_statement_'+str(self.if_nested_level)+'_'+str(self.if_instruction_counter[self.if_nested_level])+'_'+str(self.inner_if_counters[self.if_nested_level][self.if_instruction_counter[self.if_nested_level]])+\
                                                        '\n  b if_statement_'+str(self.if_nested_level)+'_'+str(self.if_instruction_counter[self.if_nested_level])+'_'+str(self.inner_if_counters[self.if_nested_level][self.if_instruction_counter[self.if_nested_level]]+1)+'\n']
            elif p[0] == '>=':
                self.lines_start = self.lines_start+['\n# compare statement \n']
                if p[1][0] == 'digit':
                    self.lines_start = self.lines_start+['  mov w1, #'+str(self.fragment(p[1]))+'\n']
                else:
                    self.lines_start = self.lines_start+['  ldr w1, '+str(self.fragment(p[1]))+'\n']
                
                if p[2][0] == 'digit':
                    self.lines_start = self.lines_start+['  mov w2, #'+str(self.fragment(p[2]))]
                else:
                    self.lines_start = self.lines_start+['  ldr w2, '+str(self.fragment(p[2]))]

                if self.while_if_condition_flag == 1:
                    self.lines_start = self.lines_start+['\n  cmp w1, w2\n  bge if_statement_'+str(self.if_nested_level)+'_'+str(self.if_instruction_counter[self.if_nested_level])+'_'+str(self.inner_if_counters[self.if_nested_level][self.if_instruction_counter[self.if_nested_level]])+\
                                                        '\n  b if_statement_'+str(self.if_nested_level)+'_'+str(self.if_instruction_counter[self.if_nested_level])+'_'+str(self.inner_if_counters[self.if_nested_level][self.if_instruction_counter[self.if_nested_level]]+1)+'\n'] 
            elif p[0] == '==':
                self.lines_start = self.lines_start+['\n# compare statement \n']
                if p[1][0] == 'digit':
                    self.lines_start = self.lines_start+['  mov w1, #'+str(self.fragment(p[1]))+'\n']
                else:
                    self.lines_start = self.lines_start+['  ldr w1, '+str(self.fragment(p[1]))+'\n']
                
                if p[2][0] == 'digit':
                    self.lines_start = self.lines_start+['  mov w2, #'+str(self.fragment(p[2]))]
                else:
                    self.lines_start = self.lines_start+['  ldr w2, '+str(self.fragment(p[2]))]
                if self.while_if_condition_flag == 1:
                    self.lines_start = self.lines_start+['\n  cmp w1, w2\n  beq if_statement_'+str(self.if_nested_level)+'_'+str(self.if_instruction_counter[self.if_nested_level])+'_'+str(self.inner_if_counters[self.if_nested_level][self.if_instruction_counter[self.if_nested_level]])+\
                                                        '\n  b if_statement_'+str(self.if_nested_level)+'_'+str(self.if_instruction_counter[self.if_nested_level])+'_'+str(self.inner_if_counters[self.if_nested_level][self.if_instruction_counter[self.if_nested_level]]+1)+'\n']                                                                      
            elif p[0] == 'digit':
                return p[1]
            elif p[0] == 'variable':
                return p[1]
            elif p[0] == '+':
                self.lines_start = self.lines_start+['\n# Addition\n']
                self.lines_start = self.lines_start+['  stp w2, w3, [sp, #-16]!\n']
                if p[1][0] == 'digit':
                    self.lines_start = self.lines_start+['  mov w2, #'+str(self.fragment(p[1]))+'\n']
                elif p[1][0] == 'variable':
                    self.lines_start = self.lines_start+['  ldr w2, #'+str(self.fragment(p[1]))+'\n']
                else:
                    self.fragment(p[1])
                    self.lines_start = self.lines_start+['  mov w2, w1\n']
                if p[2][0] == 'digit':
                    self.lines_start = self.lines_start+['  mov w3, #'+str(self.fragment(p[2]))+'\n']
                elif p[2][0] == 'variable':
                    self.lines_start = self.lines_start+['  ldr w3, #'+str(self.fragment(p[2]))+'\n']
                else:
                    self.fragment(p[2])
                    self.lines_start = self.lines_start+['  mov w3, w1\n']
                self.lines_start = self.lines_start+['  add w1, w2, w3\n']
                self.lines_start = self.lines_start+['  ldp w2, w3, [sp], #16\n']
                return
            elif p[0] == '-':
                self.lines_start = self.lines_start+['\n# Substitution\n']
                self.lines_start = self.lines_start+['  stp w2, w3, [sp, #-16]!\n']
                if p[1][0] == 'digit':
                    self.lines_start = self.lines_start+['  mov w2, #'+str(self.fragment(p[1]))+'\n']
                elif p[1][0] == 'variable':
                    self.lines_start = self.lines_start+['  ldr w2, #'+str(self.fragment(p[1]))+'\n']
                else:
                    self.fragment(p[1])
                    self.lines_start = self.lines_start+['  mov w2, w1\n']
                if p[2][0] == 'digit':
                    self.lines_start = self.lines_start+['  mov w3, #'+str(self.fragment(p[2]))+'\n']
                elif p[2][0] == 'variable':
                    self.lines_start = self.lines_start+['  ldr w3, #'+str(self.fragment(p[2]))+'\n']
                else:
                    self.fragment(p[2])
                    self.lines_start = self.lines_start+['  mov w3, w1\n']
                self.lines_start = self.lines_start+['  sub w1, w2, w3\n']
                self.lines_start = self.lines_start+['  ldp w2, w3, [sp], #16\n']
                return
            elif p[0] == '*':
                self.lines_start = self.lines_start+['\n# Multiplication\n']
                self.lines_start = self.lines_start+['  stp w2, w3, [sp, #-16]!\n']
                if p[1][0] == 'digit':
                    self.lines_start = self.lines_start+['  mov w2, #'+str(self.fragment(p[1]))+'\n']
                elif p[1][0] == 'variable':
                    self.lines_start = self.lines_start+['  ldr w2, #'+str(self.fragment(p[1]))+'\n']
                else:
                    self.fragment(p[1])
                    self.lines_start = self.lines_start+['  mov w2, w1\n']
                if p[2][0] == 'digit':
                    self.lines_start = self.lines_start+['  mov w3, #'+str(self.fragment(p[2]))+'\n']
                elif p[2][0] == 'variable':
                    self.lines_start = self.lines_start+['  ldr w3, #'+str(self.fragment(p[2]))+'\n']
                else:
                    self.fragment(p[2])
                    self.lines_start = self.lines_start+['  mov w3, w1\n']
                self.lines_start = self.lines_start+['  mul w1, w2, w3\n']
                self.lines_start = self.lines_start+['  ldp w2, w3, [sp], #16\n']
                return
            elif p[0] == '/':
                self.lines_start = self.lines_start+['\n# Division\n']
                self.lines_start = self.lines_start+['  stp w2, w3, [sp, #-16]!\n']
                if p[1][0] == 'digit':
                    self.lines_start = self.lines_start+['  mov w2, #'+str(self.fragment(p[1]))+'\n']
                elif p[1][0] == 'variable':
                    self.lines_start = self.lines_start+['  ldr w2, #'+str(self.fragment(p[1]))+'\n']
                else:
                    self.fragment(p[1])
                    self.lines_start = self.lines_start+['  mov w2, w1\n']
                if p[2][0] == 'digit':
                    self.lines_start = self.lines_start+['  mov w3, #'+str(self.fragment(p[2]))+'\n']
                elif p[2][0] == 'variable':
                    self.lines_start = self.lines_start+['  ldr w3, #'+str(self.fragment(p[2]))+'\n']
                else:
                    self.fragment(p[2])
                    self.lines_start = self.lines_start+['  mov w3, w1\n']
                self.lines_start = self.lines_start+['  sdiv w1, w2, w3\n']
                self.lines_start = self.lines_start+['  ldp w2, w3, [sp], #16\n']
                return     
            elif p[0] == 'while':
                self.registry_while_if_condition_flag = self.registry_while_if_condition_flag + [self.while_if_condition_flag]
                self.while_if_condition_flag = 2

                self.while_nested_level = self.while_nested_level+1

                if(len(self.while_instruction_counter)<self.while_nested_level+1):
                    self.while_instruction_counter.append(0)
                else:
                    self.while_instruction_counter[self.while_nested_level] = self.while_instruction_counter[self.while_nested_level]+1
                
                self.fragment(p[1])
                self.lines_start = self.lines_start+['\n# while_statement_'+str(self.while_nested_level)+'_'+str(self.while_instruction_counter[self.while_nested_level])+
                                                        '\nwhile_statement_'+str(self.while_nested_level)+'_'+str(self.while_instruction_counter[self.while_nested_level])+':\n']
                self.fragment(p[2])
                self.fragment(p[1])
                
                self.lines_start = self.lines_start+['\n# end_while_statement_'+str(self.while_nested_level)+'_'+str(self.while_instruction_counter[self.while_nested_level])+
                                                        '\nend_while_statement_'+str(self.while_nested_level)+'_'+str(self.while_instruction_counter[self.while_nested_level])+':\n']

                self.while_nested_level = self.while_nested_level-1
                self.while_if_condition_flag = self.registry_while_if_condition_flag[-1]
                self.registry_while_if_condition_flag.pop()
                return
            elif p[0] == 'blocks':
                if p[1][0] == 'main':
                    self.fragment(p[1])
                    self.fragment(p[2])
                elif p[2][0] == 'main':
                    self.fragment(p[2])
                    self.fragment(p[1])
                else:
                    self.fragment(p[2])
                    self.fragment(p[1])              
                return
            elif p[0] == 'func':
                self.lines_start = self.lines_start+['\n   b '+str(p[1])+'_jump\n']
                self.lines_start = self.lines_start+['\n#'+str(p[1])+'\n']
                if(p[3] != ''):
                    self.fragment(p[3])
                self.lines_start = self.lines_start+['\n'+str(p[1])+':\n']
                self.lines_start = self.lines_start+['  stp w2, w3, [sp, #-16]!\n']
                self.lines_start = self.lines_start+['  stp w4, w5, [sp, #-16]!\n']

                self.fragment(p[4])
                self.lines_start = self.lines_start+['  ldp w4, w5, [sp], #16\n']
                self.lines_start = self.lines_start+['  ldp w2, w3, [sp], #16\n']
                self.lines_start = self.lines_start+['\n   ret\n']

                self.lines_start = self.lines_start+['\n'+str(p[1])+'_jump:\n']
                
                return
            elif p[0] == 'func_use':
                if(p[1] != ''):
                    self.fragment(p[2])
                self.lines_start = self.lines_start+['\n   bl '+str(p[1])+'\n']
            elif p[0] == 'expressions':
                self.fragment(p[1])
                self.fragment(p[2])
                return
            elif p[0] == ',':
                self.fragment(p[1])
                self.fragment(p[2])
                return
        else:
            return p

    precedence = (  

    ('left','PLUS','MINUS'),
    ('left', 'MULTIPLY', 'DIVIDE')
    )

    def p_code(self, p):
        '''
        code    : code_block
                | code_blocks
        '''
        print(p[1])
        self.fragment(p[1])
        

    def p_code_blocks(self, p):
            '''
            code_blocks : code_block code_blocks
                        | code_block code_block
            '''
            p[0]=('blocks', p[1],p[2])
    
    def p_code_block(self, p):
        '''
        code_block  : main
                    | funct_def 
        '''
        p[0]=p[1]

        # FUNCTION USE

    def p_function_use(self, p):
        '''
        instruction   : NAME LEFT_BRACKET empty RIGHT_BRACKET SEMICOLON
                    | NAME LEFT_BRACKET expression RIGHT_BRACKET SEMICOLON
                    | NAME LEFT_BRACKET function_input RIGHT_BRACKET SEMICOLON
        '''
        p[0] = ('func_use',p[1],p[3])

    def p_var_func_input(self,p):
        '''
        function_input  : expression COMA expression
                        | expression COMA function_input
        '''
        p[0] = (p[2], p[1], p[3])

        # FUNCTION DEFINITION

    def p_function_def(self, p):
        '''
        funct_def   : INT_FUN NAME funct_param LEFT_CURLY_BRACKET instruction RIGHT_CURLY_BRACKET
                    | VOID NAME funct_param LEFT_CURLY_BRACKET instruction RIGHT_CURLY_BRACKET
        '''
        p[0] = ('func',p[2],p[1],p[3],p[5])

    def p_function_parameters(self, p):
        '''
        funct_param : LEFT_BRACKET empty RIGHT_BRACKET
                    | LEFT_BRACKET expression RIGHT_BRACKET
                    | LEFT_BRACKET expressions RIGHT_BRACKET
        '''
        p[0] = (p[2])

    def p_expressions(self, p):
        '''
        expressions : expression COMA expression
                    | expressions COMA expression
        '''
        p[0] = ('expressions',p[1],p[3])

    

    def p_main_code(self, p):
        '''
        main : MAIN LEFT_CURLY_BRACKET instruction RIGHT_CURLY_BRACKET
             | MAIN LEFT_CURLY_BRACKET condition RIGHT_CURLY_BRACKET
             | MAIN LEFT_CURLY_BRACKET empty RIGHT_CURLY_BRACKET
        '''
        p[0] = (p[1],p[3])


    def p_return(self,p):
        '''
        instruction : RETURN instruction 
        '''
        p[0] = (p[1], p[2])

    def p_condition(self,p):
        '''
        condition : LEFT_BRACKET expression MORE expression RIGHT_BRACKET
                   | LEFT_BRACKET expression LESS expression RIGHT_BRACKET
                   | LEFT_BRACKET expression MORE_OR_EQUAL expression RIGHT_BRACKET
                   | LEFT_BRACKET expression LESS_OR_EQUAL expression RIGHT_BRACKET
                   | LEFT_BRACKET expression IS_EQUAL expression RIGHT_BRACKET
        '''
        p[0] = (p[3], p[2], p[4])


        # WHILE DECLARATION

    def p_while(self,p):
        '''
        instruction : WHILE condition LEFT_CURLY_BRACKET instruction RIGHT_CURLY_BRACKET
        '''
        p[0] = (p[1],p[2],p[4])

        # IF BLOCK DECLARATION

    def p_if(self,p):
        '''
        instruction : IF condition LEFT_CURLY_BRACKET instruction RIGHT_CURLY_BRACKET else
                   | IF condition LEFT_CURLY_BRACKET instruction RIGHT_CURLY_BRACKET if_else_block
        '''
        p[0] = (p[1],p[2],p[4],p[6])

    def p_if_else(self,p):
        '''
        if_else_block : IF_ELSE condition LEFT_CURLY_BRACKET instruction RIGHT_CURLY_BRACKET else
                      | IF_ELSE condition LEFT_CURLY_BRACKET instruction RIGHT_CURLY_BRACKET if_else_block
        '''
        p[0] = (p[1],p[2],p[4],p[6])

    def p_else(self,p):
        '''
        else    : ELSE LEFT_CURLY_BRACKET instruction RIGHT_CURLY_BRACKET
                | ELSE LEFT_CURLY_BRACKET empty RIGHT_CURLY_BRACKET
        '''
        p[0] = (p[1],p[3])

        # BASE MATH 

    def p_expression(self,p):
        '''
        expression  : expression MULTIPLY expression
                    | expression DIVIDE expression
                    | expression PLUS expression
                    | expression MINUS expression
        '''
        p[0] =  (p[2], p[1], p[3])

    def p_base_instruction(self,p):
        '''
        instruction : expression SEMICOLON
                    | declaration SEMICOLON
        '''
        p[0] = ('exec',p[1])

        # JOINING EXPRESSION IN CODE

    def p_instruction_collector(self,p):
        '''
        instruction    : instruction instruction
        '''
        p[0] = ('sequentional_exec',p[1], p[2])

        # INTEGER

    def p_int(self,p):
        '''
        expression : INT
        '''
        p[0] = ('digit',p[1])

    def p_Expression_int_var(self,p):
        '''
        expression : NAME
        '''
        p[0] = ('variable',p[1])
    def p_Expression_string_var(self,p):
        '''
        expression  : APOSTROF NAME APOSTROF
        '''
        p[0] = ('\"'+p[2]+'\\n\"')

    def p_var_int_decl(self,p):
        '''
        declaration : INT_FUN NAME
        '''
        p[0] = ('declare','.word',p[2])

    def p_var_str_decl(self,p):
        '''
        declaration : STRING NAME 
        '''
        p[0] = ('declare','.ascii',p[2])

    def p_expression_var_assign(self,p):
        '''
        expression  : declaration EQUALS expression
                    | NAME EQUALS expression
        '''
        p[0] = ('assign',p[1],p[3])

    def p_var_declarations(self,p):
        '''
        declarations    : declaration COMA declaration
                        | declaration COMA declarations
        '''
        p[0] = (p[1],p[3])

    def p_print(self,p):
        '''
        instruction : PRINT LEFT_BRACKET expression RIGHT_BRACKET SEMICOLON
        '''
        p[0] = (p[1],p[3])


    def p_error(self,p):
        print("Syntax error found!")

    def p_empty(self,p):
        '''
        empty :
        '''
        p[0] = ''

