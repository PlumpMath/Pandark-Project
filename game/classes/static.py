from game.classes.generic import Generic

#from pandark.physics.composer import Composer

class Static(Generic):

	yaml_tag = u'!Static'

	def init(self,model,props):
		Generic.__init__(self,model,props)
		self.__setPhysics()

	def __setPhysics(self):


		#self.model.flattenLight()

		#body = physicsMgr.createRigidBody('trimesh',self.model,self.physics)

		body = physicsMgr.createRigidBody(self.physics['shapetype'],self.model,self.physics)
		
		np = render.attachNewNode(body)


		#self.pos = (self.pos[0], self.pos[1], self.pos[2]/2)

		np.setPosQuat(self.pos,self.quat)

		#physicsMgr.world.attachRigidBody(body)

		self.model.reparentTo(np)

		print self.model, self.physics['shapetype']

		self._cleanUp()

	def getSize(self,model):
		hpr = model.getHpr()
		model.setHpr(0,0,0)
		minLimit, maxLimit = model.getTightBounds()
		model.setHpr(hpr) 
		return maxLimit - minLimit