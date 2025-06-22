


from Bio.Blast import NCBIWWW, NCBIXML
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
from Bio.Align.Applications import ClustalOmegaCommandline

# 1. Εκτέλεση BLASTP για 8 ομόλογους 
# Η ακολουθία της ανθρώπινης κυτοχρωμικής C
sequence = Seq("MGDVEKGKKIFIMKCSQCHTVEKGGKHKTGPNLHGLFGRKTGQAPGYSYTAANKNKGIIWGEDTLMEYLENPKKYIPGTKMIFAGIKKKEERADLIAYLKKATNE")
record = SeqRecord(sequence, id="Cytochrome_c_Human", description="Cytochrome c Homo sapiens")

# Εκτέλεση BLASTP
print("Εκτελείται BLASTP...")
result_handle = NCBIWWW.qblast("blastp", "nr", record.format("fasta"), entrez_query="all[filter] NOT Homo sapiens[organism]", hitlist_size=10)

# Ανάλυση αποτελεσμάτων
blast_records = NCBIXML.read(result_handle)

# Εκτύπωση των 8 πρώτων ομόλογων ακολουθιών
print("\nΟμόλογες ακολουθίες:")
for alignment in blast_records.alignments[:8]:
    print(f"> {alignment.title}")
    for hsp in alignment.hsps:
        print(f"Ακολουθία:\n{hsp.sbjct}\n")
        break  # Μόνο το πρώτο HSP
# Αποθήκευση ακολουθιών σε FASTA
SeqIO.write([human_seq] + homologs, "all_sequences.fasta", "fasta")

# 2. Pairwise alignments
for homolog in homologs:
    SeqIO.write([human_seq, homolog], "temp_pair.fasta", "fasta")
    clustal = ClustalOmegaCommandline(infile="temp_pair.fasta", outfile=f"pairwise_{homolog.id}.aln5", force=True, seqtype="Protein")
    clustal()

# 3. Πολλαπλή Στοίχιση
clustal = ClustalOmegaCommandline(infile="all_sequences.fasta", outfile="multiple_alignment.aln5", force=True, seqtype="Protein")
clustal()