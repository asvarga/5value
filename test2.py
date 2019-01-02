
from util import *

from z3 import *
import math

########

n = 5

NAMES = {}
def name(x, n=None):
	if n: 
		NAMES[x] = n
		return x
	try:	return NAMES[x]
	except:	return str(x)

### Variables ###

# Implication: nxn-matrix of integer variables
I = name(tuple( tuple( Int("%s->%s" % (i, j)) for j in range(n) ) for i in range(n) ), 'I')
# Negation: n-vector of integer variables
N = name(tuple( Int("-%s" % i) for i in range(n) ), 'N')
# Designated set: n-vector of bools
D = BoolVector('D', n)

### Formulas ###

f = []

def ind(vec, i):
	veci = Int("%s[%s]" % (name(vec), i))
	for j in range(len(vec)): 
		f.append(Implies(i == j, veci == vec[j]))
	return veci

def ind2(vec, i, j):
	vecij = Int("%s[%s][%s]" % (name(vec), i, j))
	for k in range(len(vec)): 
		for l in range(len(vec[k])):
			f.append(Implies(And(i == k, j == l), vecij == vec[k][l]))
	return vecij


# x = name(Int('x'), 'x')
pp( ind(N, Int('x')) )
pp( ind2(I, Int('y'), Int('z')) )
pp(f)










