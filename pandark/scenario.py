from pandark.managers.physicsmanager import PhysicsManager
from pandark.managers.lightsmanager import LightsManager
from pandark.managers.camerasmanager import CamerasManager
from pandark.managers.animationsmanager import AnimationsManager

import yaml

from panda3d.core import AmbientLight, Fog

import game.classes

class Scenario(object):

	def __init__(self,environment,nodes,lights,cameras,entities,animations,staticGeoms,yamlList):

		self.sceneNode = render.attachNewNode('sceneNode')

		self.environment = environment
		self.nodes       = nodes
		self.lights      = lights
		self.cameras     = cameras         
		self.entities    = entities       
		self.animations  = animations
		self.staticGeoms = staticGeoms
		self.yamlList    = yamlList

		self.physicsMgr = PhysicsManager()
		self.lightsMgr  = LightsManager()
		self.camerasMgr = CamerasManager()
		self.animsMgr   = AnimationsManager()

		self.reset()

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

		self.sceneNode.clearModelNodes()
		self.sceneNode.flattenStrong() 
		self.sceneNode.setShaderAuto()

	def reset(self):		
		self.__entitiesDict = {}

	def getEnt(self,name):		
		pass

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
		self.animsMgr.createAnimation(cam, self.animations[ props['name'] ] )

	def createEntity(self,props):
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

	def __del__(self):
		base.setBackgroundColor(0,0,0,1)
		

		self.lightsMgr.destroy()
		self.camerasMgr.destroy()
		self.physicsMgr.destroy()
		self.animsMgr.destroy()

		self.sceneNode.setShaderOff()

		for i in self.sceneNode.getChildren():
			#self.sceneNode.clearLight(i)
			print i, '*removed*'
			i.remove()

		self.sceneNode.remove()

		print 'delete Scene'