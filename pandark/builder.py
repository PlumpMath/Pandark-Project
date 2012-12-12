#from direct.stdpy.file import open as openFile
#from direct.stdpy import thread
#from panda3d.core import NodePath, Point3
import yaml

import game.classes
from panda3d.core import AmbientLight, Fog
from panda3d.core import DirectionalLight, PointLight, Spotlight, PerspectiveLens

'''TODO: Separate Class File'''
class LightManager(object):

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


lightMgr = LightManager()

class Builder(object):

	def __init__(self,environment,nodes,lights,cameras,entities,animations,staticGeoms,yamlList):

		self.reset()

		self.environment = environment
		self.nodes       = nodes
		self.lights      = lights
		self.cameras     = cameras         
		self.entities    = entities       
		self.animations  = animations
		self.staticGeoms = staticGeoms

		self.yamlList = yamlList

	def start(self):
		base.setBackgroundColor( self.environment['colourBackground'] )

		alight = AmbientLight('AmbientLight')
		alight.setColor(self.environment['colourAmbient'] )
		alnp = render.attachNewNode(alight)
		render.setLight(alnp)

		if self.environment['fog']:
			fog = Fog( 'sceneName' )
			fog.setColor( self.environment['fog']['color'] ) 
			fog.setExpDensity( self.environment['fog']['expDensity'] )
			render.setFog(fog)

		[self.createNode(props) for props in self.nodes]
		[self.createLight(props) for props in self.lights]
		[self.createEntity(props) for props in self.entities]
		[self.createStaticGeoms(props) for props in self.staticGeoms]

		#[thread.start_new_thread( self.createEntity, (props, ) ) for props in self.entities]
		self.__nodesDict    = {}

	def reset(self):		
		self.__nodesDict    = {}
		self.__lightsDict   = {}
		self.__camerasDict  = {}
		self.__entitiesDict = {}

		self.__nodesDict[''] = render

	def getEnt(self,name):		
		return self.__entitiesDict[name]

	def createLight(self,props):
		lightMgr.setLight[props['type'] ](props)

	def createNode(self,props):
		#animations = self.animations[props['name']]
		parent = render.find('**/'+props['groupName']) or render

		node = NodePath(props['name'])

		node.setPos(props['pos'])

		node.setQuat(props['quat'])

		node.setScale(props['scale'])

		node.reparentTo(parent)

		self.__nodesDict[props['name']] = node

	def createEntity(self,props):

		props['parent'] = self.__nodesDict[props['groupName']]

		name =  props['name']

		ent = yaml.load( self.yamlList[name] )

		model = loader.loadModel( ent.model_path )

		ent.init(model,props)

		self.__entitiesDict[name] = ent

	def createStaticGeoms(self,props):
		path = props['configFile']

		stream = file('assets/classes/'+path+'.class', 'r')

		ent = yaml.load( stream )

		ent.init(props)