
##########################################################################################################
#
# DATE  :      11/26/2018
# AUTHOR:      Lila Fata
# FILE  :      calculateGearRatios.py
# DESCRIPTION: This script file contains the following two functions to determine gear combinations,
#              ratios and shift sequences, and prints the results to the screen -
#              * get_gear_combination() - determines gear combination providing closest ratio less
#                                         than or equal to target ratio
#              * get_shift_sequence()   - determines shift sequence to traverse from initial gear
#                                         combination to gear combination with closest ratio; each
#                                         shift can only change one gear on either front or rear
#
# ASSUMPTIONS:
# 1) Initial gear combination must be included in front and rear cogs
# 2) Front or rear gear shifts forward and not backward
#
# NOTE:
# 1) This program was executed using the IDLE Python 3.7 Shell on a Windows 10 laptop
#
##########################################################################################################

import os
import unittest

#Lists and variables to store initial test data                    
front_cogs = [38, 30]               #List to store Front cogs of bicycle drivetrain
rear_cogs = [28, 23, 19, 16]        #List to store Rear cogs of bicycle drivetrain
target_ratio = 1.6                  #Target ratio for gear combination
ratio = 1.6                         #Ratio for shift sequence 
initial_combination = [38, 28]      #List to store initial gear combination for shift sequence

##########################################################################################################
# FUNCTION:    get_gear_combination()
# DESCRIPTION: Determines the gear combination providing the closest ratio that is less than or equal to
#              the target ratio
# INPUT:       f_cogs, r_cogs, target_ratio
# OUTPUT:      Prints the calculated closet ratio (less than or equal) to the given target ratio
##########################################################################################################
def get_gear_combination(ff_cogs, rr_cogs, target_rratio):
    print("\nDetermine Gear Combination for target ratio",target_rratio)
    found_combination = False     #Initialize variable
    ratio_list = []               #Initilize list of ratios
    for front in ff_cogs:         #Looping through front cogs
        target_front = front
        for rear in rr_cogs:      #Looping through rear cogs
            target_rear = rear
            calc_ratio = front / rear                     #Calculate the ratio of front and rear cogs
            diff_ratio = abs(target_rratio - calc_ratio)  #Get absolute value of target_ratio - ratio
            ratio_list.append((front, rear, calc_ratio, diff_ratio))  #Add to store items in ratio_list
    sortedRatios = sorted(ratio_list, key=lambda ratios: ratios[3])   #Sort list by closest ratio   
    for x,y,z,a in sortedRatios:                #Go through list of ratios in sorted list        
        if (z <= target_rratio):                #Get first ratio that is less than or equal to target ratio
            print("  Front:",x,"Rear:",y,"Ratio",z)
            found_combination = True
            break
    if (not found_combination):
        print("  WARNING: Closest ratio NOT available - all ratios greater than target ratio!")

##########################################################################################################
# FUNCTION:    get_shift_sequence()
# DESCRIPTION: Determines the shift sequence to traverse from initial gear combination to the combination
#              with closest ratio
# INPUT:       f_cogs, r_cogs, ratio, initial_combination
# OUTPUT:      Prints the shift sequence of gear combinations to a gear combination with closet ratio
#              (less than or equal) to the given ratio
##########################################################################################################
def get_shift_sequence(ff_cogs, rr_cogs, rratio, init_combination):
    print("\nDetermine Shift Sequence for ratio",rratio,"and initial gear",init_combination)
    i = 0                                             #Initialize variable
    j = 0                                             #Initialize variable
    idx_front = idnx_front = 0
    idx_rear = indx_rear = 0
    shift_sequence = []                               #Initilize shift_sequence
    for i, front in enumerate(ff_cogs, start=0):      #Determine initial_combination front cog index
        if (front == init_combination[0]):
            indx_front = i
            break
    for j, rear in enumerate(rr_cogs, start=0):       #Determine initial_combination rear cog index
        if (rear == init_combination[1]):
            indx_rear = j
            break
    gear_idx = 0                                      #Initialize gear combination index
    for idx in range(indx_front,len(ff_cogs)):        #Fill shift sequences from initial_combination
        if (idx != indx_front):
            calc_ratio = ff_cogs[indx_front] / rr_cogs[indx_rear]
            diff_ratio = abs(ratio - calc_ratio)
            shift_sequence.append((gear_idx, ff_cogs[indx_front], rr_cogs[indx_rear], calc_ratio, diff_ratio))           
        for rr in rr_cogs[indx_rear:]:
            calc_ratio = ff_cogs[idx] / rr
            diff_ratio = abs(rratio - calc_ratio)
            shift_sequence.append((gear_idx, ff_cogs[idx], rr, calc_ratio, diff_ratio))
        gear_idx = gear_idx + 1                        #Number of gear combinations
    sortedRatios = sorted(shift_sequence, key=lambda ratios: (ratios[0], ratios[4]))  #Sort list
    max_calc_ratio_Info = max(sortedRatios, key=lambda x: x[3])
    avoid_Max_List = []                                #Store calculate ratios that are > given ratio
    if (max_calc_ratio_Info[3] > rratio):
        avoid_Max_List.append(max_calc_ratio_Info[0])
    found_sequence = False
    for gear,front,rear,r,diff_ratio in shift_sequence:
        if (gear not in avoid_Max_List):
            if (r <= ratio):
                found_sequence = True;
                print("  Front:",front,"Rear:",rear,"Ratio:",r)
    if (not found_sequence):
        print("  WARNING: Shift sequence NOT available!")    

##########################################################################################################
# FUNCTION:    main()
# DESCRIPTION: Performs the following tasks:
#              1) Determines gear combination with ratio closest to target ratio
#              2) Determines shift sequence of gear combination to traverse with closest ratio
# INPUT:       Sets of front and rear cogs, target ratios, and shift sequence
# OUTPUT:      Prints the gear combinations and ratios
##########################################################################################################
def main():
    #Test get_gear_combination() with input data
    get_gear_combination(front_cogs, rear_cogs, target_ratio)
    get_gear_combination(front_cogs, rear_cogs, 0.9)
    get_gear_combination(front_cogs, rear_cogs, 4.2)
    get_gear_combination([34,23], [44,22,56], target_ratio)    
    get_gear_combination([34,23], [44,22,56], 0.9)
    get_gear_combination([34,23], [44,22,56], 4.2)

    print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    
    #Test get_shift_sequence() with input data
    get_shift_sequence(front_cogs, rear_cogs, ratio, initial_combination)
    get_shift_sequence(front_cogs, rear_cogs, 0.9, initial_combination)
    get_shift_sequence(front_cogs, rear_cogs, 4.2, initial_combination)
    get_shift_sequence([37,29], [27,22,18,15], ratio, [37,27])
    get_shift_sequence([34,23], [44,22,56,16], 0.9, [23,44])     
    get_shift_sequence([34,23], [44,22,56,16], 4.2, [23,56])
    
if __name__ == "__main__":
    main()
