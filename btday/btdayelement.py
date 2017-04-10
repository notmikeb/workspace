import lxml
from lxml import etree

class PropertyListElement(etree.ElementBase):
    def getDataList(self):
        data = []
        for i in range(len(self)):
            # objValueString, sName, typeString
            if self[i].tag == "{http://schemas.datacontract.org/2004/07/DAY.Utilities}DynamicProperty":
                data.append([self[i][1].text, self[i][0].text, self[i][2].text])
            else:
                print len(self[i]), self[i].tag
        return data

class TestCaseElement(etree.ElementBase):
    tag = "TestCase"
    @property
    def tcName(self):
        tagname = 'tcName'
        #if self.nsmap[None]:
        #    tagname = "{" + "{}".format(self.nsmap[None]) + "}" + tagname
        #print tagname
        for i in range(len(self)):
            if self[i].tag == tagname:
                return self[i].text
            else:
                #print self[i].tag, type(self[i].tag), tagname
                pass
        return "UnknownTcName"
    def hasChild(self):
        for i in range(len(self)):
            if isinstance(self[i], TestCaseElement):
                return True
        return False
    def childCount(self):
        num = 0
        for i in range(len(self)):
            if isinstance(self[i], TestCaseElement):
                num+=1
        return num
    def getChild(self, index):
        num = 0
        for i in range(len(self)):
            if isinstance(self[i], TestCaseElement):
                if index == num:
                   return self[i]
                num+=1
        return None
    def getFieldList(self):
        field = {}
        for i in range(len(self)):
            if not isinstance(self[i], TestCaseElement) and not isinstance(self[i], PropertyListElement):
                field[self[i].tag] = self[i].text
        return field

    def getPropertyList(self):
        for i in range(len(self)):
            if isinstance(self[i], PropertyListElement):
               return self[i]
        return None


def remove_namespace(doc, namespace):
    """Remove namespace in the passed document in place."""
    ns = u'{%s}' % namespace
    nsl = len(ns)
    for elem in doc.getiterator():
        if elem.tag.startswith(ns):
            elem.tag = elem.tag[nsl:]

g_ns1 = "http://www.w3.org/2001/XMLSchema-instance"
g_ns2 = "http://schemas.datacontract.org/2004/07/DAY.TestPlan"

lookup = etree.ElementNamespaceClassLookup()
parser = etree.XMLParser()
parser.set_element_class_lookup(lookup)

namespace = lookup.get_namespace('http://schemas.datacontract.org/2004/07/DAY.TestPlan')
namespace['TestCase'] = TestCaseElement
namespace['PropertyList'] = PropertyListElement

namespace = lookup.get_namespace('')
namespace['TestCase'] = TestCaseElement
namespace['PropertyList'] = PropertyListElement

## example
#xml = "".join( open("sample.xml","r").readlines())
#root = etree.XML(xml, parser)
