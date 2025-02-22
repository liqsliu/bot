


l = []
for i in range(5120):
    l.append(2**i)






def check_my(v):
    for i in l:
        if i&v > 0:
            print(i, end=" ")
            continue
        if i > v:
            break


def check1(v):
    while v > 0:
        print(v&-v, end=" ")
        v-=v&-v


def check2(v):
    while v > 0:
        t = int(f"1{format(v,'b').replace('1','0')[1:]}", 2)
        print(t, end=" ")
        v-=t



def check1():
    if 8 > 5:
        pass

def check1():
    if 8 & 5<<1 > 0:
        pass

def check2():
#    if 8 & ~5 == 0:
    if 8 & 5<<1 != 0:
        pass

def check3():
    if 8 <= 5<<1:
        pass

def check4():
    if 8 & ~5 > 0:
        pass

def check5():
    if 8 & ~5:
        pass

def check6():
    if 8 & ~5 is not 0:
        pass


import sys
from time import time
if sys.argv:
    pass
    if len(sys.argv) > 2:
        times = int(sys.argv[1])
        f = int(sys.argv[2])

        j = 1
        while j < f:
            print("check", end="")
            print(j, end=": ")
            i = 0
            now = time()
            while i < times:
                exec(f"check{j}()")
                i += 1
            print(time()-now)
            j += 1

    else:
        print(sys.argv)
else:

    k=82844838999393
    from time import time
    now = time()
    t=time()
    check_my(k)
    print(t-now)

    now=t
    check1(k)
    t=time()
    print(t-now)
    now=t
    check2(k)
    t=time()
    print(t-now)

