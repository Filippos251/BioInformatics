def weighted_edit_distance(s1, s2, d=1, r=2, e=0):
    n, m = len(s1), len(s2)
    D = [[0] * (m + 1) for _ in range(n + 1)]

    # Initialisation of firts row and first column
    for i in range(n + 1):
        D[i][0] = i * d  # delete
    for j in range(m + 1):
        D[0][j] = j * d  # insert

    # Matrix initialisation based on the operations
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            cost_match_or_replace = e if s1[i - 1] == s2[j - 1] else r
            D[i][j] = min(
                D[i - 1][j] + d,                   # Delete
                D[i][j - 1] + d,                   # Insert
                D[i - 1][j - 1] + cost_match_or_replace  # Matching or Replacement
            )

    return D[n][m], D

def print_edit_distance_table(D, s1, s2):
    # Matrix representation
    print("     ", "  ".join([" "] + list(s2)))
    for i, row in enumerate(D):
        if i == 0:
            print(" ", row)
        else:
            print(s1[i - 1], row)

# Example!!
#if __name__ == "__main__":
#    S1 = "ABCBDAB"
#    S2 = "BDCAB"

#    d_cost, table = weighted_edit_distance(S1, S2, d=1, r=2, e=0)

#    print(f"Απόσταση μετασχηματισμού με βάρη: {d_cost}")
#    print_edit_distance_table(table, S1, S2)
