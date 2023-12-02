
def solve_gauss(A, b):
    n = len(A)
    x = [] # make vector with zeros
    for i in range(0, n):
        x.append(0)

        if A[i][i] == 0:
            return None
    
    for i in range(0, n):
        for k in range(i+1, n):
            b[k] = b[k] - b[i]*A[k][i]/A[i][i]
            tmp = []
            for j in range(0, n):
                tmp.append(A[i][j]*A[k][i]/A[i][i])
            for j in range(0, n):
                A[k][j] -= tmp[j]

    for i in range(n-1, -1, -1):
        sum = 0
        for j in range(i+1, n):
            sum = sum + A[i][j]*x[j]

        x[i] = (b[i]-sum)/A[i][i]

    return x