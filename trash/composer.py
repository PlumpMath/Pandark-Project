import re

from direct.directbase import DirectStart

from pandark.managers.physicsmanager import PhysicsManager

physicsMgr = PhysicsManager()

physicsMgr.debug().show()

model = loader.loadModel('assets/models/chairs/hidden_compound')

model.clearModelNodes()

render.setRenderModeWireframe()

base.wireframeOff()

body = physicsMgr.getRigidBody()
body.setMass(0)

physicsMgr.world.attachRigidBody( body )
np = render.attachNewNode(body)

"""----------------------------------------------"""

def getSize(model):

	hpr = model.getHpr()

	model.setHpr(0,0,0)

	minLimit, maxLimit = model.getTightBounds()

	model.setHpr(hpr) 

	return maxLimit - minLimit


def complexu(child,shapetype):
	child.flattenLight()
	pos,hpr,scale = child.getPos(), child.getHpr(), child.getScale()
	geom = child.node().getGeom(0)
	physicsMgr.addShape[shapetype](body,geom,pos,hpr,scale)


def primitive(child,shapetype):
	pos,hpr,scale = child.getPos(), child.getHpr(), child.getScale()
	size = getSize(child)
	physicsMgr.addShape[shapetype](body,size,pos,hpr,scale)

shapes = {}
shapes['trimesh'] = complexu
shapes['hull']    = complexu
shapes['box']     = primitive

def shapeGenarator(shapetype):
	shapes[shapetype](child,shapetype)

children = model.find('**/collisions').getChildren()

for child in children:

	name = child.getName()

	shape = re.findall("[a-z]+",name.lower())[0].split('-')

	shapeGenarator(shape[0])

	if len(shape)>1: child.remove()

model.reparentTo(np)

"""----------------------------------------------"""

def task(task):
	physicsMgr.world.doPhysics(globalClock.getDt())
	return task.cont

taskMgr.add(task,'task')

run()