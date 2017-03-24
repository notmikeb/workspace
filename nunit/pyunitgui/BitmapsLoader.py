#from wxPython.wx import *
import wx

class BitmapsLoader:
	def load(self,pattern,count):
		files=map(lambda n: pattern%n, range(1,1+count))
		bml=[]
		for name in files:
			bml.append(wx.Bitmap(name, wx.BITMAP_TYPE_BMP))
		return bml
