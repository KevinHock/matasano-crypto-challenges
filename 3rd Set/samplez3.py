from z3 import *

x = BitVec('x',32)
y = BitVec('y',32)

s = Solver()
s.add(x==y^(LShR(y,11)))
s.add(x==0x91b33933)

s.add()

print s.check()
m = s.model()
print [_.name()+": "+str(m[_]) for _ in s.model().decls()]
print [_.name()+": "+str(m[_]) for _ in s.model().decls()]


print 'x was '+str(hex(2444441907))

print 'y is '+str(hex(2443250962))