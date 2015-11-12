import xml.etree.ElementTree as tree
LRG_tree = tree.parse('LRG_263.xml')
root = LRG_tree.getroot()


for parent in LRG_tree.getiterator('fixed_annotation'):
    for child in parent:
            if child.tag == 'transcript':
                transcript_name = child.attrib
                print transcript_name

            	for child in child:
                	if child.tag == 'exon':
                		exon_name = child.attrib['label']
                		print 'Exon: ', exon_name


                		for child in child:	
                			if child.tag == 'coordinates':
                				if child.attrib['coord_system'] == 'LRG_263': #change this to be the ID number at the begining 	
                					LRG_no = child.attrib['coord_system']
                					start_coord_exon = child.attrib['start']
                					end_coord_exon = child.attrib['end']
                					strand_no = child.attrib['strand']
                					print 'LRG number: ', LRG_no
                					print 'Exon start: ', start_coord_exon
                					print 'Exon end: ', end_coord_exons
                					print 'Strand number: ', strand_no
                					print ''


	 