
from z3 import *

from functools import reduce

########

def isInt(x): return isinstance(x, int)
def notInt(x): return not isInt(x)

# Return the first "M" models of formula list of formulas F 
def get_models(F, M=math.inf, V=None):
	results = 0
	s = Solver()
	s.add(F)
	while results < M and s.check() == sat:
		m = s.model()
		yield m
		results += 1

		# Create a new constraint the blocks the current model
		block = []

		if V:
			# block a specific set of variables/evaluations
			block = [v != m.evaluate(v) for v in V]
		else:
			# block set of all variables/evaluations
			for d in m:
				# d is a declaration
				if d.arity() > 0:
					raise Z3Exception("uninterpreted functions are not supported")
				# create a constant from declaration
				c = d()
				if is_array(c) or c.sort().kind() == Z3_UNINTERPRETED_SORT:
					raise Z3Exception("arrays and uninterpreted sorts are not supported")
				block.append(c != m[d])
		s.add(Or(block))
		

def dmap(f, x):
	if isinstance(x, list): return [dmap(f, xi) for xi in x]
	if isinstance(x, tuple): return tuple(dmap(f, xi) for xi in x)
	return f(x)

def meval(m, x): 
	def f(xi):
		# mxi = m[xi]
		mxi = m.evaluate(xi)
		if is_true(mxi): 	return "T"
		if is_false(mxi): return " "
		if mxi is None: 	return "?"
		return mxi
	return dmap(f, x)

NAMES = {}
def NAME(x, n=None):
	if n: 
		NAMES[x] = n
		return x
	try:	return NAMES[x]
	except:	return str(x)

IND_MEMO = {}

def ind(mat, *inds, fs={}, name=None, Type=Int):
	# if no vars, just get value
	if all(map(isInt, inds)): return reduce(lambda acc,ind: acc[ind], inds, mat)

	# memoize
	key = dmap(id, (mat, inds))
	if key in IND_MEMO: return IND_MEMO[key]

	# create a new variable for result, to be returned
	var = Type(name or "%s%s" % (NAME(mat), list(inds)))
	IND_MEMO[key] = var

	# chop out layers with non-variable indices
	def trim(mat, i=0):
		if i >= len(inds): return mat
		ind = inds[i]
		if isInt(ind): return trim(mat[ind], i+1)
		return tuple(trim(m, i+1) for m in mat)
	mat = trim(mat)
	inds = tuple(filter(notInt, inds))
	
	# build formulas describing var
	def build(mat2, *inds2):
		if len(inds) == len(inds2):
			fs.append(Implies(And(*[i == i2 for (i, i2) in zip(inds, inds2)]), var == mat2))
		else:
			for i in range(len(mat2)): build(mat2[i], *(list(inds2)+[i]))
	build(mat)
	return var




