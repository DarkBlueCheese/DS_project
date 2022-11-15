import rpyc
import time
import math
import numpy as np
rpyc.core.protocol.DEFAULT_CONFIG['allow_pickle'] = True

conn_01 = rpyc.connect('localhost', port = 8101, config = rpyc.core.protocol.DEFAULT_CONFIG)
conn_02 = rpyc.connect('localhost', port = 8102, config = rpyc.core.protocol.DEFAULT_CONFIG)

my_list = []

# prompt the user for the input
num1: int = int(input('Enter the start number:'))
num2: int = int(input('Enter the amount of prime numbers:'))

# Start to record time
time_start = time.time()

def spliter(num2):
    # when get the input num2, condition: num2 >= 1

    if num2 == 1:
        return 1, 0

    elif num2 % 2 == 1:
        num_to_SV_01 = math.ceil(num2/2)
        num_to_SV_02 = math.floor(num2/2)
        return num_to_SV_01, num_to_SV_02

    elif num2 % 2 == 0:
        num_to_SV_01 = int(num2/2)
        num_to_SV_02 = int(num2/2)
        return num_to_SV_01, num_to_SV_02

num2_SV_01, num2_SV_02 = spliter(num2)



# #####################
# # Get the outcomes from SV_01 and SV_02
#     # All case can handle the case of num1 == 0 or 1 or 2 as well!
# # outcome_01 = {There exist Z such that 3 + 4x where x is positive integers}
# # outcome_02 = {There exist Z such that 5 + 4x where x is positive integers}
# outcome_01 = list(conn_01.root.findPrimeUntilDesired_SV_01(num1, num2_SV_01))
# print(time.time() - time_start)
# outcome_02 = list(conn_02.root.findPrimeUntilDesired_SV_02(num1, num2_SV_02))
# print(time.time() - time_start)
# ##################


outcome_01_raw = rpyc.async_(conn_01.root.findPrimeUntilDesired_SV_01)(num1, num2_SV_01)
print(time.time() - time_start)


outcome_02_raw = rpyc.async_(conn_02.root.findPrimeUntilDesired_SV_02)(num1, num2_SV_02)
print(time.time() - time_start)

# print(f'{len(list(outcome_02_raw.value))} {outcome_02_raw.value}')
# print(f'ping: {time.time() - time_start}')
# print(f'{len(list(outcome_01_raw.value))} {outcome_01_raw.value}')
# print(f'ping2: {time.time() - time_start}')
# # outcome_01_raw.wait()
print(f'ping3: {time.time() - time_start}')
# # outcome_02_raw.wait()
my_list.append(outcome_01_raw.value)
my_list.append(outcome_02_raw.value)
print(f'ping3a: {time.time() - time_start}')
numpi = np.array(outcome_01_raw.value)
print(f'ping3b: {time.time() - time_start}')
print(numpi)
print(f'ping3c: {time.time() - time_start}')
# print(outcome_01_raw.value + outcome_02_raw.value)
# print(type(outcome_01_raw.value.list))
print(f'ping4: {time.time() - time_start}')

print(outcome_02_raw.value[-1])
print(f'ping4a: {time.time() - time_start}')
# new_type = outcome_02_raw.value + outcome_01_raw.value
# print(new_type)
print(f'ping4b: {time.time() - time_start}')
outcome_02 = np.array(outcome_02_raw.value)
print(f'ping5: {time.time() - time_start}')

outcome_01 = np.array(outcome_01_raw.value)
print(f'ping6: {time.time() - time_start}')
# print(f'{outcome_02_raw.value}')
# print(f'{type(list(outcome_02_raw.value))}')
print(time.time() - time_start)
print(f'{len(outcome_01)}, {len(outcome_02)}')

# # # # #
# Challenge : This is not yet completed
# The code will ruin when num2 becomes large
# Ex
# prime numbers when num1 = 2, num2 =32 -> 
# [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127]
# However, 
# SV_01 -> [5, 13, 17, 29, 37, 41, 53, 61, 73, 89, 97, 101, 109, 113, 137, 149]
# SV_02 -> [7, 11, 19, 23, 31, 43, 47, 59, 67, 71, 79, 83, 103, 107, 127]
# Since we don't know the distribution of prime number with
# Z_01 that 1 + 4x where x are positive Z
# Z_02 that 3 + 4x where x are positive Z
# Thus, somehow, we have to do some engineering
# To check whether the SV_02 has any additional prime number which are smaller than the biggest number of SV_01
# And vice versa

# Get the last(== biggest) prime number of each list 
# Then find is there any hidden prime number b/w two lists
print(time.time() - time_start)


print(type(int(outcome_01_raw.value[-1])))

outcome_01_last = int(outcome_01_raw.value[-1])
outcome_02_last = int(outcome_02_raw.value[-1])
print(f'{outcome_01_last} , {outcome_02_last}')
print(f'{outcome_01[0]} , {outcome_02[0]}')
extra_outcome = []
print(time.time() - time_start)
# if maximum prime number is greater than 2
if max(np.concatenate((outcome_01, outcome_02), axis=None)) > 2:

    # balancer will returns (extra_prime_list, indicator)
    if outcome_01_last > outcome_02_last:
        print(f'A1 {time.time() - time_start}')
        extra_outcome_raw = rpyc.async_(conn_02.root.balancer)(outcome_01_last, outcome_02_last)
        extra_outcome = np.array(extra_outcome_raw.value)
        # extra_outcome_raw = conn_02.root.balancer(outcome_01_last, outcome_02_last)
        print(f'A2 {time.time() - time_start}')
        print(f'extra : {np.array(extra_outcome_raw.value)}')
        print(f'A3 {time.time() - time_start}')
        # extra_outcome = extra_outcome_raw.value

    elif outcome_01_last < outcome_02_last:
        # call SV_01
        extra_outcome = list(conn_01.root.balancer(outcome_01_last, outcome_02_last)[0])


print(extra_outcome)

final_outcome = sorted(np.concatenate((outcome_01, outcome_02, extra_outcome), axis=None))[:num2]
print(num2)
# final_outcome = sorted(np.concatenate((outcome_01, outcome_02), axis=None))[:num2]
process_time = time.time() - time_start
print(f'len : {len(final_outcome)} , outcomes : {final_outcome}')
print(f'len : {len(final_outcome)}')
print(f'{process_time : .5f}')