

def get_ids(file_in):
    from Bio.Blast import NCBIXML
    blast = NCBIXML.parse(open(file_in)) #extract name of genes from xml-blast
    with open(str(file_in).replace('.xml','')+'.txt','w') as fh:
        for record in blast :
            for n in record.alignments:
                print (str(n)[:str(n).find('|',5):],file=fh)
    return str(file_in).replace('.xml','')+'.txt'  #return file where are the ids


def get_ids_from_server(file_in):
    from Bio import Entrez
    from Bio import SeqIO
    from Bio.SeqRecord import SeqRecord
    from Bio.Seq import Seq
    from urllib.error import URLError
    Entrez.email = "your@email.com" #use your email!
    n =1
    records = []
    num_lines = sum(1 for line in open(file_in))
    try:
        for gi_name in open(file_in):  #fetch the sequences from the server
            handle = Entrez.efetch(db="protein", id=gi_name, rettype="gb", retmode="text")
            entry = SeqIO.read(handle, "genbank")
            records += [SeqRecord(Seq(str(entry.seq)), id=entry.id, description=entry.description)]
            SeqIO.write(records, 'feched.fasta', "fasta")
            print(n,'out of ',num_lines,' (',round(n/num_lines*100,2),'%) ,fetched gene: ',entry.description)
            n += 1
        SeqIO.write(records, 'feched.fasta', "fasta")
    except ValueError or TimeoutError or URLError:
        SeqIO.write(records, 'feched.fasta', "fasta")
        print(records)
        print('stopped at ',entry.id,' with ',round(n/num_lines,2),'% finished')

file_name = 'your_blast_xml_file.xml'
get_ids_from_server(get_ids(file_name))
