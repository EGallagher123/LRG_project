#--------------------------------------------------------------------------------------------------------
# importing and parsing the XML document

LRG_code = raw_input('Please enter your LRG file name (with file extension): ')

import xml.etree.ElementTree as tree 
LRG_tree = tree.parse(LRG_code)
root = LRG_tree.getroot()


#--------------------------------------------------------------------------------------------------------
# this section will extract information from the xml file such as the LRG id number for the gene and the reference sequence source.
# this information (LRG id_no) will be used in a later section of code in order to check that the correct exon locations are correct.

for parent in LRG_tree.getiterator('fixed_annotation'):
	for child in parent:
		if child.tag == 'id':
			id_no = child.text
			print 'LRG file number: ', id_no
		if child.tag == 'sequence_source':
			seq_source = child.text
			print 'Reference sequence source: ', seq_source

# This section prints out the name of the gene from the xml file
for parent in LRG_tree.getiterator('updatable_annotation'):
	for child in parent:
		if child.tag == 'annotation_set' and child.attrib['type'] == 'lrg':
			for child in child:
				if child.tag == 'lrg_locus':
					gene_name = child.text
					print 'Gene name: ', gene_name


#--------------------------------------------------------------------------------------------------------
# Initiating lists for future use

list_of_starts = []
list_of_ends = []
exon_start_minus_1 = []
intron_seq = []


#--------------------------------------------------------------------------------------------------------
# Gets genome sequence from XML file and converts from string into a list

#look throuh the parent tags to find the one of interest
for parent in LRG_tree.getiterator('fixed_annotation'):
#within the parent of interest look for the child tag of interest
	for child in parent:
		if child.tag == 'sequence':
			#define the text within the child tag as a text variable
			sequence = child.text
			#onvert the variable to a list
			genome_list = list(sequence)
			#print genome_list[:10]


#--------------------------------------------------------------------------------------------------------
#For loops to extract inforamtion about the start and end positions of the exons, alongside checks to make sure that the correct information is being extracted. start and end positions are put into lists.

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

list_of_starts = map(int, list_of_starts) 
list_of_ends = map(int, list_of_ends)

print 'Exon start positons:', list_of_starts 
print 'Exon end positions:', list_of_ends


#--------------------------------------------------------------------------------------------------------
#calculates the number of introns in the sequence by taking the number of exons and minusing one.

number_of_introns = len(list_of_starts) - 1

print 'number of introns: ', number_of_introns


#--------------------------------------------------------------------------------------------------------
# minuses one from all the exon start positions to get the value for the end of the intron 

for item in list_of_starts:
		item_minus_1 = item - 1
		exon_start_minus_1.append(item_minus_1)
print 'Exon start - 1: ', exon_start_minus_1


#--------------------------------------------------------------------------------------------------------
# removes the first start value of the exon, and the last end value of the exon as these are not needed to calculate introns

exon_start_minus_1.pop(0)

print 'starts: ', exon_start_minus_1

list_of_ends.pop(number_of_introns)

print 'ends: ', list_of_ends


#--------------------------------------------------------------------------------------------------------
# Getting the intron sequence using intron coordinates


len_lis_starts = len(list_of_starts) -1 #to set the range for the loop using the number of introns


#loops through each intron using the coordinates stored in the list of ends and the exon start minus 1 paired to give the boundaries of the introns. 
for item in range(len_lis_starts): 
	a = list_of_ends[item]
	b = exon_start_minus_1[item]
	intron_seq = genome_list[a:b]
	intron_seq_string = ''.join(intron_seq)
	print a
	print b	
	print intron_seq_string

#--------------------------------------------------------------------------------------------------------
'''
'''
                		for child in child:	#the next code will look for the children of exon under the coordinates tag. 
                			if child.tag == 'coordinates':
                				if child.attrib['coord_system'] == 'LRG_263': #change this to be the ID number at the begining 	
                					LRG_no = child.attrib['coord_system'] #we want to print this so the user can manually check the LRG number
                					start_coord_exon = child.attrib['start'] #this will show the exon start position
                					end_coord_exon = child.attrib['end'] #this will show the exon end position
                					strand_no = child.attrib['strand'] #this ensures that the correct strand is being looked at. It also enables another check as only the genomic sequence has strand number information. If no strand information is present, it is likely that the information is not correct about the start and the end. 
                					print 'LRG number: ', LRG_no
                					print 'Exon start: ', start_coord_exon
                					print 'Exon end: ', end_coord_exons
                					print 'Strand number: ', strand_no
                					print ''
'''

