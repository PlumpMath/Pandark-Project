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

import re

class PhysicsManager(object):

    num_rigidBodies = 0
    num_ghosts      = 0

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

        #self.composer = Composer()
        self.addShape['compound'] = self.__addCompound

       # self.shapesList = self.addShape.keys()

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
        PhysicsManager.num_rigidBodies+=1
        return BulletRigidBodyNode(name or 'rigidbody'+str(PhysicsManager.num_rigidBodies) )

    def createRigidBody(self, shapetype, model, props={}, name=None):
        body = self.getRigidBody(name)
        self.addShape[shapetype](body, model)
        props = dict(self.getRigidBodyDefaultProps().items() + props.items() )
        self.setBodyProps(body, props)
        self.world.attachRigidBody( body )
        return body         

    def getGhost(self, name=None):
        PhysicsManager.num_ghosts+=1
        return BulletGhostNode(name or 'ghost'+str(PhysicsManager.num_ghosts) )

    def createGhost(self, shapetype, size, name=None):        
        ghost = self.getGhost(name)
        self.addShape[shapetype](ghost, size) 
        self.world.attachGhost(ghost)
        return ghost  

    def attachRigidBody(self, body, props):
        self.setBodyProps(body, props)
        self.world.attachRigidBody(body)

    def __addCompound(self, body, model):
        self.createCompound(model,body)   

    def __addSphere(self, body, model, pos=(0,0,0), hpr=(0,0,0), scale=(1,1,1) ):
        size = self.getSize(model)
        shape = BulletSphereShape( max(size)/2 )
        body.addShape(shape, TransformState.makePosHprScale(pos,hpr,scale) )

    def __addBox(self, body, model, pos=(0,0,0), hpr=(0,0,0), scale=(1,1,1) ):
        size = self.getSize(model)
        shape = BulletBoxShape( size/2 )
        body.addShape(shape, TransformState.makePosHprScale(pos,hpr,scale) )

    def __addCylinder(self, body, model, pos=(0,0,0), hpr=(0,0,0), scale=(1,1,1) ):
        size = self.getSize(model)
        shape = BulletCylinderShape(max(size.x,size.y)/2, size.z, ZUp)
        body.addShape( shape, TransformState.makePosHprScale(pos,hpr,scale) )

    def __addCapsule(self, body, model, pos=(0,0,0), hpr=(0,0,0), scale=(1,1,1) ):
        size = self.getSize(model)
        diam = max(size.x,size.y)
        shape = BulletCapsuleShape(diam/2, size.z-diam, ZUp)       
        body.addShape( shape, TransformState.makePosHprScale(pos,hpr,scale) )

    def __addCone(self, body, model, pos=(0,0,0), hpr=(0,0,0), scale=(1,1,1) ):
        size = self.getSize(model)
        shape = BulletConeShape(max(size.x,size.y)/2, size.z, ZUp)
        body.addShape( shape, TransformState.makePosHprScale(pos,hpr,scale) )

    def __addConvexHull(self, body, model, pos=(0,0,0), hpr=(0,0,0), scale=(1,1,1) ):        
        
        def one():
            geom = model.node().getGeom(0)          
            shape = BulletConvexHullShape()
            shape.addGeom(geom)
            body.addShape( shape, TransformState.makePosHprScale(pos,hpr,scale) )
            return []

        children =  model.findAllMatches('**/+GeomNode') or one()

        model.flattenLight()

        for piece in children:
            shape = BulletConvexHullShape()
            geom = piece.node().getGeom(0)
            shape.addGeom(geom)
            body.addShape( shape, TransformState.makePosHprScale(pos,hpr,scale) )

    def __addTriangleMesh(self, body, model, pos=(0,0,0), hpr=(0,0,0), scale=(1,1,1), dynamic=True):        
        
        mesh = BulletTriangleMesh()
      
        def one():
            geom = model.node().getGeom(0)            
            mesh.addGeom(geom)
            return []

        children =  model.findAllMatches('**/+GeomNode') or one()

        model.flattenLight()

        for piece in children:
            geom = piece.node().getGeom(0)
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
        #debugNP.show()
        debugNP.node().showWireframe(True)
        debugNP.node().showConstraints(True)
        debugNP.node().showBoundingBoxes(False)
        debugNP.node().showNormals(False)        
        self.world.setDebugNode(debugNP.node())
        return debugNP

    def getSize(self,model):        
        hpr = model.getHpr()
        model.setHpr(0,0,0)
        minLimit, maxLimit = model.getTightBounds()
        model.setHpr(hpr) 
        return maxLimit - minLimit

    def setShape(self, model, body):
        #To Re-Do
        name = model.getName()

        pos,hpr,scale = model.getPos(), model.getHpr(), model.getScale()    

        shapetype = re.findall("[-a-z]+",name.lower())[0].split('-')

        shapetype = filter(None,shapetype)
        
        if shapetype[0] in self.addShape.keys():
            self.addShape[shapetype[0]](body,model,pos,hpr,scale)

        not '-' in name or model.remove()

    def createCompound(self, model, body):
        children = model.find('**/*').getChildren() or model.getChildren()

        [self.setShape(child,body) for child in children]
