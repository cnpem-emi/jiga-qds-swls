import time # std module
import pyvisa as visa # http://github.com/hgrecco/pyvisa - pyvisa for connectivity
#from matplotlib.pyplot import draw, show
import matplotlib.pyplot as plt # http://matplotlib.org/ - for plotting
import numpy as np # http://www.numpy.org
import threading

ddb=0.01 #Delay para facilitar o debug

def close(args=''):
    for thread in threading.enumerate(): 
        print("after thread started:", thread.name)
    print("start closing figure")
    time.sleep(30)
    plt.close('all')

def plot_scope(scaled_time, scaled_wave):
    # plotting
    plt.plot(scaled_time, scaled_wave)
    plt.title('channel 1') #plot label
    plt.xlabel('time (seconds)') # x label
    plt.ylabel('voltage (volts)') # y label
    print("look for plot window...")
    #draw() #Keeps the code running
    #plt.show(block=False)
    for thread in threading.enumerate(): 
        print("before start thread:", thread.name)
    routine=threading.Thread(target=close, args=(1,))
    routine.start()
    plt.show()
    for thread in threading.enumerate(): 
        print("after finished thread:", thread.name)
    

def read_scope():
    print("start read_scope")
    # VISA descriptor to identify the test and measurement device
    # Please update the VISA descriptor from the query result from pyvisa visa_address = 'USB0::1689::261::Q300209::0::INSTR'
    visa_address='USB0::0x0699::0x0378::C010836::0::INSTR'
    rm = visa.ResourceManager()
    scope = rm.open_resource(visa_address)
    print(scope.query('*IDN?'))
    print("OK connect")
    scope.timeout = 10000 # ms
    print("1")
    scope.encoding = 'latin_1'
    print("1")
    scope.read_termination = '\n'
    print("1")
    scope.write_termination = None
    print("1")
    #scope.write('*cls') # clear ESR
    print("1")
    scope.write('header OFF')
    print("finished writting")
    time.sleep(ddb)

    # acquisition
    scope.write('acquire:state OFF') # stop
    print(" try will start")    
    scope.write('acquire:stopafter SEQUENCE;state ON') # single
    time.sleep(ddb*2)
    r = scope.query('*opc?')
    print("finished acquisition")
    time.sleep(ddb)

    # curve configuration
    scope.write('data:encdg SRIBINARY') # signed integer
    scope.write('data:source CH1')
    scope.write('data:start 1')
    acq_record = int(scope.query('horizontal:recordlength?'))
    scope.write('data:stop {}'.format(acq_record))
    scope.write('wfmoutpre:byt_n 1') # 1 byte per sample
    print("finished curve configuration")
    time.sleep(ddb)

    # data query
    bin_wave = scope.query_binary_values('curve?', datatype='b', container=np.array, chunk_size = 1024**2)
    print("finished data query")
    data = ['Brazil', 652090, 'BR', 'BRA']
    print("len(bin_wave):", len(bin_wave))
    """
    with open('scope.csv', 'w', encoding='UTF8') as f:
        writer = csv.writer(f)            
        #writer.writerow(bin_wave)
        writer.writerow(data) 
    """
    time.sleep(ddb)
    
    # retrieve scaling factors
    wfm_record = int(scope.query('wfmoutpre:nr_pt?'))
    pre_trig_record = int(scope.query('wfmoutpre:pt_off?'))
    t_scale = float(scope.query('wfmoutpre:xincr?'))
    t_sub = float(scope.query('wfmoutpre:xzero?')) # sub-sample trigger correction
    v_scale = float(scope.query('wfmoutpre:ymult?')) # volts / level
    v_off = float(scope.query('wfmoutpre:yzero?')) # reference voltage
    v_pos = float(scope.query('wfmoutpre:yoff?')) # reference position (level)
    # disconnect
    scope.close()
    rm.close()
    # create scaled vectors
    # horizontal (time)

    total_time = t_scale * wfm_record
    t_start = (-pre_trig_record * t_scale) + t_sub
    t_stop = t_start + total_time
    scaled_time = np.linspace(t_start, t_stop, num=wfm_record, endpoint=False)
    print("finished retrieve scaling factors")
    time.sleep(ddb)

    # vertical (voltage)
    unscaled_wave = np.array(bin_wave, dtype='double') # data type conversion 
    scaled_wave = (unscaled_wave - v_pos) * v_scale + v_off

    plot_scope(scaled_time, scaled_wave)
    print("finished vertical (voltage)")
    time.sleep(ddb)
     
error=0
while (error<10):
    try:
        print("activate read_scope()")
        read_scope()
        error=0
    except:
        error=error+1
        print("Error in communication with scope number:", error, "(application will close after 10 errors in a row).")
    time.sleep(2)
print("Application finished due to errors in communication with scope")
time.sleep(4)
 
"""
#Remains:
Correct error DC;
correct fail when amplituded changed;
automatic autoscale to avoid signal lost 9already happened due to it;
create function to identify voltage value;
save file to csv
add try execept tp waveform generator script.
"""
#https://www.tek.com/en/documents/application-note/using-raspberry-pi-to-control-your-oscilloscope
