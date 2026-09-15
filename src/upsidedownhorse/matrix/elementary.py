
# src/upsidedownhorse/matrix/elementary.py
import torch


def rowswap(matrix, source, target):
    """Swap the contents of row `source` with row `target`. Returns the matrix."""
    temp = matrix[source].clone()      # 1. stash source SAFELY (view trap!)
    matrix[source] = matrix[target]    # 2. target -> source
    matrix[target] = temp              # 3. stashed source -> target
    return matrix


def rowscale(matrix, source, factor):
    matrix[source] = matrix[source] * factor
    return matrix

def rowreplacement(matrix, first, second, j, k):
    matrix[first] = j * matrix[first] + k * matrix[second]
    return matrix


def rref(matrix):
    """Return the reduced row echelon form of `matrix` (float tensor)."""
    M = matrix.clone().float()          # float clone: don't truncate, don't mutate input
    rows, cols = M.shape
    pivot_row = 0                        # next row that needs a pivot

    for col in range(cols):             # sweep left to right, one column at a time
        if pivot_row >= rows:           # ran out of rows -> done
            break

        # 1. find a row at/below pivot_row with a nonzero entry in this column
        pivot = None
        for r in range(pivot_row, rows):
            if M[r, col] != 0:
                pivot = r
                break
        if pivot is None:               # whole column is zero here -> no pivot, skip
            continue

        # 2. bring the pivot row up into position
        if pivot != pivot_row:
            rowswap(M, pivot, pivot_row)

        # 3. scale pivot row so the pivot element becomes 1
        rowscale(M, pivot_row, 1 / M[pivot_row, col])

        # 4. zero out this column in every OTHER row
        for r in range(rows):
            if r != pivot_row and M[r, col] != 0:
                rowreplacement(M, r, pivot_row, 1, -M[r, col])

        # 5. advance to the next pivot row
        pivot_row += 1

    return M


if __name__ == "__main__":
    # Test sequence from sub-task 8:
    M = torch.tensor([[1, 3, 0, 0, 3],
                      [0, 0, 1, 0, 9],
                      [0, 0, 0, 1, -4]], dtype=torch.float)

    print("Start:\n", M)

    rowswap(M, 0, 1)                    # R1 <-> R2
    print("After R1<->R2:\n", M)

    rowscale(M, 0, 1/3)                 # (1/3) R1
    print("After (1/3)R1:\n", M)

    rowreplacement(M, 2, 0, 1, -3)     # R3 = -3*R1 + R3  -> j=1 (R3), k=-3 (R1)
    print("After R3=-3R1+R3:\n", M)

    # Then test rref on its own matrix:
    A = torch.tensor([[0, 1, 2],
                      [1, 1, 1],
                      [2, 4, 6]], dtype=torch.float)
    print("rref:\n", rref(A))



