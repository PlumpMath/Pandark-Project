from game.classes.generic import Generic

#from pandark.physics.composer import Composer

class Static(Generic):

    yaml_tag = u'!Static'

    def init(self,model,props):
    	Generic.__init__(self,model,props)
    	self.__setPhysics()

    def __setPhysics(self):

		body = physicsMgr.createRigidBody('hull',self.model,self.physics)

		#body = physicsMgr.createRigidBody(self.physics['shapetype'],self.model,self.physics)
		
		np = render.attachNewNode(body)

		np.setPosQuat(self.pos,self.quat)

		#physicsMgr.world.attachRigidBody(body)

		self.model.reparentTo(np)

		print self.model, self.physics['shapetype']

		self._cleanUp()
