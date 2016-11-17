

class mydir():
  i = 1
  #__slots__ == []
  def __repr__(self):
    print "mydir __repr__"
    return "__repr__(mydir)"
    
  def items(self):
    return [(1,2), (3,4)]

  def __getattribute__(self, key):
    try: 
        return object.__getattribute__(self, key)
    except:
        if key in self:
           return self[key]
        else:
           raise
  def __dir__(self):
    print("mydir __dir__")
    names = [k for k in self.keys() ]
    return names
  def __str__(self):
    return "daylong"
  def __iter__(self):
    while self.i < 5:
      yield "{}".format(self.i)
      self.i += 1
    self.i = 0

a = mydir()
print (a)
print(repr(a))
for i in a:
  print (i)
for i in a:
  print (i)