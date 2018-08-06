from direct.showbase.ShowBase import ShowBase
import sys

print(sys.version) 
class MyApp(ShowBase):
 
    def __init__(self):
        ShowBase.__init__(self)
 
app = MyApp()
app.run()