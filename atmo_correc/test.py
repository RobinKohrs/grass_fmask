#!/bin/bash
import os
import pprint
import subprocess

cmd = "L2A_Process --help"
subprocess.call(cmd, shell = True)
