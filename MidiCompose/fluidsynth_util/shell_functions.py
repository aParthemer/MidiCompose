import subprocess

from MidiCompose.fluidsynth_util import SCRIPT_PATHS

def make_executable(path):
    subprocess.call(["bash",SCRIPT_PATHS.MAKE_EXECUTABLE,path])

def generate_fs_config():
    pass