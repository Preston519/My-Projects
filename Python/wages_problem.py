# A simple toy problem
# Given a schedule in the form {0, 1}+ as a string, a number of free days k, a fixed daily rate fixedPay,
# and a bonus, find the optimal earnings if we assign our free days.
# We can assign free days to any day marked 0, turning it to 1. A day worked earns us fixedPay wages.
# If we also worked the previous day, then the day additionally earns us bonus wages.

# Solved by reframing into a Knapsack problem

def findMax(schedule, k, fixedPay, bonus):
    a = []
    b = []
    count = 1
    for i in range(len(schedule) - 1):
        if schedule[i] != schedule[i+1]:
            if schedule[i] == "0":
                a.append(count)
            else:
                b.append(count)
            count = 0
        count += 1
    ends0 = False
    if schedule[-1] == "0":
        ends0 = True
        a.append(count)
    else:
        b.append(count)
    
    # Total weight is total days free. Weight of each item is days spent. Value is the earnings gained
    c = [0] * (k+1)
    for i in range(len(a)):
        for j in range(k, a[i]-1, -1):
            c[j] = max(c[j], c[j-a[i]] + a[i] * (fixedPay + bonus) + (0 if ends0 and i == len(a)-1 else bonus))
    
    maxnum = 0
    for x in range(1, len(c)):
        if c[maxnum] < c[x]:
            maxnum = x
    print(maxnum)
    return sum((x*(fixedPay + bonus) - bonus) for x in b) + c[maxnum] + (k-maxnum) * (fixedPay + bonus)
    
print(findMax("10010111", 2, 4, 3))