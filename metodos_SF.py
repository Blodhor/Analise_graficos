# Bibliotecas necessarias para uso do matplot
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import (inset_axes, InsetPosition, mark_inset)
	
#Leitura de arquivo simples de duas colunas 
def XY(nome='arquivo.dat'):
	xname = 'X'
	yname = 'Y'
	f=open(nome)
	t = f.readlines() # copiando todo texto
	f.close()
	x = []
	y = []
	for i in t: # leitura do arquivo
		# i == uma linha do arquivo
		data = i.split() 
		if i != '' and i[0] == '#':
			xname = data[0][1:]
			yname = data[1]
		elif len(data) == 2:
			x.append( float(data[0]) )
			y.append( float(data[1]) )
		
	return [(xname,yname), x, y]

#Calculo de distancia entre dois pontos
def dist(atm1=(1,-2,3), atm2=(0,5,-6)):
	x1, y1, z1 = atm1
	x2, y2, z2 = atm2
	r = ((x1-x2)**2 + (y1-y2)**2 + (z1-z2)**2)**0.5
	return round(r,2)

#Leitura de um arquivo PDB com varios modelos de ligante em sequencia
#Extracao da posicao das cabonilas dos ligantes e criacao de uma lista
# de elementos (modelos,(afinidade,distancia))
def list_AEvsR(ser_hydroxyl=(-1.062,-12.604,-11.209), file = 'all_Nice_dock.pdb'):
	# leitura do arquivo
	f = open(file,'r')
	temp = f.readlines()
	f.close()

	models     = [] # id do modelo
	affinities = [] # energia de ligacao
	rcarbs     = [] # distancia desejada
	hetatm     = [] # coordenadas
	
	for i in range(len(temp)):
		if 'model' not in temp[i].lower():
			if 'REMARK VINA RESULT:' in temp[i]:
				affinities.append(float(temp[i][20:].split()[0]))
			elif 'HETATM' in temp[i]:
				#coordenadas atomicas
				hetatm.append(temp[i])
			elif 'CONECT' in temp[i]:
				#descricao das ligacoes
				temp_c = temp[i].split()
				if len(temp_c) == 5:
					# 1 atomo ligado a 3 outros 
					main_atm = int(temp_c[1])
					# procurar na lista de coordenadas
					main_info = hetatm[main_atm - 1].split()
					# atomo ligado 1
					alt1 = int(temp_c[2])
					alt1_info = hetatm[alt1 - 1].split()
					# atomo ligado 2
					alt2 = int(temp_c[3])
					alt2_info = hetatm[alt2 - 1].split()
					# atomo ligado 3
					alt3 = int(temp_c[4])
					alt3_info = hetatm[alt3 - 1].split()
					c_count = 0
					o_count = 0
					# contagem de Carbonos e Oxigenios ligados
					for t in [alt1_info[2],alt2_info[2],alt3_info[2]]:
						if t == 'C':
							c_count += 1
						elif t == 'O':
							o_count += 1
					
					if main_info[2] == 'C' and c_count == 1 and o_count == 2:
						# encontramos a carbonila
						main_xyz = (float(main_info[5]),float(main_info[6]),float(main_info[7]))
						# salvar distancia
						rcarbs.append(dist(atm1=ser_hydroxyl,atm2=main_xyz))
		elif 'model' in temp[i].lower() and 'model' in temp[i+1].lower():
			# salvando a id do modelo # id superior se refere ao todo, e a inferior aos arquivos individuais
			hetatm = []
			models.append(temp[i]) 

	# formatacao da saida		
	label_out = []
	exc = 0
	h = 0
	#afinidade eh referente ao modelo
	for i in range(len(rcarbs)):
		exc +=1
		label_out.append( (models[h],(affinities[h],rcarbs[i])) )
		if exc == 2:
			# existem 2 carbonilas por modelo
			exc = 0
			h += 1

	return label_out

# Metodos swap, partition e SortZerothTupple pertencem a 
# ordenacao otima do quicksort
def swap(t=[(0,'1'),(-6,'2')], ith = 0, jth = 1):
	'''Inverte as posições i e j da lista t'''
	if ith != jth:
		temp   = t[ith]
		t[ith] = t[jth]
		t[jth] = temp

def partition(t=[(0,'1'),(-6,'2')], begin= 0, end = 1):
	#valor escolhido para ordenar 
	pivot = t[end]
	rpos  = begin -1
	for i in range(begin,end):
		if t[i][0] < pivot[0]:
			rpos += 1
			swap(t,rpos,i)
	swap(t,rpos+1,end) 
	''' 
	Ex:
	lista = 8 2 3 7 4 6
	pivot = 6
	r     = -1

	it 0:
		8 < 6 = False
		8 2 3 7 4 6
	it 1:
		2<6 = True
		r = 0
		swap(0,1)
		2 8 3 7 4 6
	it 2:
		3<6= True
		r=1
		swap(1,2)
		2 3 8 7 4 6
	it 3:
		7<6=False
		2 3 8 7 4 6
	it 4:
		4<6= True
		r=2
		swap(2,4)
		2 3 4 7 8 6
	it 5:
		6<6 =False
		loop end
		swap(r+1=3,5)
		2 3 4 6 8 7
		retorna posicao do pivot
	'''
	return 	rpos+1

def SortZerothTupple(t=[(0,'1'),(-6,'2')], begin= 0, end = 1):
	# condicao de parada do loop infinito
	# = lista possui mais de 1 elemento
	if begin < end:
		# ajuste correto do pivot
		pivot = partition(t=t,begin=begin,end=end)
		# ordenacao da lista menor que o pivot
		a = SortZerothTupple(t=t,begin=begin,end=pivot-1)
		# ordenacao da lista maior que o pivot
		b = SortZerothTupple(t=t,begin=pivot+1,end=end)

#Imprime os cinco primeiros elementos de um lista
def print_top5(lista=[],par="r_hc"):
	top = []
	if len(lista) < 5:
		top = lista
	else:
		top = lista[0:5]
	print('\n5 menores "%s" encontrados:\n'%par)
	for i in top:
		print(i)

#Separa um conjunto de dados em duas regioes e cria listas para 
#distancia e distancia+afinidade
def filt_simples(dados=[('modelo i',('ae', 'r'))],bw_limit=-5.5):

	# modelos bons
	r_g      = [] # X
	ae_g     = [] # Y
	# modelos ruins
	r_w      = [] # X
	ae_w     = [] # Y
	# lista para ordenacao em 'r'
	rVmodel    = []
	# lista para ordenacao em somas 'r'+'ae'
	rPaeVmodel = []

	for i in dados:
		#lista : ('r','modelo','ae'), ...
		rVmodel.append( (i[1][1], i[0], "Ae = %f"%i[1][0]) )
		#lista: ('ae'+'r','modelo','ae;r',('ae','r')),...
		rPaeVmodel.append( (i[1][0]+i[1][1], i[0], "Ae = %f; r_hc = %f"%(i[1][0],i[1][1]), i[1]) )
		if i[1][0] <= bw_limit:
			# se 'ae'< limite, elemento pertence
			# a lista de bons
			ae_g.append(i[1][0])
			r_g.append(i[1][1])
		else:
			# elemento pertence a lista de ruins
			ae_w.append(i[1][0])
			r_w.append(i[1][1])
	return 	(r_g,ae_g,r_w,ae_w,rVmodel,rPaeVmodel)

#Plot em linha ou em pontos de um conjunto de dados
#Apresenta o grafico pela interface do matplot
def Plot_simples(linha=True, X = [], Y = [], Xaxis = "Frame",
 Yaxis = "reference", name = "Título",dpi=100, font=10):
	
	fig = plt.figure(dpi=dpi)
	if linha:
		plt.plot(X,Y)
	else:
		plt.plot(X,Y,'o')
	plt.title(name, fontsize=font)
	plt.ylabel(Yaxis, fontsize=font)
	plt.xlabel(Xaxis, fontsize=font)
	plt.grid(True)
	plt.show()

#Plot sofisticado com duas cores e grafico interior
#Salva o grafico diretamente sem usar a interface
def plot_AEvsR(dpi=300,file_name='Figure_3.jpeg',inset=True,
pointsize=4,Xg=[],Yg=[],g_color='royalblue',Xw=[],Yw=[],
w_color='deepskyblue',Xg_ins=[],Yg_ins=[],mark_color='black',
titulo ="",eixoy="Vina score (kcal/mol)",eixox="$r_{hc}\,(\AA)$"):

	# outras cores:: 'mediumseagreen', 'deepskyblue'
	fig, ax1 = plt.subplots(dpi=dpi)
	ax1.plot(Xg,Yg,'o',color=g_color,ms=pointsize)
	ax1.plot(Xw,Yw,'o',color=w_color,ms=pointsize)
	ax1.set_xlabel(eixox,fontsize=12)
	ax1.set_ylabel(eixoy,fontsize=12)
	#ax1.set_xlim(2.5,17)
	ax1.set_ylim(-6.0,-1.8)
	if inset:
		# Criando um conjunto de eixos interiores
		ax2 = plt.axes([0,0,1,1])
		# Definindo a posicao do grafico interno no externo
		ip = InsetPosition(ax1, [0.5,0.525,0.5,0.475]) 
		# arg: figura externa; [posicao X , Y do interno;
		#  largura%, altura% respectivas ao grafico externo]
		ax2.set_axes_locator(ip)
		# Marcando de onde veio o interior
		# zorder grande faz o interior ser desenhado por cima do externo
		mark_inset(ax1, ax2, loc1=2, loc2=4, fc="none", ec=mark_color,zorder=5)
		ax2.plot(Xg_ins,Yg_ins,'o',color=g_color,ms=pointsize)

	plt.savefig(file_name,bbox_inches='tight')
	#plt.show()

#Mensagens de ajuda
def Help(arg ='arquivo.py'):
	print("Modo de uso:\n $ pythonCompilerV3+ %s FILE.dat PLOT_NOME\n"%arg)

def Help_2(arg = ['AvR_DockingPlot.py', '-h']):
	print("Modo de uso:\n(1): $ pythonCompilerV3+ %s PDBFILE.pdb\n"%arg[0])
	print("(2): $ pythonCompilerV3+ %s PDBFILE.pdb ref Xcoord Ycoord Zcoord"%arg[0])

#Codigo principal do Ex1
def Main_1(arg = ['Plot.py', 'FILE.dat', 'nome']):
	#	0	   1		2
	dados = XY(nome=arg[1])
	#     = [(xname,yname), X, Y]	
	Plot_simples(X=dados[1],Y=dados[2],
	Xaxis=dados[0][0],Yaxis=dados[0][1],
	name=arg[2],dpi=100,font=10)

#Codigo principal do Ex2
def Main_2(ref=(-1.062,-12.604,-11.209),arg=['Plot.py', 'FILE.dat'],linha=True):
	
	dados = list_AEvsR(ser_hydroxyl=ref,file=arg[1])
	#    == [('model i', (float('ae'), float('r')) ),...]
	x = []
	y = []
	for i in dados:
		x.append( i[1][1] )
		y.append( i[1][0] )
	Plot_simples(linha=linha,X=x,Y=y,Xaxis="Distância",
	Yaxis="Afinidade",name="Exemplo 2",
	dpi=100,font=10)

#Codigo principal do Ex3
def Main_3(ref=(-1.062,-12.604,-11.209), arg = ['Plot.py', 'PDBFILE.pdb'], inset_factor=10):
	# ref := hidroxila da serina

	# lista de modelos 
	# == [('modelo i', (float('ae'), float('r')) ), ...]
	data = list_AEvsR(ser_hydroxyl=ref,file=arg[1])
	bw_limit=-5.5
	# gerando listas de modelos 'bons' e 'ruins'
	# e criando listas de 'r' e de 'r+ae'
	r_g,ae_g,r_w,ae_w,rVmodel,rPaeVmodel = filt_simples(dados=data,bw_limit=bw_limit)
	
	#plot com filtragem simples
	plot_AEvsR(Xg=r_g,Yg=ae_g,Xw=r_w,Yw=ae_w,
	dpi=100,file_name='Ex3_cor.jpeg',inset=False)

	# ordenando listas de 'r' e de 'r+ae'
	SortZerothTupple(t=rVmodel,begin=0,end=len(rVmodel)-1)
	SortZerothTupple(t=rPaeVmodel,begin=0,end=len(rPaeVmodel)-1)

	# selecionando dados do grafico interior	
	Xg_ins = []
	Yg_ins = []
	for i in range(int(len(rPaeVmodel)/inset_factor)):
		if rPaeVmodel[i][3][0] <= bw_limit:
			# menos de 10% dos melhores modelos de 'r+ae'
			Yg_ins.append(rPaeVmodel[i][3][0])
			Xg_ins.append(rPaeVmodel[i][3][1])

	# Impressao dos melhores 5 de cada lista
	print_top5(rVmodel,"$r_{hc}$")
	print_top5(rPaeVmodel,"$r_{hc}+ae$")
	# gerando grafico com inset	
	plot_AEvsR(dpi=100,file_name='Ex3_inset.jpeg',inset=True,
	Xg=r_g,Yg=ae_g,Xw=r_w,Yw=ae_w,Xg_ins=Xg_ins,Yg_ins=Yg_ins)
