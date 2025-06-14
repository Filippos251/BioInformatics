def compute_lcs_length(s1, s2):
    n, m = len(s1), len(s2)
    # Create matrix (n+1) x (m+1)
    L = [[0] * (m + 1) for _ in range(n + 1)]

    #Matrix Initialisation 
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if s1[i - 1] == s2[j - 1]:
                L[i][j] = L[i - 1][j - 1] + 1
            else:
                L[i][j] = max(L[i - 1][j], L[i][j - 1])
    
    return L[n][m], L

def reconstruct_lcs(s1, s2, L):
    i, j = len(s1), len(s2)
    lcs = []

    # Backtracking to reconstruct LCS
    while i > 0 and j > 0:
        if s1[i - 1] == s2[j - 1]:
            lcs.append(s1[i - 1])
            i -= 1
            j -= 1
        elif L[i - 1][j] >= L[i][j - 1]:
            i -= 1
        else:
            j -= 1

    return ''.join(reversed(lcs))

def edit_distance_from_lcs(s1, s2):
    u, L = compute_lcs_length(s1, s2)
    d = len(s1) + len(s2) - 2 * u
    return d, u, reconstruct_lcs(s1, s2, L)


# Example!!
#if __name__ == "__main__":
#   S1 = "ABCBDAB"
#   S2 = "BDCAB"

#    d, u, lcs_str = edit_distance_from_lcs(S1, S2)

#    print(f"LCS μήκος: {u}")
#    print(f"LCS συμβολοσειρά: {lcs_str}")
#    print(f"Απόσταση μετασχηματισμού D(n,m): {d}")
