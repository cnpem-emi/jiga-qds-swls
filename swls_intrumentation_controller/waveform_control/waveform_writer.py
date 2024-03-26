class WaveformWriter:
    def __init__(self, waveform_generator) -> None:
        self.waveform_generator = waveform_generator
        self.ACCEPTED_FUNCTION_TYPES = ['SINusoid', 'SQUare', 'TRIangle', 
                                        'RAMP', 'PULSe', 'NOIS', 'PRBS', 'DC']
    
    def write(self, waveform_command : str):
        self.waveform_generator.write(waveform_command)

    def change_voltage(self, amplitude : int):
        if amplitude < 0:
            raise Exception("Amplitude Must Be Absolute")
        
        self.write(':SOURce%d:VOLTage %G' % (1, amplitude)) #Amplitude (in V).

    def change_frequency_hz(self, freq_hz):
        self.write(':SOURce%d:FREQuency %G' % (1, freq_hz)) #Frequency (in Hz).
        
    def change_offset(self, offset_value):
        #Offset (em V.) Lembrar que o valor médio da senoide e o valor DC são: 2*OFFSet.
        self.write(':SOURce%d:VOLTage:OFFSet %G' % (1, offset_value))
    
    def change_phase(self, phase_value):
        if phase_value not in range(360):
            raise Exception("Phase Value not in Range 0 to 360")
        self.write(':SOURce%d:PHASe %s' % (1, phase_value)) #Valor de 0º a 360º.

    def change_function_type(self, function_type : str):
        if function_type not in self.ACCEPTED_FUNCTION_TYPES:
            raise Exception(f"Function Type {function_type}  
                            not accepted by the waveform generator")

        self.write(':SOURce%d:FUNCtion %s' % (1,function_type)) 
