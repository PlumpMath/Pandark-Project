from panda3d.core import DirectionalLight, PointLight, Spotlight, PerspectiveLens

class LightsManager(object):

	def __init__(self):
		self.__lightsDict = {}
		self.setLight = {}
		self.setLight['directional'] = self.__setDirectionalLight
		self.setLight['point']       = self.__setPointLight
		self.setLight['spot']        = self.__setSpotlight

	def __setDirectionalLight(self,props):
		light = DirectionalLight(props['name'])
		light.setShadowCaster(props['castShadows'],1024,1024)
		lens = PerspectiveLens()
		light.setLens(lens)
		lens.setFov(1200/props['pos'].z)	
		#light.showFrustum()
		self.__setLight(light,props)

	def __setPointLight(self,props):
		#for p in props:print p,props[p]
		light = PointLight(props['name'])
		light.setAttenuation(props['attenuation'])
		#light.showFrustum()	
		#print light.getPoint()
		#light.setPoint( Point3(props['pos']) )
		self.__setLight(light,props)

	def __setSpotlight(self,props):
		light = Spotlight(props['name'])
		light.setShadowCaster(props['castShadows'],2048,2048)
		light.setAttenuation(props['attenuation'])		
		lens = PerspectiveLens()
		lrange = props['range'] / 0.0174533 #to fix Ogremax values
		lens.setFov(lrange.x)
		lens.setFilmSize(5096); 
		light.setLens(lens)
		#light.showFrustum()	
		#print 'exp',light.getExponent()
		self.__setLight(light,props)

	def __setLight(self,light,props):
		light.setColor(props['colourDiffuse'])		
		light.setSpecularColor(props['colourSpecular'])
		light.setScene(render)
		node = render.attachNewNode(light)
		node.setPosQuat(props['pos'], props['quat'] )
		render.setLight(node)

		self.__lightsDict[props['name'] ] = light

	def getLight(self,name):
		return self.__lightsDict[name]