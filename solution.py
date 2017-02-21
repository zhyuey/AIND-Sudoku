from copy import deepcopy

rows = 'ABCDEFGHI'
cols = '123456789'

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s+t for s in A for t in B]

boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
left_diag_units = [rows[i] + cols[i] for i in range(9)]
right_diag_units = [rows[i] + cols[8-i] for i in range(9)]
unitlist = row_units + column_units + square_units
unitlist.append(left_diag_units)
unitlist.append(right_diag_units)
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

assignments = []

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}
    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers
    for unit in unitlist:
        
        val_two_list = [values[box] for box in unit if len(values[box]) == 2]
        # make the list unique
        val_two_set = set(val_two_list)
        
        # a naked twin value is with length 2 and count 2
        for val in val_two_set:
            if val_two_list.count(val) == 2:
                # This is a twin
                for box in unit:
                    if values[box] != val:
                        for digit in val:
                            values[box] = values[box].replace(digit, '')
    
    return values
            
            
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
    chars = []
    digits = '123456789'
    for c in grid:
        if c in digits:
            chars.append(c)
        if c == '.':
            chars.append(digits)
    assert len(chars) == 81
    return dict(zip(boxes, chars))


def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    print


def eliminate(values):
    """
    Eliminate all impossible digits for every box based on basic rule
    Args:
        values(dict): The sudoku in dictionary form
    Returns:
        values(dict): The sudoku in dictionary form after elimination
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit,'')
    return values


def only_choice(values):
    """
    Eliminate all impossible digits for every box based on only choice principle
    Args:
        values(dict): The sudoku in dictionary form
    Returns:
        values(dict): The sudoku in dictionary form after only-choice technique
    """
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
    return values


def reduce_puzzle(values):
    """
    Use eliminate, only_choice, naked_twins techniques repeated to eliminate impossible digits
    Args:
        values(dict): The sudoku in dictionary form
    Returns:
        values(dict): The sudoku in dictionary form after a series of constraint based operation
    """
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        values = only_choice(values)
        values = naked_twins(values)
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def search(values):
    """
    Using deep-first search to solve
    Args:
        The sudoku in dictionary form
    Returns:
        The sudoku in dictionary form if we find a solution
        False if we cannot find a solution
    """
    
    #reduce the puzzle using the previous function
    values = reduce_puzzle(values)

    if not values:
        return False

    unsolved_boxes = [box for box in boxes if len(values[box]) > 1]
    if (len(unsolved_boxes) == 0):
        return values
    else:
        # Choose one of the unfilled squares with the fewest possibilities
        len_unsolved_box = [len(values[box]) for box in unsolved_boxes]
        min_poss = min(len_unsolved_box)
        min_boxes = [box for box in unsolved_boxes if len(values[box]) == min_poss]
        assert len(min_boxes) > 0
        min_box = min_boxes[0]
        
        # use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
        for digit in values[min_box]:
            values_new = deepcopy(values)
            values_new[min_box] = digit
            values_new = search(values_new)
            if values_new:
                return values_new
        
        return False
        

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = grid_values(grid)
    values = search(values)
    return values

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
