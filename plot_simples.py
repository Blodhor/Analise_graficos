# Parte 1: conjunto de dados simples

if __name__ == "__main__":
	# Bibliotecas
	from metodos_SF import (Main_1, Help)
	from sys import argv as arg
	
	if len(arg) == 3:
		Main_1(arg=arg)
	else:
		Help(arg[0])