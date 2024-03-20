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

#Leituras de paramêtros:
read_all = wg.query(':SOURce%d:APPLy?' % (1))  #Leitura do formato de onda, frequência(Hz), amplitude(V) e offset(V), atuais, antes da edição desses parâmetros.
print(read_all)
#Leitura de cada um dos paramêtros, atuais, antes de suas edições:
volt = wg.query(':SOURce%d:VOLTage?' % (1))  
print(volt)
freq = wg.query(':SOURce%d:FREQuency?' % (1))  
print(freq)
offset = wg.query(':SOURce%d:VOLTage:OFFSet?' % (1))  
print(offset)
phase = wg.query(':SOURce%d:PHASe?' % (1))  
print(phase)
func = wg.query(':SOURce%d:FUNCtion?' % (1))  
print(func)

wg.write(':OUTPut%d %d' % (1, 1)) #Liga a geração de onda no canal 1.

#Edição de parâmetros do gerador:
wg.write(':SOURce%d:VOLTage %G' % (1, 2)) #Amplitude (em V).
wg.write(':SOURce%d:FREQuency %G' % (1, 1000)) #Frequência (em Hz).
wg.write(':SOURce%d:VOLTage:OFFSet %G' % (1, 0)) #Offset (em V.) Lembrar que o valor médio da senoide e o valor DC são: 2*OFFSet.
wg.write(':SOURce%d:PHASe %s' % (1, 58))#Valor de 0º a 360º.
wg.write(':SOURce%d:FUNCtion %s' % (1, 'SINusoid')) #Formatos aceitos: 'SINusoid' 'SQUare' 'TRIangle' 'RAMP' 'PULSe' 'NOIS' 'PRBS'  'DC'.

#wg.write(':OUTPut%d %d' % (1, 0)) #Desliga a geração de onda no canal 1.

read_all_new = wg.query(':SOURce%d:APPLy?' % (1)) #Leitura do formato de onda, frequência(Hz), amplitude(V) e offset(V), após a edição desses parâmetros.
print(read_all_new)
#Leitura de cada um dos paramêtros, após a edição desses parâmetros:
volt_new = wg.query(':SOURce%d:VOLTage?' % (1))  
print(volt_new)
freq_new = wg.query(':SOURce%d:FREQuency?' % (1))  
print(freq_new)
offset_new = wg.query(':SOURce%d:VOLTage:OFFSet?' % (1))  
print(offset_new)
phase_new = wg.query(':SOURce%d:PHASe?' % (1))  
print(phase_new)
func_new = wg.query(':SOURce%d:FUNCtion?' % (1))  
print(func_new)

#Finalização:
wg.close()
rm.close()

