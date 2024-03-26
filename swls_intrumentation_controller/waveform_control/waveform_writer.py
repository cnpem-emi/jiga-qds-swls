
from swls_intrumentation_controller.waveform_control.device_specific_commands import WRITE_COMMANDS, ACCEPTED_FUNCTION_TYPES

class WaveformWriter:
    def __init__(self, waveform_generator) -> None:
        self.waveform_generator = waveform_generator
        
    
    def write(self, waveform_command : str):
        self.waveform_generator.write(waveform_command)

    def change_voltage(self, amplitude : int, channel : int = 1):
        if amplitude < 0:
            raise Exception("Amplitude Must Be Absolute")
        #Amplitude (in V).
        self.write(WRITE_COMMANDS.change_voltage.format(channel=channel, voltage=amplitude)) 

    def change_frequency_hz(self, freq_hz, channel : int = 1):
        #Frequency (in Hz).
        self.write(WRITE_COMMANDS.change_frequency.format(channel=channel, frequency=freq_hz))
        
    def change_offset(self, offset_value, channel : int = 1):
        #Offset (em V.) Lembrar que o valor médio da senoide e o valor DC são: 2*OFFSet.
        self.write(WRITE_COMMANDS.change_offset.format(channel=channel, offset=offset_value))
    
    def change_phase(self, phase_value, channel : int = 1):
        if phase_value not in range(360):
            raise Exception("Phase Value not in Range 0 to 360")
        self.write(WRITE_COMMANDS.change_phase.format(channel=channel, phase=phase_value)) #Value from 0º to 360º.

    def change_function_type(self, function_type : str, channel : int = 1):
        if function_type not in ACCEPTED_FUNCTION_TYPES.keys():
            raise Exception(f"Function Type {function_type}  
                            not accepted by the waveform generator")

        self.write(WRITE_COMMANDS.change_function_type.format(channel = channel,
                    function_type=ACCEPTED_FUNCTION_TYPES[function_type])) 
