def global_alignment(v, w, match=1, mismatch=-1, gap=-1):
    n, m = len(v), len(w)
    
    # Δημιουργία πινάκων G και backtrack
    G = [[0 for _ in range(m+1)] for _ in range(n+1)]
    backtrack = [['' for _ in range(m+1)] for _ in range(n+1)]

    # Αρχικοποίηση πρώτης γραμμής και πρώτης στήλης
    for i in range(1, n+1):
        G[i][0] = i * gap
        backtrack[i][0] = '↑'
    for j in range(1, m+1):
        G[0][j] = j * gap
        backtrack[0][j] = '←'
    backtrack[0][0] = '•'  # Αφετηρία

    # Υπολογισμός πίνακα G και συμπλήρωση backtrack
    for i in range(1, n+1):
        for j in range(1, m+1):
            if v[i-1] == w[j-1]:
                score = match
            else:
                score = mismatch

            diag = G[i-1][j-1] + score
            up = G[i-1][j] + gap
            left = G[i][j-1] + gap

            G[i][j] = max(diag, up, left)

            if G[i][j] == diag:
                backtrack[i][j] = '↖'
            elif G[i][j] == up:
                backtrack[i][j] = '↑'
            else:
                backtrack[i][j] = '←'

    # Οπισθοδρόμηση για εξαγωγή στοίχισης
    aligned_v = ''
    aligned_w = ''
    i, j = n, m

    while i > 0 or j > 0:
        if backtrack[i][j] == '↖':
            aligned_v = v[i-1] + aligned_v
            aligned_w = w[j-1] + aligned_w
            i -= 1
            j -= 1
        elif backtrack[i][j] == '↑':
            aligned_v = v[i-1] + aligned_v
            aligned_w = '-' + aligned_w
            i -= 1
        elif backtrack[i][j] == '←':
            aligned_v = '-' + aligned_v
            aligned_w = w[j-1] + aligned_w
            j -= 1

    return G, backtrack, aligned_v, aligned_w, G[n][m]

# Παράδειγμα εκτέλεσης
v = "TTAGTTAAGTG"
w = "ATTGTGAATT"

G, backtrack, aligned_v, aligned_w, score = global_alignment(v, w)

# Εκτύπωση αποτελεσμάτων
print("Βέλτιστη στοίχιση:")
print(aligned_v)
print(aligned_w)
print("Σκορ:", score)

print("\nΠίνακας G:")
for row in G:
    print(' '.join(f"{cell:3}" for cell in row))

print("\nΠίνακας οπισθοδρόμησης:")
for row in backtrack:
    print(' '.join(f"{cell:2}" for cell in row))