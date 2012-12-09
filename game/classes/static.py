from game.classes.generic import Generic

#from pandark.physics.composer import Composer

class Static(Generic):

	yaml_tag = u'!Static'

	def init(self,model,props):
		Generic.__init__(self,model,props)

	def getSize(self,model):
		hpr = model.getHpr()
		model.setHpr(0,0,0)
		minLimit, maxLimit = model.getTightBounds()
		model.setHpr(hpr) 
		return maxLimit - minLimit