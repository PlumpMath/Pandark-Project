from panda3d.core import NodePath, Point3
#from direct.stdpy.file import open as openFile
#from direct.stdpy import thread
import yaml

import game.classes

from panda3d.core import PointLight, Spotlight, PerspectiveLens

class Test(object):

	def __init__(self):
		print "======================================================="

class LightManager(object):
	def __init__(self):
		self.setLight = {}
		self.setLight['point'] = self.__setPointLight	
		self.setLight['spot'] = self.__setSpotLight

	def __setPointLight(self,props):
		for p in props:print p,props[p]
		light = PointLight(props['name'])
		light.showFrustum()	
		#print light.getPoint()
		#light.setPoint( Point3(props['pos']) )
		#light.upcastToLensNode()
		self.__setLight(light,props)

	def __setSpotLight(self,props):
		light = Spotlight(props['name'])
		lens = PerspectiveLens()
		print 1.0472 / 0.0174533#(x/ogremax value)
		lens.setFov(60)
		light.setLens(lens)
		light.showFrustum()	
		print 'exp',light.getExponent()

		self.__setLight(light,props)

	def __setLight(self,light,props):
		light.setColor(props['colourDiffuse'])
		light.setAttenuation(props['attenuation'])
		light.setSpecularColor(props['colourSpecular'])
		node = render.attachNewNode(light)
		node.setPosQuat(props['pos'], props['quat'] )
		render.setLight(node)


lightMgr = LightManager()

class Builder(object):

	def __init__(self,nodes,lights,cameras,entities,animations,staticGeoms,yamlList):

		self.reset()

		self.nodes       = nodes
		self.lights      = lights
		self.cameras     = cameras         
		self.entities    = entities       
		self.animations  = animations
		self.staticGeoms = staticGeoms

		self.yamlList = yamlList

	def start(self):
		[self.createNode(props) for props in self.nodes]
		[self.createLight(props) for props in self.lights]
		[self.createEntity(props) for props in self.entities]
		[self.createStaticGeoms(props) for props in self.staticGeoms]

		#[thread.start_new_thread( self.createEntity, (props, ) ) for props in self.entities]
		self.__nodesList    = {}

	def reset(self):		
		self.__nodesList    = {}
		self.__lightsList   = {}
		self.__camerasList  = {}
		self.__entitiesList = {}

		self.__nodesList[''] = render

	def getEnt(self,name):		
		return self.__entitiesList[name]

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

		self.__nodesList[props['name']] = node

	def createEntity(self,props):

		props['parent'] = self.__nodesList[props['groupName']]

		name =  props['name']

		ent = yaml.load( self.yamlList[name] )

		model = loader.loadModel( ent.model_path )

		ent.init(model,props)

		self.__entitiesList[name] = ent

	def createStaticGeoms(self,props):
		path = props['configFile']

		stream = file('assets/classes/'+path+'.class', 'r')

		ent = yaml.load( stream )

		ent.init(props)