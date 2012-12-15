#from direct.stdpy.file import open as openFile
#from direct.stdpy import thread
#from panda3d.core import NodePath, Point3
from pandark.managers.physicsmanager import PhysicsManager
from pandark.managers.lightsmanager import LightsManager
from pandark.managers.camerasmanager import CamerasManager
from pandark.managers.animationsmanager import AnimationsManager

import __builtin__
__builtin__.physicsMgr = PhysicsManager()
__builtin__.lightsMgr = LightsManager()

__builtin__.animsMgr = AnimationsManager()

import yaml

from panda3d.core import AmbientLight, Fog

import game.classes

class Scenario(object):

	def __init__(self,environment,nodes,lights,cameras,entities,animations,staticGeoms,yamlList):

		__builtin__.camerasMgr = CamerasManager()

		self.sceneNode = render.attachNewNode('sceneNode')

		self.reset()

		self.environment = environment
		self.nodes       = nodes
		self.lights      = lights
		self.cameras     = cameras         
		self.entities    = entities       
		self.animations  = animations
		self.staticGeoms = staticGeoms
		self.yamlList    = yamlList

		self.initManagers()

	def initManagers(self):
		#from pandark.managers.physicsmanager import PhysicsManager
		self.physicsMgr = physicsMgr#PhysicsManager()

		#from pandark.managers.lightsmanager import LightsManager
		self.lightsMgr = lightsMgr#LightsManager()

		#from pandark.managers.camerasmanager import CamerasManager
		self.camerasMgr = camerasMgr#CamerasManager()

		#from pandark.managers.animationsmanager import AnimationsManager
		self.animsMgr = animsMgr#AnimationsManager()

	def begin(self):
		base.setBackgroundColor( self.environment['colourBackground'] )

		alight = AmbientLight('AmbientLight')
		alight.setColor(self.environment['colourAmbient'] )
		alnp = self.sceneNode.attachNewNode(alight)
		self.sceneNode.setLight(alnp)

		if self.environment['fog']:
			fog = Fog( 'sceneName' )
			fog.setColor( self.environment['fog']['color'] )

			if self.environment['fog']['mode'] == "linear":
				fog.setLinearRange(self.environment['fog']['linearStart']*1000,self.environment['fog']['linearEnd']*1000)
			else:
				fog.setExpDensity( self.environment['fog']['expDensity'] )

			self.sceneNode.setFog(fog)

		[self.createNode(props) for props in self.nodes]
		[self.createLight(props) for props in self.lights]
		[self.createCamera(props) for props in self.cameras]
		[self.createEntity(props) for props in self.entities]
		# [self.createStaticGeoms(props) for props in self.staticGeoms]


		self.sceneNode.setShaderAuto()


		#self.animsMgr.play('Camera01', 'idle', True) 

	def reset(self):		
		self.__nodesDict    = {}
		self.__lightsDict   = {}
		self.__camerasDict  = {}
		self.__entitiesDict = {}

		self.environment = None
		self.nodes       = None
		self.lights      = None
		self.cameras     = None         
		self.entities    = None       
		self.animations  = None
		self.staticGeoms = None
		self.yamlList    = None

		self.__nodesDict[''] = self

	def getEnt(self,name):		
		return self.__entitiesDict[name]

	def createNode(self,props):
		parent = self.find('**/'+props['groupName']) or self.sceneNode

		node = self.sceneNode.attachNewNode(parent)

		node.setPos(props['pos'])

		node.setQuat(props['quat'])

		node.setScale(props['scale'])

		self.animsMgr.createAnimation(node, self.animations[ props['name'] ] )

	def createLight(self,props):
		parent = self.sceneNode.find('**/'+props['groupName']) or self.sceneNode
		light = self.lightsMgr.createLight[props['type'] ](props)
		light.node().setScene(parent)
		light.reparentTo(parent)
		parent.setLight(light)

		self.animsMgr.createAnimation(light, self.animations[ props['name'] ] )

	def createCamera(self,props):
		cam = self.camerasMgr.createCamera(props)
		#self.camerasMgr.active( props['name'] )
		self.animsMgr.createAnimation(cam, self.animations[ props['name'] ] )

	def createEntity(self,props):
		#props['parent'] = self.__nodesDict[props['groupName']]

		name =  props['name']

		ent = yaml.load( self.yamlList[name] )

		model = loader.loadModel( ent.model_path )

		body = self.physicsMgr.createRigidBody(ent.physics['shapetype'],model,ent.physics)		

		ent.init(model,body,props)

		np = self.sceneNode.attachNewNode(body)

		np.setPosQuat(ent.pos,ent.quat)

		model.reparentTo(np)

		self.__entitiesDict[name] = ent

		self.animsMgr.createAnimation(ent.getNode(), self.animations[name])

	def createStaticGeoms(self,props):
		path = props['configFile']

		stream = file('assets/classes/' + path + '.class', 'r')

		ent = yaml.load( stream )

		ent.init(props)

	def destroy(self):

		self.sceneNode.setShaderOff()

		self.reset()

		self.camerasMgr.destroy()

		self.animsMgr.destroy()

		self.lightsMgr.destroy()

		self.physicsMgr.destroy()		

		self.sceneNode.clearLight()

		self.sceneNode.clearFog()

		self.sceneNode.removeNode()

		self.sceneNode.remove()

	def __del__(self):
		print 'de'