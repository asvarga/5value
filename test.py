
from util import *

from z3 import *
import math

########

n = 5

### Variables ###

INT = IntSort()
BOOL = BoolSort()


# Negation: n-vector of integer variables
# N = [ Int("-%s" % i) for i in range(n) ]
# N = IntVector('N', n)
N = Array('N', INT, INT)
# Designated set: n-vector of bools
# D = [ Bool("?%s" % i) for i in range(n) ]
# D = BoolVector('D', n)
D = Array('D', INT, BOOL)

### Object Language ###

def NOT(x):     return N[x]
def TRUE(x):    return D[x]
def FALSE(x):   return Not(TRUE(x))

### Formulas ###

f = []

# in range
f += [ And(0 <= NOT(i), NOT(i) < n) for i in range(n) ]

# not true != true
f += [ Implies(TRUE(i), Implies(NOT(i) == j, FALSE(j))) for i in range(n) for j in range(n) ]
# f += [ Implies(TRUE(i), FALSE(NOT(i))) for i in range(n) ]
# not false = true
f += [ Implies(FALSE(i), Implies(NOT(i) == j, TRUE(j))) for i in range(n) for j in range(n) ]


# make N monotonic wlog?
f += [ NOT(i) >= NOT(i+1) for i in range(n-1) ]
# 0 not in D, n-1 in D
f += [ FALSE(0), TRUE(-1) ]

### Solve ###

# for i, m in enumerate(get_models(f, 5)):
#   print("--- Model %s ---" % (i+1))
#   pp( eval(m, N) )
#   pp( eval(m, D) )
#   print()


s = Solver()
s.add(f)
if s.check() == sat:
    m = s.model()
    pp( eval(m, N) )
    pp( eval(m, D) )
else:
    print("failed to solve")


















