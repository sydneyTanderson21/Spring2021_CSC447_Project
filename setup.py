from distutils.core import setup # Need this to handle modules
import py2exe 
import math # We have to import all modules used in our program
from time import sleep
import sys
from subprocess import call
import threading
from socket import *
import random
from time import *
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP
from base64 import b64decode, b64encode
from tkinter import *
from tkinter.constants import LEFT, TOP, BOTTOM, BOTH,RIGHT, X, Y

#setup(console=['runGame.py']) # Calls setup function to indicate that we're dealing with a single console application