import numpy as np

def recursion1(v:int,b:int,P_values:list,X_present:list,weight:int,value:int,capacity:int):
    if v < capacity:
        u = v
        v = min(v + weight,capacity)
        for c_cap in range(u+1,v+1):
                P_values[c_cap] = P_values[u]
                X_present[c_cap] = X_present[u]
    
    for c_cap in range(v,weight+1,-1): 
         if P_values[c_cap] < P_values[c_cap-weight] + value:
             P_values[c_cap] = P_values[c_cap-weight] + value
             X_present[c_cap] = X_present[c_cap-weight] + b
    
    b = 2*b



def dinamic_programming_1(num_element:int,capacity:int,values:list,weights:list):

    #insieme di valori presi
    P_values = np.zeros(capacity+1)
    #segniamo se la x è presente o meno
    X_present = np.zeros(capacity+1)

    # per il primo elemento da 0 fino al suo peso-1
    c_cap = 0
    while c_cap < weights[0]-1:
        P_values[c_cap] = 0
        X_present[c_cap] = 0
        c_cap += 1
    
    v = weights[0]
    b = 2
    P_values[v] = values[0]
    X_present[v] = 1

    for m in range(2,num_element):
        recursion1(v,b,P_values,X_present,weights[m],values[m],capacity)

    z = P_values[capacity]
    return P_values,X_present,z





def dinamic_knackpack_matrix(num_element:int,capacity:int,values:list,weights:list):

    #definiamo un array di zeri su cui lavorare, grande qaundo la capacità dello zaino
    #corrisponde al primo ciclo di definizionde dello pseudo codice
    z = np.zeros((num_element,capacity+1))    
    a = np.zeros((num_element,capacity+1))
    
    #per ogni elemento che possiamo aggiungere nello zaino
    for j in range(0,num_element):
        #vado da 0 al minimo della capacità e del peso dell'elemento -1
        #in pratica finche lo zaino non è abbastanza grande non metto solo 0
        for d in range(0,weights[j]):
            #quindi assegno il valore precendete finche non ci sta nello zaino
            z[j,d] = z[j-1,d]
            #da quando il peso inizia ad avere posto nello zaino
        for d in range(weights[j],capacity+1):
            if(z[j-1,d-weights[j]] + values[j] > z[j-1,d]):
                z[j,d] = z[j-1,d-weights[j]] + values[j]
                a[j,d] = 1
            else:
                z[j,d] = z[j-1,d]
                a[j,d] = 0
    
    z_star = z[num_element-1,capacity]
    print("Massimo ottenibile: ",z_star)
    print("Matrice dei valori: \n",z)
    print("Matrice di pick: \n",a)

    
def dinamic_knackpack_single_list(num_element:int,capacity:int,values:list,weights:list):
    #definisco l'array di partenza
    z = np.zeros(capacity+1)

    #per ogni possibile elemento nello zaino
    for j in range(0,num_element):
        #parto dalla capacità e vado fino al peso dell'elemento
        for d in range(capacity,weights[j],-1):
            #se il peso dell'elemento è minore della capacità quindi ce posto per lui nello zaino
            if z[d-weights[j]] + values[j] > z[d]:
                #se il valore dello zaino meno il peso dell'elemento più il valore dell'elemento è maggiore dello zaino
                z[d] = z[d-weights[j]] + values[j]

    z_star = z[capacity]
    print("Massimo ottenibile: ",z_star)
    print("Matrice dei valori: \n",z)

#main
if __name__ == "__main__":
    dinamic_knackpack_matrix(3,10,[10,20,30],[3,3,3])
        
            

    
         