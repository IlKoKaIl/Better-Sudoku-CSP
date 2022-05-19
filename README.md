# Better-Sudoku-CSP
Treating sudoku grid as a constraint satisfaction problem: 
Using a forward checking constraint propagator and a Generalized arc consistence (GAC) constraint propagator.

Have 3 different types of constraint models:
  Binary not-equal contraints
  n-ary all different constraints 
  better sudoku cages
The three models take as input a valid  grid, which is a list
of lists, where the first list has a single element, N, which is the size of each dimension of the board, and
each following list represents a cage in the grid. Cell names are encoded as integers in the range
between 11 , ... , nn and each inner list contains the numbers of the cells that are included in the
corresponding cage, followed by the target value for that cage and the mathematical operation (0=’+’,
1=’-’, 2=’/’, 3=’*’). If a list has two elements, the
first element corresponds to a cell, and the second one — the target — is the value enforced on that
cell.
For example, the model ((3), (11,12,13,6,0), (21,22,31,2,2), ....) corresponds to a 3x3 board where:
cells 11, 12 and 13 must sum to 6, and
the result of dividing some permutation of cells 21, 22, and 31 must be 2. That is, (C21/C22)/C23 = 2
or (C21/C23)/C22 = 2, or (C22/C21)/C23 = 2, etc.

An explanation of better sudoku
The game consists of an n ×n grid where each cell of the grid can be assigned a number 1 to n. No
digit appears more than once in any row or column. Grids range in size from 3 ×3 to 9 ×9.
The game grids are divided into heavily outlined groups of cells called cages. These cages come
with a target and a mathematical operation. The numbers in the cells of each cage must produce the
target value when combined using the mathematical operation.
For any given cage, the operation can be one of addition, subtraction, multiplication or division.
Values in a cage can be combined in any order: the first number in a cage may be used to divide the
second, for example, or vice versa. Note that the four operators are “left associative” e.g., 16/4/4 is
interpreted as (16/4)/4 = 1 rather than 16/(4/4) = 16.
A puzzle is solved if all empty cells are filled in with an integer from 1 to n and all above constraints
are satisfied.
An example of a 6 ×6 grid is shown in Figure 1. Note that your solution will be tested on n ×n grids
where n can be from 3 to 9.
