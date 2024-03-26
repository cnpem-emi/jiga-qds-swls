from types import SimpleNamespace

ACCEPTED_FUNCTION_TYPES = { 'sine' : 'SINusoid',
                            'square': 'SQUare',
                            'triangle': 'TRIangle', 
                            'ramp': 'RAMP',
                            'pulse': 'PULSe',
                            'noise': 'NOIS',
                            'random-bits': 'PRBS',
                            'step': 'DC'}

WRITE_COMMANDS = SimpleNamespace(**{
    'change_voltage': ':SOURce{channel}:VOLTage {voltage}',
    'change_frequency': ':SOURce{channel}:FREQuency {frequency}', 
    'change_offset': ':SOURce{channel}:VOLTage:OFFSet {voltage}',
    'change_phase': ':SOURce{channel}:PHASe {phase}', 
    'change_function_type': ':SOURce{channel}:FUNCtion {function_type}'
})

QUERY_COMMANDS = SimpleNamespace(**{

})