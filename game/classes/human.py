from game.classes.generic import Generic

class Human(Generic):

    yaml_tag = u'!Human'

    def init(self,model,props):
    	Generic.__init__(self,model,props)
    	self.__setPhysics()

    def __setPhysics(self):

		size = self._getSize()

		# body = physicsMgr.createRigidBody(self.name,size,self.physics)

		# self._np = self.parent.attachNewNode(body)

		# self._np.setPosQuat(self.pos,self.quat)

		# self.model.reparentTo(self._np)

		self._cleanUp()
