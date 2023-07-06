import numpy as np

class Knapsack:

	def __init__(self, capacity=0, profits=[], weights=[]):
		""" Knapsack class for solving a knapsack problem.

		Attributes:
			profits (list of non-negative floats): profits of items
			weights (list of positive floats): weights of items
			nb_items (int): number of items
			ids: (list of ints): ids of items
			capacity (float): capacity of knapsack
		"""
		self.profits = profits
		self.weights = weights
		self.nb_items = len(profits)
		self.capacity = capacity


	def sort_by_ratio(self):
		"""Function to sort item indexes by their ratios profit/weight in a
		descending order.

		Args:
			None

		Returns:
			sorted (list of ints): item_ids sorted by profit/weight in a
									descending order
		"""
		self.ids = sorted(self.ids, key=lambda i: self.profits[i]/self.weights[i],
						reverse=True)

	def dinamic_knackpack_matrix(self):

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

	def dinamic_knackpack_single_list(self):

		num_element = len(self.profits)
		#definisco l'array di partenza
		z = np.zeros(self.capacity+1)

		#per ogni possibile elemento nello zaino
		for j in range(0,num_element):
			#parto dalla capacità e vado fino al peso dell'elemento
			for d in range(self.capacity,self.weights[j],-1):
				#se il peso dell'elemento è minore della capacità quindi ce posto per lui nello zaino
				if z[d-self.weights[j]] + self.profits[j] > z[d]:
					#se il valore dello zaino meno il peso dell'elemento più il valore dell'elemento è maggiore dello zaino
					z[d] = z[d-self.weights[j]] + self.profits[j]

		z_star = z[self.capacity]
		print("Massimo ottenibile: ",z_star)
		print("Matrice dei valori: \n",z)


#main 
if __name__ == "__main__":
	
    capacity = 15
    weights = [5, 10, 9, 8]
    profits = [7, 5, 10,6]

    my_knapsack1 = Knapsack(capacity, profits, weights)
    my_knapsack1.dinamic_knackpack_matrix()
    my_knapsack1.dinamic_knackpack_single_list()