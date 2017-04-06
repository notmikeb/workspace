from lxml import etree, objectify

#----------------------------------------------------------------------
def parseXML(xmlFile):
    """"""
    with open(xmlFile) as f:
        xml = f.read()

    root = objectify.fromstring(xml)

    # print the xml
    obj_xml = etree.tostring(root, pretty_print=True)
    print obj_xml

    # save your xml
    with open("new.xml", "w") as f:
        f.write(obj_xml)

#----------------------------------------------------------------------
if __name__ == "__main__":
    f = r'sample.xml'
    parseXML(f)
