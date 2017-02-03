from Tkinter import *
import ttk
import tkFileDialog
import tkMessageBox
import time
import string
import serial


root = Tk()
root.title("CFA Picarro Log v0.1")

current_position = StringVar()
current_position.set("#POS")
sequence_list_str = StringVar()
sequence_list_str.set("")
sequence_time = StringVar()
sequence_time.set("2 min")

acquisition_on = IntVar()
top_bag = StringVar()
dir_to_open = StringVar()
cfa_on = IntVar()
cfa_on.set(0)




################################################################
#Acquisition Methods
################################################################
def start_file():
    if acquisition_on.get() == 1:
        tkMessageBox.showwarning(title = "Warning..", \
            message = "Acquisition is running. \nStop acquisition to start a new file..")
        pass
        return
    dir_to_open.set(tkFileDialog.asksaveasfilename())
    try:
        f = open(dir_to_open.get(), "w")
        f.write("Date\tUTC_Time\tEpoch_Time\tCFA_ON\tTop_Bag\tValve_Pos\n")
        f.close
        start_acquisition_button.config(state = NORMAL)
    except:
        pass

    return None

def start_acquisition():
    acquisition_on.set(1)
    start_acquisition_button.config(state = DISABLED)
    stop_acquisition_button.config(state = NORMAL)
    start_file_button.config(state = DISABLED)
    write_to_file()
    return

def write_to_file():
    if int(acquisition_on.get()) == 1:
        if string.strip(top_bag.get()) == '':
            top_bag.set("0")
        f = open(dir_to_open.get(), "a")
        gm_time_string = time.strftime("%H:%M:%S", time.gmtime())
        date_string = time.strftime("%Y%m%d", time.gmtime())
        string_out = "%s\t%s\t%0.3f\t%i\t%s\t%s\n" \
        %(date_string, gm_time_string, time.time(), int(cfa_on.get()), top_bag.get(), current_position.get())
        print(string_out),
        f.write(string_out)
        f.close()

        root.after(1000, write_to_file)
    elif int(acquisition_on.get()) == 0:
        print("acquisition off")
        pass
    return

def stop_acquisition():
    acquisition_on.set(0)
    start_acquisition_button.config(state = NORMAL)
    stop_acquisition_button.config(state = DISABLED)
    start_file_button.config(state = NORMAL)
    print("stopping acquisition..")

    return None

def update_label_colors():
    if acquisition_on.get() == 1:
        label_acquisition_on.config(bg = "#009933", text = "ACQ_ON")
    elif acquisition_on.get() == 0:
        label_acquisition_on.config(bg = "#CC0000", text = "ACQ_OFF")

    if cfa_on.get() == 1:
        label_cfa_on.config(bg = "#009933", text = "CFA_ON")
    elif cfa_on.get() == 0:
        label_cfa_on.config(bg = "#CC0000", text = "CFA_OFF")

    root.after(610, update_label_colors)

    return


########################################################
#Valve Control methods
########################################################
def step_up():
    """
    Steps up valve position
    """
    ser.open()
    int_cp = int(current_position.get())
    if int_cp<6:   
        new_position = int_cp + 1
    elif int_cp == 6:
        new_position = 1

    msg = "GO0" + str(new_position) + "\r\n"
    print msg
    ser.write(msg)
    ser.close()
    current_position.set(new_position)
    check_cp()

    return

def step_down():
    """
    Steps down valve position
    """
    ser.open()
    int_cp = int(current_position.get())
    if int_cp>1:   
        new_position = int_cp - 1
    elif int_cp == 1:
        new_position = 6
    msg = "GO0" + str(new_position) + "\r\n"
    print msg
    ser.write(msg)
    ser.close()
    current_position.set(new_position)
    check_cp()

    return

def check_cp():
    """
    Checks current position
    """
    ser.open()
    ser.flushInput()
    ser.write("CP\r\n")
    a = ser.readline()
    print(a)
    condition = (len(a) == 17) | ("Position" in a)
    if condition:
        print("conditiontrue")
        cp = a[-2]
        print cp
        current_position.set(cp)
    ser.close()
    # root.after(100, check_cp)
    return


def run_sequence():
    """
    Runs sequence
    """

    seq = string.split(sequence_list_str.get(), ",")
    possible_positions = ["1", "2", "3", "4", "5", "6"]
    for j in seq:
        if string.strip(j) not in possible_positions:
            tkMessageBox.showerror(message = "Wrong valve positions in sequence string.\nPositions 1-6 separated by comma", \
                title = "Warning", icon = 'error')
            return

    seq_time = int(string.split(sequence_time.get())[0])
    seq_time_secs = seq_time*60

    

    return



addr_serial = '/dev/cu.PL2303-00001014'
print("Opening serial port at %s" %addr_serial)
try:
    ser = serial.Serial(addr_serial, 9600, timeout = 2)
    print("Checking bi-directional com")
    ser.write("VR\r\n")
    valve_firmware = ser.readline()
    print(valve_firmware)
    print("\n\n")
    print("Switching to port 1...........")
    ser.write("GO01\r\n")
    print(ser.readline())
    ser.close()
    check_cp()

except:
    print("Could not open serial port at %s" %addr_serial)
    


leftframe = Frame(root, borderwidth = 3, relief = "raised", pady = 10, padx = 20)
leftframe.pack(fill = BOTH, side = LEFT, expand = 1)


step_up_button = Button(leftframe, text = "step_up", font = ("Helvetica bold", 15), padx = 10, pady = 20, command = step_up)
step_up_button.grid(row = 0, column = 0)

step_down_button = Button(leftframe, text = "step_down", font = ("Helvetica bold", 15), padx = 10, pady = 20, command = step_down)
step_down_button.grid(row = 0, column = 2, sticky = W)

label_current_position = Label(leftframe, textvariable = current_position, font = ("Helvetica bold", 30), bg = "#CC0000", padx = 10, pady = 20)
label_current_position.grid(row = 2, column = 1, rowspan = 2, padx = 20, pady = 20, sticky = W+E+S+N)



start_file_button = Button(leftframe, text = "Start_File", padx = 2, pady = 6, command = start_file)
start_file_button.grid(column = 0, row = 4, sticky = (W+E))

start_acquisition_button = Button(leftframe, text = "Start_Acq", pady = 6, padx = 10, command = start_acquisition, state = DISABLED)
start_acquisition_button.grid(column = 1, row = 4, sticky = (W), padx = 10)

stop_acquisition_button = Button(leftframe, text = "Stop_Acq", pady = 6, padx = 10, command = stop_acquisition, state = DISABLED)
stop_acquisition_button.grid(column = 1, row = 4, sticky = (E), padx = 10)


Label(leftframe, text = "TopBag:").grid(column = 0, row = 5, sticky = (E))

bag_entry = Entry(leftframe, width = 9, textvariable = top_bag)
bag_entry.grid(column = 1, row = 5, sticky = (W), padx = 9)


cfa_checkbutton = Checkbutton(leftframe, text = "CFA ON/OFF", variable = cfa_on)
cfa_checkbutton.grid(column = 0, row = 6, sticky = W)

label_cfa_on = Label(leftframe, text = "CFA_OFF", font = ("Helvetica bold", 30), bg = "#CC0000", padx = 10, pady = 10)
label_cfa_on.grid(row = 6, column = 1, padx = 20, pady = 20, sticky = W+E+S+N)

label_acquisition_on = Label(leftframe, text = "ACQ_OFF", font = ("Helvetica bold", 30), bg = "#CC0000", padx = 10, pady = 10)
label_acquisition_on.grid(row = 6, column = 2, padx = 20, pady = 20, sticky = W+E+S+N)

label_saving_to = Label(leftframe, text = "Saving to: ")
label_saving_to.grid(row = 7, column = 0)
label_saving_to_1 = Label(leftframe, textvariable = dir_to_open)
label_saving_to_1.grid(row = 7, column = 1, sticky = W)



rightframe = Frame(root, pady = 10, padx = 20, bd = 3)
rightframe.pack(side = LEFT, fill = BOTH, expand = 1)

label_seq_panel = Label(rightframe, text = "Sequence Panel", font = ("Helvetica, bold italic", 20))
label_seq_panel.grid(row = 0, column = 0, sticky = W+E, pady = 20, columnspan = 2)


sequence_label = Label(rightframe, text = "sequence config", padx = 6, pady = 6)
sequence_label.grid(row = 1, column = 0, pady = 10)

sequence_entry = Entry(rightframe, textvariable = sequence_list_str)
sequence_entry.grid(row = 1, column = 1, pady = 10, sticky = W)

sequence_time_label = Label(rightframe, text = "Choose seq. time:")
sequence_time_label.grid(row = 2, column = 0, pady = 10)

sequence_times = ("2 min", "5 min", "10 min", "15 min", "20 min")
sequence_time_combo = OptionMenu(rightframe, sequence_time, "2 min", "5 min", "10 min", "15 min", "20 min", "30 min", "60 min", "90 min")
sequence_time_combo.grid(row = 2, column = 1, pady = 10, sticky = W)

sequence_go_button = Button(rightframe, text = "Go!", padx = 20, pady = 10, command = run_sequence)
sequence_go_button.grid(row = 4, column = 0, columnspan = 2, pady = 10)



update_label_colors()




root.mainloop()
