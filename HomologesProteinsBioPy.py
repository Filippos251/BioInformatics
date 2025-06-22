from Bio.Blast import NCBIWWW, NCBIXML
from Bio import SeqIO

# 1. Ανάγνωση της FASTA για την Cytochrome c1 (P08574) από τοπικό αρχείο
fasta_path = r"C:\Users\32472\Desktop\Βιοπληροφορική\Project1\Ερώτημα 6\CYC1 (P08574).fasta"
with open(fasta_path, "r") as fasta_file:
    record = SeqIO.read(fasta_file, "fasta")
    fasta_data = f">{record.description}\n{str(record.seq)}\n"

# 2. BLASTP αναζήτηση
print("Running BLASTP for P08574...")
result_handle = NCBIWWW.qblast("blastp", "nr", fasta_data, entrez_query="NOT synthetic[organism]")

# 3. Ανάλυση αποτελεσμάτων
blast_record = NCBIXML.read(result_handle)

# 4. Εκτύπωση 8 πρώτων ομόλογων από διαφορετικούς οργανισμούς
count = 0
print("\nTop 8 homologous sequences from other organisms:\n")
for aln in blast_record.alignments:
    title = aln.title
    if "Homo sapiens" not in title and "synthetic construct" not in title.lower():
        count += 1
        print(f"{count}. {title}")
        if count >= 8:
            break