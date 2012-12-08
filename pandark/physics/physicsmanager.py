""" Panda3d - Bullet Physics Manager
by Fred Ukita """

from panda3d.core import TransformState, Vec3

from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletPlaneShape
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletBoxShape, BulletCapsuleShape, BulletConeShape, BulletCylinderShape, BulletSphereShape
from panda3d.bullet import BulletConvexHullShape
from panda3d.bullet import BulletTriangleMesh
from panda3d.bullet import BulletTriangleMeshShape
from panda3d.bullet import BulletCharacterControllerNode
from panda3d.bullet import BulletGhostNode
from panda3d.bullet import ZUp

class PhysicsManager(object):    

    def __init__(self, gravity=(0,0,-9.81) ):
        self.world = BulletWorld()
        self.world.setGravity(Vec3(gravity) )

        self.addShape = {}
        self.addShape['plane']    = self.__addPlane
        self.addShape['sphere']   = self.__addSphere  
        self.addShape['box']      = self.__addBox
        self.addShape['cylinder'] = self.__addCylinder
        self.addShape['capsule']  = self.__addCapsule
        self.addShape['cone']     = self.__addCone
        self.addShape['hull']     = self.__addConvexHull
        self.addShape['trimesh']  = self.__addTriangleMesh

    def getRigidBodyDefaultProps(self):
        props = {}
        props['mass']         = .0
        props['friction']     = .5
        props['restitution']  = .0
        props['adamping']     = .0
        props['ldamping']     = .0
        props['asleep']       = .08
        props['lsleep']       = 1.
        props['deactivation'] = True
        props['kinematic']    = False
        return props

    def getRigidBody(self, name=None):
        return BulletRigidBodyNode(name or 'rigidbody')

    def createRigidBody(self, shapetype, sizeOrGeom, props={}, pos=(0,0,0), hpr=(0,0,0), scale=(1,1,1), name=None):
        body = self.getRigidBody(name)
        self.addShape[shapetype](body,sizeOrGeom,pos,hpr,scale)
        props = dict(self.getRigidBodyDefaultProps().items() + props.items() )
        self.setBodyProps(body, props)
        self.world.attachRigidBody( body )
        return body

    def getGhost(self, name=None):
        return BulletRigidBodyNode(name or 'ghost')

    def createGhost(self, shapetype, size, name=None):        
        ghost = self.getGhost(name)
        self.addShape[shapetype](ghost, size) 
        self.world.attachGhost(ghost)
        return ghost  

    def attachRigidBody(self, body, props):
        self.setBodyProps(body, props)
        self.world.attachRigidBody(body)  

    def __addSphere(self, body, size, pos=(0,0,0), hpr=(0,0,0), scale=(1,1,1) ):
        shape = BulletSphereShape( max(size)/2 )
        body.addShape(shape, TransformState.makePosHprScale(pos,hpr,scale) )

    def __addBox(self, body, size, pos=(0,0,0), hpr=(0,0,0), scale=(1,1,1) ):
        shape = BulletBoxShape( size/2 )
        body.addShape(shape, TransformState.makePosHprScale(pos,hpr,scale) )

    def __addCylinder(self, body, size, pos=(0,0,0), hpr=(0,0,0), scale=(1,1,1) ):
        shape = BulletCylinderShape(max(size.x,size.y)/2, size.z, ZUp)
        body.addShape( shape, TransformState.makePosHprScale(pos,hpr,scale) )

    def __addCapsule(self, body, size, pos=(0,0,0), hpr=(0,0,0), scale=(1,1,1) ):
        diam = max(size.x,size.y)
        shape = BulletCapsuleShape(diam/2, size.z-diam, ZUp)       
        body.addShape( shape, TransformState.makePosHprScale(pos,hpr,scale) )

    def __addCone(self, body, size, pos=(0,0,0), hpr=(0,0,0), scale=(1,1,1) ):
        shape = BulletConeShape(max(size.x,size.y)/2, size.z, ZUp)
        body.addShape( shape, TransformState.makePosHprScale(pos,hpr,scale) )

    def __addConvexHull(self, body, geom, pos=(0,0,0), hpr=(0,0,0), scale=(1,1,1) ):
        shape = BulletConvexHullShape()
        shape.addGeom(geom)
        body.addShape( shape, TransformState.makePosHprScale(pos,hpr,scale) )

    def __addTriangleMesh(self, body, geom, pos=(0,0,0), hpr=(0,0,0), scale=(1,1,1), dynamic=True):
        mesh = BulletTriangleMesh()
        mesh.addGeom(geom)
        shape = BulletTriangleMeshShape(mesh, dynamic=dynamic )
        body.addShape( shape, TransformState.makePosHprScale(pos,hpr,scale) )

    def __addPlane(self, body, size=(0,0,1), pos=(0,0,0), hpr=(0,0,0), scale=(1,1,1) ):
        shape = BulletPlaneShape(Vec3(size), 0)
        body.addShape( shape, TransformState.makePosHprScale(pos,hpr,scale)  )

    def setBodyProps(self, body, props):        
        body.setMass( props['mass'] )
        body.setFriction( props['friction'] )
        body.setRestitution( props['restitution'] )
        body.setAngularDamping( props['adamping'] )
        body.setLinearDamping( props['ldamping'] )
        body.setAngularSleepThreshold( props['asleep'] )
        body.setLinearSleepThreshold( props['lsleep'] )
        if not props['deactivation']:
            body.setDeactivationEnabled( False )
        body.setKinematic( props['kinematic'] )

    def characterController(self, name, height, mass, radius, step_height):
        shape = BulletCapsuleShape(radius, height - 2*radius, ZUp)
        body = BulletRigidBodyNode(name)
        body.setMass(mass)
        body.addShape(shape)
        return BulletCharacterControllerNode(shape, step_height, name)
    
    def debug(self):
        from panda3d.bullet import BulletDebugNode
        debugNP = render.attachNewNode(BulletDebugNode('Debug') )
        debugNP.show()
        debugNP.node().showWireframe(True)
        debugNP.node().showConstraints(True)
        debugNP.node().showBoundingBoxes(False)
        debugNP.node().showNormals(False)        
        self.world.setDebugNode(debugNP.node())
        return debugNP


""" ============================ TEST ============================ """

if __name__ == '__main__':

    from direct.directbase import DirectStart

    base.cam.setPos(0,-100,0)

    base.cam.lookAt(0,0,-10)

    from physicsmanager import PhysicsManager

    physicsMgr = PhysicsManager()

    physicsMgr.debug().show()

    '''Plane'''
    plane = physicsMgr.createRigidBody('plane', Vec3(0,0,1), pos=(0,0,-20) )

    props = {'mass':10}

    '''Primitive Shapes'''
    box = physicsMgr.createRigidBody('box', Vec3(3,3,3), props)

    np = render.attachNewNode(box)

    np.setPos(Vec3(20,0,0))

    sphere = physicsMgr.createRigidBody('sphere', Vec3(3,0,0), props)

    np = render.attachNewNode(sphere)

    np.setPos(Vec3(10,0,0))

    cylinder = physicsMgr.createRigidBody('cylinder', Vec3(3,0,10), props)

    np = render.attachNewNode(cylinder)

    np.setPos(Vec3(0,0,0))

    props = {'mass':10,'deactivation':False}

    cone = physicsMgr.createRigidBody('cone', Vec3(3,0,10), props)

    np = render.attachNewNode(cone)

    np.setPos(Vec3(-10,0,0))

    capsule = physicsMgr.createRigidBody('capsule', Vec3(3,0,10), props)

    np = render.attachNewNode(capsule)

    np.setPos(Vec3(-20,0,0))


    '''Complex Shapes''' 
    # model = loader.loadModel('your_model.egg')

    # geom = model.findAllMatches('**/+GeomNode').getPath(0).node().getGeom(0)

    # hull = physicsMgr.createRigidBody('hull', geom, props )

    # np = render.attachNewNode(hull)

    # np.setPos(Vec3(30,0,0))

    # trimesh = physicsMgr.createRigidBody('trimesh', geom, props )

    # np = render.attachNewNode(trimesh)

    # np.setPos(Vec3(-30,0,0))


    def task(task):
        physicsMgr.world.doPhysics(globalClock.getDt())
        return task.cont

    taskMgr.add(task,'task')

    run()