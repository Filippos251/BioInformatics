def affine_gap_alignment(A, B, match=1, gap_open=2, gap_extend=1):
    n = len(A)
    m = len(B)
    
    INF = float('-inf')

    # DP πίνακες, Οι τρεις πίνακες αντιστοιχούν σε τρεις καταστάσεις για κάθε θέση.
    M = [[INF] * (m + 1) for _ in range(n + 1)]
    X = [[INF] * (m + 1) for _ in range(n + 1)]
    Y = [[INF] * (m + 1) for _ in range(n + 1)]

    # Αρχικοποίηση
    M[0][0] = 0
    for i in range(1, n + 1):
        X[i][0] = -gap_open - (i - 1) * gap_extend #Η gap_open είναι η ποινή για να ξεκινήσει ένα κενό.
        M[i][0] = X[i][0]
    for j in range(1, m + 1):
        Y[0][j] = -gap_open - (j - 1) * gap_extend # gap_extend είναι η ποινή για κάθε επιπλέον χαρακτήρα μέσα στο ίδιο κενό.
        M[0][j] = Y[0][j]

    # Υπολογισμός πίνακα
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            # Αντιστοίχιση ή mismatch
            score = match if A[i - 1] == B[j - 1] else -gap_open - gap_extend
            M[i][j] = max(M[i - 1][j - 1], X[i - 1][j - 1], Y[i - 1][j - 1]) + score

            # Gap στη B (προσθήκη χαρακτήρα στην A)
            X[i][j] = max(M[i - 1][j] - gap_open, X[i - 1][j] - gap_extend)

            # Gap στη A (προσθήκη χαρακτήρα στην B)
            Y[i][j] = max(M[i][j - 1] - gap_open, Y[i][j - 1] - gap_extend)

    # Τελικό σκορ
    final_score = max(M[n][m], X[n][m], Y[n][m])
    return final_score
	

#e.g.
#A = "ACG"
#B = "AG"
#score = affine_gap_alignment(A, B, match=1, gap_open=2, gap_extend=1)
#print("Βαθμολογία στοίχισης:", score)