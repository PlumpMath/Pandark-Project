from panda3d.core import PerspectiveLens

class CamerasManager(object):

	def __init__(self):
		self.__camerasDict = {}
		self.currCam = base.cam

	def getCamera(self,name):
		return self.__camerasDict[name]

	def createCamera(self,props):
		name = props['name']

		np = base.makeCamera(base.win, camName=name )

		np.setPosQuat( props['pos'], props['quat'] )

		np.node().setActive(0)
		
		self.__camerasDict[name] = np

		return np

	def active(self,camName):
		cam = self.__camerasDict[camName]
		cam.node().setActive(1)
		self.currCam.node().setActive(0)
		self.currCam = cam
