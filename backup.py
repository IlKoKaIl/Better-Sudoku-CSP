#Look for #IMPLEMENT tags in this file.

'''
Construct and return funpuzz CSP models.
'''

from cspbase import *
import itertools


def binary_ne_grid(funpuzz_grid):
    """A model of a funpuzz grid (without cage constraints) built using only binary all-different
    constraints for both the row and column constraints.

    Returns a CSP object representing a FunPuzz Grid CSP problem along with an array of variables
    for the problem. That is return:

       funpuzz_csp, variable_array

    where funpuzz_csp is a csp representing funpuzz grid using binary constraints
    to enforce row and column constraints and variable_array is a list of lists:

       [ [  ]
         [  ]
         .
         .
         .
         [  ] ]

    such that variable_array[i][j] is the Variable (object) that you built to represent the value
    to be placed in cell i,j of the funpuzz Grid.

    Note that this model does not require implementation of cage constraints.
    """
    dimensions = funpuzz_grid[0][0]
    domain = []
    for i in range(1, dimensions+1):
        domain.append(i)

    satisfiable = list(itertools.permutations(domain, 2))
    variables = _create_var(domain)
    un_nested_var = list(itertools.product(domain, domain))
    csp = CSP('Binary_ne', un_nested_var)
    csp = _create_cons_row(csp, variables, satisfiable)
    csp = _create_cons_col(csp, variables, satisfiable)

    return csp, variables


def _create_var(domain):
    variables = []
    for row in range(1, len(domain)+1):
        temp = []
        for col in range(1, len(domain)+1):
            temp_var = Variable(str(row)+str(col), domain)
            temp.append(temp_var)
        variables.append(temp)

    return variables


def _create_cons_row(csp, variables, satisfiable):
    for row in variables:
        for col in row:
            for rest in row:
                if col != rest:
                    c = Constraint(str(col) + str(rest), [col, rest])
                    c.add_satisfying_tuples(satisfiable)
                    csp.add_constraint(c)
    return csp


def _create_cons_col(csp, variables, satisfiable):
    changed_variables = []
    for i in range(len(variables)):
        temp_col = []
        for j in range(len(variables)):
            temp_col.append(variables[j][i])
        changed_variables.append(temp_col)

    for row in changed_variables:
        for col in row:
            for rest in row:
                if col != rest:
                    c = Constraint(str(col) + str(rest), [col, rest])
                    c.add_satisfying_tuples(satisfiable)
                    csp.add_constraint(c)

    return csp


def nary_ad_grid(funpuzz_grid):
    """A model of a funpuzz grid (without cage constraints) built using only n-ary all-different
    constraints for both the row and column constraints.

    Returns a CSP object representing a Cageoky Grid CSP problem along with an array of variables
    for the problem. That is return

       funpuzz_csp, variable_array

    where funpuzz_csp is a csp representing funpuzz grid using n-ary constraints to enforce row
    and column constraints and variable_array is a list of lists:

       [ [  ]
         [  ]
         .
         .
         .
         [  ] ]

    such that variable_array[i][j] is the Variable (object) that you built to represent the value
    to be placed in cell i,j of the funpuzz Grid.

    Note that this model does not require implementation of cage constraints.
    """
    dimensions = funpuzz_grid[0][0]
    domain = []
    for i in range(1, dimensions+1):
        domain.append(i)

    variables = _create_var(domain)
    satisfiable = list(itertools.permutations(domain))
    un_nested_var = list(itertools.product(domain, domain))
    csp = CSP('Nary_ad', un_nested_var)
    csp = _create_nary_cons(csp, variables, satisfiable)
    return csp, variables


def _create_nary_cons(csp, variables, satisfiable):
    # rows
    row_count = 1
    for row in variables:
        cons_row = Constraint(f'row {row_count}', row)
        row_count += 1
        cons_row.add_satisfying_tuples(satisfiable)
        csp.add_constraint(cons_row)

    # columns
    # convert list so columns and row are flipped
    changed_variables = []
    for i in range(len(variables)):
        temp_col = []
        for j in range(len(variables)):
            temp_col.append(variables[j][i])
        changed_variables.append(temp_col)

    col_count = 1
    for col in changed_variables:
        cons_col = Constraint(f'col {col_count}', col)
        col_count += 1
        cons_col.add_satisfying_tuples(satisfiable)
        csp.add_constraint(cons_col)

    return csp


def funpuzz_csp_model(funpuzz_grid):
    """A model built using your choice of (1) binary binary not-equal, or (2) n-ary all-different
    constraints for the grid, together with (3) funpuzz cage constraints. That is, you will
    choose one of the previous two grid models and expand it to include cage constraints
    for the funpuzz Variation.

    Returns a CSP object representing a Cageoky Grid CSP problem along with an array of variables
    for the problem. That is return

       funpuzz_csp, variable_array

    where funpuzz_csp is a csp representing funpuzz grid using constraints
    to enforce cage, row and column constraints and variable_array is a list of lists

       [ [  ]
         [  ]
         .
         .
         .
         [  ] ]

    such that variable_array[i][j] is the Variable (object) that you built to represent the value
    to be placed in cell i,j of the funpuzz Grid.

    Note that this model does require implementation of cage constraints.
    """
    boardcsp , varrow = binary_ne_grid(funpuzz_grid)
    lispos = [i for i in range(1, funpuzz_grid[0][0] + 1)]
    for cage in funpuzz_grid[1:]:
        if cage[-1] == 0:
            size = len(cage) - 2
            rowcomp = list(itertools.product(lispos, repeat=size))
            colcomp = []
            for row in rowcomp:
                if sum(row) == cage[-2]:
                    colcomp.append(row)
            varlist = []
            for var in cage[0:size]:
                varlist.append(varrow[var // 10 - 1][var%10-1])

            con = Constraint(f"{varlist}", varlist)
            con.add_satisfying_tuples(colcomp)
            boardcsp.add_constraint(con)

        if cage[-1] == 1:
            size = len(cage) - 2
            rowcomp = list(itertools.product(lispos,repeat =size))
            colcomp = []
            for row in rowcomp:
                if 2*max(row) - sum(row) == cage[-2]:
                    colcomp.append(row)
            varlist = []
            for var in cage[0:size]:
                varlist.append(varrow[var // 10 - 1][var%10-1])

            con = Constraint(f"{varlist}", varlist)
            con.add_satisfying_tuples(colcomp)
            boardcsp.add_constraint(con)

        if cage[-1] == 3:
            size = len(cage) - 2
            rowcomp = list(itertools.product(lispos,repeat = size))
            colcomp = []
            for row in rowcomp:
                if prod(row) == cage[-2]:
                    colcomp.append(row)
            varlist = []
            for var in cage[0:size]:
                varlist.append(varrow[var // 10 - 1][var%10-1])

            con = Constraint(f"{varlist}", varlist)
            con.add_satisfying_tuples(colcomp)
            boardcsp.add_constraint(con)

        if cage[-1] == 2:
            size = len(cage) - 2
            rowcomp = list(itertools.product(lispos,repeat = size))
            colcomp = []
            for row in rowcomp:
                if max(row)**2 / prod(row) == cage[-2]:
                    colcomp.append(row)
            varlist = []
            for var in cage[0:size]:
                varlist.append(varrow[var // 10 - 1][var%10-1])

            con = Constraint(f"{varlist}", varlist)
            con.add_satisfying_tuples(colcomp)
            boardcsp.add_constraint(con)

    return boardcsp, varrow

def prod(row):
    value = 1
    for i in row:
        value = value * i
    return value

def _create_satisfying_tuples(operater, ):
    pass
