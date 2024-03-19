# NOTE: the default pyvisa import works well for Python 3.6+
# if you are working with python version lower than 3.6, use 'import visa' instead of import pyvisa as visa

import pyvisa as visa
import time
visa.log_to_screen() #Facilita debug.

#Inicialização:
rm = visa.ResourceManager()
wg = rm.open_resource('USB0::0x0957::0x2507::MY57100781::0::INSTR') 

#Exemplo de algumas configurações básicas:
string = wg.query('*IDN?')
a = wg.query('*OPT?')
b = wg.query('*OPC?')
print(string, a, b)

#Edição de parâmetros do gerador:
wg.write(':SOURce%d:VOLTage %G' % (1, 0.2))
wg.write(':SOURce%d:FREQuency %G' % (1, 1000))
wg.write(':SOURce%d:VOLTage:OFFSet %G' % (1, 0.14)) #Lembrar que o valor médio da senoide é: 2*OFFSet.
wg.write(':SOURce%d:FUNCtion %s' % (1, 'SINusoid'))
wg.write(':SOURce%d:PHASe %s' % (1, 0))

#Finalização:
wg.close()
rm.close()

