''''''
import xml.etree.ElementTree as tree

''' Four lists are initialised for future use: list_of_starts; list_of_ends; exon_start_minus_1; intron_seq '''
list_of_starts = []
list_of_ends = []
exon_start_minus_1 = []
intron_seq = []

'''A FASTA file is opened and the output of this code will be saved within this file.'''
out_file = open('gene_introns.fasta', 'w')

'''The user is asked to input a filename using 'raw_input' and this is saved as 'LRG_code'''
LRG_code = raw_input('Please enter your LRG file name (with file extension): ')

'''The xml file corresponding to 'LRG_code' is parsed using ElementTree'''
LRG_tree = tree.parse(LRG_code)

#--------------------------------------------------------------------------------------------------------
'''Section 1: This section extracts information from the xml file (LRG ID, RefSeq ID, Gene name)'''

def get_id_no(parsed_tree):
	'''The 'get_id_no' function returns the LRG ID number using a for loop'''
	for parent in parsed_tree.getiterator('fixed_annotation'):
		for child in parent:
			if child.tag == 'id':
				id_no = child.text
			return id_no


def get_seq_source(parsed_tree):
	'''The 'get_seq_source' function returns the reference sequence ID using a for loop'''
	for parent in parsed_tree.getiterator('fixed_annotation'):
		for child in parent:						
			if child.tag == 'sequence_source':
				return child.text				


def get_gene_name(parsed_tree):
	''' The 'get_gene_name' function returns the name of the gene using a for loop'''
	for parent in parsed_tree.getiterator('updatable_annotation'):
		for child in parent:
			if child.tag == 'annotation_set' and child.attrib['type'] == 'lrg':
				for child in child:
					if child.tag == 'lrg_locus':
						return child.text
	
'''The get_id_no, get_seq_source and get_gene_name functions are called and the outputs are printed'''
id_no = get_id_no(LRG_tree)
print 'LRG ID: ', id_no	
seq_source = get_seq_source(LRG_tree)
print 'RefSeq ID: ', seq_source
gene_name = get_gene_name(LRG_tree)
print 'Gene: ', gene_name

#--------------------------------------------------------------------------------------------------------
'''Section 2: This section gets the entire genome sequence from the xml file and converts it from a string into a list'''

def get_genome_list(parsed_tree):
	'''The 'get_genome_list' function gets the genome sequence from the XML file and checks that all nucleotides are allowed'''
	nucleotide_list = ['A', 'T', 'G', 'C']
	non_nucleotides = 0
	is_nucleotides = 0
	#look throuh the parent tags to find the one of interest
	for parent in parsed_tree.getiterator('fixed_annotation'):
	#within the parent of interest look for the child tag of interest
		for child in parent:
			if child.tag == 'sequence':
				#define the text within the child tag as a text variable
				sequence = child.text
				#onvert the variable to a list
				genome_list = list(sequence)
				#print genome_list[:10]

	for nucleotide in genome_list:
		if nucleotide not in nucleotide_list:
			non_nucleotides += 1		
		else: 
			is_nucleotides += 1	
	
	if non_nucleotides > 0:
		return 'Error: non-nucleotide present'
	else:
		return genome_list

'''The output from get_genome_list function is saved within the 'genome_list' variable for future use'''
genome_list = get_genome_list(LRG_tree)


 #-------------------------------------------------------------------------------------------------------
'''Section 3: This section uses for loops to extract the start and end positions of the exons from the xml file and checks the correct informatrion in extracted. The start positions of all exons are added
   added to list_of_starts and the end positions are added to list_of_ends.'''
for parent in LRG_tree.getiterator('fixed_annotation'): #this code finds the parent in the tree
    for child in parent: #the firs child that needs to be identified is the transcript child
            if child.tag == 'transcript': #if the child tag is transcript then we want to print out the transcript name
                transcript_name = child.attrib
                #print transcript_name

            	for child in child: #next we need to identify the exon number that we are looking at and print it
                	if child.tag == 'exon':
                		exon_name = child.attrib['label']
                		#print 'Exon: ', exon_name

				for child in child:
					if child.tag == 'coordinates':
						if child.attrib['coord_system'] == id_no: #change this to be the ID number at the begining
           						start_coord_exon = child.attrib['start'] 
           						list_of_starts.append(start_coord_exon)
           						end_coord_exon = child.attrib['end']
           						list_of_ends.append(end_coord_exon)
           						strand_no = child.attrib['strand'] #this ensures that the correct strand is being looked at. It also enables another check as only the genomic sequence has strand number information. If no strand information is present, it is likely that the information is not correct about the start and the end. 			           		

             				
#--------------------------------------------------------------------------------------------------------
#turns the strins into integers in the list of starts and end exon positions
'''The lists with exon positions are composed of strings so the 'map' python function converts these into lists of integers. Then, the length of each list minus 1 is used to calculate the total number of 
   introns and this number is printed.'''
list_of_starts = map(int, list_of_starts) 
list_of_ends = map(int, list_of_ends)

number_of_introns = len(list_of_starts) - 1

print 'Number of expected introns: ', number_of_introns
print ''

#--------------------------------------------------------------------------------------------------------
'''For list_of_starts, the intron end positions are calculated using each start position minus 1'''
for item in list_of_starts:
		item_minus_1 = item - 1
		exon_start_minus_1.append(item_minus_1)


#--------------------------------------------------------------------------------------------------------
'''The 'pop' python function is used to remove the first value in the exon_start_minus_1 list and remove the last value in the list_of_ends list. This finalises the intron start and end positions'''
exon_start_minus_1.pop(0)
list_of_ends.pop(number_of_introns)

#--------------------------------------------------------------------------------------------------------
'''Section 4: This section takes the intron positions, maps them to the genome_list and takes slices from the list, converting them into strings of nucleotides. These outputs are then exported into
   the FASTA file created earlier'''

len_lis_starts = len(list_of_starts) -1 #to set the range for the loop using the number of introns

#loops through each intron using the coordinates stored in the list of ends and the exon start minus 1 paired to give the boundaries of the introns. 
for item in range(len_lis_starts): 
	a = list_of_ends[item]
	b = exon_start_minus_1[item]

	assert(b>=a), 'Intron end is smaller than intron start'

	intron_seq = genome_list[a:b]
	intron_seq_string = ''.join(intron_seq)
	print 'Intron number: ', item + 1
	print 'Intron position: ', a, '-', b	
	print intron_seq_string
	print ''
	item_string = str(item + 1)
	Intron_seq_label = '> intron|' 
	item_and_seq_label = Intron_seq_label + item_string
	out_file.write(item_and_seq_label)
	word_start = '|Start|'
	out_file.write(word_start)
	a_string = str(a)
	out_file.write(a_string)
	word_end = '|End|'
	out_file.write(word_end)
	b_string = str(b)
	out_file.write(b_string)
	out_file.write("\n")
	out_file.write(intron_seq_string)
	out_file.write("\n")
	out_file.write("\n")




