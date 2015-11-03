import Koza
import Nguyen3
import Nguyen5
import Nguyen7
import Nguyen10
import Keijzer6
import Korns12
import Vladislavleva1
import Pagie1

problems = 6
p = 6
n = 30
while p <= problems:
    if p == 1:
        Koza.run(n, p)
        p += 1
    if p == 2:
        Nguyen3.run(n, p)
        p += 1
    if p == 3:
        Nguyen5.run(n, p)
        p += 1
    if p == 4:
        Nguyen7.run(n, p)
        p += 1
    if p == 5:
        Nguyen10.run(n, p)
        p += 1
    if p == 6:
        Keijzer6.run(n, p)
        p += 1
    if p == 7:
        Vladislavleva1.run(n, p)
        p += 1
    if p == 8:
        Pagie1.run(n, p)
        p += 1
    if p == 9:
        Korns12.run(n, p)
        p += 1
