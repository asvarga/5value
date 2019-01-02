
from z3 import *

########

# Return the first "M" models of formula list of formulas F 
def get_models(F, M=math.inf):
    result = []
    s = Solver()
    s.add(F)
    while len(result) < M and s.check() == sat:
        m = s.model()
        result.append(m)
        # Create a new constraint the blocks the current model
        block = []
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
        yield m
    # return result

def dmap(f, x):
	if isinstance(x, list): return [dmap(f, xi) for xi in x]
	return f(x)

def eval(m, x): 
	def f(xi):
		mxi = m[xi]
		# mxi = m.evaluate(xi)
		if is_true(mxi): 	return "T"
		if is_false(mxi): return " "
		if mxi is None: 	return "?"
		return mxi
	return dmap(f, x)

def ind(vec, *args, f, name=None):
	var = Int(name or "%s%s" % (NAME(vec), list(args)))
	def loop(val, *args2):
		if len(args) == len(args2):
			f.append(Implies(And(*[v == x for (v, x) in zip(args, args2)]), var == val))
		else:
			for i in range(len(val)): loop(val[i], *(list(args2)+[i]))
	loop(vec)
	return var