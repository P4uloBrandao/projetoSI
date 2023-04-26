import itertools
lst = [3,2,1,0]
for comb in itertools.combinations(lst, 2):
    newLst = [0,0,0,0]
    for x in comb:
        newLst[x] = 1
    print(newLst)
