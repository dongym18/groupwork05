# -*- coding: utf-8 -*-
"""
Created on Sat Mar 21 10:09:38 2020

This file is written to filter the conditional git diff statements 
and store txt files in the same file path.

Conditions to be met include:
multiple file changed,
for at least some those files: add == remove,
for some files: add> remove.
Of course there is no files add<remove.
eg.git diff --numstat HEAD~467..HEAD~466
1       1       drivers/clk/at91/at91sam9260.c
1       1       drivers/clk/at91/at91sam9rl.c
1       1       drivers/clk/at91/at91sam9x5.c
1       1       drivers/clk/at91/pmc.c
1       1       drivers/clk/at91/sama5d2.c
1       1       drivers/clk/at91/sama5d4.c
40      22      drivers/clk/clk.c
2       0       drivers/clk/imx/clk-composite-8m.c
1       0       drivers/clk/imx/clk-imx7ulp.c
1       1       drivers/clk/imx/clk-pll14xx.c
4       2       drivers/clk/qcom/gcc-sc7180.c
2       0       drivers/clk/qcom/gpucc-msm8998.c

The required parameters from left to right are: 
the minimum HEAD value, 
the maximum HEAD value, 
the local warehouse address, 
the minimum number of rows recorded, 
the maximum number of rows recorded, 
"add">"remove" the minimum number of rows, 
"add"="remove" the minimum number of rows.
"""
__copyright__ = "2020, Lanzhou University"
__license__ = 'GPLV2'
__author__ = "Group 5"
__email__ = "yuhaozhang18@lzu.edu.cn"
__status__ = "done"


from subprocess import Popen, PIPE, DEVNULL

def GitDiff(HEAD_head, HEAD_end, repo, min_lines, max_lines, min_greater, min_equal):
    
    commund_list = []#Create an empty list to include eligible git communds.
    
    #Filter each commund by looping through the communds.
    for i in range(HEAD_head, HEAD_end+1):
        head1 = str(i)#First number.
        head2 = str(i-1)#Second number.
        gitdiff = "git diff --numstat HEAD~" + head1 + "..HEAD~" + head2#Build the git command.
        gitdiff_list = Popen(gitdiff, cwd=repo, stdout=PIPE, stderr=DEVNULL, shell=True)#Instantiate a popen object.
        gitdiff_list.wait()#Wait for execution to complete.
        data, res = gitdiff_list.communicate()#Get records through communicate.
        record = data.decode("utf-8").split("\n")#Decode and rearrange data by "\n".
        
        add_remove = []#Create an empty list to hold the numbers "add" and "remove".
        
        #Loop through the numbers in each row of the record.
        for i in range(len(record)-1):
            num = record[i].split("\t")#Rearrange data by "\t".
            add_remove.append([int(num[0]), int(num[1])])#Add the numbers "add" and "remove" to the list.
        
        #Set the 0 for greater than, equal to, and less than.
        greater = 0
        equal = 0
        less = 0
        
        #Use conditional statements to determine whether the number of rows of the records of this git command is within the range.
        if min_lines <= len(add_remove) <= max_lines:
            #Cases greater than, equal to, and less than are counted separately.
            for i in add_remove:
                if i[0] > i[1]:
                    greater += 1
                elif i[0] == i[1]:
                    equal += 1
                elif i[0] < i[1]:
                    less += 1
                    
            #Use conditional statements to determine whether the numbers "add" and "remove" of the records of this git command meet the conditions.
            if greater >= min_greater and equal >= min_equal and less == 0:
                commund_list.append(gitdiff)#Add eligible git commands to commund_list.
                print(gitdiff)
            else:
                pass
            
        else:
            pass
        
    print(commund_list)#Print eligible git commands.

    #Stores eligible git commands.
    with open('gitdiff.txt', 'w') as gd:
        for i in commund_list:
            gd.write(i+"\n")
    
    print("Finished.")#Confirm that execution is complete.

GitDiff(401, 500, "E:\SourceTree Clone\linux-kernel\linux", 8, 16, 3, 5)