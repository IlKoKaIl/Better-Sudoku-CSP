import itertools
d =4
cell_domain = [i + 1 for i in range(d)]


satisfying_tuples = [(i, j) for i in cell_domain for j in cell_domain if i != j]


a = list(itertools.product([1,2,3,4], repeat = 2))

print(a)
i = a[1]
print(sum(i))
d2 = range(1, d+1)
permutations = list(itertools.permutations(d2))
