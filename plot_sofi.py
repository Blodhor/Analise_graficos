# Parte 3: conjunto de dados complexo e plot sofisticado

if __name__ == "__main__":
	#Bibliotecas
	from metodos_SF import (Main_3, Help_2)
	from sys import argv as arg
	
	if len(arg) == 2:
		Main_3(arg=arg)
	elif len(arg) == 6 and arg[2].lower() == 'ref':
		Main_3(ref=(float(arg[3]),float(arg[4]),float(arg[5])),arg=arg)
	else:
		Help_2(arg[0])