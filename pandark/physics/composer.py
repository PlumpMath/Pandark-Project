import re

class Composer(object):

	def __init__(self):
		Composer.shapesList = physicsMgr.addShape.keys()

	def getSize(self,model):		
		hpr = model.getHpr()
		model.setHpr(0,0,0)
		minLimit, maxLimit = model.getTightBounds()
		model.setHpr(hpr) 
		return maxLimit - minLimit

	def setShape(self,model,body):
		#To Re-Do

		name = model.getName()

		pos,hpr,scale = model.getPos(), model.getHpr(), model.getScale()	

		shapetype = re.findall("[-a-z]+",name.lower())[0].split('-')

		if set(shapetype).issubset( ['trimesh','hull'] ):
			#model.flattenLight()
			sizeOrGeom = model.node().getGeom(0)
		else:				
			sizeOrGeom = self.getSize(model)

		shapetype = filter(None,shapetype)

		#if shapetype[0] in list(self.shapes.keys()):
		if shapetype[0] in self.shapesList:
			physicsMgr.addShape[shapetype[0]](body,sizeOrGeom,pos,hpr,scale)

		not '-' in name or model.remove()


	def createCompound(self,model,body):
		np = render.attachNewNode(body)

		children = model.find('**/*').getChildren() or model.getChildren()

		[self.setShape(child,body) for child in children]			

		return np

	def composeMulti(self,model,group='*'):
		children = model.find('**/*').getChildren()

		for child in children:

			name = child.getName()

			if len( child.getChildren() ) > 1:

				body = physicsMgr.getRigidBody()

				'''------------------
				TODO:
				- load props file
				------------------'''

				body.setMass(0)

				physicsMgr.world.attachRigidBody( body )

				np = self.createCompound(child,body)

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


""" ============================ TEST ============================ """

if __name__ == '__main__':

	from direct.directbase import DirectStart

	from physicsmanager import PhysicsManager

	physicsMgr = PhysicsManager()

	physicsMgr.debug().show()

	render.setRenderModeWireframe()

	model = loader.loadModel('../../assets/models/chairs/chair')

	composer = Composer()

	multi = 0

	if multi:		
		composer.composeMulti(model)
	else:	
		body = physicsMgr.getRigidBody()	
		body.setMass(0)
		#body.setDeactivationEnabled(False)
		np = composer.createCompound(model,body)
		physicsMgr.world.attachRigidBody(body)
		model.reparentTo(np)


	def task(task):
		physicsMgr.world.doPhysics(globalClock.getDt())
		return task.cont

	taskMgr.add(task,'task')

	run()