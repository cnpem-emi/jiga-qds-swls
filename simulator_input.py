#Import das bibliotecas
import time
import random
#import numpy as np

#Definição de variáveis:
ts=10 #Tempo de amostragem (ns)
txtts=ts #Editável para que se mostre um outro valor para o tempo de amostragem no .txt (representado em outra unidade).
uts="ns" #Unidade do tempo de amostragem no .txt (no Python é sempre em ns).
#Observação: valores de tensão serão usados somente até 3ª casa depois da vírgula.
va0=0 #Valor mínimo da tensão analógica antes de ser convertida. Em V.
va1=5 #Valor máximo da tensão analógica antes de ser convertida. Em V.
vat=2.5 #Valor esperado da tensão analógica a ser aceita. Em V.
vai=2 #Margem de erro (para + e para -) para que a tensão analógica seja aceita. Em V.
bit=8 #Número de bits usado na discretização.
nin=1 #Número de entradas a se realizar a medida.

#Variáveis definidas úteis na simulação:
na=10 #Número de amostras por input
out=0
str0='      0    ' #String com 0 do reset e número de espaços.

#Variáveis geradas:
va0=round(va0, 3)
va1=round(va1, 3)
vat=round(vat, 3)
vai=round(vai, 3)
valow=vat-vai #Valor mínimo da tensão analógica a ser aceita. Em V. 
vahigh=vat+vai #Valor máximo da tensão analógica a ser aceita. Em V.

#Conversões AD. Tensões (até 3ª casa depois da vírgula):
def ad(va):
    vd0=bin(int(((va-va0)/(va1-va0))*(pow(2,bit)-1)))
    vd=vd0.lstrip('0b') #Remove a string '0b' inicial do python.
    vd=vd.zfill(bit) #Acressenta 0s a esquerda correspondentes ao número de bits.
    print("binário:", vd)
    return vd

vlow=ad(valow) #Maximo aceito em binário.
vhigh=ad(vahigh) #Mínimo aceito em binário.

#lines = ["#time	rst	vdet	vlow	vhig	out "] #Linhas iniciais do .txt.

    
for i in range (0, nin):
    outstring="out"+str(i) #string com o valor do número da saída
    #ov.append(out)
    if i>=1:
        #lines.append("\n\n\n#time	rst	vdet	vlow	vhig	"+outstring)
        pass #Fazer parte para mais de uma input, caso necessário. 
    for a in range(0, na):
        varan=random.randint(0,(vahigh*1000))/1000 #Tensão aleatória analógica.
        #varan=a
        print("V analógico:", varan)
        vran=ad(varan) #Tensão aleatória em binários.
        print("V digital", vran)
        if (vlow<vran<vhigh):
            out=1 #Tensão dentro dos limites.
        else:
            out=0 #Tensão fora dos limites.
        
        line=["\n"+str(ts)+str0+str(vran)+' '+str(vlow)+' '+str(vhigh)+' '+str(out)]#strings que irão formar uma linha no txt
       
        with open('input.txt', 'a') as f:
            f.write('\n'.join(line)) #Escrita de uma linha extra no txt


