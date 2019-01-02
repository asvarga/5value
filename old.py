

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
