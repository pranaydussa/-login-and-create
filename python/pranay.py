a=int(input())
b=a
for i in range(1,a+1):
    spaces=" " * b
    stars="* " *i
    print(spaces+stars)
    b=b-1
