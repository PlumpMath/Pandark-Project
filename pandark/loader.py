from panda3d.core import Vec3, Quat
from xml.dom import minidom
from builder import Builder
# import time
# import yaml
#from direct.stdpy import thread
#from greenlet import greenlet
class Loader(object): 

    physics_attrs =\
    ['shapetype','mass','friction','ldamping','adamping','lsleep','asleep','restitution','deactivation','kinematic'] 

    def __init__(self,callback):
        self.callback = callback
        self.reset()

    def reset(self):
        self.nodes       = []
        self.lights      = []
        self.cameras     = []         
        self.entities    = []        
        self.animations  = {}
        self.staticGeoms = []
        self.configs     = {}

        self.modelsLoaded = 0

    def preload(self,sceneName):
        sceneName = 'assets/scenarios/' + sceneName + '.scene'

        xml = minidom.parse( sceneName + '.userdata.xml' )

        entities = xml.getElementsByTagName('Entity')

        self.entitiesSetup( entities )

        self.loadScene( sceneName )   

        scene = Builder(self.nodes,self.lights,self.cameras,self.entities,self.animations,self.staticGeoms,self.configs)

        self.reset()

        self.callback(scene)

    def entitiesSetup(self,entities):

        #objs = {}

        models = []

        attributes = ['model_path']

        for ent in entities:

            name = ent.getAttribute('__name')

            if 'Group' in name:continue

            txt = ent.getElementsByTagName('class')[0].childNodes[0].data + '\n'

            txt += 'name: ' + name + '\n'

            for attr in attributes:                
                txt += attr + ': ' + ent.getElementsByTagName(attr)[0].childNodes[0].data + '\n'

            txt += 'physics: \n'

            txt += ' name: ' + name + '\n'

            for attr in self.physics_attrs:
                txt += ' ' + attr + ': ' + ent.getElementsByTagName(attr)[0].childNodes[0].data + '\n'

            self.configs[name] = txt

            models.append( ent.getElementsByTagName('model_path')[0].childNodes[0].data )

        models = list( set(models) )  

        loader.loadModel(models)

    def loadScene(self,sceneName):
        xml = minidom.parse( sceneName )

        for xmlNode in xml.getElementsByTagName('staticGeometry'):
            name = xmlNode.getAttribute('name')
            props = {}
            props['name']       = name
            props['origin']     = self.__getVec3(xmlNode,'origin')
            props['dimensions'] = self.__getVec3(xmlNode,'dimensions')  
            props['configFile'] = name.split('_')[0] 
            self.staticGeoms.append( props )

        for xmlNode in xml.getElementsByTagName('node'):
            self.__parsing(xmlNode)

    """ Scene Elements Parsing
    -----------------------------------------------------------------------------------------------------------------"""    
    def __parsing(self,xmlNode):        
        if xmlNode.getElementsByTagName('node'):
            '''if node is a Group'''            
            self.nodes.append(self.__getBasicProps(xmlNode))
        else:
            if xmlNode.getElementsByTagName('entity'):
                self.entities.append( self.__getBasicProps(xmlNode) )

            elif xmlNode.getElementsByTagName('light'): 
                self.lights.append( self.__getLightProps(xmlNode) )
            
            elif xmlNode.getElementsByTagName('camera'): 
                self.cameras.append( self.__getBasicProps(xmlNode) )

        if xmlNode.getElementsByTagName('animations'): 
            self.__getAnimations(xmlNode.getElementsByTagName('animations')[0])

    """ Get Animations 
    -----------------------------------------------------------------------------------------------------------------"""
    
    def __getAnimations(self,animations):
        parent     = animations.parentNode.getAttribute('name')
        animations = animations.getElementsByTagName('animation')
        self.animations[parent] = {}

        for anim in animations:
            name   = anim.getAttribute('name').split('_')[1];
            loop   = self.str2Bool(anim.getAttribute('loop'))
            enable = self.str2Bool(anim.getAttribute('enable'))
            keyframes = anim.getElementsByTagName('keyframe')

            self.animations[parent][name] = {}
            self.animations[parent][name]['loop']   = loop
            self.animations[parent][name]['enable'] = enable
            self.animations[parent][name]['seq']    = []

            for kf in keyframes:
                time        = float(kf.getAttribute('time'))
                translation = self.__getVec3(kf,'translation')
                rotation    = self.__getQuat(kf)
                scale       = self.__getScale(kf)
                self.animations[parent][name]['seq'].append((time, translation, rotation, scale))
        
    """ Get Basic Properties of the Elements 
   -----------------------------------------------------------------------------------------------------------------"""
    
    def __getBasicProps(self,xmlNode):
        #print xmlNode.getAttribute('id')  
        props = {}    
        props['name']      = xmlNode.getAttribute('name')    
        props['pos']       = self.__getPos(xmlNode)
        props['quat']      = self.__getQuat(xmlNode)
        props['scale']     = self.__getVec3(xmlNode,'scale')
        props['groupName'] = xmlNode.parentNode.getAttribute('name') #or 'render'

        self.animations[props['name']] = None

        return props

    def __getLightProps(self,xmlNode):
        '''Light'''
        props = self.__getBasicProps(xmlNode)
        light = xmlNode.getElementsByTagName('light')[0]
        props['type']    = light.getAttribute('type')
        props['power']   = light.getAttribute('power')
        props['visible'] = light.getAttribute('visible')
        props['color']   = self.__getColor(xmlNode)
        return props

    def __getVec3(self,xmlNode,tag):
        '''Vec3'''
        vec3 = xmlNode.getElementsByTagName(tag)[0]            
        x = float( vec3.getAttribute('x') )
        y = float( vec3.getAttribute('y') )
        z = float( vec3.getAttribute('z') )
        return Vec3(x,y,z)


    def __getPos(self,xmlNode):
        '''Vec3'''
        vec3 = xmlNode.getElementsByTagName('position')[0]            
        x = float( vec3.getAttribute('x') )
        y = float( vec3.getAttribute('y') )
        z = float( vec3.getAttribute('z') )
        return Vec3(x,y,z/2)
    
    def __getQuat(self,xmlNode):
        '''quaternion'''
        rotation = xmlNode.getElementsByTagName('rotation')[0]
        w = float( rotation.getAttribute('qw') )
        x = float( rotation.getAttribute('qx') )
        y = float( rotation.getAttribute('qy') )
        z = float( rotation.getAttribute('qz') )            
        return Quat(w,x,y,z)
    
    def __getColor(self,xmlNode,attribute='colourDiffuse',alpha=1):
        '''color'''
        xmlNode = xmlNode.getElementsByTagName(attribute)[0]
        r = float( xmlNode.getAttribute('r') )
        g = float( xmlNode.getAttribute('g') )
        b = float( xmlNode.getAttribute('b') )
        return (r,g,b,alpha)
    
    def __getClipping(self,xmlNode):
        clipping = xmlNode.getElementsByTagName('clipping')[0] 
        near     = float( clipping.getAttribute('near') ) 
        far      = float( clipping.getAttribute('far') )
        
        if near == .0:
            near = 1
        
        return near, far 

    def str2Bool(self,s):
        b = {'true':True, 'false':False}
        return b[s]