import galois
import numpy as np
MOD = 7514777789

points = []

for line in open('encoded.txt', 'r').read().strip().split('\n'):
    x, y = line.split(' ')
    points.append((int(x), int(y)))

#GF = galois.GF(MOD)
#
#matrix = []
#solution = []
#for point in points:
#    print(f"[*] Point: {point}")
#    x, y = point
#    solution.append(GF(y % MOD))
#
#    row = []
#    for i in range(len(points)):
#        row.append(GF((x ** i) % MOD))
#    
#    matrix.append(GF(row))
#
#open('output.bmp', 'wb').write(bytearray(np.linalg.solve(GF(matrix), GF(solution)).tolist()[:-1]))

# ============ CHATGPT solution ===================================
from scipy.sparse.linalg import cg  # Conjugate Gradient solver

MOD = 7514777789
GF = galois.GF(MOD)

# Convert points into solution vector (y-values)
solution = np.array([GF(y) for _, y in points], dtype=GF)

# Define matrix-free multiplication function
def matvec(v):
    result = np.zeros(len(points), dtype=GF)
    for i, (x, _) in enumerate(points):
        result[i] = sum(GF(pow(x, j, MOD)) * v[j] for j in range(len(points)))
    return result

# Solve Ax = b where A is defined by matvec and b is the solution vector
# Using `cg` (Conjugate Gradient) for the iterative solution
x_approx, info = cg(matvec, solution)

# Write the solution to a file, convert to byte array if required
with open('output.bmp', 'wb') as f:
    f.write(bytearray(x_approx.tolist()[:-1]))
