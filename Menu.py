import Koza
import Nguyen3
import Nguyen5
import Nguyen7
import Nguyen10
import Korns12

problems=5
p=3
n=30
while p<=problems:
    if p==1:
        Koza.run(n,p)
        p+=1
    if p==2:
        Nguyen3.run(n,p)
        p+=1
    if p==3:
        Nguyen5.run(n,p)
        p+=1
    if p==4:
        Nguyen7.run(n,p)
        p+=1
    if p==5:
        Nguyen10.run(n,p)
        p+=1
    if p==7:
        Korns12.run(n,p)
        p+=1
