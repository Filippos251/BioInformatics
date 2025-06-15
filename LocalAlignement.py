import numpy as np
import matplotlib.pyplot as plt

# Σκορ
match = 10
mismatch = -5
gap = -7

# Ακολουθίες
v = "TTAGTTAAGTG"
w = "ATTGTGAATT"

n = len(v)
m = len(w)

# Πίνακες
score = np.zeros((n + 1, m + 1), dtype=int)
trace = np.full((n + 1, m + 1), '', dtype=object)

# Υπολογισμός score και traceback
max_score = 0
max_pos = (0, 0)

for i in range(1, n + 1):
    for j in range(1, m + 1):
        diag = score[i - 1][j - 1] + (match if v[i - 1] == w[j - 1] else mismatch)
        up = score[i - 1][j] + gap
        left = score[i][j - 1] + gap
        score[i][j] = max(0, diag, up, left)

        if score[i][j] == 0:
            trace[i][j] = ''
        elif score[i][j] == diag:
            trace[i][j] = '↖'
        elif score[i][j] == up:
            trace[i][j] = '↑'
        elif score[i][j] == left:
            trace[i][j] = '←'

        # Εύρεση θέσης μέγιστου score (αρχή traceback)
        if score[i][j] > max_score:
            max_score = score[i][j]
            max_pos = (i, j)

# Traceback

i, j = max_pos
aligned_v = ""
aligned_w = ""

while score[i][j] != 0:
    if trace[i][j] == '↖':
        aligned_v = v[i - 1] + aligned_v
        aligned_w = w[j - 1] + aligned_w
        i -= 1
        j -= 1
    elif trace[i][j] == '↑':
        aligned_v = v[i - 1] + aligned_v
        aligned_w = "-" + aligned_w
        i -= 1
    elif trace[i][j] == '←':
        aligned_v = "-" + aligned_v
        aligned_w = w[j - 1] + aligned_w
        j -= 1
    else:
        break

#Local Alignement

print("Βέλτιστο Local Alignment:")
print("v: ", aligned_v)
print("   ", "".join(["|" if a == b else " " for a, b in zip(aligned_v, aligned_w)]))
print("w: ", aligned_w)
print("Score:", max_score)

#Matrix Visualisation

fig, ax = plt.subplots(figsize=(13, 8))
ax.set_axis_off()

row_labels = [' '] + list(v)
col_labels = [' '] + list(w)

table_data = []
for i in range(n + 1):
    row = []
    for j in range(m + 1):
        val = score[i][j]
        arrow = trace[i][j]
        row.append(f"{arrow}\n{val}" if arrow else f"{val}")
    table_data.append(row)

table = ax.table(
    cellText=table_data,
    rowLabels=row_labels,
    colLabels=col_labels,
    loc='center',
    cellLoc='center',
    colLoc='center'
)

table.scale(1.1, 1.3)
table.auto_set_font_size(False)
table.set_fontsize(10)
plt.title("Πίνακας Τοπικής Στοίχισης (Local Alignment)", fontsize=14)
plt.tight_layout()
plt.savefig("local_alignment_traceback.png", dpi=300)
plt.show()
