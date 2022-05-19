from funpuzz_csp import *
from propagators import *

boards = [[[3], [11, 21, 3, 0], [12, 22, 2, 1], [13, 23, 33, 6, 3], [31, 32, 5, 0]],
          [[4], [11, 21, 6, 3], [12, 13, 3, 0], [14, 24, 3, 1], [22, 23, 7, 0], [31, 32, 2, 2], [33, 43, 3, 1],
           [34, 44, 6, 3], [41, 42, 7, 0]],
          [[5], [11, 21, 4, 1], [12, 13, 2, 2], [14, 24, 1, 1], [15, 25, 1, 1], [22, 23, 9, 0], [31, 32, 3, 1],
           [33, 34, 44, 6, 3], [35, 45, 9, 0], [41, 51, 7, 0], [42, 43, 3, 1], [52, 53, 6, 3], [54, 55, 4, 1]],
          [[6], [11, 21, 11, 0], [12, 13, 2, 2], [14, 24, 20, 3], [15, 16, 26, 36, 6, 3], [22, 23, 3, 1],
           [25, 35, 3, 2], [31, 32, 41, 42, 240, 3], [33, 34, 6, 3], [43, 53, 6, 3], [44, 54, 55, 7, 0],
           [45, 46, 30, 3], [51, 52, 6, 3], [56, 66, 9, 0], [61, 62, 63, 8, 0], [64, 65, 2, 2]]]


test_fc = True
test_gac = True
test_mrv = True


def print_funpuzz_soln(var_array):
    for row in var_array:
        print([var.get_assigned_value() for var in row])


def test_mrv_fun():
    a = Variable('A', [1])
    b = Variable('B', [1])
    c = Variable('C', [1])
    d = Variable('D', [1])
    e = Variable('E', [1])

    simple_csp = CSP("Simple", [a, b, c, d, e])

    count = 0
    for i in range(0, len(simple_csp.vars)):
        simple_csp.vars[count].add_domain_values(range(0, count))
        count += 1

    var = ord_mrv(simple_csp)

    if var:
        if var.name == simple_csp.vars[0].name:
            print("Passed Ord MRV Test")
        else:
            print("Failed Ord MRV Test")
    else:
        print("No Variable Returned from Ord MRV")


def test_gac_fun():
    for b in boards:
        print("Solving board")
        try:
            csp, var_array = funpuzz_csp_model(b)
        except NotImplementedError:
            print("Please implement csp model + gac before testing")
            continue
        solver = BT(csp)
        print("=======================================================")
        print("GAC")
        #solver.bt_search(prop_GAC)
        solver.bt_search(prop_GAC, var_ord=ord_mrv) #uncomment this when you've completed ord_mrv! The heuristic should make a difference in terms of the # of variable assignments!
        print("=======================================================")
        print("Solution")
        print_funpuzz_soln(var_array)


def test_fc_fun():
    for b in boards:
        print("Solving board")
        try:
            csp, var_array = funpuzz_csp_model(b)
        except NotImplementedError:
            print("Please implement csp model + fc before testing")
            continue
        solver = BT(csp)
        print("=======================================================")
        print("FC")
        #solver.bt_search(prop_FC)
        solver.bt_search(prop_FC, var_ord=ord_mrv)  #uncomment this when you've completed ord_mrv! The heuristic should make a difference in terms of the # of variable assignments!
        print("=======================================================")
        print("Solution")
        print_funpuzz_soln(var_array)


if __name__ == '__main__':
    if test_fc: test_fc_fun()
    if test_gac: test_gac_fun()
    if test_mrv: test_mrv_fun()

