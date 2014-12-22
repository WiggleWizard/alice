#!/usr/bin/python
import os

import system.globals
system.globals.BASE_PATH    = os.path.dirname(os.path.realpath(__file__))
system.globals.SYSTEM_PATH  = os.path.normpath(system.globals.BASE_PATH + "/system/")
system.globals.PLUGINS_PATH = os.path.normpath(system.globals.BASE_PATH + "/plugins/")

from system.alice import Alice
alice = Alice()