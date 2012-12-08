from panda3d.core import Vec3
#from pandac.PandaModules import TransformState

from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletPlaneShape
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletBoxShape, BulletCapsuleShape, BulletConeShape, BulletCylinderShape, BulletSphereShape
from panda3d.bullet import BulletConvexHullShape
from panda3d.bullet import BulletTriangleMesh
from panda3d.bullet import BulletTriangleMeshShape
from panda3d.bullet import BulletCharacterControllerNode
#from panda3d.bullet import BulletVehicle
from panda3d.bullet import BulletGhostNode
from panda3d.bullet import ZUp

from panda3d.core import TransformState

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

    def createGhost(self,name,shape,size):        
        ghost = BulletGhostNode( name )
        self.addShape[shape]( ghost, size ) 
        self.world.attachGhost( ghost )
        return ghost

    def __createRigidBody(self,name,size,props):        
        body = self.__getRigidBody( name, props )
        self.addShape[ props['shape'] ]( body, size ) 
        self.world.attachRigidBody( body )
        return body

    def createRigidBody(self):
        return BulletRigidBodyNode()

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

    def __addAdaptiveShape(self, body, size, pos=(0,0,0), hpr=(0,0,0), scale=(1,1,1), type='capsule'):
        height = max(size.x,size.y,size.z)
        diam = min(size.x,size.y,size.z)
        if type == 'capsule':
            shape = BulletCapsuleShape(diam/2, height-diam, ZUp)
        elif type == 'cylinder':
            shape = BulletCylinderShape(diam/2, height, ZUp)
        vec = (0,0,0)
        if size.x > size.z:vec=(0,0,90)
        if size.y > size.x:vec=(0,90,0)
        hpr+=vec
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
   
    def createPlane(self, name, size):
        shape = BulletPlaneShape(size, 1) 
        node = BulletRigidBodyNode(name)
        node.addShape(shape)        
        self.world.attachRigidBody(node)
        return node

    def createConvexHull(self,geom,props):
        shape = BulletConvexHullShape()
        shape.addGeom(geom)
        body = self.__getRigidBody(props)
        body.addShape(shape)
        #body.setDeactivationEnabled(False)
        self.world.attachRigidBody(body)
        return body

    def createConvexHull2(self,props,model):

        np = self.__getRigidBody(props)

        for geomNP in model.findAllMatches('**/+GeomNode'): 
            geomNode = geomNP.node() 
            ts = geomNP.getTransform(model) 
            for geom in geomNode.getGeoms(): 
                shape = BulletConvexHullShape() 
                shape.addGeom(geom)
                np.addShape(shape, ts)

        np.setMass(1.0) 
        #np.setCollideMask(BitMask32.allOn()) 
        self.world.attachRigidBody(np)

        return np

    def createTriangleMesh(self,geom,props):
        mesh = BulletTriangleMesh()
        mesh.addGeom(geom)
        shape = BulletTriangleMeshShape(mesh, dynamic=props['dynamic'])
        body = self.__getRigidBody(props)
        body.addShape(shape)
        #body.setDeactivationEnabled(False)
        self.world.attachRigidBody(body)
        return body

    def __getRigidBody(self,props):
        body = BulletRigidBodyNode()        
        self.setBodyProps(body,props)
        return body

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
        print 'Name:'+props['name'], 'Class:'+props['class']        
        print 'mass',body.getMass()
        print 'friction',body.getFriction()
        print 'restitution',body.getRestitution()
        print 'lsleep',body.getLinearSleepThreshold()
        print 'asleep',body.getAngularSleepThreshold()
        print 'ldamping',body.getLinearDamping()
        print 'adamping',body.getAngularDamping()
        #print 'kinematic',body.getKinematic()
        print '-------------------------------------------------------'