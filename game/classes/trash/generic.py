import yaml
from panda3d.bullet import BulletRigidBodyNode

class Generic(yaml.YAMLObject):	

	def init(self,model,props):
		self.name   = props['name']
		self.pos    = props['pos']
		self.quat   = props['quat']
		self.scale  = props['scale']
		self.parent = render.find('**/'+props['groupName']) or render

		#self.parent = render

		self.__model = model	
		self.__configPhysics()
		self._init()
		self.__cleanUp()

	def getNode(self):
		return self.__np

	def _doPhysics(self,body,size):pass

	def __configPhysics(self):
		body = BulletRigidBodyNode( self.name )        
		body.setMass( self.mass )
		body.setFriction( self.friction )
		body.setRestitution( self.restitution )
		body.setAngularDamping( self.adamping )
		body.setLinearDamping( self.ldamping )
		body.setAngularSleepThreshold( self.asleep )
		body.setLinearSleepThreshold( self.lsleep )
		if not self.deactivation:
			body.setDeactivationEnabled(False)
		body.setKinematic( self.kinematic )

		self.__model.setScale(self.scale)

		self.__model.flattenLight()

		minLimit, maxLimit = self.__model.getTightBounds()
		size = maxLimit - minLimit

		#physicsMgr.createCapsule(body,size[0]/2,size[2])
		self._doPhysics(body,size)

		self.__np = self.parent.attachNewNode(body)
		self.__np.setPos(self.pos)
		self.__np.setQuat(self.quat)
		#self.__np.setScale(self.scale)

		self.__model.reparentTo(self.__np)
		#elf.__model.setScale(self.scale)		

	def __cleanUp(self):
		self.init = None		
		self.model = None
		del \
		self.init,\
		self.model,\
		self.parent,\
		self.pos,\
		self.quat,\
		self.scale,\
		self.mass,\
		self.friction,\
		self.restitution,\
		self.adamping,\
		self.ldamping,\
		self.asleep,\
		self.lsleep,\
		self.deactivation,\
		self.kinematic

	def __del__(self):
		self.__model.remove()