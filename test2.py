
from util import *

from z3 import *
import math

########

n = 5
f = []

NAMES = {}
def NAME(x, n=None):
	if n: 
		NAMES[x] = n
		return x
	try:	return NAMES[x]
	except:	return str(x)

### Variables ###

# Implication: nxn-matrix of integer variables
I = NAME(tuple( tuple( Int("%s->%s" % (i, j)) for j in range(n) ) for i in range(n) ), 'I')
# Negation: n-vector of integer variables
N = NAME(tuple( Int("-%s" % i) for i in range(n) ), 'N')
# Designated set: n-vector of bools
D = BoolVector('D', n)

def NOT(x, name=None): 	  return ind(N, x, f=f, name=name or "-%s" % x)
def IMP(x, y, name=None): return ind(I, x, y, f=f, name=name or "(%s->%s)" % (x, y))
def OR(x, y, name=None):  return IMP(IMP(p, q), q, name=name or "(%s||%s)" % (x, y))
def AND(x, y, name=None): return NOT(OR(NOT(x), NOT(y)), name=name or "(%s&&%s)" % (x, y))


# x = name(Int('x'), 'x')
# pp( ind(N, Int('x')) )
# pp( ind2(I, Int('y'), Int('z')) )
# pp( ind(N, Int('x')) )
# pp( ind(I, Int('y'), ind(N, Int('x'))) )
# pp(NOT(Int('z')))
p, q = map(Int, "pq")
# pp(IMP(IMP(p, q), q))
pp(AND(p, q))
pp(f)










