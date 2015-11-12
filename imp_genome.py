import xml.etree.ElementTree as tree
LRG_tree = tree.parse('LRG_263.xml')

for parent in LRG_tree.getiterator('fixed_annotation'):
	for child in parent:
		if child.tag == 'sequence':
			sequence = child.text
			genome_list = list(sequence)
			print genome_list[0:10]

