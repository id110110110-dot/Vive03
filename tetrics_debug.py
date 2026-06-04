SHAPES = [
  [],
  [[1, 1, 1, 1]],
  [[2, 0, 0], [2, 2, 2]],
  [[0, 0, 3], [3, 3, 3]],
  [[4, 4], [4, 4]],
  [[0, 5, 5], [5, 5, 0]],
  [[6, 6, 0], [0, 6, 6]],
  [[7, 7, 7], [0, 7, 0]]
]

def rotate(matrix, dir):
    for y in range(len(matrix)):
        for x in range(y):
            matrix[x][y], matrix[y][x] = matrix[y][x], matrix[x][y]
    if dir > 0:
        for row in matrix:
            row.reverse()
    else:
        matrix.reverse()

for i in range(1, len(SHAPES)):
    mat = [row[:] for row in SHAPES[i]]
    rotate(mat, 1)
    print('shape', i)
    for row in mat:
        print(row)
    print()
