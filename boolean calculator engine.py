'''
###########################################
#         BOOLEAN CALCULATOR ENGINE       #
#                                         #
#                                         #
#                                         #
#           Python Version: 3.9.1         #
#     Written by: Santosh Subramanian     #
#                                         #
###########################################                                        

HONORS PROJECT: BOOLEAN CALCULATOR ENGINE (VLSI CAD LOGIC: PART1)
'''

import sys
import copy
from itertools import islice
def func_proc(new_file):
    PCN_CUBELIST=[]
    divlist=[]
    elim_space=[]
    prefinlist=[x.strip().split(' ') for x in new_file] #converting the file into a list
    for i in range(0,len(prefinlist)):
        if not prefinlist[i]==['']:
            elim_space.append(prefinlist[i]) #to eliminate unnecessary spaces from the list like ['']
    finlist=[list(map(int,x)) for x in elim_space] #converting string list elements into integers
    var_nos=finlist[0][0] #Total number of variables present in the given function
    cubelist_nos=finlist[1][0] #Total number of product terms present in the given function
    cubelist=copy.deepcopy(finlist)
    del cubelist[0:2] #deleting var and cube nos sublists as they are no longer necessary
    for x in range(0,cubelist_nos):
        del cubelist[x][0]  
    for i in cubelist:
        for j in range(1,(var_nos+1)):  #converting the cubelist into its Positional Cube Notation (PCN) 
            if (j in i):
                PCN_CUBELIST.append('01')
            elif((-j) in i):
                PCN_CUBELIST.append('10')
            else:
                PCN_CUBELIST.append('11')
    div=int(len(PCN_CUBELIST)/var_nos)
    for z in range(0,div):
        divlist.append(var_nos)
    PCN_CUBELIST_ITER=iter(PCN_CUBELIST)
    PCN_FINAL_CUBELIST=[list(islice(PCN_CUBELIST_ITER,elem)) for elem in divlist]
    return PCN_FINAL_CUBELIST,var_nos #final PCN cubelist

def drct_complement(PCN_FORM,var_nos): #directly complements if the length of the func is '1' (Demorgan's laws: A'BC= A+B'+C')
    direct_complement=[['11' for j in range(0,var_nos)] for i in range(0,var_nos)]
    count=0
    for x in range(0,var_nos):
        if(PCN_FORM[0][x]=='11'):
            count=count+1
        elif(PCN_FORM[0][x]=='10'):
            direct_complement[count][x]='01'
            count=count+1
        elif(PCN_FORM[0][x]=='01'):
            direct_complement[count][x]='10'
            count=count+1
    dc_cube=['11']*var_nos
    direct_complement=[x for x in direct_complement if x != dc_cube]
    return direct_complement

def split_var(PCN_FORM,var_nos): #to find the splitting variable.  Rules: Find the binate variable appearing in most cubes. If a tie, perform |T-C|
    #for each binate variable and select the one with the lowest value of |T-C|. Even then if its a tie, select one with the lowest index.
    #If there are no binate variables, check for unate variables. If there is a tie, go for the one with lowest index
    VAR_CUBELIST=[] 
    divisorlist=[]
    binate_cubelist=[] #contains binate cubelists. A cubelist is binate if it contains '01' and '10'
    unate_cubelist=[] #contains unate cubelists. A cubelist is unate if it contains either '01' or '10' and not both.   Ex: [01,01,11], [10,10,10],[01,11,11]
    count_cubelist=[] #contains the count of '11's from each cube in the binate/unate cubelist. The cube with the least no of '11's appears in most product terms. 
    T_C_cubelist=[] #contains the |T-C| value
    for y in range(0,var_nos):
        for x in range(0,len(PCN_FORM)):
            VAR_CUBELIST.append(PCN_FORM[x][y])
    divisor=int(len(VAR_CUBELIST)/len(PCN_FORM))
    for z in range(0,divisor):
        divisorlist.append(len(PCN_FORM))
    VAR_CUBELIST_ITER=iter(VAR_CUBELIST)
    VAR_FINAL_CUBELIST=[list(islice(VAR_CUBELIST_ITER,elem)) for elem in divisorlist]
    for i in VAR_FINAL_CUBELIST:
        if(('01' in i) and ('10' in i)):
            binate_cubelist.append(i)
        else:
            unate_cubelist.append(i)
    if(binate_cubelist==[]): 
        for i in unate_cubelist:
            counter=0
            for y in i:
                if(y=='11'):
                    counter=counter+1
            count_cubelist.append(counter)
        if(len(set(count_cubelist))==1): #returns 1 if all elements in a list are the same. 
            splitting_variable_cube=unate_cubelist[count_cubelist.index(count_cubelist[0])] #if '1', indicates a tie
            x_splitting_variable=VAR_FINAL_CUBELIST.index(splitting_variable_cube) 
        else:
            count_index=count_cubelist.index(min(count_cubelist)) #not a tie
            splitting_variable_cube=unate_cubelist[count_index]
            x_splitting_variable=VAR_FINAL_CUBELIST.index(splitting_variable_cube)
    else:
        for j in binate_cubelist:
            count=0
            for y in j:
                if(y=='11'):
                    count=count+1
            count_cubelist.append(count)
        if(len(set(count_cubelist))==1): #tie
            for z in binate_cubelist:
                true_form=0 #true form is '01'
                comp_form=0 #complement form is '10'
                for b in z:
                    if(b=='01'):
                        true_form=true_form+1 
                    elif(b=='10'):
                        comp_form=comp_form+1
                    else:
                        true_form=true_form
                        comp_form=comp_form
                T_C=true_form-comp_form
                if(T_C>=0): #or simply use abs(T_C)
                    T_C_final=T_C
                else:
                    T_C_final=-T_C
                T_C_cubelist.append(T_C_final)
            if(len(set(T_C_cubelist))==1): #tie (choose one with lowest index)
                splitting_variable_cube=binate_cubelist[T_C_cubelist.index(T_C_cubelist[0])]
                x_splitting_variable=VAR_FINAL_CUBELIST.index(splitting_variable_cube)
            else:
                TC_index=T_C_cubelist.index(min(T_C_cubelist))
                splitting_variable_cube=binate_cubelist[TC_index]
                x_splitting_variable=VAR_FINAL_CUBELIST.index(splitting_variable_cube)
        else:
            count_index=count_cubelist.index(min(count_cubelist))
            splitting_variable_cube=binate_cubelist[count_index]
            x_splitting_variable=VAR_FINAL_CUBELIST.index(splitting_variable_cube)
    return x_splitting_variable #our splitting variable found

def Cofactor_Calculator(PCN_FORM,splitting_variable,choice,var_nos):
    pos_neg=[]
    countcf=0
    temp='01'
    if choice=='01': #positive
        temp='10'
    for x in range(len(PCN_FORM)):
        if not PCN_FORM[x][splitting_variable]==temp: #for postitive cofactor  If '10' is present at spl cube index, ignore.
            #for negative cofactor: if '01' is present at splitting variable index, ignore
            pos_neg.append([])
            for y in range(len(PCN_FORM[x])):
                pos_neg[countcf].append(PCN_FORM[x][y])
            pos_neg[countcf][splitting_variable]='11' #at splitting variable index, change value to '11' 
            countcf=countcf+1
    dc=0
    for x in range(len(pos_neg)):
        counter1 = 0
        for y in range(var_nos):
            if pos_neg[x][y] == '11' :
                 counter1=counter1+1
        if counter1==var_nos:
            dc=1
            lis_t_p = x   
    if dc== 1 :
        dcc=[]
        dcc.append([])
        dcc[0] = ['11']*var_nos
        return dcc
    return pos_neg

def PCN_AND(function,splitting_variable,choice) : #ANDing splitting variable with cofactors { Ex: (x AND Complement(+ve CF)) OR (x' AND Complement(-ve CF))}
    for x in range(len(function)):
        function[x][splitting_variable]= choice
    return function

#ORing of functions
def PCN_OR(function_p,function_n): #shannon expansion complement version: (x AND Complement(+ve CF)) OR (x' AND Complement(-ve CF)))
    function_ret =[]
    function_ret.extend(function_p)
    function_ret.extend(function_n)
    return function_ret

#Function to write output into file
def printer(Out,vars_in):
    fh=open(r"C:\Users\user\Desktop\ProgrammingAssignment1Files\BOOL_CALC_ENG_OP_6.txt","w") #destination file location for output to be written
    fh.write(str(vars_in)+"\n")
    fh.write(str(len(Out))+"\n")
    for x in Out:
        y=[i for i in x if i != "11"]
        fh.write(str(len(y))+" ")
        for i in range(0,len(y)):
            if y[i] == "01":
                fh.write(str(i+1))
            elif y[i] == "10":
                fh.write(str(-(i+1)))
            if i != len(y)-1:
                fh.write(" ")
        fh.write("\n")  
    fh.close()

            
def Complement(PCN_FORM,var_nos):
    if(len(PCN_FORM)== 0):  # F has no cubes.
        return [[ '11' for y in range(0, var_nos)]]
    elif(len(PCN_FORM)== 1): # F has just 1 cube.
        return drct_complement(PCN_FORM,var_nos)
    else: #recursion
        splitting_variable=split_var(PCN_FORM,var_nos)
        Positive_Cofactor=Cofactor_Calculator(PCN_FORM,splitting_variable,'01',var_nos)
        Negative_Cofactor=Cofactor_Calculator(PCN_FORM,splitting_variable,'10',var_nos)
        Positive_Cofactor=Complement(Positive_Cofactor,var_nos)
        Negative_Cofactor=Complement(Negative_Cofactor,var_nos)
        AND_x=PCN_AND(Positive_Cofactor,splitting_variable,'01')
        AND_xbar=PCN_AND(Negative_Cofactor,splitting_variable,'10')
        return PCN_OR(AND_x,AND_xbar)

def unate_recursive_complement(file_to_read):
    test_locate=r"C:\Users\user\Desktop\ProgrammingAssignment1Files\BooleanCalculatorEngine\1.pcn" #file location
    index=test_locate.index("Engine")
    new=list(test_locate)
    new[index+7]=file_to_read #changes "file.pcn" automatically depending upon the input specified in cmd file
    location_of_file="".join(new)
    file=open(location_of_file,"r") #new file address
    PCN_FORM,var_nos=func_proc(file)
    Output=Complement(PCN_FORM,var_nos)
    printer(Output,var_nos)
    file.close()
    return Output,var_nos

def function_unate(function,var_nos): #to complement the already URP complemented PCN cubelist (NOT OPERATION)
    Output=Complement(function,var_nos)
    return Output

    
def main():
    print("Boolean Calculator Engine")
    print("By SANTOSH SUBRAMANIAN")
    eliminate=[]
    function_store_list=[]
    bool_file=open(r"C:\Users\user\Desktop\ProgrammingAssignment1Files\BooleanCalculatorEngine\cmd6.txt","r")
    boolean_calc_list=[x.strip().split(' ') for x in bool_file] #converting the file into a list
    for i in range(0,len(boolean_calc_list)):
        if not boolean_calc_list[i]==['']:
            eliminate.append(boolean_calc_list[i])
    print(eliminate)
    for k in range(0,51):
        function_store_list.append('') #creating a list full of '' to store resultant cubes in exact location as specified by the operating cmd file
    for i in eliminate:
        if(i[0]=='r'): #if first element in the i sublist is 'r', read file, do urc and store complement in the above created list,at the location specified in cmdfile
            file_to_read=i[1]
            tempor,var_nos=unate_recursive_complement(file_to_read)
            function_store_list[int(i[1])]=tempor
        elif(i[0]=='+'): #if '+' do OR operation
            tempor1=PCN_OR(function_store_list[int(i[2])],function_store_list[int(i[3])])
            function_store_list[int(i[1])]=tempor1
        elif(i[0]=='!'): #if '!' do a NOT operation [Basically do URC all over again]
            tempor2=function_unate(function_store_list[int(i[2])],var_nos)
            function_store_list[int(i[1])]=tempor2
        elif(i[0]=='&'): #AND OPERATION [EX: A AND B= NOT((NOT A)OR(NOT B))] you cant straightaway AND two cubelists. 
            tempor3=PCN_OR(function_store_list[int(i[2])],function_store_list[int(i[3])])
            tempor4=function_unate(tempor3,var_nos)
            function_store_list[int(i[1])]=tempor4
        elif(i[0]=='p'):
            print("\n")
            print("FINAL FUNCTION CUBELIST")
            print("\n")
            print(function_store_list[int(i[1])])
            printer(function_store_list[int(i[1])],var_nos) #final output after logical operations stored in destination file
        else:
            pass

main()
    
#the end

