# Parte 2: conjunto complexo e plot simples

if __name__ == "__main__":
	#Bibliotecas
	from metodos_SF import (Main_2, Help_2)
	from sys import argv as arg
	
	L = 1 #Assume 0(plot em linha) ou 1 (plot sem linha)
	if len(arg) == 2:
		Main_2(arg=arg,linha=[True,False][L])
	elif len(arg) == 6 and arg[2].lower() == 'ref':
		Main_2(ref=(float(arg[3]),float(arg[4]),float(arg[5])),arg=arg,linha=[True,False][L])
	else:
		Help_2(arg[0])