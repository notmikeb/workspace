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
    @property
    def tcName(self):
        tagname = 'tcName'
        if self.nsmap[None]:
            tagname = "{" + "{}".format(self.nsmap[None]) + "}" + tagname
        #print tagname
        for i in range(len(self)):
            if self[i].tag == tagname:
                return self[i].text
        return "UnknowTcName"
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
        field = []
        for i in range(len(self)):
            if not isinstance(self[i], TestCaseElement) and not isinstance(self[i], PropertyListElement):
                field.append([self[i].tag, self[i].text])
        return field

    def getPropertyList(self):
        for i in range(len(self)):
            if isinstance(self[i], PropertyListElement):
               return self[i]
        return None


lookup = etree.ElementNamespaceClassLookup()
parser = etree.XMLParser()
parser.set_element_class_lookup(lookup)

namespace = lookup.get_namespace('http://schemas.datacontract.org/2004/07/DAY.TestPlan')
namespace['TestCase'] = TestCaseElement
namespace['PropertyList'] = PropertyListElement

namespace = lookup.get_namespace('')
namespace['PropertyList'] = PropertyListElement

## example
#xml = "".join( open("sample.xml","r").readlines())
#root = etree.XML(xml, parser)
