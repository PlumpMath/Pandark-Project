import re

class Composer(object):

	shapes = {}

	def __init__(self):
		self.shapes['trimesh']  = self.complex
		self.shapes['hull']     = self.complex
		self.shapes['box']      = self.primitive
		self.shapes['sphere']   = self.primitive
		self.shapes['cylinder'] = self.primitive
		self.shapes['capsule']  = self.primitive
		self.shapes['cone']     = self.primitive

	def getSize(self,model):		
		hpr = model.getHpr()
		model.setHpr(0,0,0)
		minLimit, maxLimit = model.getTightBounds()
		model.setHpr(hpr) 
		return maxLimit - minLimit

	def complex(self,child,shapetype):
		child.flattenLight()
		pos,hpr,scale = child.getPos(), child.getHpr(), child.getScale()
		geom = child.node().getGeom(0)
		physicsMgr.addShape[shapetype](body,geom,pos,hpr,scale)

	def primitive(self,child,shapetype):
		pos,hpr,scale = child.getPos(), child.getHpr(), child.getScale()
		size = self.getSize(child)
		physicsMgr.addShape[shapetype](body,size,pos,hpr,scale)

	def compose(self,model):

		children = model.find('**/collisions')

		if not children:
			children = model.find('**/*')

		children = children.getChildren()

		for child in children:

			name = child.getName()

			#print name

			#print re.findall("[-a-z]+",name.lower())[0].split('-')

			shapetype = re.findall("[-a-z]+",name.lower())[0].split('-')

			if len(shapetype)>1:
				if shapetype[1] in self.shapes:
					self.shapes[shapetype[1]](child,shapetype[1])
					child.remove()
					continue
				child.reparentTo(model.getParent().getParent())
				#print "'%s' is not a name of a shapetype!!!" % (shapetype[1])
			else:
				if shapetype[0] in self.shapes:
					self.shapes[shapetype[0]](child,shapetype[0])
					continue
				#child.reparentTo(model.getParent().getParent())
				#print "'%s' is not a name of a shapetype" % (shapetype[0])

		return True

"""----------------------------------------------"""

if __name__ == '__main__':

	from direct.directbase import DirectStart

	from physicsmanager import PhysicsManager

	physicsMgr = PhysicsManager()

	physicsMgr.debug().show()

	model = loader.loadModel('../../assets/models/chairs/mix_compound')

	model.clearModelNodes()

	render.setRenderModeWireframe()

	#base.wireframeOff()

	body = physicsMgr.getRigidBody()

	body.setMass(10)

	physicsMgr.world.attachRigidBody( body )

	np = render.attachNewNode(body)

	model.reparentTo(np)

	composer = Composer()

	composer.compose(model)

	def task(task):
		physicsMgr.world.doPhysics(globalClock.getDt())
		return task.cont

	taskMgr.add(task,'task')

	run()