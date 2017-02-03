import sys
import scipy as sc
from scipy import signal
sys.path.append("/Users/vasilis/")
sys.path.append("/home/vasileios/")
import vaspy
from vaspy import syttensen
import bunch_syttensen
import numpy as np
import matplotlib.pyplot as plt
import time
import pickle
import copy
import json
import os


#####################################################################
####### Read params from json file......................
###################################################################
json_path = raw_input("Give full path for json file: ")
f = open(json_path, "r")
json_params = json.load(f)
f.close()

data_filepath = json_params["data_file"]
log_filepath = json_params["cfa_log_file"]
cfa_top_bag_for_cal = json_params["top_bag_flag"]


step_duration = json_params["step_duration"]
step_duration = step_duration*60.
pct_on = json_params["pct_on"]
pct_off = json_params["pct_off"]
t_on = pct_on/100.*step_duration
t_off = pct_off/100.*step_duration

std1_d17 = json_params["std1_d17"]
std1_d18 = json_params["std1_d18"]
std1_dD = json_params["std1_dD"]

std2_d17 = json_params["std2_d17"]
std2_d18 = json_params["std2_d18"]
std2_dD = json_params["std2_dD"]

std3_d17 = json_params["std3_d17"]
std3_d18 = json_params["std3_d18"]
std3_dD = json_params["std3_dD"]
#####################################################################


# step_duration = 20 #in min
# step_duration = step_duration*60
# pct_on = 40.
# pct_off = 90.
# t_on = pct_on/100*step_duration
# t_off = pct_off/100*step_duration
# data_filepath = "/Users/vasilis/Desktop/HKDS2004-20151009-132834Z-DataLog_User.dat"
# log_filepath = "/Users/vasilis/Desktop/Friday-oct-9-2015.cal"
# cfa_top_bag_for_cal = -999



plt.close("all")
plt.ion()
log_data = np.loadtxt(log_filepath, skiprows = 1, dtype = "S10")
cfa_date = log_data[:,0]
cfa_utc_time = log_data[:,1]
cfa_epoch_time = log_data[:,2].astype(float)
cfa_on_flag = log_data[:,3].astype(int)
cfa_top_bag = log_data[:,4].astype(int)
valco_pos = log_data[:,5].astype(int)


bunch_instance = bunch_syttensen.Bunch()
bunch_instance.read_data(data_filepath)


crit1 = (cfa_top_bag == cfa_top_bag_for_cal)
indexes = np.where(crit1)[0] #indexes in the log file
epoch_1 = cfa_epoch_time[indexes[0]] #epoch start in the log file
epoch_2 = cfa_epoch_time[indexes[-1]] #epoch end in the log file
index_1 = np.where(bunch_instance.epoch>epoch_1)[0][0] #index start picarro bunch instance
index_2 = np.where(bunch_instance.epoch>epoch_2)[0][0] #index start picarro bunch instance
bunch_instance_cal = bunch_instance.pick(index_1, index_2)
bunch_instance_cal.index_i = np.arange(np.size(bunch_instance_cal.d18))

bunch_instance_cal.plot()
smoothed_dD = bunch_instance_cal.smooth(bunch_instance_cal.dD, 100, window = "bartlett")
diff_dD = np.gradient(smoothed_dD)
plt.figure(123)
plt.plot(diff_dD)
minima_indexes = signal.argrelmin(diff_dD, order = 800)[0]
print minima_indexes
plt.plot(minima_indexes, diff_dD[minima_indexes], "ro")


epoch_std1_on = bunch_instance_cal.epoch[minima_indexes[0]] + t_on
epoch_std1_off = bunch_instance_cal.epoch[minima_indexes[0]] + t_off
std1_index_on = np.where(bunch_instance_cal.epoch > epoch_std1_on)[0][0]
std1_index_off = np.where(bunch_instance_cal.epoch > epoch_std1_off)[0][0]

epoch_std2_on = bunch_instance_cal.epoch[minima_indexes[1]] + t_on
epoch_std2_off = bunch_instance_cal.epoch[minima_indexes[1]] + t_off
std2_index_on = np.where(bunch_instance_cal.epoch > epoch_std2_on)[0][0]
std2_index_off = np.where(bunch_instance_cal.epoch > epoch_std2_off)[0][0]

epoch_std3_on = bunch_instance_cal.epoch[minima_indexes[2]] + t_on
epoch_std3_off = bunch_instance_cal.epoch[minima_indexes[2]] + t_off
std3_index_on = np.where(bunch_instance_cal.epoch > epoch_std3_on)[0][0]
std3_index_off = np.where(bunch_instance_cal.epoch > epoch_std3_off)[0][0]

plt.figure(13)
plt.subplot(211)
plt.plot(bunch_instance_cal.epoch - bunch_instance_cal.epoch[0], bunch_instance_cal.dD, "r")
plt.plot(bunch_instance_cal.epoch[minima_indexes] - bunch_instance_cal.epoch[0], \
    bunch_instance_cal.dD[minima_indexes], "bo")
plt.plot(bunch_instance_cal.epoch[std1_index_on:std1_index_off] - bunch_instance_cal.epoch[0], \
    bunch_instance_cal.dD[std1_index_on:std1_index_off], "b")
plt.plot(bunch_instance_cal.epoch[std2_index_on:std2_index_off] - bunch_instance_cal.epoch[0], \
    bunch_instance_cal.dD[std2_index_on:std2_index_off], "b")
plt.plot(bunch_instance_cal.epoch[std3_index_on:std3_index_off] - bunch_instance_cal.epoch[0], \
    bunch_instance_cal.dD[std3_index_on:std3_index_off], "b")
plt.xlabel("sec")

plt.subplot(212)
plt.plot(bunch_instance_cal.epoch - bunch_instance_cal.epoch[0], bunch_instance_cal.d18, "b")
plt.plot(bunch_instance_cal.epoch[minima_indexes] - bunch_instance_cal.epoch[0], \
    bunch_instance_cal.d18[minima_indexes], "ro")
plt.plot(bunch_instance_cal.epoch[std1_index_on:std1_index_off] - bunch_instance_cal.epoch[0], \
    bunch_instance_cal.d18[std1_index_on:std1_index_off], "r")
plt.plot(bunch_instance_cal.epoch[std2_index_on:std2_index_off] - bunch_instance_cal.epoch[0], \
    bunch_instance_cal.d18[std2_index_on:std2_index_off], "r")
plt.plot(bunch_instance_cal.epoch[std3_index_on:std3_index_off] - bunch_instance_cal.epoch[0], \
    bunch_instance_cal.d18[std3_index_on:std3_index_off], "r")

std1_d18_mean = np.mean(bunch_instance_cal.d18[std1_index_on:std1_index_off])
std1_d18_std = np.std(bunch_instance_cal.d18[std1_index_on:std1_index_off])
std1_dD_mean = np.mean(bunch_instance_cal.dD[std1_index_on:std1_index_off])
std1_dD_std = np.std(bunch_instance_cal.dD[std1_index_on:std1_index_off])
std1_h2o_mean = np.mean(bunch_instance_cal.h2o[std1_index_on:std1_index_off])
std1_h2o_std = np.std(bunch_instance_cal.h2o[std1_index_on:std1_index_off])

std2_d18_mean = np.mean(bunch_instance_cal.d18[std2_index_on:std2_index_off])
std2_d18_std = np.std(bunch_instance_cal.d18[std2_index_on:std2_index_off])
std2_dD_mean = np.mean(bunch_instance_cal.dD[std2_index_on:std2_index_off])
std2_dD_std = np.std(bunch_instance_cal.dD[std2_index_on:std2_index_off])
std2_h2o_mean = np.mean(bunch_instance_cal.h2o[std2_index_on:std2_index_off])
std2_h2o_std = np.std(bunch_instance_cal.h2o[std2_index_on:std2_index_off])

std3_d18_mean = np.mean(bunch_instance_cal.d18[std3_index_on:std3_index_off])
std3_d18_std = np.std(bunch_instance_cal.d18[std3_index_on:std3_index_off])
std3_dD_mean = np.mean(bunch_instance_cal.dD[std3_index_on:std3_index_off])
std3_dD_std = np.std(bunch_instance_cal.dD[std3_index_on:std3_index_off])
std3_h2o_mean = np.mean(bunch_instance_cal.h2o[std3_index_on:std3_index_off])
std3_h2o_std = np.std(bunch_instance_cal.h2o[std3_index_on:std3_index_off])

p_cal_18 = np.polyfit([std1_d18_mean, std3_d18_mean], [std1_d18, std3_d18], 1)
p_cal_D = np.polyfit([std1_dD_mean, std3_dD_mean], [std1_dD, std3_dD], 1)

std2_d18_cal = np.polyval(p_cal_18, std2_d18_mean)
std2_dD_cal = np.polyval(p_cal_D, std2_dD_mean)

json_params_out = copy.deepcopy(json_params)
json_params_out["std1_d18_mean"] = std1_d18_mean
json_params_out["std1_d17_mean"] = "nan"
json_params_out["std1_dD_mean"] = std1_dD_mean

json_params_out["std2_d18_mean"] = std2_d18_mean
json_params_out["std2_d17_mean"] = "nan"
json_params_out["std2_dD_mean"] = std2_dD_mean

json_params_out["std3_d18_mean"] = std3_d18_mean
json_params_out["std3_d17_mean"] = "nan"
json_params_out["std3_dD_mean"] = std3_dD_mean

json_params_out["std1_d18_std"] = std1_d18_std
json_params_out["std1_d17_std"] = "nan"
json_params_out["std1_dD_std"] = std1_dD_std

json_params_out["std2_d18_std"] = std2_d18_std
json_params_out["std2_d17_std"] = "nan"
json_params_out["std2_dD_std"] = std2_dD_std

json_params_out["std3_d18_std"] = std3_d18_std
json_params_out["std3_d17_std"] = "nan"
json_params_out["std3_dD_std"] = std3_dD_std

json_params_out["std2_d18_cal"] = std2_d18_cal
json_params_out["std2_d17_cal"] = "nan"
json_params_out["std2_dD_cal"] = std2_dD_cal

json_params_out["p_cal_18"] = p_cal_18.tolist()
json_params_out["p_cal_17"] = "nan"
json_params_out["p_cal_D"] = p_cal_D.tolist()

json_params_out["h2o_mean"] = np.mean((std1_h2o_mean, std2_h2o_mean, std3_h2o_mean))
json_params_out["h2o_std"] = np.mean((std1_h2o_std, std2_h2o_std, std3_h2o_std))
json_params_out["epoch_time_start"] = epoch_1

json_out_filepath = os.path.splitext(log_filepath)[0] + ".json"
f = open(json_out_filepath, "w")
json.dump(json_params_out, f)
f.close()


time_started = time.strftime("%d/%m/%Y %H:%M:%S", time.gmtime(epoch_1))
report_string = "Time started: %s\n" %time_started
report_string = report_string + 40*"-" + "\nPulse Duration (min): %i\n" %json_params_out["step_duration"]
report_string = report_string + "pct_on: %i" %json_params_out["pct_on"]
report_string = report_string + "\npct_off: %i\n" %json_params_out["pct_off"]
report_string += 40*"-"
report_string = report_string + "\nStandards Used:\n1:"
report_string = report_string + " %0.4f, %0.4f, %0.4f" %(json_params_out["std1_d17"],\
    json_params_out["std1_d18"], json_params_out["std1_dD"])
std1_Dxs = json_params_out["std1_dD"] - 8*json_params_out["std1_d18"]
std1_17xs = 1e6*(np.log(json_params_out["std1_d17"]*1e-3+1) - \
    0.528*np.log(json_params_out["std1_d18"]*1e-3+1))
report_string = report_string + ", %0.4f, %0.2f" %(std1_Dxs, std1_17xs)

report_string = report_string + "\n2:"
report_string = report_string + " %0.4f, %0.4f, %0.4f" %(json_params_out["std2_d17"],\
    json_params_out["std2_d18"], json_params_out["std2_dD"])
std2_Dxs = json_params_out["std2_dD"] - 8*json_params_out["std2_d18"]
std2_17xs = 1e6*(np.log(json_params_out["std2_d17"]*1e-3+1) - \
    0.528*np.log(json_params_out["std2_d18"]*1e-3+1))
report_string = report_string + ", %0.4f, %0.2f" %(std2_Dxs, std2_17xs)

report_string = report_string + "\n3:"
report_string = report_string + " %0.4f, %0.4f, %0.4f" %(json_params_out["std3_d17"],\
    json_params_out["std3_d18"], json_params_out["std3_dD"])
std3_Dxs = json_params_out["std3_dD"] - 8*json_params_out["std3_d18"]
std3_17xs = 1e6*(np.log(json_params_out["std3_d17"]*1e-3+1) - \
    0.528*np.log(json_params_out["std3_d18"]*1e-3+1))
report_string = report_string + ", %0.4f, %0.2f" %(std3_Dxs, std3_17xs) 

report_string = report_string + "\n" + 40*"-" + "\nWater concentration:\n[H2O]_mean: %0.1f" \
%(json_params_out["h2o_mean"])
report_string = report_string + "\n[H2O]_std: %0.1f\n" %(json_params_out["h2o_std"])
report_string = report_string + 40*"-" + "\n"   

# report_string = report_string + "d17 stats\n" + "standard_1_std: %0.2f\n" %json_params_out["std1_d17_std"]
# report_string = report_string + "standard_2_std: %0.2f\n" %json_params_out["std2_d17_std"]
# report_string = report_string + "standard_3_std: %0.2f\n" %json_params_out["std3_d17_std"]
# report_string = report_string + "slope: %0.4f" %(json_params_out["p_cal_17"][0]) + "\n"
# report_string = report_string + "intercept: %0.4f" %(json_params_out["p_cal_17"][1]) + "\n"
# report_string = report_string + "std2_check: %0.4f" %(json_params_out["std2_d17_cal"]) + "\n"
# report_string = report_string + "std2_offset: %0.4f" %(json_params_out["std2_d17"] - json_params_out["std2_d17_cal"]) + "\n" + 40*"-" + "\n"

report_string = report_string + "d18 stats\n" + "standard_1_std: %0.2f\n" %json_params_out["std1_d18_std"]
report_string = report_string + "standard_2_std: %0.2f\n" %json_params_out["std2_d18_std"]
report_string = report_string + "standard_3_std: %0.2f\n" %json_params_out["std3_d18_std"]
report_string = report_string + "slope: %0.4f" %(json_params_out["p_cal_18"][0]) + "\n"
report_string = report_string + "intercept: %0.4f" %(json_params_out["p_cal_18"][1]) + "\n"
report_string = report_string + "std2_check: %0.4f" %(json_params_out["std2_d18_cal"]) + "\n"
report_string = report_string + "std2_offset: %0.4f" %(json_params_out["std2_d18"] - json_params_out["std2_d18_cal"]) + "\n" + 40*"-" + "\n"

report_string = report_string + "dD stats\n" + "standard_1_std: %0.2f\n" %json_params_out["std1_dD_std"]
report_string = report_string + "standard_2_std: %0.2f\n" %json_params_out["std2_dD_std"]
report_string = report_string + "standard_3_std: %0.2f\n" %json_params_out["std3_dD_std"]
report_string = report_string + "slope: %0.4f" %(json_params_out["p_cal_D"][0]) + "\n"
report_string = report_string + "intercept: %0.4f" %(json_params_out["p_cal_D"][1]) + "\n"
report_string = report_string + "std2_check: %0.4f" %(json_params_out["std2_dD_cal"]) + "\n"
report_string = report_string + "std2_offset: %0.4f" %(json_params_out["std2_dD"] - json_params_out["std2_dD_cal"]) + "\n" + 40*"-" + "\n"


print report_string
f = open(os.path.splitext(log_filepath)[0] + ".txt", "w")
f.write(report_string)
f.close()











