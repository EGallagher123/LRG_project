def imp_genome():
	for parent in LRG_tree.getiterator('fixed_annotation'):
		for child in parent:
			if child.tag == 'sequence':
				sequence = child.text
				genome_list = list(sequence)
				print genome_list