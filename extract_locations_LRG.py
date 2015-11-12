import xml.etree.ElementTree as tree #this code is used to test and it is a copy of the code already written in the "LRG_import_xml.py file"
LRG_tree = tree.parse('LRG_263.xml')
root = LRG_tree.getroot()


for parent in LRG_tree.getiterator('fixed_annotation'): #this code finds the parent in the tree
    for child in parent: #the firs child that needs to be identified is the transcript child
            if child.tag == 'transcript': #if the child tag is transcript then we want to print out the transcript name
                transcript_name = child.attrib
                print transcript_name

            	for child in child: #next we need to identify the exon number that we are looking at and print it
                	if child.tag == 'exon':
                		exon_name = child.attrib['label']
                		print 'Exon: ', exon_name


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


	 