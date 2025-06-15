def read_fasta(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    return ''.join(line.strip() for line in lines if not line.startswith('>'))

def align(s1, s2, match=1, mismatch=-1, gap=-2):
    n, m = len(s1), len(s2)
    # Initialize DP table
    L = [[0] * (m + 1) for _ in range(n + 1)]

    # Initialize first row and column
    for i in range(1, n + 1):
        L[i][0] = i * gap
    for j in range(1, m + 1):
        L[0][j] = j * gap

    # Fill the table
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if s1[i - 1] == s2[j - 1]:
                score = match
            else:
                score = mismatch
            L[i][j] = max(
                L[i - 1][j - 1] + score,  # Match/Mismatch
                L[i - 1][j] + gap,        # Deletion (gap in s2)
                L[i][j - 1] + gap         # Insertion (gap in s1)
            )

    # Reconstruct alignment (not LCS now, but alignment string)
    i, j = n, m
    align1 = []
    align2 = []

    while i > 0 and j > 0:
        current = L[i][j]
        if s1[i - 1] == s2[j - 1]:
            score = match
        else:
            score = mismatch
        if current == L[i - 1][j - 1] + score:
            align1.append(s1[i - 1])
            align2.append(s2[j - 1])
            i -= 1
            j -= 1
        elif current == L[i - 1][j] + gap:
            align1.append(s1[i - 1])
            align2.append('-')
            i -= 1
        else:
            align1.append('-')
            align2.append(s2[j - 1])
            j -= 1

    while i > 0:
        align1.append(s1[i - 1])
        align2.append('-')
        i -= 1
    while j > 0:
        align1.append('-')
        align2.append(s2[j - 1])
        j -= 1

    return ''.join(reversed(align1)), ''.join(reversed(align2)), L[n][m]

#if __name__ == "__main__":
#    s1 = read_fasta("MERS_Cov.fasta.txt")
#    s2 = read_fasta("SarsCov.fasta.txt")
#
#    a1, a2, score = align(s1, s2, match=1, mismatch=-1, gap=-2)
#    print(f"Alignment score: {score}")
#    print(f"\nAligned Sequences:\n{s1} ↔ {s2}")
#    print(f"\n{s1}:\n{a1}\n{s2}:\n{a2}")
