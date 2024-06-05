a=input()
print(type(a))
a=int(a)
b=a
for i in range(1,a+1):
    spaces=" " * b
    stars="* " *i
    print(spaces+stars)
    b=b-1
