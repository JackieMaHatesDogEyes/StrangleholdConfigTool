"""
    Python-based config and modification tool for the 2007 game Stranglehold.

    You need Python 3 to run this script. (Duh!)

    Place it in root folder (NOT IN Binaries/ or StrangleholdGame/).

    Run with 'python3 Stranglehold.py' or use the batch file 'Stranglehold.bat'.

    The code is pretty crappy at the moment, but it works and is probably way more readable than it should be.
"""

from shutil import move
from os import makedirs as mkdir
from glob import glob
from os.path import exists
from subprocess import run
from os import chdir as cd
from os import path
import json
from datetime import datetime
from os import remove as rm
import sys

file_location = ""
if getattr(sys, 'frozen', False):
    file_location = sys.executable
elif __file__:
    file_location = __file__

working_dir = path.dirname(path.realpath(file_location))
print("Working Directory:", working_dir)
cd(working_dir)

def mv(src, dst):
    if exists(src):
        move(src, dst)

opts = {
    "NO_INTROS": True, # Set to True to disable intros
    "DXVK": True, # Set to True to enable DXVK (requires DXVK (32-bit for DX9) to be installed)
    "WINDOWED": False, # Set to True to enable windowed mode (can only be enabled via command-line arguments; Currently not working)
    "NO_VSYNC": False, # Set to True to disable VSync (not yet implemented)
    "SET_4K_RESOLUTION": False, # Set to True to set the resolution to 4K
    "CLEAN_DXVK_CACHE": False, # Set to True to clean the DXVK cache (requires DXVK to be installed)
    "TimePlayedSeconds": 0, # Do not change this value manually
    
}

if not exists("Stranglehold.json"):
    f = open("Stranglehold.json", "w")
    json.dump(opts, f, indent=4)
else:
    f = open("Stranglehold.json", "r")
    opts = json.load(f)
    f.close()

NO_INTROS = opts["NO_INTROS"] 

DXVK = opts["DXVK"]

WINDOWED = opts["WINDOWED"] 

NO_VSYNC = opts["NO_VSYNC"] 

SET_4K_RESOLUTION = opts["SET_4K_RESOLUTION"]

TIME_PLAYED = opts["TimePlayedSeconds"]
CLEAN_DXVK_CACHE = opts["CLEAN_DXVK_CACHE"]

mkdir(".stranglehold", exist_ok=True)

if NO_INTROS:
    mv("StrangleholdGame/Movies/intro_Legal_Euro.bik", ".stranglehold/intro_Legal_Euro.bik")
    mv("StrangleholdGame/Movies/intro_Legal_US.bik", ".stranglehold/intro_Legal_US.bik")
    mv("StrangleholdGame/Movies/intro_Logo_Midway_HD.bik", ".stranglehold/intro_Logo_Midway_HD.bik")
    mv("StrangleholdGame/Movies/intro_Logo_Shared.bik", ".stranglehold/intro_Logo_Shared.bik")
    mv("StrangleholdGame/Movies/intro_Logo_TigerHill_HD.bik", ".stranglehold/intro_Logo_TigerHill_HD.bik")
    mv("StrangleholdGame/Movies/intro_Logo_Unreal.bik", ".stranglehold/intro_Logo_Unreal.bik")
    mv("StrangleholdGame/Movies/intro_c0010_bink.bik", ".stranglehold/intro_c0010_bink.bik")
else:
    if not exists("StrangleholdGame/Movies/intro_Legal_Euro.bik"):
        mv(".stranglehold/intro_Legal_Euro.bik", "StrangleholdGame/Movies/intro_Legal_Euro.bik")
    if not exists("StrangleholdGame/Movies/intro_Legal_US.bik"):
        mv(".stranglehold/intro_Legal_US.bik", "StrangleholdGame/Movies/intro_Legal_US.bik")
    if not exists("StrangleholdGame/Movies/intro_Logo_Midway_HD.bik"):
        mv(".stranglehold/intro_Logo_Midway_HD.bik", "StrangleholdGame/Movies/intro_Logo_Midway_HD.bik")
    if not exists("StrangleholdGame/Movies/intro_Logo_Shared.bik"):
        mv(".stranglehold/intro_Logo_Shared.bik", "StrangleholdGame/Movies/intro_Logo_Shared.bik")
    if not exists("StrangleholdGame/Movies/intro_Logo_TigerHill_HD.bik"):
        mv(".stranglehold/intro_Logo_TigerHill_HD.bik", "StrangleholdGame/Movies/intro_Logo_TigerHill_HD.bik")
    if not exists("StrangleholdGame/Movies/intro_Logo_Unreal.bik"):
        mv(".stranglehold/intro_Logo_Unreal.bik", "StrangleholdGame/Movies/intro_Logo_Unreal.bik")
    if not exists("StrangleholdGame/Movies/intro_c0010_bink.bik"):
        mv(".stranglehold/intro_c0010_bink.bik", "StrangleholdGame/Movies/intro_c0010_bink.bik")

if DXVK:
    if exists("Binaries/d3d9.dll"):
        pass # DXVK is already installed and enabled
    elif exists("Binaries/_d3d9.dll"):
        mv("Binaries/_d3d9.dll", "Binaries/d3d9.dll") # DXVK is already installed but not enabled
    else:
        raise FileNotFoundError("DXVK is not installed but is enabled in Stranglehold.py")
else:
    if exists("Binaries/d3d9.dll"):
        mv("Binaries/d3d9.dll", "Binaries/_d3d9.dll") # Rename DXVK to disable it
    else:
        pass # DXVK is already disabled
    
cmdline_args = [""]

if WINDOWED:
    #cmdline_args.append("-windowed")
    print("Skipping windowed mode as it is currently not working")

if SET_4K_RESOLUTION:
    cmdline_args.append("-ResX=3840")
    cmdline_args.append("-ResY=2160")


cd("Binaries/")

args = ["Retail-Stranglehold.exe"] + cmdline_args

now = datetime.now()

# Start Stranglehold
run(args)

timePlayed = datetime.now() - now


opts["TimePlayedSeconds"] += TIME_PLAYED

f = open(working_dir + "/Stranglehold.json", "w")
json.dump(opts, f, indent=4)


if CLEAN_DXVK_CACHE:
    rm("Retail-Stranglehold.dxvk-cache")
    rm("Retail-Stranglehold_d3d9.log")