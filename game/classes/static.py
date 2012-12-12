from game.classes.generic import Generic
#from panda3d.core import VBase4
#from pandark.physics.composer import Composer
#from panda3d.core import Material

class Static(Generic):

	yaml_tag = u'!Static'

	def init(self,model,body,props):
		Generic.__init__(self,model,body,props)

		#myMaterial = Material()		
		#myMaterial.setAmbient(VBase4(0,0,1,1))
		#myMaterial.setDiffuse(VBase4(1,0,0,1))
		#myMaterial.setShininess(5.0)
		#myMaterial.setSpecular(VBase4(0,0,0,1))
		#myMaterial.setEmission(VBase4(0,1,0,1))
		#print myMaterial.getDiffuse(), myMaterial.getSpecular(), myMaterial.getEmission()
		#model.setMaterial(myMaterial) 