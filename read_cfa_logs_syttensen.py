"""
#######################################################################################
Changes history for read_cfa_logs.py
#
#03112014: Modified to using pickle_bunch method so the gil files are 
#          pickles of the python dictionaries
#
#######################################################################################
"""

import sys
sys.path.append("/Users/vasilis/")
sys.path.append("/home/vasileios/")
import vaspy
from vaspy import syttensen
import vaspy.syttensen.bunch_syttensen as bunch_syttensen
import numpy as np
import matplotlib.pyplot as plt
import time
import pickle
import copy

plt.close("all")
plt.ion()
log_filepath = raw_input("Give full filepath of logfile: ")
# log_filepath = "/Users/vasilis/Desktop/cfa_log_south_dome_027_046.log"
log_data = np.loadtxt(log_filepath, skiprows = 1, dtype = "S10")
cfa_date = log_data[:,0]
cfa_utc_time = log_data[:,1]
cfa_epoch_time = log_data[:,2].astype(float)
cfa_on_flag = log_data[:,3].astype(int)
cfa_top_bag = log_data[:,4].astype(int)

data_filepath = raw_input("Give full filepath of cfa dat file: ")
# data_filepath = "/Users/vasilis/Documents/picarro/Syttensen/bunch_sdome_smow.gil"
b = bunch_syttensen.Bunch()
b.read_data(data_filepath)

out_filepath = raw_input("Give filepath (up to bag nr.) for output files: ")


unique_bags = np.unique(cfa_top_bag)
print(("Top bags of separate runs:" , unique_bags))

nr_of_runs = np.size(unique_bags)
for j in unique_bags:
    crit = (cfa_top_bag == j) & (cfa_on_flag == 1)
    indexes = np.where(crit)[0]
    print(indexes)
    try:
        epoch_1 = cfa_epoch_time[indexes[0]]
        epoch_2 = cfa_epoch_time[indexes[-1]]
        index_1 = np.where(b.epoch>epoch_1)[0][0]
        index_2 = np.where(b.epoch>epoch_2)[0][0]
        b1 = b.pick(index_1, index_2)
        filepath_1 = out_filepath + "renland_" + str(j) + "_bunch.gil"
        b1.pickle_bunch(filepath_1)
        print("Writing %s\n\n" %filepath_1)
        try:
            run1 = bunch_syttensen.Run(b1)
            run1.locate()
            b1.plot()
            filepath_2 = out_filepath + "renland_" + str(j) + "_run.gil"
            run1.pickle_bunch(filepath_2)
        except:
            print("Run with top bag %i not located properly." %j)

    except:
        print("Condition not true for unique top bag field %i" %j)


    raw_input("press any key to continue with next section")


plt.close("all")




