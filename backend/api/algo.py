import numpy as np

class Knapsack:

	def __init__(self, capacity=0, profits=[], weights=[]):
		""" Knapsack class for solving a knapsack problem.

		Attributi:
			profitti (elenco di variabili non negative): profitti deglie elementi 
			pesi (elenco di variabili positive): pesi degli elementi
			nb_items (int): numero di elementi
			capacità (float): capacità dello zaino
		"""
		self.profits = profits
		self.weights = weights
		self.nb_items = len(profits)
		self.capacity = capacity
		self.order_profits = [0]*len(profits)
		self.order_weights = [0]*len(profits)

	def _find_original_position(self,pick:list):
		original_pick = []
		for i in range(0,self.nb_items):
			#per ongi elemento non ordinato
			weight = self.weights[i]
			profit = self.profits[i]
			index = 0

			#cerco indice di stessi pesi stessi valori
			for j in range(0,self.nb_items):
				if (weight == self.order_weights[j] and profit == self.order_profits[j]):
					index = j
					break
				
			original_pick.append(pick[index])

		return original_pick
	
	def sort_by_ratio(self):
		"""
		Funzione che organizza i valori in base al loro rapporto profitto/peso
		"""
		group = []
		for i in range(self.nb_items):
			group.append((int(self.profits[i])/int(self.weights[i]),int(self.profits[i]),int(self.weights[i])))
		group.sort(key=lambda x:x[0],reverse=True)
		
		# print(group)
		for i in range(self.nb_items):
			self.order_profits[i] = group[i][1]
			self.order_weights[i] = group[i][2]

	def dynamic_knapsack_matrix(self):

		num_element = len(self.profits)

		#definiamo un array di zeri su cui lavorare, grande qaundo la capacità dello zaino
		#corrisponde al primo ciclo di definizionde dello pseudo codice
		z = np.zeros((num_element,self.capacity+1)) 
		a = np.zeros((num_element,self.capacity+1))
		
		#per ogni elemento che possiamo aggiungere nello zaino
		for j in range(0,num_element):
			#vado da 0 al minimo della capacità e del peso dell'elemento -1
			#in pratica finche lo zaino non è abbastanza grande non metto solo 0
			for d in range(0,self.weights[j]):
				#quindi assegno il valore precendete finche non ci sta nello zaino
				z[j,d] = z[j-1,d]
				#da quando il peso inizia ad avere posto nello zaino
			for d in range(self.weights[j],self.capacity+1):
				if(z[j-1,d- self.weights[j]] + self.profits[j] > z[j-1,d]):
					z[j,d] = z[j-1,d- self.weights[j]] + self.profits[j]
					a[j,d] = 1
				else:
					z[j,d] = z[j-1,d]
					a[j,d] = 0

		z_star = z[num_element-1,self.capacity]
		print("Massimo ottenibile: ",z_star)
		print("Matrice dei valori: \n",z)
		print("Matrice di pick: \n",a)
		return {"z_star":z_star,"z":z.tolist(),"a":a.tolist()}
	
	def _pick_matrix_for_iterative_dp2(self, c: int, n_items: int, memory: list):
		"""
		Funzione che ritorna la lista di elementi scelti per ogni iterazione della funzione dp2
		"""
		X = [0]*n_items
		index = c
		i = n_items-1
		while (i>=0):
			if i == 0:
				if (memory[i][index] != 0):
					X[i] = 1
			else:
				if (memory[i-1][index] != memory[i][index]):
					X[i] = 1
					index = index - self.order_weights[i]
			i = i-1
		return X

	def dynamic_knapsack_single_list(self):

		memory = []

		b = 2
		X = 1

		#definisco l'array di partenza
		z = [0]*(self.capacity+1)

		#per ogni possibile elemento nello zaino
		for j in range(0,self.nb_items):
			#parto dalla capacità e vado fino al peso dell'elemento
			for d in range(self.capacity,self.order_weights[j]-1,-1):
				#se il peso dell'elemento è minore della capacità quindi ce posto per lui nello zaino
				if z[d-self.order_weights[j]] + self.order_profits[j] > z[d]:
					#se il valore dello zaino meno il peso dell'elemento più il valore dell'elemento è maggiore dello zaino
					z[d] = z[d-self.order_weights[j]] + self.order_profits[j]
			#aggiungo la lista di valori alla memoria cosi da passarla al front end
			memory.append(z.copy())

		z_star = z[self.capacity]
		a = self._pick_matrix_for_iterative_dp2(self.capacity, self.nb_items, memory)
		# print("Massimo ottenibile: ",z_star)
		# print("Matrice dei valori: \n",z)
		return {"z_star":z_star,"memory":memory, "pick": self._find_original_position(a)}

	"""
	Input:
	v = il peso che attualmente abbiamo nello zaino
	P = la lista di profitti aggiornata
	X = la lista di elementi aggiornata
	w_m = il peso considerato nello stato attuale
	p_m = il profitto considerato nello stato attuale
	"""
	def rec1(self,v:int,P:list,X:list,w_m:int,p_m:int,b:int):
		# in pratica per ogni peso succesivo al primo
		if v < self.capacity:
				u = v
				#ricalcoliamo v per lo stato corrente
				v = min(v+w_m,self.capacity)
				#partedo dalla posizione subito successiva a quella del pese precedente
				#fino alla posizione v che considera la posizione aggiornata con il nuovo peso
				for c_cap in range(u+1,v+1):
					#Aggiorno il profitto
					P[c_cap] = P[u]
					#Aggiorno la lista di elementi
					X[c_cap] = X[u]	
		#passo ricorsivo che corrisponde allas formula di ricorsine di bellman
		for c_cap in range(v,w_m,-1):
			#se il profitto è minore del profitto precedente più il profitto dell'elemento
			if P[c_cap] < P[c_cap-w_m] + p_m:
				#aggiorno il profitto
				P[c_cap] = P[c_cap-w_m] + p_m
				#aggiorno la lista di elementi
				X[c_cap] = X[c_cap-w_m] + b
				#X = X + b

		b = 2*b
		return v,P,X,b
		

	"""
	Input
	del numero di elementi -> che è nb_items
	del peso massimo -> che è la capacità
	della lista di profitti -> che è self.order_profits
	della lista di pesi -> che è self.order_weights

	Output
	il valore massimo ottenibile -> che è z_star
	la lista di elementi scelti -> che è X_cap
	"""
	def dp1(self):

		memory = []

		#inizializzo la lista di elementi scelti
		X = [0]*(self.capacity+1)
		#inizializzo la lista di profitti
		P = [0]*(self.capacity+1)
		b = 2
		

		# #inizio mettendo 0 fino a che il primo elemento non possa stare nello zaino
		# for c_cap in range(0,self.order_weights[0]):
		# 	#metto a 0 il profitto 
		# 	P[c_cap] = 0
		# 	#metto a 0 la lista di elementi scelti
		# 	X[c_cap] = 0

		#sarebbe il peso corrente che porta lo zaino
		v = self.order_weights[0]
		#setto il profitto del primo elemento da quando ci sta nello zaino
		P[v] = self.order_profits[0]
		#setto a 1 la lista di elementi scelti
		X[v] = 1

		#aggiungo la lista di valori alla memoria cosi da passarla al front end
		memory.append(P.copy())

		#per ogni elemento che posso mettere nello zaino
		for m in range(1,self.nb_items):
			#richiamo la funzione ricorsiva
			v,P,X,b = self.rec1(v,P,X,self.order_weights[m],self.order_profits[m],b)

			#aggiungo la lista di valori alla memoria cosi da passarla al front end
			memory.append(P.copy())

		if (sum(self.order_weights) < self.capacity):
			z = P[sum(self.order_weights)]
			list_bin = list(bin(X[sum(self.order_weights)]))[2:]
		else:
			z = P[self.capacity]
			list_bin = list(bin(X[self.capacity]))[2:]
		list_bin.reverse()

		while(len(list_bin)!=self.nb_items):
			list_bin.append('0')

		print("Massimo ottenibile: ",z)
		print("Matrice dei valori: \n",P)
		print("pick: \n",list_bin)
		return {"z_star":z,"memory":memory,"pick":self._find_original_position([eval(i) for i in list_bin])}