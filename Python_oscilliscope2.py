import time
import pyvisa as visa # http://github.com/hgrecco/pyvisa - pyvisa for connectivity
import matplotlib.pyplot as plt # http://matplotlib.org/ - for plotting
import numpy as np # http://www.numpy.org
import threading
import datetime
import timeit


#Defining variables:

#General variables:
#thr=10 #Threshold value (values above threshold will generate exceptions and will have their moment of transition from below to above threshold captured).
ddb=0.01 #Delay to facilitate debugging.
cycles=0 #Numbers of cycles of the code.

#Scale variables:
autoset=True #True: uses autoscale. False: doesn't use autoscale (if autoset is False when scope is initialized).
#autoset=False #True: uses autoscale. False: doesn't uses autoscale (if autoset is False when scope is initialized).
autoset2=False #Activates autoscale in each measure cicle of the loop (not only in the start).
std_wfm = 100000 #standard wfm_record.
std_trigger = 0 #standard triger record.
std_tscale = 3.2e-08 # standard t_scale.
std_tsub =  -0.002 #standard sub-sample trigger correction.
std_vscale =  0.04 #standard volts / level. 0.0.4 2 e 3 V; 0.08 4 e 5 V. CAUTION: if the scale is wrong the scope can mismeasure.
std_voff =  0 #standard reference voltage
std_vpos = 0 #standard reference position (level).
standard_scale=(std_wfm, std_trigger, std_tscale, std_tsub, std_vscale, std_voff, std_vpos) 

#Trigger variables:
threshold = 2.32 #In Volts. WILL BE ROUNDED FOR THE CLOSEST MULTIPLE OF 40 mV. Voltage level that activates trigger (example: 0.08 = 80mV). 
trigger_type = 'EDGe' #Defines the type of the trigger: EDGe, LOGic, PULSe, BUS or VIDeo.
trigger_channel = 'CH1' #Defines the channel of the trigger (example: CH1).
trigger_coupling = 'DC' #Defines the coupling of the trigger: DC, High Frequency(HF) Reject, Low Frequency(LF) Reject or Noise Reject.
trigger_slope = 'RISE' #Defines the trigger slope (rising or falling edge).
trigger_holdoff = 20.000E-9 #In seconds. Period during which the trigger will not generate a trigger event.

#Plot variables:
y_min=-3.2 #Minimal value of y-axis in plot.
y_max=3.2 #Maximal value of y-axis in plot.

    

def read_scope():
    
    def close():
        #for thread in threading.enumerate(): 
        #print("after thread started:", thread.name)
        print("start closing figure")
        time.sleep(30)        
        plt.close('all')
        
    def date_seconds():
        hour=datetime.datetime.now().isoformat(timespec='hours') #Date with hour.
        minutes=datetime.datetime.now().minute
        seconds=datetime.datetime.now().second
        dt=str(hour)+'-'+str(minutes)+'-'+str(seconds) #Date with seconds, but without ":" character so that it can be used to save images.
        print("h m s:", hour, minutes, seconds)
        print("dt:", dt)
        return dt
        
    def plot_scope(scaled_time, scaled_wave, trigger_level_read):        
        print("start plot_scope")
        min_scale_time=min(scaled_time)
        max_scale_time=max(scaled_time)
        #plt.plot(scaled_time, scaled_wave)        
        print("trigger_level_read:", trigger_level_read)
        fig, ax = plt.subplots()
        ax.plot(scaled_time, scaled_wave, label='Oscilloscope Measure(V)', color='b')        
        ax.hlines(y=float(trigger_level_read), xmin=min_scale_time, xmax=max_scale_time, label='Threshold Voltage(V)', color='r', linestyles='--')        
        plt.legend(loc="lower right")
        plt.title('Voltage of trigger activation') #plot title
        plt.xlabel('Time (Seconds)') # x label
        plt.ylabel('Voltage (Volts)') # y label          
        plt.ylim(y_min, y_max) #Delimitates y-axis        
        dt=date_seconds() #Date until seconds.
        plt.savefig('data\scopetrigger'+dt+'.png') #Saving the figure with the date, so that old plots aren't  overwritten. 
        plt.show()
        #time.sleep(10)  
        #routine=threading.Thread(target=close, daemon=True) #if not daemon, Python might raise exceptions.
        #routine.start()
        
        

    def horizontal_wave(wfm_record, pre_trig_record, t_scale, t_sub, v_scale, v_off, v_pos):
        print("start horiziontal wave")
        #Horizontal (time):
        total_time = t_scale * wfm_record
        t_start = (-pre_trig_record * t_scale) + t_sub
        t_stop = t_start + total_time
        scaled_time = np.linspace(t_start, t_stop, num=wfm_record, endpoint=False)
        print("finished retrieve scaling factors horizontal (time)")
        time.sleep(ddb)
        return scaled_time
        
    def vertical_wave(bin_wave, wfm_record, pre_trig_record, t_scale, t_sub, v_scale, v_off, v_pos):
        #Vertical (voltage):
        
        unscaled_wave = np.array(bin_wave, dtype='double') # data type conversion 
        scaled_wave = (unscaled_wave - v_pos) * v_scale + v_off
        print("finished retrieve scaling factors horizontal vertical (voltage)")
        time.sleep(ddb)
        return scaled_wave

    def generate_wave(bin_wave, trigger_level_read):
        (wfm_record, pre_trig_record, t_scale, t_sub, v_scale, v_off, v_pos)=readscale()
        #Creating scaled vectors:
        scaled_time=horizontal_wave(wfm_record, pre_trig_record, t_scale, t_sub, v_scale, v_off, v_pos)
        scaled_wave=vertical_wave(bin_wave, wfm_record, pre_trig_record, t_scale, t_sub, v_scale, v_off, v_pos)
        plot_scope(scaled_time, scaled_wave, trigger_level_read)#Function plot
        
    def writescale(wfm_record, pre_trig_record, t_scale, t_sub, v_scale, v_off, v_pos):
        print("writescale")
        scope.write('WFMINPRE:NR_PT'+str(wfm_record))
        scope.write('WFMInpre:PT_Off'+str(pre_trig_record))
        scope.write('WFMInpre:XINcr'+str(t_scale))
        scope.write('wfminpre:xzero'+str(t_sub))
        scope.write('wfminpre:ymult'+str(v_scale))
        scope.write('wfminpre:yzero'+str(v_off))
        scope.write('wfminpre:yoff'+str(v_pos))

    def readscale():
        #Retrieving scale factors.
        wfm_record = int(scope.query('wfmoutpre:nr_pt?'))
        pre_trig_record = int(scope.query('wfmoutpre:pt_off?'))
        t_scale = float(scope.query('wfmoutpre:xincr?'))
        t_sub = float(scope.query('wfmoutpre:xzero?')) # sub-sample trigger correction.
        v_scale = float(scope.query('wfmoutpre:ymult?')) # volts / level.
        v_off = float(scope.query('wfmoutpre:yzero?')) # reference voltage.
        v_pos = float(scope.query('wfmoutpre:yoff?')) # reference position (level).
        print("wfm_record, pre_trig_record, t_scale, t_sub, v_scale, v_off, v_pos:", wfm_record, pre_trig_record, t_scale, t_sub, v_scale, v_off, v_pos)
        return (wfm_record, pre_trig_record, t_scale, t_sub, v_scale, v_off, v_pos)
        
    def autoscale():
        #Function to activate autoset/autoscale.        
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

    def single_trigger():
        counter=0
        trigger_state=scope.query('TRIGger:STATE?')
        while(trigger_state!='READY'):
            scope.write('FPANEL:PRESS SINGleseq') #This command equals to pressing the single button.
            time.sleep(5)
            trigger_state=scope.query('TRIGger:STATE?')
            counter=counter+1
            if counter==5:
                trigger_state='READY' #Break loop to avoid infinites tries of pressing the single button.
                print("Error activating single in scope") 
        if (trigger_state=='SAV') or (trigger_state=='TRIG'): #Case that trigger is already activated.
            print("Trigger already activated at sttart of application")
            instant_image()

    def read_trigger():
        trigger_state_read = scope.query('TRIGger:STATE?') #Returns the state of the trigger: ARMED, AUTO, READY, SAVE or TRIGGER.
        trigger_type_read = scope.query("TRIGger:A:TYPe?") #Returns the type of the trigger: EDGe, LOGic, PULSe, BUS or VIDeo.
        trigger_source_read = scope.query('TRIGGER:A:EDGE:SOURCE?') #Returns the channel of the trigger (example: CH1).
        trigger_coupling_read = scope.query('TRIGGER:A:EDGE:COUPLING?') #Returns the coupling of the trigger: DC, High Frequency(HF) Reject, Low Frequency(LF) Reject or Noise Reject.
        trigger_slope_read = scope.query('TRIGGER:A:EDGE:SLOPE?') #Returns the trigger slope (rising or falling edge).
        trigger_level_read = scope.query('TRIGger:A:LEVel?') #Returns the voltage level that activates trigger in Volts (example: 0.04 = 40mV)
        trigger_holdoff_read = scope.query('TRIGGER:A:HOLDOFF:TIME?') #Returns the holdoff time (period during which the trigger will not generate a trigger event, in seconds).
        print("trigger state:",trigger_state_read)
        print("trigger type:",trigger_type_read)
        print("trigger channel:",trigger_source_read)
        print("trigger dc?:",trigger_coupling_read)
        print("trigger border:",trigger_slope_read)  
        print("trigger voltage (V):",trigger_level_read)
        print("trigger holdoff time (s):",trigger_holdoff_read)
        return(trigger_state_read, trigger_type_read, trigger_source_read, trigger_coupling_read, trigger_slope_read, trigger_level_read, trigger_holdoff_read)

    def write_trigger():
        print("start trigger writing")
        scope.write('TRIGger:A:TYPe '+trigger_type) #Defines the type of the trigger: EDGe, LOGic, PULSe, BUS or VIDeo.
        scope.write('TRIGGER:A:EDGE:SOURCE '+trigger_channel) #Defines the channel of the trigger (example: CH1).
        scope.write('TRIGGER:A:EDGE:COUPLING '+trigger_coupling) #Defines the coupling of the trigger: DC, High Frequency(HF) Reject, Low Frequency(LF) Reject or Noise Reject.
        scope.write('TRIGGER:A:EDGE:SLOPE '+trigger_slope) #Defines the trigger slope (rising or falling edge).
        scope.write('TRIGGER:A:LEVEL '+str(threshold)) #Defines the voltage level that activates trigger in Volts (example: 0.04 = 40mV)
        scope.write('TRIGGER:A:HOLDOFF:TIME '+str(trigger_holdoff)) #Defines the holdoff time (period during which the trigger will not generate a trigger event, in seconds).
        single_trigger()
        print("single")


    def csv(bin_wave):
        """
        data = ['Brazil', 652090, 'BR', 'BRA']
        with open('scope.csv', 'w', encoding='UTF8') as f:
        writer = csv.writer(f)            
        #writer.writerow(bin_wave)
        writer.writerow(data) 
        """
        pass

    def acquire_curve():
        bin_wave=scope.query_binary_values('curve?', datatype='b', container=np.array, chunk_size = 1024**2)       
        (wfm_record, pre_trig_record, t_scale, t_sub, v_scale, v_off, v_pos)=readscale()
        max_wave=(max(bin_wave) - v_pos) * v_scale + v_off
        print("len(bin_wave):", len(bin_wave))
        print("max_wave:", max_wave)        
        time.sleep(5) #small delays makes communication too fast, which will cause troubles in restart communication when scripts restarts.     
        return bin_wave

        
    def setting_acquisition():
        #Start acquisition  
        max_wave=0
        #scope.write('acquire:state OFF') # stop         
        #scope.write('acquire:stopafter SEQUENCE;state ON') # single
        #Curve configuration:
        scope.write('data:encdg SRIBINARY') # signed integer
        scope.write('data:source CH1')
        scope.write('data:start 1')
        acq_record = int(scope.query('horizontal:recordlength?'))
        scope.write('data:stop {}'.format(acq_record))
        scope.write('wfmoutpre:byt_n 1') # 1 byte per sample
        print("finished curve configuration")
        time.sleep(ddb)              
        bin_wave=acquire_curve()        
        return bin_wave


    def disconnect_scope():
        # disconnect
        scope.close()
        rm.close()
        #print("power:", scope.query('PSC?'))

    def curve_data(trigger_level_read):
        print("curve_data")
        bin_wave=setting_acquisition()
        csv(bin_wave)
        generate_wave(bin_wave, trigger_level_read)
    

    def check_wave(trigger_level_read):        
        if autoset2:
            print("start ats")
            (wfm_record, pre_trig_record, t_scale, t_sub, v_scale, v_off, v_pos)=autoscale()
            
        #while (scope.query('TRIGger:STATE?')!='TRIG'):
        while (scope.query('TRIGger:STATE?')=='READY'): 
            print("trigger state:", scope.query('TRIGger:STATE?'))           
            time.sleep(1)
        
        print("trigger state:", scope.query('TRIGger:STATE?'))       
        time.sleep(ddb)                
        curve_data(trigger_level_read)

    def instant_image():
        #Function to generate a function quickly.
        (trigger_state_read, trigger_type_read, trigger_source_read, trigger_coupling_read, trigger_slope_read, trigger_level_read, trigger_holdoff_read)=read_trigger()
        curve_data(trigger_level_read)
    

    def initialization():
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
        return rm, scope

    def autoset_config():
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

        return (wfm_record, pre_trig_record, t_scale, t_sub, v_scale, v_off, v_pos)

    def cycle_trigger():
        #Function that start checks for scopes triggering.
        (wfm_record, pre_trig_record, t_scale, t_sub, v_scale, v_off, v_pos)=autoset_config()
        (trigger_state_read, trigger_type_read, trigger_source_read, trigger_coupling_read, trigger_slope_read, trigger_level_read, trigger_holdoff_read)=read_trigger()
        write_trigger()
        (trigger_state_read, trigger_type_read, trigger_source_read, trigger_coupling_read, trigger_slope_read, trigger_level_read, trigger_holdoff_read)=read_trigger()
        time.sleep(1)
        check_wave(trigger_level_read)
    
    #init()
    (rm, scope)=initialization()    
    while True:
        cycle_trigger()
        time.sleep(0.5)


#MAIN    
error=0
while (error<10):
    try:
        print("activate read_scope()")
        read_scope()
        error=0
    except:
        time.sleep(10)
        error=error+1
        print("Error in communication with scope number:", error, "(application will close after 10 errors in a row).")
    time.sleep(2)
disconnect_scope()
print("Application finished due to errors in communication with scope")
time.sleep(4)
 
"""
#Remains:
Function of automate printing
Define offset impedance of WAVEFORM GENERATOR (NOT SCOPE!!).
Control the place wheter trigger is placed in acquisition (to be not only in the final of the 10000 points).
Mode of read data via trigger and continuous.
Trigger catches EVERY DC transitions AND NEVER AFTER THEN.
Erros that sometimes occurs in plots.
Check to see if it´s possible to use a defined scale when autoscale was used after initialization in a way that the scales are applieds and doesn´t generates error after several runs.
Real time measure.
Correct problem to restart communication after deafult scale.
Correct voltage with different scale
correct fail when amplituded changed;
automatic autoscale to avoid signal lost 9already happened due to it;
create function to identify voltage value;
save file to csv
add try execept tp waveform generator script.
"""
#https://www.tek.com/en/documents/application-note/using-raspberry-pi-to-control-your-oscilloscope

#unit test python
#vunit
#github action


