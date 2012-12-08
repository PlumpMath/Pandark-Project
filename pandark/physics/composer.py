import re

class Composer(object):

	def __init__(self):
		self.shapesList = ['trimesh','hull','box','sphere','cylinder','capsule','cone']

	def getSize(self,model):		
		hpr = model.getHpr()
		model.setHpr(0,0,0)
		minLimit, maxLimit = model.getTightBounds()
		model.setHpr(hpr) 
		return maxLimit - minLimit

	def setShape(self,model,body):

		name = model.getName()

		pos,hpr,scale = model.getPos(), model.getHpr(), model.getScale()	

		shapetype = re.findall("[-a-z]+",name.lower())[0].split('-')

		if set(shapetype).issubset( ['trimesh','hull'] ):
			#model.flattenLight()
			sizeOrGeom = model.node().getGeom(0)
			print sizeOrGeom
		else:				
			sizeOrGeom = self.getSize(model)

		shapetype =  filter(None,shapetype)

		#if shapetype[0] in list(self.shapes.keys()):
		if shapetype[0] in self.shapesList:
			physicsMgr.addShape[shapetype[0]](body,sizeOrGeom,pos,hpr,scale)

		not '-' in name or model.remove()


	def composeMulti(self,model,group='*'):
		children = model.find('**/*').getChildren()

		for child in children:

			name = child.getName()

			if len( child.getChildren() ) > 1:
				body = physicsMgr.getRigidBody()

				body.setMass(0)
				#body.setDeactivationEnabled(False)

				physicsMgr.world.attachRigidBody( body )

				np = render.attachNewNode(body)

				children2 = child.getChildren()

				for child2 in children2:
					self.setShape(child2,body)
				
				child.reparentTo(np)

				continue

			pos,hpr,scale = child.getPos(),child.getHpr(),child.getScale()

			child.setPosHprScale((0,0,0),(0,0,0),(1,1,1))

			body = physicsMgr.getRigidBody()

			body.setMass(1)			

			np = render.attachNewNode(body)

			np.setPosHprScale(pos,hpr,scale)

			child.reparentTo(np)

			self.setShape(child,body)

			physicsMgr.world.attachRigidBody( body )

	def addPrimitiveShape(self,body,model,shapetype):
		size = self.getSize(model)
		physicsMgr.addShape[shapetype](body,size)

	def addComplexShape(self,body,model,shapetype):
		geom = model.node().getGeom(0)
		physicsMgr.addShape[shapetype](body,geom)


"""Testing ---------------------------------------------"""

if __name__ == '__main__':

	from direct.directbase import DirectStart

	from physicsmanager import PhysicsManager

	physicsMgr = PhysicsManager()

	physicsMgr.debug().show()

	model2 = loader.loadModel('../../assets/models/chairs/mix_compound')

	model2.clearModelNodes()

	render.setRenderModeWireframe()

	#base.wireframeOff()

	# body2 = physicsMgr.getRigidBody()

	# body2.setMass(0)

	# physicsMgr.world.attachRigidBody( body2 )

	# np2 = render.attachNewNode(body2)

	# model2.reparentTo(np2)

	composer = Composer()


	model = loader.loadModel('../../assets/models/chairs/multi_compound')

	composer.composeMulti(model)


	# model1 = loader.loadModel('../../assets/models/chairs/mix_compound')
	# body1 = physicsMgr.getRigidBody()
	# #print body1.getFriction()
	# body1.setMass(0)
	# body1.setDeactivationEnabled(False)
	# physicsMgr.world.attachRigidBody( body1 )
	# np1 = render.attachNewNode(body1)
	# model1.reparentTo(np1)
	# composer.composeMix(model1,body1)


	def task(task):
		physicsMgr.world.doPhysics(globalClock.getDt())
		return task.cont

	taskMgr.add(task,'task')

	run()