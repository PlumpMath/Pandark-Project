######################
## OgreMax File Parser
## By Fred Ukita
######################

from panda3d.core import Vec2, Vec3, Vec4, Quat
from xml.dom import minidom
from builder import Builder

class Loader(object):    

    def __init__(self,onload):
        self.physics_attrs = ['shapetype','mass','friction','ldamping','adamping','lsleep','asleep','restitution','deactivation','kinematic'] 
        self.onload = onload
        self.reset()

    def reset(self):
        self.environment = {}
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

        scene = Builder(self.environment,self.nodes,self.lights,self.cameras,self.entities,self.animations,self.staticGeoms,self.configs)

        self.reset()

        self.onload(scene)

    def entitiesSetup(self,entities):

        """Yaml Generator"""

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

        models = list(set(models) )  

        '''TODO: Load Manager'''
        loader.loadModel(models)

    def loadScene(self,sceneName):
        xml = minidom.parse( sceneName )

        if xml.getElementsByTagName('environment'):
            #Set Colour Background
            environment = xml.getElementsByTagName('environment')[0]
            self.environment['colourBackground'] = self.__getColor(environment,'colourBackground')
            self.environment['colourAmbient']    = self.__getColor(environment,'colourAmbient')

            self.environment['fog'] = {}

            if environment.getElementsByTagName('fog'):
                fog = environment.getElementsByTagName('fog')[0]
                mode        = fog.getAttribute('mode')            
                color       = self.__getColor(fog,'colourDiffuse')
                linearStart = float(fog.getAttribute('linearStart') or 0) 
                linearEnd   = float(fog.getAttribute('linearEnd')   or 0)
                expDensity  = float(fog.getAttribute('expDensity')  or 0)

                self.environment['fog'] = {'mode':mode,'color':color,'linearStart':linearStart,'linearEnd':linearEnd,'expDensity':expDensity}

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

                t = self.__getVec3(kf,'translation')#Hack to fix 3dsmax Z position: "z/2"
                translation = Vec3(t.x,t.y,t.z/2)#Hack to fix 3dsmax Z position: "z/2"
                
                #translation = self.__getVec3(kf,'translation')#No hack
                rotation    = self.__getQuat(kf)
                scale       = self.__getVec3(kf,'scale')
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
        props['groupName'] = xmlNode.parentNode.getAttribute('name')

        self.animations[props['name']] = None

        return props

    def __getLightProps(self,xmlNode):
        '''Light'''
        props = self.__getBasicProps(xmlNode)
        light = xmlNode.getElementsByTagName('light')[0]
        props['type']    = light.getAttribute('type') 
        #props['power']   = light.getAttribute('power')       
        props['visible'] = light.getAttribute('visible')
        props['colourDiffuse']  = self.__getColor(xmlNode)
        props['colourSpecular'] = self.__getColor(xmlNode,'colourSpecular')
        props['castShadows']    = self.str2Bool(light.getAttribute('castShadows') )        

        '''Light Attenuation'''
        if light.getElementsByTagName('lightAttenuation'):
            attenuation = light.getElementsByTagName('lightAttenuation')[0]
            constant = float(attenuation.getAttribute('constant') )
            linear   = float(attenuation.getAttribute('linear') )
            quadric  = float(attenuation.getAttribute('quadric') )
            props['attenuation'] = Vec3(constant,linear,quadric)

        '''Light Range'''
        lightRange = light.getElementsByTagName('lightRange')
        props['range'] = not lightRange or self.__getRange(lightRange[0])

        #Hack
        p = props['pos']
        props['pos'] = Vec3(p.x,p.y,p.z*2)

        return props

    def __getRange(self,xmlNode):        
        inner = float(xmlNode.getAttribute('inner') )
        outer = float(xmlNode.getAttribute('outer') )
        return Vec2(outer, inner)

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
        z = float( vec3.getAttribute('z') ) / 2 #Hack to fix 3dsmax Z position: "z/2"
        return Vec3(x,y,z)
    
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
        return Vec4(r,g,b,alpha)
    
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