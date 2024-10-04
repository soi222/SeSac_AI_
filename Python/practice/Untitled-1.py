class A:
    def __init__(s, a, a_id):
        s.a = a 
        s.a_id = a_id 

    def print_a(s):
        print(f'called print_a with {s}')
        print(s.a)

    def __str__(self):
        return str(self.a_id)
    

    def __add__(self, other):
        print(f'addition between {self} and {other}')
        return self.a + other.a
    
    def __eq__(self, other):
        print(f'is equal between {self} and {other}')
        return self.a == other.a 

a = A(1, 'a')
b = A(1, 'a')

print(a == b)

"""
print(a.a)
a.print_a()
A.print_a(a)

b.print_a()
A.print_a(b)
"""
print(a+b)

1+3 

print(A.__add__(a, b))