import sys
import math

x=4856545.00001

m=5.00001
n=5.76793
s=0.00001

while m<=n:
    res = m % s
    res2 = math.remainder(m, s)
    if res2 == 0:
        continue
    else:
        print(m, s, res, res2)
        break

    m += s
    
