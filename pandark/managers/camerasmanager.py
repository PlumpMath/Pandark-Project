from panda3d.core import PerspectiveLens
import math
class CamerasManager(object):

	def __init__(self):
		self.currCam = base.cam
		self.__camerasDict = {}		
		self.__camerasDict['default'] = self.currCam

	def getCamera(self,name):
		if name in self.__camerasDict:return self.__camerasDict[name]
		print 'Camera not found.'
		return self.currCam

	def createCamera(self,props):
		name = props['name']

		cam = base.makeCamera(base.win, camName=name )

		cam.setPosQuat( props['pos'], props['quat'] )

		cam.node().setActive(0)

		lens = cam.node().getLens()

		lens.setNearFar( props['clipping'].x, props['clipping'].y )

		fov = math.degrees( props['fov'] ) 

		lens.setFov(fov*lens.getAspectRatio(), fov)
		
		self.__camerasDict[name] = cam

		return cam

	def active(self,camName):
		cam = self.__camerasDict[camName]
		cam.node().setActive(1)
		self.currCam.node().setActive(0)
		self.currCam = cam
