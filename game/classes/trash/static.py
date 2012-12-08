from game.classes.generic import Generic

class Static(Generic):

	yaml_tag = u'!Static'

	def _init(self):pass

	def _doPhysics(self,body,size):
		physicsMgr.createBox(body,size)

