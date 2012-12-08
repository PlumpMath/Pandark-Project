"""1968's core FSM."""

from direct.fsm.FSM import FSM

from menuproxy import MenuProxy

from loader import Loader

from pandark.managers.physicsmanager import PhysicsManager

import __builtin__

__builtin__.physicsMgr = PhysicsManager()

import subprocess

from direct.stdpy import threading

import os

class Core(FSM):
    """knows Menu, Scenario and Loading."""
    def __init__(self):
        FSM.__init__(self, "Core Game Control")
        # We might need to put a loading screen in front of menu if we get some
        # fancy menu screens.
        self.defaultTransitions = {"Menu":["Loading",],
                                   "Loading":["Scenario",],
                                   "Scenario":["Menu", "Loading"]
                                   }
        # Optional, but prevents a warning message.
        # The scenario task chain gives us grouping option.
        # It might get replaced by an own task manager, by chance.
        #taskMgr.setupTaskChain("scenario", frameBudget=-1,numThreads=1)        

        self.doPhysics = physicsMgr.world.doPhysics

        self.getDt = globalClock.getDt

        self.loader = Loader(self.onLoad)

        physicsMgr.debug().show() 

    def popen(self, onExit, popenArgs):
        def runInThread(onExit, popenArgs):
            proc = subprocess.Popen(popenArgs)
            proc.wait()
            onExit()
            return
        thread = threading.Thread(target=runInThread, args=(onExit, popenArgs))
        thread.start()
        # returns immediately after the thread starts
        return thread 

    #Hack mode
    def popen2(self, callback, popenArgs):
        subprocess.Popen(popenArgs)
        def check(task):
            if os.path.isfile('tmp/.cache'):
                #os.unlink("cache.txt")
                callback()                
                return task.done
            return task.cont

        taskMgr.add(check,'waiting',sort=10)
        #print os.path.isfile('ok.txt')

    def onCache(self):
        print '--- Models were cached'
        #self.m=loader.loadModel('game/assets/models/humans/rachel') 
        #self.m.reparentTo(render)
         

    def onLoad(self,scene):
        #self.popen2(self.onCache, ['ppython', 'load.py'])

        self.scene = scene
        self.scene.start()
        taskMgr.add( self.mainLoop, 'mainLoop' )


    def mainLoop(self,task):
        #if 'EOF' == self.x.stdout.readline():print '--------------------'
        #print os.path.isfile('ok.txt')
        self.doPhysics( self.getDt() )
        return task.cont      

    '''FSM'''

    def enterLoading(self, scenario):
        print 'Loading', scenario
        self.loader.preload(scenario)
        
        # TODO: put this into gui package and add a black background
        # self.loading = OnscreenText(text="LOADING", pos=(0,0), scale=0.1,
        #                        align=TextNode.ACenter, fg=(1,1,1,1))
        # self.preloader = scenarioPreloader(scenario)
        # base.graphicsEngine.renderFrame()
        # base.graphicsEngine.renderFrame()
        # self.preloader.preloadFast()  # depends on the loading screen
        # # Other preloader methods would specify a callback that calls
        # # self.demand(scenario), but preloadFast() is executed in one frame, so
        # # we can safely demand that from here. Interactive loading screens
        # # might require special handling.
        # self.demand("Scenario", scenario)

    def exitLoading(self):
        pass
        # self.loading.destroy()
        # del self.loading
        # del self.preloader

    def enterScenario(self, scenario):
        pass
        # self.scenario = ScenarioProxy(scenario)
        # self.scenario.begin()

    def exitScenario(self):
        pass
        # self.scenario.destroy()
        # del self.scenario

    def enterMenu(self, menu, *args):
        self.menu = MenuProxy(menu, *args)
        #import game.gui as gui
        #self.menu = getattr(gui, menu)()

    def exitMenu(self):
        print 'Exit Menu'
        # self.menu.destroy()
