from Bio.Blast import NCBIWWW, NCBIXML
from Bio import SeqIO, pairwise2
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord

# 1. FASTA ακολουθία της ανθρώπινης πρωτεΐνης
human_seq = SeqRecord(
    Seq("MPSAHLVLAAGVGTGSTAQSVQTGKTCEFYGHGLAILMPEDWGPELALQLSFPDLSICGPNDPWNSQANGRIAHIELYLRELEQGYYEIIPQLPIERLKHGELSEETDNFTWGYRRIDAGMADDRGLFQTLDIFDGSEYPGPVTHAVQWVREVGQPMDDGRKLGIGGGSTGVLGILDSKGDASDAGQGINPAAHTLGHTILATKYRMGLEAFKDNAGYVQDLIESLKTQRPIQLAFPEDLSGSWILFGGHEGFRLLNEEKLSDITSGPWELFVGR"),
    id="HUMAN_GOT2",
    description="Aspartate aminotransferase, mitochondrial [Homo sapiens]"
)

# 2. BLASTP αναζήτηση
print("Running BLASTP...")
result_handle = NCBIWWW.qblast(
    program="blastp",
    database="nr",
    sequence=human_seq.format("fasta"),
    entrez_query="NOT Homo sapiens[Organism]",
    format_type="XML"
)

# 3. Ανάλυση αποτελεσμάτων και λήψη των 8 πρώτων ομόλογων
blast_record = NCBIXML.read(result_handle)
homologs = [human_seq]
count = 0
for alignment in blast_record.alignments:
    if count >= 8:
        break
    hsp = alignment.hsps[0]
    seq = Seq(hsp.sbjct.replace('-', ''))
    homologs.append(SeqRecord(seq, id=f"HOMOLOG_{count+1}", description=alignment.hit_def))
    count += 1

# 4. Αποθήκευση των 9 συνολικών ακολουθιών σε αρχείο FASTA
with open("homologs.fasta", "w") as fasta_out:
    SeqIO.write(homologs, fasta_out, "fasta")
print("Saved homologs.fasta")

# 5. Δημιουργία ζευγαρωτών στοιχίσεων (pairwise) και αποθήκευση
with open("pairwise.aln5", "w") as f:
    for i in range(1, len(homologs)):
        aln = pairwise2.align.globalxx(human_seq.seq, homologs[i].seq, one_alignment_only=True)[0]
        f.write(f">HUMAN_GOT2 vs {homologs[i].id}\n")
        f.write(pairwise2.format_alignment(*aln))
        f.write("\n")
print("Saved pairwise.aln5")

# 6. Πολλαπλή στοίχιση ΜΗΔΕΝΙΖΕΤΑΙ
# Αν δεν θέλεις καθόλου MSA, απλώς μην το εκτελέσεις:
# os.system("clustalo -i homologs.fasta -o msa_output.aln5 --outfmt=clu --force")
# print("Saved msa_output.aln5")