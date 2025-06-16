import tkinter as tk
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def global_alignment(v, w, match=1, mismatch=-1, gap=-1):
    n, m = len(v), len(w)
    G = [[0] * (m + 1) for _ in range(n + 1)]
    backtrack = [[''] * (m + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        G[i][0] = i * gap
        backtrack[i][0] = '↑'
    for j in range(1, m + 1):
        G[0][j] = j * gap
        backtrack[0][j] = '←'
    backtrack[0][0] = '•'

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            score = match if v[i - 1] == w[j - 1] else mismatch
            diag = G[i - 1][j - 1] + score
            up = G[i - 1][j] + gap
            left = G[i][j - 1] + gap
            max_val = max(diag, up, left)
            G[i][j] = max_val
            dirs = ''
            if diag == max_val: dirs += '↖'
            if up == max_val: dirs += '↑'
            if left == max_val: dirs += '←'
            backtrack[i][j] = dirs

    aligned_v, aligned_w = '', ''
    i, j = n, m
    while i > 0 or j > 0:
        if '↖' in backtrack[i][j]:
            aligned_v = v[i - 1] + aligned_v
            aligned_w = w[j - 1] + aligned_w
            i -= 1
            j -= 1
        elif '↑' in backtrack[i][j]:
            aligned_v = v[i - 1] + aligned_v
            aligned_w = '-' + aligned_w
            i -= 1
        else:
            aligned_v = '-' + aligned_v
            aligned_w = w[j - 1] + aligned_w
            j -= 1

    return G, backtrack, aligned_v, aligned_w, G[n][m]


def local_alignment(v, w, match=10, mismatch=-5, gap=-7):
    n, m = len(v), len(w)
    V = [[0] * (m + 1) for _ in range(n + 1)]
    backtrack = [[''] * (m + 1) for _ in range(n + 1)]

    max_score = 0
    max_positions = []

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            score = match if v[i - 1] == w[j - 1] else mismatch
            diag = V[i - 1][j - 1] + score
            up = V[i - 1][j] + gap
            left = V[i][j - 1] + gap
            best = max(0, diag, up, left)
            V[i][j] = best

            dirs = ''
            if best == 0:
                dirs = ''
            if diag == best: dirs += '↖'
            if up == best: dirs += '↑'
            if left == best: dirs += '←'
            backtrack[i][j] = dirs

            if best > max_score:
                max_score = best
                max_positions = [(i, j)]
            elif best == max_score:
                max_positions.append((i, j))

    # Επιλέγουμε το πρώτο μέγιστο για το traceback
    i, j = max_positions[0]
    aligned_v, aligned_w = '', ''
    while i > 0 and j > 0 and V[i][j] != 0:
        if '↖' in backtrack[i][j]:
            aligned_v = v[i - 1] + aligned_v
            aligned_w = w[j - 1] + aligned_w
            i -= 1
            j -= 1
        elif '↑' in backtrack[i][j]:
            aligned_v = v[i - 1] + aligned_v
            aligned_w = '-' + aligned_w
            i -= 1
        elif '←' in backtrack[i][j]:
            aligned_v = '-' + aligned_v
            aligned_w = w[j - 1] + aligned_w
            j -= 1
        else:
            break

    return V, backtrack, aligned_v, aligned_w, max_score


def visualize(G, backtrack, v, w, frame):
    fig, ax = plt.subplots(figsize=(10, 8))
    G_np = np.array(G)
    cax = ax.matshow(G_np, cmap='coolwarm')
    fig.colorbar(cax)

    ax.set_xticks(range(len(w) + 1))
    ax.set_yticks(range(len(v) + 1))
    ax.set_xticklabels([''] + list(w))
    ax.set_yticklabels([''] + list(v))

    for i in range(len(G)):
        for j in range(len(G[0])):
            txt = f"{G[i][j]}\n{backtrack[i][j]}"
            ax.text(j, i, txt, ha='center', va='center', fontsize=7)

    ax.set_title("Πίνακας Σκορ + Δείκτες")
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack()


def run_alignment():
    v = entry1.get().strip().upper()
    w = entry2.get().strip().upper()
    method = align_type.get()

    if not v or not w:
        messagebox.showerror("Σφάλμα", "Δώσε και τις δύο ακολουθίες.")
        return

    for char in v + w:
        if char not in 'ACGT':
            messagebox.showerror("Σφάλμα", "Επιτρέπονται μόνο χαρακτήρες A, C, G, T.")
            return

    if method == 'global':
        G, backtrack, aligned_v, aligned_w, score = global_alignment(v, w)
    else:
        G, backtrack, aligned_v, aligned_w, score = local_alignment(v, w)

    result_text.set(f"{'Ολική' if method=='global' else 'Τοπική'} στοίχιση:\n{aligned_v}\n{aligned_w}\nΣκορ: {score}")

    for widget in frame_plot.winfo_children():
        widget.destroy()

    visualize(G, backtrack, v, w, frame_plot)


# === GUI ===
root = tk.Tk()
root.title("Στοίχιση Ακολουθιών DNA (Global / Local)")

tk.Label(root, text="Ακολουθία v:", font=("Arial", 12)).pack()
entry1 = tk.Entry(root, width=40, font=("Courier", 12))
entry1.pack()

tk.Label(root, text="Ακολουθία w:", font=("Arial", 12)).pack()
entry2 = tk.Entry(root, width=40, font=("Courier", 12))
entry2.pack()

align_type = tk.StringVar(value='global')
tk.Label(root, text="Επιλογή στοίχισης:", font=("Arial", 12)).pack(pady=5)
tk.Radiobutton(root, text="Ολική", variable=align_type, value='global', font=("Arial", 11)).pack()
tk.Radiobutton(root, text="Τοπική", variable=align_type, value='local', font=("Arial", 11)).pack()

tk.Button(root, text="Στοίχιση", command=run_alignment, font=("Arial", 12)).pack(pady=5)

result_text = tk.StringVar()
tk.Label(root, textvariable=result_text, font=("Courier", 12), justify="left").pack(pady=5)

frame_plot = tk.Frame(root)
frame_plot.pack()

root.mainloop()
