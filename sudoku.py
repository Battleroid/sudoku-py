def inflate(line):
    grid = list()
    cnt = 0

    for i in range(9):
        row = list()
        for j in range(9):
            row.append(int(line[cnt]))
            cnt += 1
        grid.append(row)

    return grid


def legal(row, col, val, grid):
    # col check
    for i in range(9):
        if row == i:
            continue
        else:
            if val == grid[i][col]:
                return False

    # row check
    for i in range(9):
        if col == i:
            continue
        else:
            if val == grid[row][i]:
                return False

    # block check
    row_offset = (row / 3) * 3
    col_offset = (col / 3) * 3
    for r in range(3):
        for c in range(3):
            if (row_offset + r) == row and (col_offset + c) == col:
                continue
            else:
                if val == grid[row_offset + r][col_offset + c]:
                    return False

    return True


def already_valid(row, col, grid):
    val = grid[row][col]
    return legal(row, col, val, grid)


def solvable(grid):
    can_solve = False
    empty = True
    for row in range(9):
        for col in range(9):
            if grid[row][col] != 0:
                empty = False
                if already_valid(row, col, grid):
                    can_solve = True
                else:
                    return False

    return can_solve or empty


def solve(row, col, grid):
    # import pprint
    if row == 9:
        row = 0
        col += 1
        if col == 9:
            return True

    if grid[row][col] != 0:
        return solve(row + 1, col, grid)

    for val in range(1, 10):
        if legal(row, col, val, grid):
            grid[row][col] = val
            if solve(row + 1, col, grid):
                return True
    grid[row][col] = 0

    return False


if __name__ == '__main__':
    import pprint
    import sys
    if len(sys.argv) > 1:
        grid = inflate(sys.argv[1])
        solve(0, 0, grid)
        pprint.pprint(grid)
    else:
        print 'Incorrect usage'
