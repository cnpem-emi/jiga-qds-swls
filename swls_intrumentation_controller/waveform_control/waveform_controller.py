import pyvisa as visa
from swls_intrumentation_controller.waveform_control.info_reader import WaveformInfoReader
from swls_intrumentation_controller.waveform_control.waveform_writer import WaveformWriter

USB_RESOURCE_STR = 'USB0::0x0957::0x2507::MY57100781::0::INSTR'

class WaveformController(WaveformInfoReader, WaveformWriter):
    def __init__(self): 
        # Some initial Config
        resource_manager = visa.ResourceManager()
        self.waveform_generator = resource_manager.open_resource(USB_RESOURCE_STR) 
        WaveformInfoReader.__init__(self, self.waveform_generator)
        WaveformWriter.__init__(self, self.waveform_generator)

   
        