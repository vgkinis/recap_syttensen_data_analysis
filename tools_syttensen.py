import numpy as np
import scipy as sp
from Tkinter import *
import ttk
import tkFileDialog
import tkMessageBox
import matplotlib.pyplot as plt
import os
import os.path
import sys
sys.path.append("/Users/vasilis/")
sys.path.append("/home/vasileios/")
import time
import copy
import pickle
import bunch_syttensen


class SyttensenTools(object):

    def __init__(self):
        return


    def combine_dat(self, directory):
        """

        """
        top_bunch = bunch_syttensen.Bunch()
        list_of_files = os.listdir(directory)
        for j in list_of_files:
            fullpath = os.path.join(directory, j)
            print("Reading...%s") %fullpath
            new_bunch = bunch_syttensen.Bunch()
            new_bunch.read_data(fullpath)
            top_bunch.concat(new_bunch)

        return top_bunch
