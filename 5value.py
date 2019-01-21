
from util import *

from z3 import *
import math

########

n = 5		# number of truth values in logic	
fs = []		# formulas

### Variables ###

# Implication: nxn-matrix of integer variables
I = NAME(tuple( tuple( Int("%s->%s" % (i, j)) for j in range(n) ) for i in range(n) ), 'I')
# Designated set: n-vector of bools
D = NAME(tuple( Bool("?%s" % i) for i in range(n) ), 'D')

### Operations ###

# ints always correspond to object-level/non-classical truth values
# bools always correspond to meta-level/classical truth values
# these all accept either variables or values, and return variables

# int -> bool
def TRUE (p, name=None): return ind(D, p, fs=fs, name=name or "?%s" % p, Type=Bool)
def FALSE(p, name=None): return Not(TRUE(p, name=name))

# int+ -> int
def IMP(p, q, name=None): return ind(I, p, q, fs=fs, name=name or "(%s->%s)" % (p, q))
def NOT(p,    name=None): return IMP(p, 0,           name=name or "-%s"      % p)
def OR (p, q, name=None): return IMP(IMP(p, q), q,   name=name or "(%s||%s)" % (p, q))
def AND(p, q, name=None): return NOT(IMP(p, NOT(q)), name=name or "(%s&&%s)" % (p, q))

N =       tuple(NOT(i)   for i in range(n))
O = tuple(tuple(OR (j,i) for i in range(n)) for j in range(n)) 	# bug: not sure why I had to transpose these
A = tuple(tuple(AND(j,i) for i in range(n)) for j in range(n)) 	# bug: not sure why I had to transpose these

### Formulas ###

# in range
fs += [ And(0 <= NOT(i),    NOT(i)    < n) for i in range(n) ]
fs += [ And(0 <= IMP(i, j), IMP(i, j) < n) for i in range(n) for j in range(n) ]

# not true isn't true
fs += [ Implies(TRUE(i), FALSE(NOT(i))) for i in range(n) ]
# not not true is true
fs += [ Implies(TRUE(i), TRUE(NOT(NOT((i))))) for i in range(n) ]

# |== (not not p) -> p
fs += [ TRUE(IMP(NOT(NOT(i)), i)) for i in range(n) ]
# |=/= p or (not p)
fs.append(Not(And(*[ TRUE(OR(i, NOT(i))) for i in range(n) ])))
# |=/= p -> (p and p)
fs.append(Not(And(*[ TRUE(IMP(i, AND(i, i))) for i in range(n) ])))

# MP
fs += [ Implies(And(TRUE(IMP(i, j)), TRUE(i)), TRUE(j)) for i in range(n) for j in range(n) ]
# Cases
fs += [ Implies(TRUE(OR(i, j)), TRUE(k)) == And(Implies(TRUE(i), TRUE(k)), Implies(TRUE(j), TRUE(k)))
		for i in range(n) for j in range(n) for k in range(n) ]
# Left Conj
fs += [ Implies(And(TRUE(i), TRUE(j)), TRUE(k)) == Implies(TRUE(AND(i, j)), TRUE(k))
		for i in range(n) for j in range(n) for k in range(n) ]
# Right Conj
fs += [ TRUE(AND(i, j)) == And(TRUE(i), TRUE(j)) for i in range(n) for j in range(n) ]

### Domain Restriction ###

# specify truth designation
fs += [TRUE(i) == (i>=n-2) for i in range(n)]

# monotonicity of negation
fs += [NOT(i) >= NOT(i+1) for i in range(n-1)] + [D[-1]]
# specify negation
fs += [NOT(i) == n-1-i 	for i in range(n)]

# symmetry over antidiagonal
fs += [IMP(i,j) == IMP(n-1-j,n-1-i) for i in range(n) for j in range(n)]

# specify corners
# fs += [IMP(0,0) == n-1, IMP(0,-1) == n-1, IMP(-1,0) == 0, IMP(-1,-1) == n-1]
# specify edges
fs += [IMP(0,i)  == n-1   	for i in range(n)]
fs += [IMP(-1,i) == i 	  	for i in range(n)]
fs += [IMP(i,0)  == n-1-i 	for i in range(n)]
fs += [IMP(i,-1) == n-1   	for i in range(n)]
# monotonicity of implication
fs += [IMP(i,j) <= IMP(i,j+1) for i in range(n) for j in range(n-1)]
fs += [IMP(i,j) >= IMP(i+1,j) for i in range(n-1) for j in range(n)]

### Solve ###

pp("%s Formulas\n" % len(fs))

M = 50			# number of models to generate
V = None #N + D # set of variables of which to avoid full repeats ("None" for all)

for i, m in enumerate(get_models(fs, M, V)):
	print("--- Model %s ---" % (i+1))
	pp( meval(m, I) )
	pp( meval(m, N) )
	pp( meval(m, D) )
	pp( meval(m, O) )
	pp( meval(m, A) )
	print()





