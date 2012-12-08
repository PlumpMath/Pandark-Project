import re
from direct.directbase import DirectStart
from pandark.managers.physicsmanager import PhysicsManager

physicsMgr = PhysicsManager()

physicsMgr.debug().show()

model = loader.loadModel('assets/models/chairs/collisions')

model.clearModelNodes()

render.setRenderModeWireframe()

#base.wireframeOff()

def getSize(model):
	hpr = model.getHpr()

	model.setHpr(0,0,0)

	model.flattenLight()

	minLimit, maxLimit = model.getTightBounds()

	model.setHpr(hpr) 

	return maxLimit - minLimit

body = physicsMgr.createBody('teste')
np = render.attachNewNode(body)

for child in  model.find('**/collisions').getChildren():
	name,pos,hpr,scale = child.getName(), child.getPos(), child.getHpr(), child.getScale()
	#size = getSize(child)	

	shape = re.findall("[a-z]+",name.lower())[0]

	if shape == 'trimesh':
		geom = child.node().getGeom(0)
		physicsMgr.addShape[shape](body,geom,pos,hpr,scale)
	elif shape == 'hull':
		geom = child.node().getGeom(0)
		physicsMgr.addShape[shape](body,geom,pos,hpr,scale)
	else:
		size = getSize(child)
		physicsMgr.addShape[shape](body,size,pos,hpr,scale)
		print name, size

	child.remove()


model.reparentTo(np)

def task(task):
	physicsMgr.world.doPhysics(globalClock.getDt())
	return task.cont

taskMgr.add(task,'task')

run()