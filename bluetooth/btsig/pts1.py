import xml.etree.ElementTree as ET

tree = ET.parse("sample1.xml")

# this element holds the phonebook entries
#<project>
#  <qdid>130773</qdid>
#  <project_name>tuv</project_name>
#  <pics>
#    <profile>
#      <name>1L2CAP</name>
#      <item>
#        <table>2</table>
#        <row>19</row>
#      </item>


def sort_pics(tree):
  container = tree.find("pics")
  data = []
  for elem in container:
    key = elem.findtext("name")
    print('key ' + key)
    data.append((key, elem))
  data.sort()

  # insert the last item from each tuple
  container[:] = [item[-1] for item in data]

def get_key_by_table_row(key1, key2):
  key = "table" + " " * (10-len(key1)) + key1 + "-" 
  key += " " * (10-len(key2)) + key2
  return key

def sort_profile( subroot):
  container = subroot
  print("subroot is " + repr(subroot))
  name = subroot.findtext('name')
  data = []
  predata = []
  for elem in container:
     if elem.tag == 'item':
        key1 = elem.findtext("table")
        key2 = elem.findtext("row")
        key = get_key_by_table_row(key1,key2) 
        data.append( (key, elem) ) # prepare to sort
     else:
        predata.append(elem)

  print('before "{}"'.format(name))
  print("\n".join( [i[0] for i in data] ) )
  data.sort()
  print('after "{}"'.format(name))
  print("\n".join( [i[0] for i in data] ) )

  # insert the last item from each tuple
  container[:] =  predata + [item[-1] for item in data]


# sort elements under pics
#sort_pics(tree)

# sort elements under  pics/profile
container = tree.find('pics')
pall = container.findall('profile')
if pall:
  for p1 in pall:
    sort_profile(p1)
  container[:] = [p0 for p0 in pall]


#tree.write("sample2.xml")
with open('sample2.xml', 'w') as f1:
  f1.write(ET.tostring(tree.getroot(), encoding='utf8').decode())

def get_dict_count(filename):
  tree = ET.parse("sample1.xml")
  adict = {}
  for i in tree.iter():
    if i.tag:
       adict[i.tag] = adict.setdefault( i.tag, 0) + 1
    else:
       adict['None'] = adict.setdefault( 'None', 0) + 1
  return adict

def dict_compare(dict1, dict2):
  keys = dict2.keys()
  for k1 in dict1.keys():   
      if k1 not in keys:
          raise Exception("dict2 doens't have '{}' tag count".format(k1))
      if dict1[k1] != dict2[k1]:
          raise Exception("dict1[{}] {} != dict2[{}] {}".format(k1, dict1[k1], k1, dict2[k1]))
  keys = dict1.keys()
  for k1 in dict2.keys():   
      if k1 not in keys:
          raise Exception("dict1 doens't have '{}' tag count".format(k1))
      if dict1[k1] != dict2[k1]:
          raise Exception("dict1[{}] {} != dict2[{}] {}".format(k1, dict1[k1], k1, dict2[k1]))
  if len(dict1.keys()) != len(dict2.keys()):
      raise Exception("dict1 and dict2 key number not match")
      
# auto check some tag count
adict1 = get_dict_count("sample1.xml")
adict2 = get_dict_count("sample2.xml")
dict_compare(adict1, adict2)


