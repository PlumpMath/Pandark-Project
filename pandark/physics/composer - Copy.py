import re

class Composer(object):

	shapes = {}

	def __init__(self):
		self.shapes['trimesh']  = self.__complex
		self.shapes['hull']     = self.__complex
		self.shapes['box']      = self.__primitive
		self.shapes['sphere']   = self.__primitive
		self.shapes['cylinder'] = self.__primitive
		self.shapes['capsule']  = self.__primitive
		self.shapes['cone']     = self.__primitive

	def getSize(self,model):		
		hpr = model.getHpr()
		model.setHpr(0,0,0)
		minLimit, maxLimit = model.getTightBounds()
		model.setHpr(hpr) 
		return maxLimit - minLimit

	def __complex(self,child,shapetype,body):
		child.flattenLight()
		pos,hpr,scale = child.getPos(), child.getHpr(), child.getScale()
		geom = child.node().getGeom(0)
		physicsMgr.addShape[shapetype](body,geom,pos,hpr,scale)

	def __primitive(self,child,shapetype,body):
		pos,hpr,scale = child.getPos(), child.getHpr(), child.getScale()
		size = self.getSize(child)
		physicsMgr.addShape[shapetype](body,size,pos,hpr,scale)

	def composeMix(self,model,body):

		children = model.find('**/collisions')

		if not children:
			children = model.find('**/*')

		children = children.getChildren()

		for child in children:

			name = child.getName()	

			print name,'llll'		

			shapetype = re.findall("[-a-z]+",name.lower())[0].split('-')

			if len(shapetype)>1:
				if shapetype[1] in self.shapes:
					self.shapes[shapetype[1]](child,shapetype[1],body)
					child.remove()
					continue
				child.reparentTo(model.getParent().getParent())
				#print "'%s' is not a name of a shapetype!!!" % (shapetype[1])
			else:
				if shapetype[0] in self.shapes:
					self.shapes[shapetype[0]](child,shapetype[0],body)
					continue

			#child.reparentTo(model.getParent().node())
				#child.reparentTo(model.getParent().getParent())
				#print "'%s' is not a name of a shapetype" % (shapetype[0])

	def composeMulti2(self,model,group='*'):

		children = model.find('**/*').getChildren()

		for child in children:

			name = child.getName()

			shapetype = re.findall("[-a-z]+",name.lower())[0].split('-')

			if shapetype in ('trimesh','hull') :
				child.flattenLight()
				sizeOrGeom = child.node().getGeom(0)
			else:				
				sizeOrGeom = self.getSize(child)

			body = physicsMgr.createRigidBody(shapetype[0],sizeOrGeom)

			np = render.attachNewNode(body)

			np.setPosHprScale(child.getPos(),child.getHpr(),child.getScale())

			child.setPosHprScale((0,0,0),(0,0,0),(1,1,1))

			child.reparentTo(np)



	def composeMix2(self,model,body):
		children = model.getChildren()

		for child in children:
			name = child.getName()
			self.setShape(child,body)
			#not '-' in name or child.remove()

	def setShape(self,model,body):

		name = model.getName()

		pos,hpr,scale = model.getPos(), model.getHpr(), model.getScale()	

		shapetype = re.findall("[-a-z]+",name.lower())[0].split('-')

		if set(shapetype).issubset( ['trimesh','hull'] ):
			#model.flattenLight()
			sizeOrGeom = model.node().getGeom(0)
		else:				
			sizeOrGeom = self.getSize(model)

		shapetype =  filter(None,shapetype)

		if shapetype[0] in list(self.shapes.keys()):
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
							
				self.composeMix2(child,body)
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