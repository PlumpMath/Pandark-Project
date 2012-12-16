import os, multiprocessing
from pandac.PandaModules import loadPrcFile, loadPrcFileData
from pandac.PandaModules import Filename
loadPrcFile(Filename.expandFrom("$MAIN_DIR/etc/config.prc"))

coresNum =  multiprocessing.cpu_count() #int( os.environ["NUMBER_OF_PROCESSORS"] )

if coresNum > 1:
    threadsNum = str(pow(coresNum,3) )
    loadPrcFileData('', 'loader-num-threads ' + threadsNum )

from direct.showbase.ShowBase import ShowBase

from pandark.core import Core

class Main(ShowBase):
  
    def __init__(self):
        ShowBase.__init__(self)

        self.core = Core()

        self.core.demand("Menu", "MainMenu")

        self.accept('a', self.load)
        self.accept('escape', self.exit)

        self.run()

    def load(self):
        #scene name
        sceneName = "scenario01"
        self.core.demand("Loading", sceneName)

    def exit(self):
        base.graphicsEngine.removeAllWindows()
        ShowBase.destroy(self)
        os._exit(0)

try:
    import psyco
    psyco.full()    
except ImportError:
    print 'Psyco is not installed.'


Main()