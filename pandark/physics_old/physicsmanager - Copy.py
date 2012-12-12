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

# import string, random
# def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
#     gid = ''.join(random.choice(chars) for x in xrange(size))
#     print 'id:',gid
#     return gid

class PhysicsManager(object):    

    def __init__(self,gravity=(0,0,-9.81)):
        self.world = BulletWorld()
        self.world.setGravity(Vec3(gravity))

        self.addShape = {}
        self.addShape['sphere']   = self.__addSphere  
        self.addShape['box']      = self.__addBox
        self.addShape['cylinder'] = self.__addCylinder
        self.addShape['capsule']  = self.__addCapsule
        self.addShape['cone']     = self.__addCone
        self.addShape['hull']     = self.__addConvexHull
        self.addShape['trimesh']  = self.__addTriangleMesh

    def getRigidBodyDefaultProps(self):
        props = {}
        props['mass'] = 1.
        props['friction'] = .5
        props['restitution'] = .0
        props['adamping'] = .0
        props['ldamping'] = .0
        props['asleep'] = .08
        props['lsleep'] = 1.
        props['deactivation'] = True
        props['kinematic'] = False
        return props

    def getRigidBody(self,name=None):
        return BulletRigidBodyNode(name or 'rigidbody')

    def createRigidBody(self,shapetype,sizeOrGeom,props={},pos=(0,0,0),hpr=(0,0,0),scale=(1,1,1),name=None):
        body = self.getRigidBody(name)
        self.addShape[shapetype](body,sizeOrGeom,pos,hpr,scale)
        props = dict(self.getRigidBodyDefaultProps().items() + props.items())
        self.setBodyProps(body, props)
        self.world.attachRigidBody( body )
        return body

    def createGhost(self,name,shape,size):        
        ghost = BulletGhostNode( name )
        self.addShape[shape]( ghost, size ) 
        self.world.attachGhost( ghost )
        return ghost  

    def attachRigidBody(self,body,props):
        self.setBodyProps(body,props)
        self.world.attachRigidBody( body )  

    def __addSphere(self, body, size, pos=(0,0,0), hpr=(0,0,0), scale=(1,1,1) ):
        shape = BulletSphereShape( max(size)/2 )
        body.addShape( shape, TransformState.makePosHprScale(pos,hpr,scale) )

    def __addBox(self, body, size, pos=(0,0,0), hpr=(0,0,0), scale=(1,1,1) ):
        shape = BulletBoxShape( size/2 )
        body.addShape( shape, TransformState.makePosHprScale(pos,hpr,scale) )

    def __addCylinder(self, body, size, pos=(0,0,0), hpr=(0,0,0), scale=(1,1,1) ):
        shape = BulletCylinderShape(max(size.x,size.y)/2, size.z, ZUp)
        body.addShape( shape, TransformState.makePosHprScale(pos,hpr,scale) )

    def __addCapsule(self, body, size, pos=(0,0,0), hpr=(0,0,0), scale=(1,1,1) ):
        diam = max(size.x,size.y)
        shape = BulletCapsuleShape(diam/2, size.z-diam, ZUp)       
        body.addShape( shape, TransformState.makePosHprScale(pos,hpr,scale) )

    # def __addAdaptiveShape(self, body, size, pos=(0,0,0), hpr=(0,0,0), scale=(1,1,1), type='capsule'):
    #     height = max(size.x,size.y,size.z)
    #     diam = min(size.x,size.y,size.z)
    #     if type == 'capsule':
    #         shape = BulletCapsuleShape(diam/2, height-diam, ZUp)
    #     elif type == 'cylinder':
    #         shape = BulletCylinderShape(diam/2, height, ZUp)
    #     vec = (0,0,0)
    #     if size.x > size.z:vec=(0,0,90)
    #     if size.y > size.x:vec=(0,90,0)
    #     hpr+=vec
    #     body.addShape( shape, TransformState.makePosHprScale(pos,hpr,scale) )

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

    def __addPlane(self, body, size, pos=(0,0,0), hpr=(0,0,0), scale=(1,1,1) ):
        shape = BulletPlaneShape(size, 1)
        body.addShape( shape, TransformState.makePosHprScale(pos,hpr,scale) )

    def setBodyProps(self,body,props):        
        body.setMass(props['mass'])
        body.setFriction(props['friction'])
        body.setRestitution(props['restitution'])
        body.setAngularDamping(props['adamping'])
        body.setLinearDamping(props['ldamping'])
        body.setAngularSleepThreshold(props['asleep'])
        body.setLinearSleepThreshold(props['lsleep'])
        if not props['deactivation']:
            body.setDeactivationEnabled(False)
        body.setKinematic(props['kinematic'])

    def characterController(self,name, height, mass, radius, step_height):
        shape = BulletCapsuleShape(radius, height - 2*radius, ZUp)
        body = BulletRigidBodyNode(name)
        body.setMass(mass)
        body.addShape(shape)
        return BulletCharacterControllerNode(shape, step_height, name)
    
    def debug(self):
        from panda3d.bullet import BulletDebugNode
        debugNP = render.attachNewNode(BulletDebugNode('Debug'))
        debugNP.show()
        debugNP.node().showWireframe(True)
        debugNP.node().showConstraints(True)
        debugNP.node().showBoundingBoxes(False)
        debugNP.node().showNormals(False)        
        self.world.setDebugNode(debugNP.node())
        return debugNP

    def __log(self,props,body):
        #print 'Name:'+props['name'], 'Class:'+props['class']        
        print 'mass',body.getMass()
        print 'friction',body.getFriction()
        print 'restitution',body.getRestitution()
        print 'lsleep',body.getLinearSleepThreshold()
        print 'asleep',body.getAngularSleepThreshold()
        print 'ldamping',body.getLinearDamping()
        print 'adamping',body.getAngularDamping()
        #print 'kinematic',body.getKinematic()
        print '-------------------------------------------------------'