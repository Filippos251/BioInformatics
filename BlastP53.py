from Bio.Blast import NCBIWWW, NCBIXML
from Bio import SeqIO
import requests
from io import StringIO
from Bio.SeqRecord import SeqRecord
from Bio.Seq import Seq
from Bio import pairwise2

# Λήψη FASTA για την Cytochrome c1
uniprot_id = "P08574"
url = f"https://www.uniprot.org/uniprot/{uniprot_id}.fasta"
response = requests.get(url)
fasta_data = response.text

# BLASTP αναζήτηση
print("Running BLASTP...")
result_handle = NCBIWWW.qblast("blastp", "nr", fasta_data, entrez_query="NOT synthetic[organism]")

# Ανάγνωση αποτελεσμάτων
blast_record = NCBIXML.read(result_handle)

# Λίστα για αποθήκευση των ομόλογων ακολουθιών
homologs = []

count = 0
for alignment in blast_record.alignments:
    if "Homo sapiens" in alignment.hit_def:
        continue
    hsp = alignment.hsps[0]
    seq = hsp.sbjct.replace('-', '')  # Αφαίρεση κενού
    record = SeqRecord(
        Seq(seq),
        id=alignment.hit_id,
        description=alignment.hit_def
    )
    homologs.append(record)
    count += 1
    if count == 8:
        break

# Προσθήκη και της ανθρώπινης ακολουθίας
human_record = SeqIO.read(StringIO(fasta_data), "fasta")
homologs.insert(0, human_record)

# Αποθήκευση όλων σε FASTA
SeqIO.write(homologs, "homologs.fasta", "fasta")
print("✅ Saved 9 sequences to homologs.fasta")

# Ζευγαρωτή στοίχιση ανθρώπινης με τις υπόλοιπες
with open("pairwise_alignments.aln5", "w") as out_file:
    for i in range(1, len(homologs)):
        aln = pairwise2.align.globalxx(homologs[0].seq, homologs[i].seq, one_alignment_only=True)[0]
        out_file.write(f">Alignment between {homologs[0].id} and {homologs[i].id}\n")
        out_file.write(f"{aln.seqA}\n{aln.seqB}\n\n")
print("✅ Saved pairwise alignments to pairwise_alignments.aln5")