from direct.fsm.FSM import FSM

from menuproxy import MenuProxy

from loader import Loader

#import os, subprocess

#from direct.stdpy import threading

class Core(FSM):
    """knows Menu, Scenario and Loading."""
    def __init__(self):
        FSM.__init__(self, "Core Game Control")
        self.loader = Loader(self.enterScenario)

    def toggleDebug(self):
        if self.debugNP.isHidden():
            #render.setShaderAuto()
            self.debugNP.show()
        else:
            #render.setShaderOff()
            #render.clearLight()
            self.debugNP.hide()

    # def popen(self, onExit, popenArgs):
    #     def runInThread(onExit, popenArgs):
    #         proc = subprocess.Popen(popenArgs)
    #         proc.wait()
    #         onExit()
    #         return
    #     thread = threading.Thread(target=runInThread, args=(onExit, popenArgs))
    #     thread.start()
    #     # returns immediately after the thread starts
    #     return thread

    def mainLoop(self,task):
        dt = self.getDt()
        self.doPhysics(dt)
        return task.cont      

    '''FSM'''

    def enterLoading(self, scenario):
        print 'Loading', scenario
        self.loader.preload(scenario)

    def exitLoading(self):
        pass
        # self.loading.destroy()
        # del self.loading
        # del self.preloader

    def enterScenario(self, scene):
        self.scene = scene
        print 'Enter Scenario'

        self.doPhysics = scene.physicsMgr.world.doPhysics

        self.getDt = globalClock.getDt
        
        self.debugNP = scene.physicsMgr.debug()        

        self.scene = scene

        #self.scene.sceneNode.setShaderAuto()

        self.scene.begin()

        #self.scene.clearModelNodes() 

        #self.scene.flattenStrong()        

        self.mainLoop = taskMgr.add( self.mainLoop, 'mainLoop' )

        self.accept('f1', base.toggleWireframe)
        self.accept('f2', base.toggleTexture)
        self.accept('f3', self.toggleDebug)
        self.accept('r', self.clearScene)

    def clearScene(self):
        self.debugNP.hide()
        taskMgr.remove( self.mainLoop )
        del self.mainLoop
        self.scene.destroy()
        del self.scene
        del self.doPhysics
        del self.getDt
        del self.debugNP
        self.demand("Loading", 'scenario01')

    def exitScenario(self):
        pass
        # for child in render.getChildren(): 
        #     #if child != base.camera:
        #     print child, 'removed'
        #     child.removeNode()

    def enterMenu(self, menu, *args):
        self.menu = MenuProxy(menu, *args)
        #import game.gui as gui
        #self.menu = getattr(gui, menu)()

    def exitMenu(self):
        print 'Exit Menu'
        # self.menu.destroy()
