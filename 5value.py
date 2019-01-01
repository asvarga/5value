
from util import *

from z3 import *
import math

########

n = 5


### Variables ###

# Implication: nxn-matrix of integer variables
# I = [ [ Int("%s->%s" % (i, j)) for j in range(n) ] for i in range(n) ]
# Negation: n-vector of integer variables
N = [ Int("-%s" % i) for i in range(n) ]
# Designated set: n-vector of bools
D = [ Bool("?%s" % i) for i in range(n) ]

### Object Language ###

# ((int -> term) -> [term]) -> [term]
def T(f): return f(lambda x: D[x])
def F(f): return f(lambda x: Not(D[x]))

# int -> ((int -> term) -> [term])
def V(x): return lambda f: [ f(x) ]


# ((int -> term) -> [term]) -> ((int -> term) -> [term])
def NOT(i_t_ts):return lambda i_t: [ t for r in range(n) for t in i_t_ts(lambda q: Implies(r == N[q], i_t(r))) ]


# def IMP(x, y): 	return I[x][y]
# def NOT(x):		return N[x]

# def OR(x, y):  	return IMP(IMP(x, y), y)
# def AND(x, y): 	return NOT(OR(NOT(x), NOT(y)))

### Formulas ###

f = []

# in range
f += [ And(0 <= N[i], N[i] < n) for i in range(n) ]
# f += [ And(0 <= I[i][j], I[i][j] < n) for i in range(n) for j in range(n) ]



# not true != true
# f += [ Implies(TRUE(i), Implies(NOT(i) == j, FALSE(j))) for i in range(n) for j in range(n) ]
f += [ Implies(D[i], t) for i in range(n) for t in F(NOT(V(i))) ]
# not false = true
# f += [ Implies(FALSE(i), Implies(NOT(i) == j, TRUE(j))) for i in range(n) for j in range(n) ]
f += [ Implies(Not(D[i]), t) for i in range(n) for t in T(NOT(V(i))) ]

pp(f)



# # |=/= p or (not p)
# f.append(Not(And(*[ OR(i, NOT(i)) for i in range(n) ])))
# |== (not not p) -> p
# f += [ 	Implies(q == N[p],
# 			Implies(r == N[q],
# 				Implies(s == I[r][p], D[s])
# 			)
# 		) for p in range(n) for q in range(n) for r in range(n) for s in range(n) ]


# V(0) 			=> lambda T: [ T(0) ]
# T(V(0))			=> [ D[0] ]
# NO(V(0)) 		=> lambda T: [ Implies(q == N[0], T(q)) for q in range(n) ]
# T(NO(V(0)))		=> [ Implies(q == N[0], D[q]) for q in range(n) ]
# NO(NO(V(0))) 	=> lambda T: [ Implies(q == N[0], Implies(r == N[q], T(r))) for q in range(n) for r in range(n) ]
# T(NO(NO(V(0))))	=> [ Implies(q == N[0], Implies(r == N[q], D[r])) for q in range(n) for r in range(n) ]


# T(NOT(NOT(0)))
# def T(L): return [D[Li] for Li in L]

# NOT(NOT(0))(TRUE)
# def T(f): return f(TRUE)



# pp(T(V(0)))

# # ((int -> term) -> [term]) -> ((int -> term) -> [term])
# # def NO(i_t_ts): return lambda i_t: [ Implies(i == N[x], t) for i in range(n) for t in i_t_ts(i_t) ]
# def NO(i_t_ts): return lambda i_t: [ t for r in range(n) for t in i_t_ts(lambda q: Implies(r == N[q], i_t(r))) ]

# pp(T(NO(NO(V(0)))))






# make N monotonic wlog?
f += [ N[i] >= N[i+1] for i in range(n-1) ]
# 0 not in D, n-1 in D
f += [ Not(D[0]), D[-1] ]
# make D monotonic wlog?
# f += [ Implies(D[i], D[i+1]) for i in range(n-1) ]





### Solve ###

for i, m in enumerate(get_models(f, 5)):
	print("--- Model %s ---" % (i+1))
	# pp( eval(m, I) )
	pp( eval(m, N) )
	pp( eval(m, D) )
	print()




# s = Solver()
# s.add(c)
# if s.check() == sat:
#     m = s.model()
#     M_D = [ m.evaluate(D[i]) for i in range(5) ]
#     print_matrix(M_D)
# else:
#     print("failed to solve")



# print_matrix(I)
# print_matrix(N)
# print_matrix(D)
# print("----")
# print_matrix(c)


