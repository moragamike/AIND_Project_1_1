assignments = []
rows = 'ABCDEFGHI'
cols = '123456789'

global attempt_num, recursion_attempts, isDiagonal
attemp_num = 0
recursion_attempts = 0
#
isDiagonal = False

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s+t for s in A for t in B]

boxes        = cross(rows, cols)
row_units    = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') 
                for cs in ('123','456','789')]
unitlist     = row_units + column_units + square_units
units        = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers        = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    grid_dict = values
    
    if grid_dict[box] == value:
        return grid_dict

    grid_dict[box] = value
    if len(value) == 1:
        assignments.append(grid_dict.copy())
        
    return grid_dict

def remove_digit(cell_values_set, digit):
    reduced_values_set = ""
    num_chars_in_values_set = len(cell_values_set)
    for i in range(0, num_chars_in_values_set):
        if(cell_values_set[i] != digit):
            reduced_values_set += cell_values_set[i]
    
    return reduced_values_set

def getMinDigitsCellKey(grid_dict, curr_min_num_digits, min_digits_key):
    curr_min_digits = 10
    
    if(isDiagonal):
        for key in boxes:
            num_digits = len(grid_dict[key])
            if(num_digits > 1) and (num_digits < curr_min_num_digits):
                curr_min_digits = num_digits
                min_digits_key = key
    else:
        for key in boxes:
            num_digits = len(grid_dict[key])
            if(num_digits > 1) and (num_digits < curr_min_num_digits):
                if(num_digits < curr_min_digits):
                    curr_min_digits = num_digits
                    min_digits_key = key
    
        return min_digits_key

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    global attempt_num
    
    grid_str = grid
    
    grid_dict = {}
    cell_ctr = 0
    for row in rows:
        for col in cols:
            key = row+str(col)
            value = grid_str[cell_ctr]
            if(value == "."):
                value = '123456789'
            grid_dict[key] = value
            cell_ctr += 1

    return grid_dict

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    grid_dict = values
    print('   1 2 3  4 5 6  7 8 9')
    print('   -------------------') 
    row_ctr = 0
    for row in rows:
        row_str = rows[row_ctr] + "| "
        row_ctr += 1
        col_ctr = 0
        for col in cols:      
            key = row+col
            display_char = grid_dict[key]
            if(len(display_char) == 1):
                row_str += display_char + " "
            else:
                row_str += ". "
            if( (col_ctr == 2)):
                row_str += "|"
            if( (col_ctr == 5)):
                row_str += "|"
            col_ctr += 1
        row_str += "|"
        if( (row_ctr == 3) or (row_ctr == 6) ):
            row_str += "\n------------------------"
        print(row_str)
    print("   --------------------\n") 
       
    return

def getNumSolvedCells(grid_dict):
    n = len([box for box in grid_dict.keys() if len(grid_dict[box]) == 1])
    return n

def eliminate(values):
    """
    Go through all the boxes, and whenever there is a box with a value,
    eliminate this value from the values of all its peers.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    grid_dict = values
    solved_values = [box for box in grid_dict.keys() if len(grid_dict[box])==1]
    for box in solved_values:
        digit = grid_dict[box]
        for peer in peers[box]:
            grid_dict[peer] = grid_dict[peer].replace(digit,'')
    return grid_dict

def only_choice(values):
    """
    Go through all the units, and whenever there is a unit with a value that 
    only fits in one box, assign the value to this box.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    grid_dict = values 
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in grid_dict[box]]
            if len(dplaces) == 1:
                grid_dict[dplaces[0]] = digit
    return grid_dict



def is_NakedTwins(digitsList, digit_1, digit_2):
    isNakedTwins = False
    if(len(digitsList) == 2):
        if (digitsList[0] == digit_1)and(digitsList[1] == digit_2):
            isNakedTwins = True
    return isNakedTwins 

def naked_twins(values):
    """
    ITERATE through ALL 9 COLUMNS and IDENTIFY Naked Twin Digit Pairs
    and Then REMOVE these digits from ANY of the OTHER Cells in SAME Column
    """
    # IDENTIFY and STORE DigitLists of LENGTH "2" in a LIST ("column_cells")
    # Also STORE the DigitLists for ALL Cells ("all_column_cells")
    grid_dict = values
    for column in range(1,10):
        all_column_cells = []
        column_cells = []
        for row in range(0,9):
            key = rows[row] + str(column )
            cell_values_str = grid_dict[key]
            all_column_cells.append(cell_values_str)
            if( len(cell_values_str) == 2):
                column_cells.append(cell_values_str)
        # Do "something" (REMOVE the Naked Twin DIGITS from ALL Other CELLS)
        # ONLY IF a COLUMN 'does' CONTAIN One "Naked Twin" PAIR
        if(len(column_cells) == 2) and (column_cells[0] == column_cells[1]): 
            naked_twin_pair = column_cells[0]
            digit_1         = naked_twin_pair[0]
            digit_2         = naked_twin_pair[1]
            # Iterate through ALL cells in COLUMN and REMOVE Naked Twin Digits
            for i in range(0,9):
                digitsList = all_column_cells[i]

                if not is_NakedTwins(digitsList, digit_1, digit_2):
                    modified_digit_set=remove_digit(digitsList, digit_1)
                    modified_digit_set=remove_digit(modified_digit_set,digit_2)
                    key = rows[i] + str(column)
                    grid_dict[key] = modified_digit_set 

    return grid_dict

def diagonal_sudoku(grid_dict):
    """
    Enforce TWO "Constrainst"
    [1] 
    "UPPER Left TO LOWER Right" Diagonal (A1, B2, C3, D4, E5, F6, G7, H8, I9)
    ONLY contains ONE copy of EACH of the 9 Digits -- {1,2,3,4,5,6,7,8,9}
    [2] 
    "UPPER Right TO LOWER Left" Diagonal (A9, B8, C7, D6, E5, F4, G3 H2, I1)
    ONLY contains ONE copy of EACH of the 9 Digits -- {1,2,3,4,5,6,7,8,9}
    """  
    # Set up LIST containers to hold the "allowed" digits for EACH Diagonal
    r_diag_cell_vals = []
    l_diag_cell_vals = []
    
    # create LISTS containing the KEY values for ALL the Diagonal Cells
    r_diag_cell_ids = ['A1','B2','C3','D4','E5','F6','G7','H8','I9']
    l_diag_cell_ids = ['A9','B8','C7','D6','E5','F4','G3','H2','I1']
    
    # STORE the CELL "Digit Sets" for EACH Diagonal CELL in their "appropriate"
    # Diagonal "container" LIST
    for i in range(0,9):
        r_diag_cell_vals.append(grid_dict[ r_diag_cell_ids[i] ])
        l_diag_cell_vals.append (grid_dict[ l_diag_cell_ids[i] ])
    
    # "Get" SINGLETONS (if ANY)
    R_diag_singletons = []
    L_diag_singletons = []
    for i in range(0,9):
        if len(l_diag_cell_vals[i]) == 1:
            L_diag_singletons.append(l_diag_cell_vals[i])
        if len(r_diag_cell_vals[i]) == 1:
            R_diag_singletons.append(r_diag_cell_vals[i]) 

    # ITERATE through ALL (9) RIGHT and LEFT Diagonal Cells and 
    # REMOVE "Singleton" DIGIT if one exists in a given CELL
    for j in range(0, len(L_diag_singletons)):
            singleton_value = L_diag_singletons[j]
            for set_id in range(0,9):
                values_set = l_diag_cell_vals[set_id]
                if(len(values_set) > 1):  
                    reduced_values_set=remove_digit(values_set,singleton_value)
                    l_diag_cell_vals[set_id] = reduced_values_set
    for j in range(0, len(R_diag_singletons)):
            singleton_value = R_diag_singletons[j]
            for set_id in range(0,9):
                values_set = r_diag_cell_vals[set_id]
                if(len(values_set) > 1):  
                    reduced_values_set=remove_digit(values_set,singleton_value)
                    r_diag_cell_vals[set_id] = reduced_values_set

    # UPDATE the (two) DIAGAONAL "DigitSets" based on any "Singletons" FOUND
    r_diag_cell_ids = ['A1','B2','C3','D4','E5','F6','G7','H8','I9']
    l_diag_cell_ids = ['A9','B8','C7','D6','E5','F4','G3','H2','I1']
    
    for i in range(0,9):
        grid_dict[ r_diag_cell_ids[i] ] = r_diag_cell_vals[i]
        grid_dict[ l_diag_cell_ids[i] ] = l_diag_cell_vals[i]             

    return grid_dict

def reduce_puzzle(values):
    """
    Iterate:
    [1] eliminate() [2] only_choice() [3] Naked Twins [4] Diagonal Test
    
    If at some point, there is a box with no available values, return False.
    If the sudoku is solved, return the sudoku.
    If after iteration of ALL (4) Functions: NO Improvement, return the sudoku
    
    Input:  A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
#    global attempt_num, isDiagonal
#    attempt_num += 1
    
    grid_dict = values
    
    # INITIALIZE "Boolean" that INDICATES if NO "Improvement"
    stalled     = False
    
    # KEEP "Iterating" Until NO Additional "Improvement"
    while (not stalled) and (getNumSolvedCells(grid_dict) != 81):
        
        solved_before = getNumSolvedCells(grid_dict)

        # create UPDATED "Allowed" Digits EACH Cell based on PEER Constraints
        grid_dict = eliminate(grid_dict)
        # create UPDATED "Singleton" CELLs if ONLY 1 Possible Digit in CELL                
        grid_dict = only_choice(grid_dict)
        # create UPDATED "Allowed" Digits in PEER Cells of "Naked Twins" Cells
        grid_dict = naked_twins(grid_dict)
        
#        if(isDiagonal):
            # create UPDATED "Allowed" Digits based on "Diagonals" Constraints
        grid_dict = diagonal_sudoku(grid_dict)
        
        solved_after   = getNumSolvedCells(grid_dict)
       
        # set BOOLEAN variable to TRUE if NO "Improvement"
        num_new_solved = (solved_after - solved_before)
        if (num_new_solved <= 0):
            stalled = True
    
    return grid_dict

def search(values):
    """
    Using depth-first search and propagation, try all possible values.
    """
    global recursion_attempts
    
    grid_dict = values
    
    # First, reduce the puzzle using various functions 
    # {eliminate, only_choice, naked_twins, diagonal}
    grid_dict     = reduce_puzzle(grid_dict)
#    if(attempt_num < 10):
#        print("["+str(attempt_num)+"]  --> CURRENT Number of SOLVED Cells: "
#                + str(getNumSolvedCells(grid_dict)))
#    else:
#        print("["+str(attempt_num)+"] --> CURRENT Number of SOLVED Cells: "
#                + str(getNumSolvedCells(grid_dict)))

    # EXIT Recursion if puzzle "SOLVED"
    if getNumSolvedCells(grid_dict) == 81:
        return grid_dict ## Solved!
        
    # RECURSE with ORIGINAL grid --> because puzzle NOT "Solved"
    else:
        # Choose one of the unfilled squares with the fewest possibilities
        # use recurrence to solve each one of the resulting sudokus
        min_digits_key         = getMinDigitsCellKey(grid_dict, 10, 'A1')
        cell_with_least_digits = grid_dict[min_digits_key]
        for digit in cell_with_least_digits:
            recursion_attempts += 1
            # use ORIGINAL grid BECAUSE the PREVIOUS Recursion FAILED 
            # SOLVE with NEW digit in cell IDENTIFIED as HAVING 
            # the LEAST number of digits REMAINING TO BE "SOLVED"
            # determine UPPER BOUND on number of RECURSION CALLS
            # get BEST (hopefully COMPLETE) solution NOW possible
            new_sudoku = grid_dict.copy()  
            new_sudoku[min_digits_key] = digit                          
            num_unsolved = 82 - getNumSolvedCells(new_sudoku)      
            if (recursion_attempts < num_unsolved):
                new_sudoku = search(new_sudoku)
                if getNumSolvedCells(new_sudoku) == 81:
                    return new_sudoku
        if getNumSolvedCells(new_sudoku) == 81:
            return new_sudoku      
    return new_sudoku ## Solved!

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
    Returns:
        The dictionary representation of the final sudoku grid. 
        False if no solution exists.
    """
    grid_dict = grid_values(grid)
    solution  = search(grid_dict)
    
    return solution
    
###############################################################################
if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...'\
    +'6..4...4....8....52.............3'
#    attempt_num = -1
    grid_dict           = grid_values(diag_sudoku_grid)
    num_one_digit_cells = getNumSolvedCells(grid_dict)
    print("\nORIGINALLY There are "+str(num_one_digit_cells)+" SOLVED Cells\n")
    display(grid_dict)
    solution_grid = solve(diag_sudoku_grid)
    print("\n################  SOLUTION  ###################\n")
    display(solution_grid)

#    try:
#        from visualize import visualize_assignments
#        visualize_assignments(assignments)
#
#    except SystemExit:
#        pass
#    except:
#        print('We could not visualize your board due to a pygame issue. 
#
# Not a problem! It is not a requirement.')
