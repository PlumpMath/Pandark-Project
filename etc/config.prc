# http://www.panda3d.org/wiki/index.php/List_of_All_Config_Variables


# window
# ------
window-title Pandark-Project
win-origin 50 50
win-size 800 600
#win-size 1280 1024
fullscreen false
#fullscreen true
#win-fixed-size 1


# paths
# -----
# where to look for all models, textures, fonts etc.
model-path assets/models
# OS dependent - will be determined by python. change to force
model-cache-dir xtmp/pandacache
default-model-extension .egg

# graphics
# --------
basic-shaders-only false
use-movietexture true
compressed-textures true
driver-compress-textures true
model-cache-textures true
# antialiasing
framebuffer-multisample false
multisamples 0
#multisamples 4
#multisamples 8
# default camera clipping
default-far 100000
# scale textures while loading (lower for more performance)
texture-scale 1
azure-bloom-filter false
azure-cartoon-ink false


# audio
# -----
#audio-library-name p3openal_audio
audio-library-namep3fmod_audio
audio-music-active true
audio-sfx-active true
audio-volume 1


# else
# ----
aux-display pandagl
aux-display pandadx9
aux-display pandadx8

load-display *

# opengl display lists support
display-lists true

# set higher on multicore processors
loader-num-threads 1

# max-num-threads
#max-num-32

#cull/draw
#threading-model cull/draw

# used when panda writes text files (unsure what's best here)
newline-mode msdos
#newline-mode unix


# debugging
# ---------
#window-type none
want-dev false
want-pstats false
# framerate limitation
sync-video false
show-frame-rate-meter true
on-screen-debug-enabled false
notify-output log.txt

# notifier verbosity levels: (spam), debug, info, warning, error, (fatal)
# the ones in brackets are only available for C++ modules (not direct)
default-directnotify-level                  warning
notify-level                                warning
#notify-level-util                           fatal
#notify-level-ShowBase                       debug
#notify-level-Actor                          debug
#notify-level-FSM                            debug
#notify-level-EventManager                   debug
#notify-level-ExceptionVarDump               debug
#notify-level-FunctionInterval               debug
#notify-level-GarbageReport                  debug
#notify-level-InputState                     debug
#notify-level-Loader                         debug
#notify-level-Messenger                      debug
#notify-level-TaskManager                    debug
#notify-level-JobManager                     debug
#notify-level-azure-camera                   debug
#notify-level-azure-control                  debug
#notify-level-ode                            spam
#notify-level-odebody                        spam
#notify-level-odegeom                        spam
#notify-level-odespace                       spam
#notify-level-odejoint                       spam
#notify-level-odeworld                       spam
#notify-level-odetrimeshdata                 spam