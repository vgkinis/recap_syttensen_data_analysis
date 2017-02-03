import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import os
import os.path
import time
import copy

class Standard():

    def __init__(self, name = "-22", d18 = -22, dD = -160., d17 = -11.):
        """

        """
        self.name = name
        self.d18 = d18
        self.dD = dD
        self.d17 = d17

        return


    def read(self, bunch_instance, index_i, index_f):
        """

        """
        section_instance = bunch_instance.pick(index_i, index_f)
        self.d18_meas = np.mean(section_instance.d18)
        self.dD_meas = np.mean(section_instance.dD)
        self.d17_meas = np.mean(section_instance.d17)
        self.std_d18 = np.std(section_instance.d18)
        self.std_dD = np.std(section_instance.dD)
        self.std_d17 = np.std(section_instance.d17)

        return

    def __str__(self):

        try:
            message = "Standard Instance\nName: " + self.name + \
                "\nd18_smow: " + str(self.d18) + "\ndD_smow: " + \
                    str(np.round(self.dD, 2)) + "\nd17_smow: " + str(np.round(self.d17, 3)) \
                    + " \nMeasured Values:\nd18: " + \
                        str(np.round(self.d18_meas, 2)) + " +- " + \
                            str(np.round(self.std_d18, 2)) + "\ndD: " + \
                                str(np.round(self.dD_meas, 2)) + " +- " +\
                                    str(np.round(self.std_dD, 2)) + "\n" + \
                                    "\nd17: " + str(np.round(self.d17_meas, 3)) + " +- " +\
                                        str(np.round(self.std_d17, 3)) + "\n"
        except:
            message = "Standard Instance\nName: " + self.name + \
                "\nd18_smow: " + str(np.round(self.d18, 2)) + "\ndD_smow: " + \
                    str(np.round(self.dD, 2)) + "\nd17_smow: " + \
                    str(np.round(self.d17, 3)) + "\nMeasured Values: Not Set\n"

        return message


class Calibration():

    def __init__(self, std1, std2):
        """

        """
        self.std1 = std1
        self.std2 = std2

        return


    def calc(self):
        """

        """
        slope_18 = (self.std2.d18 - self.std1.d18)/(self.std2.d18_meas - \
            self.std1.d18_meas)
        intercept_18 = self.std1.d18 - slope_18*self.std1.d18_meas
        p_d18 = [slope_18, intercept_18]

        slope_D = (self.std2.dD - self.std1.dD)/(self.std2.dD_meas - \
            self.std1.dD_meas)
        intercept_D = self.std1.dD - slope_D*self.std1.dD_meas
        p_dD = [slope_D, intercept_D]

        slope_17 = (self.std2.d17 - self.std1.d17)/(self.std2.d17_meas - \
        self.std1.d17_meas)
        intercept_17 = self.std1.d17 - slope_17*self.std1.d17_meas
        p_d17 = [slope_17, intercept_17]

        self.p_d18 = p_d18
        self.p_dD = p_dD
        self.p_d17 = p_d17

        return p_d18, p_dD, p_d17



    def __str__(self):
        try:
            message = "Calibration with standards: " + str(self.std1) + str(self.std2) + \
                "p_d18: " + str(np.round(self.p_d18, 3)) + "\np_dD: " + \
                    str(np.round(self.p_dD, 3)) + "\np_d17: " + \
                    str(np.round(self.p_d17, 3)) +"\n"
        except:
            message = "Calibration instance with standards: " + \
                str(self.std1) + str(self.std2) + "\n"

        return message
