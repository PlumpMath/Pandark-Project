from panda3d.core import NodePath
#from direct.stdpy.file import open as openFile
#from direct.stdpy import thread
import yaml

from game.classes.human import Human
from game.classes.door import Door
from game.classes.actionarea import ActionArea

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

	def getLight(self,name):
		return self.__lightsList[name]

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