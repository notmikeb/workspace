import wx
import wx.lib.fancytext as fancytext

class ColorGauge(wx.Control):
	default_color = "GREEN"  # "MAGENTA","BLUE"  # "GREEN" "RED" "YELLOW"
	def __init__(self, parent,id,pos=wx.DefaultPosition,size=wx.DefaultSize):
		wx.Control.__init__(self, parent, id,pos,size)
		self.SetBackgroundColour(wx.WHITE)
		self.color= ColorGauge.default_color
		self.percent = 0.0
		self.step = 0.0
		wx.EVT_PAINT(self, self.OnPaint)
		#wx.EVT_SIZE(self, self.OnSize)

	def OnPaint(self, evt):
		dc = wx.PaintDC(self)
		dc.Clear()
		dc.BeginDrawing()

		dc.SetPen( wx.Pen(self.color,0) )
		dc.SetBrush( wx.Brush(self.color) )
		w,h = self.GetSizeTuple()
		dc.DrawRectangleRect((0,0,w*self.percent,h))
		percentStr= "%d%%"% int(self.percent*100)
		tx, ty = fancytext.getExtent(percentStr, dc)
		dc.DrawText(percentStr, w/2-tx/2, h/2-ty/2)

		dc.EndDrawing()
		
	def setPercent(self,percent):
		if percent <0 or percent >1.:
			return
		self.percent = percent
	def setColor(self,color):
		self.color = color
	def getColor(self): 
		return self.color
	
	def setStep(self,step):
		self.step=step
	def makeStep(self):
		if self.percent>=1.: return
		self.percent+=self.step
		if self.percent>1.:
			self.percent=1.
		self.Refresh()
		self.Update()
	#def OnSize(self, evt):
	#	print "evt=",evt, "OnSize", self.GetSize()

class TestDialog(wx.Dialog):
	"This Dialog can be normally closed"
	def __init__(self, *args, **kwargs):
		wx.Dialog.__init__(self,*args, **kwargs)
		wx.EVT_CLOSE(self, self.OnCloseWindow)

		cid=wx.NewId()
		gauge2 = ColorGauge(self,cid, (10,10), (200,30))

		cid=wx.NewId()
		gauge = ColorGauge(self,cid, (10,70), (200,30))
		gauge.setPercent(0.51)
		gauge.SetSize((570,30)) # test resize

		cid=wx.NewId()
		gauge3 = ColorGauge(self,cid, (10,110), (570,30))
		gauge3.setPercent(0.49)
		gauge3.setColor("red")
		
		cid=wx.NewId()
		gauge4 = ColorGauge(self,cid, (10,150), (570,30))
		gauge4.setPercent(0.75)
		gauge4.setColor("yellow")

		cid=wx.NewId()
		gauge5 = ColorGauge(self,cid, (10,210), (570,30))
		gauge5.setColor("magenta")
		gauge5.setPercent(.0)
		gauge5.setStep(1./3)
		self.gauge5=gauge5
		
		cid=wx.NewId()
		btnRun = wx.Button(self, cid, "Run", (10, 260),(90,25)).SetDefault()
		wx.EVT_BUTTON(self, cid, self.OnButtonRun)
		
	def OnCloseWindow(self, event):
		self.Destroy()

	def OnButtonRun(self,event):
		self.gauge5.makeStep()

class App(wx.App):
	def OnInit(self):
		# Dialog is used here because Frame resizes its childs according to its own layout opinion
		win = TestDialog(None, -1, "Test ColorGauge", size = (600, 450))

		self.SetTopWindow(win)
		win.Show(True)
		return True

if __name__=='__main__':
	#def main(argv):
	app = App(0)
	app.MainLoop()
