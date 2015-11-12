import xml.etree.ElementTree as tree
LRG_tree = tree.parse('LRG_263.xml')

'''look throuh the parent tags to find the one of interest'''
for parent in LRG_tree.getiterator('fixed_annotation'):
'''within the parent of interest look for the child tag of interest'''	
	for child in parent:
		if child.tag == 'sequence':
			'''define the text within the child tag as a text variable'''
			sequence = child.text
			'''convert the variable to a list'''
			genome_list = list(sequence)
			print genome_list[0:10]

import xml.etree.ElementTree as tree
LRG_code = input('enter LRG code:')
LRG_tree = tree.parse('LRG_code''.xml')