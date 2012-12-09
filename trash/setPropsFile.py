import re
class Test:	

	def __init__(self):
		self.__func = {}
		self.__func[0] = self.go
		self.__func[1] = self.sleep

	def call(self,fid,*args):
		return self.__func[fid](args)
	
	def go(self,*args):
		print 'go',args

	def sleep(self,*args):
		print 'sleep',args

func = {}

name = "hide-box-props"

shapetype = re.findall("[a-z]+",name.lower())

shapetype = name.split('-')

t = Test()

t.call(1,'fred',20)