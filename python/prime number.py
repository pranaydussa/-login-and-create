a=int(input())
factors=0
for i in range(2,a):
    if a%i==0:
        factors=factors+1

if factors==0:
    print("PRIME NUMBER")

else:
    print("NOT A PRIME NUMBER")
     
