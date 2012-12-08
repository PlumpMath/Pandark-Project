from pandac.PandaModules import loadPrcFileData 
loadPrcFileData("", "window-type none") 
loadPrcFileData("", "model-cache-dir $MAIN_DIR/tmp/pandacache")
loadPrcFileData("", "load-display tinydisplay")

from direct.directbase import DirectStart

loader.loadModel('assets/models/humans/rachel')

#import os
#os.system('copy nul ./tmp/.cache')

#Hack mode
open('tmp/.cache','wb').close()


#import subprocess
#subprocess.Popen('copy nul cache.txt',shell=True)
# # import os.path
# # print os.path.isfile('ok.txt')

# import yaml

# #from pandac.PandaModules import Filename,  Multifile, readXmlStream


# import zlib
# str_object1 = open('rachel.txt', 'rb').read()
# str_object2 = zlib.compress(str_object1, 9)
# f = open('rachel.txt.zip', 'wb')
# f.write(str_object2)
# f.close()

# # f = open('rachel.txt.zip', 'rb')
# # print zlib.decompress(f.read())
# # f.close()

# import tarfile
# tar = tarfile.open("sample.tar.gz", "w:gz")
# for name in ["rachel.txt"]:
#     tar.add(name)
# tar.close()