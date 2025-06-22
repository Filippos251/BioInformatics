from Bio.Blast import NCBIWWW, NCBIXML
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord

# Ακολουθία πρωτεΐνης
sequence = (
    "GATGAPGIAGAPGFPGARGAPGPQGPSGAPGPK" +
    "X" * 50 +
    "X" * 60 +
    "X" * 60 +
    "X" * 60 +
    "X" * 60 +
    "GVQGPPGPQGPR" +
    "X" * 60 +
    "X" * 60 +
    "X" * 60 +
    "GSAGPPGATGFPGAAGR" +
    "X" * 60 +
    "X" * 25 +
    "GVVGLPGQR"
)

# Αντικατάσταση αγνώστων (X) με αλανίνες (ή άλλους υποκατάστατους, όπως glycine)
query_seq = sequence.replace("X", "A")

# Εκτέλεση BLASTP online στο NCBI
result_handle = NCBIWWW.qblast(
    program="blastp",
    database="nr",
    sequence=query_seq,
    entrez_query="Tyr[Organism]",  # Φιλτράρισμα οργανισμών που ξεκινούν με “Tyr”
    format_type="XML"
)

# Ανάλυση αποτελεσμάτων
blast_record = NCBIXML.read(result_handle)

# Εμφάνιση κορυφαίων αποτελεσμάτων
print("Top hits:")
for alignment in blast_record.alignments[:2]:  # Εμφάνιση των 2 πρώτων αποτελεσμάτων
    print(f"Organism hit: {alignment.hit_def}")
    print(f"Accession: {alignment.accession}")
    print(f"Length: {alignment.length}")
    print("-----")
