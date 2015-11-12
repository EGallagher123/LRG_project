import xml.etree.ElementTree as tree

#parses sml file
LRG_tree= tree.parse('LRG_263.xml')
root = LRG_tree.getroot()

#should print out "1.9" if worked
print root.attrib['schema_version']
