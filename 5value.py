
from util import *

from z3 import *
import math

########

n = 5		# number of truth values in logic	
fs = []		# formulas

### Variables ###

# Implication: nxn-matrix of integer variables
I = NAME(tuple( tuple( Int("%s->%s" % (i, j)) for j in range(n) ) for i in range(n) ), 'I')
# Negation: n-vector of integer variables
N = NAME(tuple( Int("-%s" % i) for i in range(n) ), 'N')
# Designated set: n-vector of bools
D = NAME(tuple( Bool("?%s" % i) for i in range(n) ), 'D')

### Operations ###

# ints always correspond to object-level/non-classical truth values
# bools always correspond to meta-level/classical truth values
# these all accept either variables or values, and return variables

# int -> bool
def TRUE(p, name=None): return ind(D, p, fs=fs, name=name or "?%s" % p, Type=Bool)
def FALSE(p, name=None): return Not(TRUE(p, name=name))

# int -> int
def NOT(p, name=None): return ind(N, p, fs=fs, name=name or "-%s" % p)
def IMP(p, q, name=None): return ind(I, p, q, fs=fs, name=name or "(%s->%s)" % (p, q))
def OR(p, q, name=None):  return IMP(IMP(p, q), q, name=name or "(%s||%s)" % (p, q))
def AND(p, q, name=None): return NOT(OR(NOT(p), NOT(q)), name=name or "(%s&&%s)" % (p, q))

### Formulas ###

# in range
fs += [ And(0 <= NOT(i), NOT(i) < n) for i in range(n) ]
fs += [ And(0 <= IMP(i, j), IMP(i, j) < n) for i in range(n) for j in range(n) ]

# assume wlog
fs += [ NOT(i) >= NOT(i+1) for i in range(n-1) ]
fs.append(D[-1])

# not true != true; not false == true
fs += [ Xor(TRUE(i), TRUE(NOT(i))) for i in range(n) ]




# |== (not not p) -> p
fs += [ TRUE(IMP(NOT(NOT(i)), i)) for i in range(n) ]
# |=/= p or (not p)
fs.append(Not(And(*[ TRUE(OR(i, NOT(i))) for i in range(n) ])))
# |=/= p -> (p and p)
# fs.append(Not(And(*[ TRUE(IMP(i, AND(i, i))) for i in range(n) ])))



### Solve ###

# pp(fs)
pp("%s Formulas\n" % len(fs))

for i, m in enumerate(get_models(fs, 5)):
	print("--- Model %s ---" % (i+1))
	pp( eval(m, I) )
	pp( eval(m, N) )
	pp( eval(m, D) )
	print()





