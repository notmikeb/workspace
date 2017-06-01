import sys
sys.path.append(r'C:\Python24\Lib')

import clr
clr.AddReference("System.Windows.Forms")

from System.Windows.Forms import Application, Form

class HelloWorldForm(Form):

    def __init__(self):
        self.Text = 'Hello World'
        self.Name = 'Hello World'

form = HelloWorldForm()
Application.Run(form)