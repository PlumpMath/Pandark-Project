#from direct.stdpy.file import open as openFile
#from direct.stdpy import thread
#from panda3d.core import NodePath, Point3
import yaml

from panda3d.core import AmbientLight, Fog

from pandark.managers.lightsmanager import LightsManager
lightsMgr = LightsManager()

from pandark.managers.animationsmanager import AnimationsManager
animsMgr = AnimationsManager()

import game.classes

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

			if self.environment['fog']['mode'] == "linear":
				fog.setLinearRange(self.environment['fog']['linearStart']*1000,self.environment['fog']['linearEnd']*1000)
			else:
				fog.setExpDensity( self.environment['fog']['expDensity'] )

			render.setFog(fog)

		[self.createNode(props) for props in self.nodes]
		[self.createLight(props) for props in self.lights]
		[self.createEntity(props) for props in self.entities]
		#[self.createAnimation(anim) for anim in self.animations]
		[self.createStaticGeoms(props) for props in self.staticGeoms]

		#[thread.start_new_thread( self.createEntity, (props, ) ) for props in self.entities]

		#self.__nodesDict    = {}

	def reset(self):		
		self.__nodesDict    = {}
		self.__lightsDict   = {}
		self.__camerasDict  = {}
		self.__entitiesDict = {}

		self.__nodesDict[''] = render

	def getEnt(self,name):		
		return self.__entitiesDict[name]

	def createNode(self,props):
		#animations = self.animations[props['name']]
		parent = render.find('**/'+props['groupName']) or render

		node = NodePath(props['name'])

		node.setPos(props['pos'])

		node.setQuat(props['quat'])

		node.setScale(props['scale'])

		node.reparentTo(parent)

		self.__nodesDict[props['name']] = node

	def createLight(self,props):
		lightsMgr.setLight[props['type'] ](props)

	def createEntity(self,props):

		props['parent'] = self.__nodesDict[props['groupName']]

		name =  props['name']

		ent = yaml.load( self.yamlList[name] )

		model = loader.loadModel( ent.model_path )

		ent.init(model,props)

		self.__entitiesDict[name] = ent

		animsMgr.createAnimation(ent.getNode(), self.animations[name])

	def createStaticGeoms(self,props):
		path = props['configFile']

		stream = file('assets/classes/'+path+'.class', 'r')

		ent = yaml.load( stream )

		ent.init(props)