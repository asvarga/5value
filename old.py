

def ind(vec, i):
	veci = Int("%s[%s]" % (NAME(vec), i))
	for j in range(len(vec)): 
		f.append(Implies(i == j, veci == vec[j]))
	return veci

def ind2(vec, i, j):
	vecij = Int("%s[%s][%s]" % (NAME(vec), i, j))
	for k in range(len(vec)): 
		for l in range(len(vec[k])):
			f.append(Implies(And(i == k, j == l), vecij == vec[k][l]))
	return vecij

def NOT(x, **kwargs): 	 return ind(N, x, **dict({'name':"-%s" % x}, **kwargs))
def IMP(x, y, **kwargs): return ind(I, x, y, **dict({'name':"(%s->%s)" % (x, y)}, **kwargs))
def OR(x, y, **kwargs):	 return IMP(IMP(p, q), q, **dict({'name':"(%s^%s)" % (x, y)}, **kwargs))



# ints always correspond to object-level/non-classical truth values
# bools always correspond to meta-level/classical truth values
# var bool -> var bool : Implies, Not, And, Or
# bool -> bool : not, and, or
# lowercase non-var versions aren't necessary but avoid tautological formulas

# int -> var bool
def true(x): return D[x]
def false(x): return Not(true(x))

# int -> var int
def imp(p, q): return I[p][q]
def neg(p): return N[p]


# f += [ Not(D[0]), D[-1] ]


# not true != true
f += [ Implies(true(i), FALSE(neg(i))) for i in range(n) ]
# not false == true
f += [ Implies(false(i), TRUE(neg(i))) for i in range(n) ]



s = Solver()
s.add(c)
if s.check() == sat:
    m = s.model()
    M_D = [ m.evaluate(D[i]) for i in range(5) ]
    print_matrix(M_D)
else:
    print("failed to solve")