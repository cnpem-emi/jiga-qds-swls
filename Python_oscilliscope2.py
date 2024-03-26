import time # std module
import pyvisa as visa # http://github.com/hgrecco/pyvisa - pyvisa for connectivity
import matplotlib.pyplot as plt # http://matplotlib.org/ - for plotting
import numpy as np # http://www.numpy.org
import threading
import datetime
import timeit

#Definindo variáveis:
thr=0.9 #Threshold value (values above threshold will generate exceptions and will have their moment of transition from below to above threshold captured).
ddb=0.01 #Delay to facilitate debugging.
autoset=True #True: uses autoscale. False: doesn't use autoscale (if autoset is False when scope is initialized).
#autoset=False #True: uses autoscale. False: doesn't uses autoscale (if autoset is False when scope is initialized).

autoset2=False #Ativa o autoscale a cada ciclo de medida.
std_wfm = 125000 #standard wfm_record
std_trigger = 0 #standard triger record
std_tscale = 3.2e-08 # standard t_scale
std_tsub =  -0.002 #standard sub-sample trigger correction
std_vscale =  0.04 #standard volts / level. 0.04 2 e 3 V; 0.08 4 e 5 V. CAUTION: if the scale is wrong the scope can mismeasure.
std_voff =  0 #standard reference voltage
std_vpos = 0 #standard reference position (level)
standard_scale=(std_wfm, std_trigger, std_tscale, std_tsub, std_vscale, std_voff, std_vpos) 

#Definindo parâmetros inicias da escala do osciloscópio:



#unit test python
#vunit
#github action


    
  
def read_scope():
    
    def close(args=''):
        #for thread in threading.enumerate(): 
        #print("after thread started:", thread.name)
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
        routine=threading.Thread(target=close, args=(1,))
        routine.start()
        plt.show()
        
    #wfm_record, pre_trig_record, t_scale, t_sub, v_scale, v_off, v_pos: 125000 0 3.2e-08 -0.002 0.08 0.0 0.0
    def writescale(wfm_record, pre_trig_record, t_scale, t_sub, v_scale, v_off, v_pos):
        print("writescale")
        scope.write('WFMINPRE:NR_PT'+str(wfm_record))
        print("first write succeeded")
        scope.write('WFMInpre:PT_Off'+str(pre_trig_record))
        scope.write('WFMInpre:XINcr'+str(t_scale))
        scope.write('wfminpre:xzero'+str(t_sub))
        scope.write('wfminpre:ymult'+str(v_scale))
        print('wfminpre:ymult'+str(v_scale))
        scope.write('wfminpre:yzero'+str(v_off))
        scope.write('wfminpre:yoff'+str(v_pos))

    def readscale():
        # retrieve scaling factors
        wfm_record = int(scope.query('wfmoutpre:nr_pt?'))
        pre_trig_record = int(scope.query('wfmoutpre:pt_off?'))
        t_scale = float(scope.query('wfmoutpre:xincr?'))
        t_sub = float(scope.query('wfmoutpre:xzero?')) # sub-sample trigger correction
        v_scale = float(scope.query('wfmoutpre:ymult?')) # volts / level
        v_off = float(scope.query('wfmoutpre:yzero?')) # reference voltage
        v_pos = float(scope.query('wfmoutpre:yoff?')) # reference position (level)
        print("wfm_record, pre_trig_record, t_scale, t_sub, v_scale, v_off, v_pos:", wfm_record, pre_trig_record, t_scale, t_sub, v_scale, v_off, v_pos)
        return (wfm_record, pre_trig_record, t_scale, t_sub, v_scale, v_off, v_pos)
        
    def autoscale():
        #Function to activate autoset/autoscale.
        #print("start autoset")
        scope.write('AUTOSET EXECute') #autoscale.  
        print("autoset")
        time.sleep(5)
        (wfm_record, pre_trig_record, t_scale, t_sub, v_scale, v_off, v_pos)=readscale()
        return(wfm_record, pre_trig_record, t_scale, t_sub, v_scale, v_off, v_pos)

    def end_autoscale():
        #Function to activate autoset/autoscale.
        print("stop autoset") 
        print("autoset undone")
        time.sleep(5)
        
    
    
    # VISA descriptor to identify the test and measurement device
    # Please update the VISA descriptor from the query result from pyvisa visa_address = 'USB0::1689::261::Q300209::0::INSTR'
    visa_address='USB0::0x0699::0x0378::C010837::0::INSTR'
    rm = visa.ResourceManager()
    scope = rm.open_resource(visa_address)
    print(scope.query('*IDN?'))   
    scope.timeout = 10000 # ms
    scope.encoding = 'latin_1'    
    scope.read_termination = '\n'   
    scope.write_termination = None    
    scope.write('*cls') # clear ESR   
    scope.write('header OFF')
    print("finished writting")
    time.sleep(ddb)    
    if autoset:
        print("start ats")
        (wfm_record, pre_trig_record, t_scale, t_sub, v_scale, v_off, v_pos)=autoscale()
    else:
        print("standard definition of scale")
        end_autoscale()
        (wfm_record, pre_trig_record, t_scale, t_sub, v_scale, v_off, v_pos)=standard_scale
        writescale(wfm_record, pre_trig_record, t_scale, t_sub, v_scale, v_off, v_pos)
        time.sleep(2)
        (wfm_record, pre_trig_record, t_scale, t_sub, v_scale, v_off, v_pos)=readscale()
        
    
    max_wave=0
    # data query
    while (max_wave<thr):
        
        if autoset2:
            print("start ats")
            (wfm_record, pre_trig_record, t_scale, t_sub, v_scale, v_off, v_pos)=autoscale()
        
        # acquisition
        scope.write('acquire:state OFF') # stop 
        print("try will start")
        scope.write('acquire:stopafter SEQUENCE;state ON') # single
        try:
            r = scope.query('*opc?')
        except:
            print("except")
            scope.write('AUTOSET EXECute') #autoscale.
            time.sleep(ddb*1000)
        
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
        start_time = datetime.datetime.now()
        bin_wave=scope.query_binary_values('curve?', datatype='b', container=np.array, chunk_size = 1024**2)
        end_time = datetime.datetime.now()
        max_wave=(max(bin_wave) - v_pos) * v_scale + v_off
        print(wfm_record, pre_trig_record, t_scale, t_sub, v_scale, v_off, v_pos)
        print("finished data query")    
        start_time2 = datetime.datetime.now()
        print("len(bin_wave):", len(bin_wave))
        end_time2 = datetime.datetime.now()
        print("max_wave:", max_wave)        
        time.sleep(10) #small delays makes communication too fast, which will cause troubles in restart communication when scripts restarts.   
        execution_time = end_time - start_time
        execution_time2 = end_time2 - start_time2
        print("Time taken to execute the commands:", execution_time, "second command", execution_time2)
        
    """
    data = ['Brazil', 652090, 'BR', 'BRA']
    with open('scope.csv', 'w', encoding='UTF8') as f:
        writer = csv.writer(f)            
        #writer.writerow(bin_wave)
        writer.writerow(data) 
    """
    time.sleep(ddb)

    
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
    print("finished vertical (voltage)")
    time.sleep(ddb)

    #Plot da função:
    plot_scope(scaled_time, scaled_wave)
   
     
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
Check to see if it´s possible to use a defined scale when autoscale was used after initialization in a way that the scales are applieds and doesn´t generates error after several runs.
Real time measure.
Correct problem to restart communication after deafult scale.
Correct voltage with different scale
Correct error DC;
correct fail when amplituded changed;
automatic autoscale to avoid signal lost 9already happened due to it;
create function to identify voltage value;
save file to csv
add try execept tp waveform generator script.
"""
#https://www.tek.com/en/documents/application-note/using-raspberry-pi-to-control-your-oscilloscope
