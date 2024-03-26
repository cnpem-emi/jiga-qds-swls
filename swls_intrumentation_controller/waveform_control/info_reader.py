# This Python class, `WaveformInfoReader`, provides methods to query and read waveform information
# from a waveform generator.
class WaveformInfoReader:
    def __init__(self, waveform_generator) -> None:
        self.waveform_generator = waveform_generator
        
    def query(self, query_string : str):
        """
        This function takes a query string as input and calls the query method of the waveform_generator
        object with that query string.
        
        @param query_string The `query_string` parameter in the `query` method is a string that
        represents the query you want to send to the waveform generator. This string typically contains
        commands or instructions that the waveform generator will interpret and execute.
        
        @return The `query` method is returning the result of calling the `query` method of the
        `waveform_generator` object with the `query_string` parameter.
        """
        return self.waveform_generator.query(query_string)
    
    def query_info(self):
        """
        The `query_info` function retrieves configuration information by querying specific commands.
        
        @return The `query_info` method is returning a concatenated string of the results of querying three
        commands: '*IDN?', '*OPT?', and '*OPC?'.
        """
        some_config_info = self.query('*IDN?') + self.query('*OPT?') \
                   + self.query('*OPC?')

        return some_config_info
    
    def read_all(self):
        """
        This function reads and returns the current settings of a waveform generator.
        
        @return The `read_all` method is returning the result of querying the instrument for the current
        settings of the waveform format, frequency (Hz), amplitude (V), and offset (V) for source 1
        before any editing of these parameters.
        """
        result = self.query(':SOURce%d:APPLy?' % (1))  #Leitura do formato de onda, frequência(Hz), amplitude(V) e offset(V), atuais, antes da edição desses parâmetros.
        return result
    
    def read_voltage(self):
        """
        The function `read_voltage` queries the voltage value from a specified source in a Python script.
        
        @return The `read_voltage` function is returning the voltage value queried from the instrument
        with the command `:SOURce1:VOLTage?`.
        """
        result = self.query(':SOURce%d:VOLTage?' % (1))  
        return result

    def read_frequency(self):
        """
        The function `read_frequency` queries and returns the frequency of a source in a Python program.
        
        @return The `read_frequency` method is returning the frequency value of the source specified by
        `:SOURce1:FREQuency?`.
        """
        result = self.query(':SOURce%d:FREQuency?' % (1))  
        return result

    def read_offset(self):
        """
        The `read_offset` function reads the voltage offset value for a specific source in Python.
        
        @return The `read_offset` method is returning the voltage offset value for the source 1.
        """
        result = self.query(':SOURce%d:VOLTage:OFFSet?' % (1))  
        return result
    
    def read_phase(self):
        """
        This Python function reads the phase value of a specified source.
        
        @return The `read_phase` method is returning the phase value of the specified source channel
        (channel 1 in this case) by querying the instrument using the command `:SOURce1:PHASe?`. The
        result of this query is then returned by the method.
        """
        result = self.query(':SOURce%d:PHASe?' % (1))  
        return result

    def read_function_type(self):
        """
        This Python function reads the function type of a source.
        
        @return The `read_function_type` function is returning the result of querying the function type
        of the source at index 1.
        """
        result = self.query(':SOURce%d:FUNCtion?' % (1))  
        return result
