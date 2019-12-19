def check(ind, pos):
    for n in range(1, pos):
        for y in range(n + 1, pos):
            if ind[n] == ind[y]:
                return False
            elif abs(ind[n] - ind[y]) == n - y:
                return False
    return True


def queen(A, cur=0):
    if cur == len(A):
        print(A)
        return 0
    for col in range(len(A)):
        A[cur], flag = col, True
        for row in range(cur):
            if A[row] == col or abs(col - A[row]) == cur - row:
                flag = False
                break
        if flag:
            queen(A, cur + 1)


queen([None] * 8)
