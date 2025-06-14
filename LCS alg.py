#LCS computing algorithm for sequences S1:n, S2:m
def lcs(s1, s2):
    n, m = len(s1), len(s2)
    L = [[0] * (m + 1) for _ in range(n + 1)]

    # Συμπλήρωση πίνακα
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if s1[i - 1] == s2[j - 1]:
                L[i][j] = L[i - 1][j - 1] + 1
            else:
                L[i][j] = max(L[i - 1][j], L[i][j - 1])

    # LCS reconstruction
    i, j = n, m
    lcs_str = []
    while i > 0 and j > 0:
        if s1[i - 1] == s2[j - 1]:
            lcs_str.append(s1[i - 1])
            i -= 1
            j -= 1
        elif L[i - 1][j] > L[i][j - 1]:
            i -= 1
        else:
            j -= 1

    return ''.join(reversed(lcs_str)), L[n][m]
