from panda3d.core import PerspectiveLens
import math

class CamerasManager(object):

	def __init__(self):
		self.currCam = base.cam
		self.__camerasDict = {}		
		self.__camerasDict['default'] = base.cam

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

	def destroy(self):		
		for cam in self.__camerasDict:
			if cam != 'default':
				print 'removing cam', cam
				self.__camerasDict[cam].remove()
		base.cam.node().setActive(1)
		self.__camerasDict = {}
		self.__camerasDict['default'] = base.cam
