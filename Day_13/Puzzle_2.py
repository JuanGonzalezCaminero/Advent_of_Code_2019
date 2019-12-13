import numpy as np
import time
from os import system

class Intcode_computer:
    def __init__(self, intcode, screen):
        #Append as many zeros after the code to the memory as the length 
        #of the original memory
        self.intcode = intcode
        self.intcode.extend([0 for i in range(100*len(intcode))])
        self.relative_base = 0
        self.program_counter = 0
        self.screen=screen
        self.output_buffer=[]
        self.score=0
        self.ball_position = []
        self.bar_position = []
    def run_program(self):
        #Execute the program
        while True:
            opcode=int(str(self.intcode[self.program_counter])[-2:])
            #Extremely unefficient switch:
            #3 parameter instructions
            if opcode==1 or opcode==2 or opcode==7 or opcode==8:
                #print("Opcode: " + str(intcode[program_counter]))
                param_1_mode=int(str(self.intcode[self.program_counter])[-3]) if\
                len(str(self.intcode[self.program_counter]))>=3 else 0
                param_2_mode=int(str(self.intcode[self.program_counter])[-4]) if\
                len(str(self.intcode[self.program_counter]))>=4 else 0
                param_3_mode=int(str(self.intcode[self.program_counter])[-5]) if\
                len(str(self.intcode[self.program_counter]))>=5 else 0

                param_1=self.get_value(param_1_mode, self.intcode[self.program_counter+1])
                param_2=self.get_value(param_2_mode, self.intcode[self.program_counter+2])
                
                #The last parameter is for writing, so we don't need the value of the
                #position it points to but the index of that position, which will be
                #the parameter itself in mode 0 and the parameter plus the base in mode 2
                if param_3_mode==0:
                    param_3=intcode[self.program_counter+3]
                elif param_3_mode==2:
                    param_3=intcode[self.program_counter+3]+self.relative_base
                #ADD
                if opcode==1:
                    self.intcode[param_3]=param_1+param_2
                #PRODUCT
                elif opcode==2:
                    self.intcode[param_3]=param_1*param_2
                #LESS THAN
                elif opcode==7:
                    self.intcode[param_3]=1 if param_1<param_2 else 0
                #EQUALS
                elif opcode==8:
                    self.intcode[param_3]=1 if param_1==param_2 else 0
                self.program_counter+=4
            #2 parameter instructions
            elif opcode==5 or opcode==6:
                param_1_mode=int(str(self.intcode[self.program_counter])[-3]) if\
                len(str(self.intcode[self.program_counter]))>=3 else 0
                param_2_mode=int(str(self.intcode[self.program_counter])[-4]) if\
                len(str(self.intcode[self.program_counter]))>=4 else 0
                param_1=self.get_value(param_1_mode, self.intcode[self.program_counter+1])
                param_2=self.get_value(param_2_mode, self.intcode[self.program_counter+2])
                #JUMP IF TRUE
                if opcode==5:
                    if param_1!=0:
                        self.program_counter=param_2
                    else:
                        self.program_counter+=3
                #JUMP IF FALSE
                elif opcode==6:
                    if param_1==0:
                        self.program_counter=param_2
                    else:
                        self.program_counter+=3

            #1 parameter instructions
            elif opcode==3 or opcode==4 or opcode==9:
                #READ
                if opcode==3:
                    time.sleep(0.0001)
                    system('clear')
                    self.render()
                    if self.ball_position[1]>self.bar_position[1]:
                        needed_move = 1
                    elif self.ball_position[1]<self.bar_position[1]:
                        needed_move = -1
                    else:
                        needed_move = 0

                    param_1_mode=int(str(self.intcode[self.program_counter])[-3]) if\
                    len(str(self.intcode[self.program_counter]))>=3 else 0
                    if param_1_mode==0:
                        #self.intcode[self.intcode[self.program_counter+1]] = int(input())
                        self.intcode[self.intcode[self.program_counter+1]] = needed_move
                    elif param_1_mode==2:
                        #self.intcode[self.intcode[self.program_counter+1]+self.relative_base] =\
                        #    int(input())
                        self.intcode[self.intcode[self.program_counter+1]+self.relative_base] = needed_move
                #WRITE
                elif opcode==4:
                    param_1_mode=int(str(self.intcode[self.program_counter])[-3]) if\
                    len(str(self.intcode[self.program_counter]))>=3 else 0
                    param_1=self.get_value(param_1_mode, self.intcode[self.program_counter+1])
                    #print(param_1)
                    self.print_to_screen(param_1)
                #INCREASE RELATIVE BASE VALUE
                elif opcode==9:
                    param_1_mode=int(str(self.intcode[self.program_counter])[-3]) if\
                    len(str(self.intcode[self.program_counter]))>=3 else 0
                    param_1=self.get_value(param_1_mode, self.intcode[self.program_counter+1])
                    self.relative_base+=param_1
                self.program_counter+=2
            elif opcode==99:
                time.sleep(0.0001)
                system('clear')
                self.render()
                print("Program complete")
                break
            else:
                print("An error has occurred")
                break
    def get_value(self, parameter_mode, parameter):
        '''
        Returns the value of the parameter based on it's mode. For mode
        0 the value returned is the value stored in the memory (intcode)
        position indicated by the parameter. For mode 1, the value of
        the parameter is returned
        '''
        if parameter_mode==0:
            return self.intcode[parameter]
        elif parameter_mode==1:
            return parameter
        elif parameter_mode==2:
            return self.intcode[parameter+self.relative_base]

    def print_to_screen(self, parameter):
        if len(self.output_buffer)!=2:
            self.output_buffer.append(parameter)
        else:
            self.output_buffer.append(parameter)
            #print(self.output_buffer)
            if self.output_buffer[-1]==0:
                self.screen[self.output_buffer[1]][self.output_buffer[0]]= 'em'
            elif self.output_buffer[-1]==1:
                self.screen[self.output_buffer[1]][self.output_buffer[0]]= 'wa'
            elif self.output_buffer[-1]==2:
                self.screen[self.output_buffer[1]][self.output_buffer[0]]= 'bl'
            elif self.output_buffer[-1]==3:
                self.screen[self.output_buffer[1]][self.output_buffer[0]]= 'hp'
                self.bar_position=[self.output_buffer[1], self.output_buffer[0]]
            elif self.output_buffer[-1]==4:
                self.screen[self.output_buffer[1]][self.output_buffer[0]]= 'ba'
                self.ball_position=[self.output_buffer[1], self.output_buffer[0]]
            elif self.output_buffer[1]==0 and self.output_buffer[0]==-1:
                self.score=self.output_buffer[-1]
            self.output_buffer=[]

    def render(self):
        for line in self.screen:
            print("")
            for i in line:
                if i=="em":
                    print(" ", end="")
                elif i=="wa":
                    print("▩", end="")
                elif i=="bl":
                    print("▣", end="")
                elif i=="hp":
                    print("▭", end="")
                elif i=="ba":
                    print("◯", end="")
        print("")
        print(self.score)
                
f = open("input")
intcode = [int(i) for i in f.read().split(",")]
f.close()
intcode[0]=2
#intcode = [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]
screen=np.zeros((22,37), dtype=object)
computer = Intcode_computer(intcode, screen)
#np.sum(computer.screen=="bl")
computer.run_program()
    
