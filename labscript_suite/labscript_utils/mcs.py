import matplotlib.pyplot as plt
import matplotlib.animation as animation
from qbstyles import mpl_style
import numpy as np
import time
import os.path
import re


fig = plt.figure(facecolor='#1a1e24',edgecolor='black')
fig.canvas.set_window_title('MCS Readings')
ax1 = fig.add_subplot(1,1,1)
mpl_style(dark=True)
data = []
old_avg_data = []
old_bin_size = 0
old_start_time = -1
old_stop_time = -1
old_plot_averages = -1
ax1.set_facecolor('#1a1e24')
plt.grid(b=True, which='minor', color='#666666', linestyle='-')
avg_path = 'C:/Users/sean/Documents/labscript/labscript_suite/logs/mcs_avg/'
old_list_of_files = os.listdir(avg_path)
numeric_const_pattern = '[-+]? (?: (?: \d* \. \d+ ) | (?: \d+ \.? ) )(?: [Ee] [+-]? \d+ ) ?'
rx = re.compile(numeric_const_pattern, re.VERBOSE)


with open("C:/Users/sean/Documents/labscript/labscript_suite/labconfig/RSPE-052096.ini", "r") as file:
    exp_name = file.readline().rstrip()
    exp_name = file.readline().rstrip().split(' ')[-1]
    connection_table_path = "C:/Users/sean/Documents/labscript/labscript_suite/userlib/labscriptlib/"+exp_name+"/connectiontable.py"


def sample_no_to_time(s):
    return 0.0001+((s-1)/10000)


def cumulative2bin(arr,bin_size):   #bin_size in sample numbers
    prev_bin = 0
    index=bin_size-1
    res = []
    while(index<len(arr)):
        res.append(int(arr[index])-prev_bin)
        prev_bin = int(arr[index])
        index = index+bin_size
    if len(res)>1:
        res[0] = 0
        res[1] = 0
    return res

def floatfromstring(s):
    match = rx.search(s)
    if match is not None:
        return round(float(match.group(0)),1)



def animate(i):
    newdata = [line.rstrip('\n') for line in open('C:/Users/sean/Documents/labscript/labscript_suite/logs/mcs_temp.txt')]
    global data, old_bin_size, old_start_time, old_stop_time, old_plot_averages, old_avg_data, old_list_of_files
    file = open(connection_table_path)
    all_lines = file.readlines()
    start_time = 0
    stop_time = -1
    bin_size = 1
    plot_averages = 1
    list_of_files = os.listdir(avg_path)

    for line in all_lines:
        line=line.strip()
        if line:
            if(line[0:14]=="MCS_start_time"):
                start_time = floatfromstring(line)
            elif(line[0:13]=="MCS_stop_time"):
                stop_time = floatfromstring(line)
            elif(line[0:12]=="MCS_bin_size"):
                bin_size = floatfromstring(line)
            elif(line[0:13]=="plot_averages"):
                plot_averages = int(floatfromstring(line))

    if(bin_size<0.1 or bin_size*10!=int(bin_size*10) or start_time<0 or stop_time<=0 or plot_averages<=0):
        ax1.set_title('ERROR, CHECK YOUR MCS PARAMETERS\nMCS DATA NOT BEING SAVED', color = '#F35654', fontsize=7)
        ax1.plot([])

    elif(newdata != data or bin_size != old_bin_size or old_start_time!=start_time or old_stop_time != stop_time or plot_averages != old_plot_averages or list_of_files != old_list_of_files):
        ax1.clear()
        ax1.set_xlabel('Time (ms)', color = 'white', fontsize=7)
        plt.xlim(start_time*1000, stop_time*1000)
        plt.minorticks_on()
        data = newdata
        old_bin_size=bin_size
        old_start_time = start_time
        old_stop_time = stop_time
        old_plot_averages = plot_averages
        
        if(plot_averages == 1):
            ax1.set_title('Bin size: %.1f ms' %bin_size, color = '#F35654', fontsize=7)
            # ax1.plot(np.linspace(start=0.1,stop=sample_no_to_time(len(newdata)), num = len(newdata)), newdata, marker='.', linewidth=0.6, color='#96ad68')
            bin_array = cumulative2bin(newdata,int(bin_size*10))
            x = np.linspace(start=100+bin_size, stop=100+len(bin_array)*bin_size, num=len(bin_array))
            ax1.plot(x, bin_array, marker='.', linewidth=0.6, color='#96ad68')

        elif(plot_averages>1):
            avg_data=[]
            temp = []
            # list_of_files = os.listdir(avg_path)
            old_list_of_files = list_of_files

            if len(list_of_files) > plot_averages:
                # oldest_file = sorted(os.listdir(avg_path), key=lambda x:os.path.getctime(os.path.join(avg_path,x)))[0]
                # os.remove(avg_path+oldest_file)
                # list_of_files = os.listdir(avg_path)
                ax1.set_title('ERROR, RUN ANOTHER SHOT OR INCREASE plot_averages TO '+str(len(list_of_files)), color = '#F35654', fontsize=7)
                ax1.plot([0])
            elif len(list_of_files)==plot_averages:
                for f in list_of_files:
                    f_path = avg_path+f
                    temp = [line.rstrip('\n') for line in open(f_path)]
                    if len(avg_data)==0: 
                        avg_data = temp
                    else:
                        avg_data = list(map(lambda x,y:int(x)+int(y), temp, avg_data))

                avg_data[:] = [x/plot_averages for x in avg_data]
                avg_bin_data = cumulative2bin(avg_data,int(bin_size*10))
                x = np.linspace(start=100+bin_size, stop=100+len(avg_bin_data)*bin_size, num=len(avg_bin_data))
                ax1.set_title('PLOTTING AVERAGE OF '+str(plot_averages)+' SHOTS\nBin size: %.1f ms' %bin_size, color = '#F35654', fontsize=7)
                ax1.plot(x, avg_bin_data, marker='.', linewidth=0.6, color='#3366cc')

                # save_data = "\n".join(map(str, avg_data))
                # with open('C:/Users/sean/Documents/labscript/labscript_suite/logs/test.txt','w+') as savefile:
                #     savefile.write(save_data)
            else:
                ax1.set_title('PLOTTING AVERAGE OF '+str(plot_averages)+' SHOTS\n'+str(len(list_of_files))+' SHOTS RECEIVED\n'+'Bin size: %.1f ms' %bin_size, color = '#F35654', fontsize=7)
                ax1.plot([0])



ani = animation.FuncAnimation(fig, animate, interval=1000)
plt.show()
