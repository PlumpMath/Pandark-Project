from panda3d.core import PerspectiveLens

class CamerasManager(object):

	def __init__(self):
		self.__camerasDict = {}

	def getCamera(self,name):
		return self.__camerasDict[name]