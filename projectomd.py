# -*- coding: utf-8 -*-
#ProjectoMD.ipynb

import random
import networkx as nx
import matplotlib.pyplot as plt
import os
#import itertools
import string

def producto_cartesiano(A):
    return [(a, b) for a in A for b in A]

def generar_relacion_aleatoria(A, p):
    R = []
    for i in range(len(A)):
        for j in range(len(A)):
            if random.random() <= p: # 0 y 1
                    R.append((A[i], A[j]))
    return R

def es_reflexiva(A, R):
    for a in A:
        if (a, a) not in R:
            return False
    return True

def es_irreflexiva(A, R):
    for a in A:
        if (a, a) in R:
            return False
    return True

def es_simetrica(R):
    for (a, b) in R:
        if (b, a) not in R:
            return False
    return True

def es_asimetrica(R):
    for (a, b) in R:
        if (b, a) in R and a != b:
            return False
    return True

def es_antisimetrica(R):
    for (a, b) in R:
        if (a != b and (a, b) in R and (b, a) in R):
            return False
    return True

def es_transitiva(R):
    for (a, b) in R:
        for (c, d) in R:
            if b == c and (a, d) not in R:
                return False
    return True

def es_equivalencia(A, R):
    return es_reflexiva(A, R) and es_simetrica(R) and es_transitiva(R)

def es_orden_parcial(A, R):
    return es_reflexiva(A, R) and es_antisimetrica(R) and es_transitiva(R)


def obtener_conjunto_cociente(A, R):
    cociente = {}
    for a in A:
        clase = [a]
        for b in A:
            if (a, b) in R:
                clase.append(b)
        cociente[a] = clase
    return cociente


def clasificar_relacion(A, R):
    es_reflexiva = all((a, a) in R for a in A)
    es_irreflexiva = all((a, a) not in R for a in A)
    es_simetrica = all((b, a) in R for (a, b) in R)
    es_asimetrica = all((a, b) not in R for (a, b) in R if a != b)
    es_antisimetrica = all(((a, b) not in R or (b, a) not in R or a == b) for a in A for b in A)
    es_transitiva = all((a, c) in R for (a, b) in R for (c, d) in R if b == c)
    es_equivalencia = es_reflexiva and es_simetrica and es_transitiva
    es_orden_parcial = es_reflexiva and es_antisimetrica and es_transitiva
    return {'reflexiva': es_reflexiva,
            'irreflexiva': es_irreflexiva,
            'simétrica': es_simetrica,
            'asimétrica': es_asimetrica,
            'antisimétrica': es_antisimetrica,
            'transitiva': es_transitiva,
            'equivalencia': es_equivalencia,
            'orden parcial': es_orden_parcial}


def obtener_conjunto_cociente(A, R):
    if not clasificar_relacion(A, R)['equivalencia']:
        return None
    clases = {}
    for a in A:
        clase = None
        for c in clases:
            if (a, c[0]) in R:
                clase = c
                break
        if not clase:
            clase = tuple([a] + [b for b in A if (a, b) in R])
            clases[clase] = True
    return list(clases.keys())

def obtener_elementos(aleatorio=False):
    elementos = set()
    ### NUNCA PASA ###
    if aleatorio:
        elementos_aleatorios = []
        while len(elementos_aleatorios) < 7:
            elemento_aleatorio = random.choice(string.ascii_letters + string.digits)
            if elemento_aleatorio not in elementos_aleatorios:
                elementos_aleatorios.append(elemento_aleatorio)
        elementos = set(elementos_aleatorios)
    #######
    else:
        while True:
            elemento = input("Ingrese un elemento del conjunto o 'salir' para terminar: ")
            if elemento.lower() == "salir":
                 if len(elementos) >= 4:
                   break
            if len(elementos) < 7 and elemento.isalnum():
                elementos.add(elemento)
            else:
                print("Elemento inválido.")
    return elementos

def obtener_relacion(elementos):
    relacion = set()
    for elemento1 in elementos:
        for elemento2 in elementos:
            respuesta = input(f"¿{elemento1} está relacionado con {elemento2}? (s/n)")
            if respuesta.lower() == "s":
                relacion.add((elemento1, elemento2))
    return relacion

def diagrama_hasse(elementos, relacion):
    if isinstance(relacion, set) and all(isinstance(x, tuple) and len(x) == 2 for x in relacion):
        # Eliminar bucles en nodos con si mismos si la relación es reflexiva
        for elemento in elementos:
            relacion.discard((elemento, elemento))
    # remove transitivity
    for a in elementos:
        for b in elementos:
            for c in elementos:
                if (a, b) in relacion and (b, c) in relacion and (a, c) in relacion:
                    relacion.discard((a, c))
    # put a good order
    positions = []
    positions.append([])
    # (1) NUCLEI
    for elemento in elementos:
        isNuclei = True
        for a in elementos:
            if a == elemento:
                continue
            if (a, elemento) in relacion and (elemento, a) not in relacion:
                isNuclei = False
                break
        if isNuclei:
            positions[0].append(elemento)
    #print(positions[0])
    # (HELPER) partners
    partners = []
    for elemento in elementos:
        for a in elementos:
            if a == elemento:
                continue
            if (a, elemento) in relacion and (elemento, a) in relacion and (a, elemento) not in partners:
                partners.append((elemento, a))
    #print(partners)
    # (N) EVERYTHING ELSE
    for i in range(1, len(elementos)):
      positions.append([])
      for elemento in positions[i-1]:
          for a in elementos:
              if (elemento, a) in relacion and (elemento, a) not in partners and (a, elemento) not in partners and a not in positions[i]:
                  positions[i].append(a)
    # now organize them in digraph
    pos = {}
    longestGroup = 0
    for i in range(len(positions)):
        if len(positions[i]) > longestGroup:
            longestGroup = len(positions[i])
    counterOfElements = []
    for i in range(len(positions)):
        counterOfElements.append(1)
    for elemento in elementos:
        for i in range(len(positions)):
            if elemento in positions[i]:
                if (len(positions[i]) == 1):
                    pos.setdefault(elemento, (2 * longestGroup * (counterOfElements[i]), i * 2))
                else:
                    pos.setdefault(elemento, (4 * longestGroup / len(positions[i]) * (counterOfElements[i]), i * 2))
                counterOfElements[i] += 1
    print(positions)
    grafo = nx.DiGraph()
    grafo.add_nodes_from(elementos)
    grafo.add_edges_from(relacion)
    posiciones = nx.spring_layout(grafo)
    nx.draw_networkx_nodes(grafo, pos, node_size=750, node_color="pink")
    nx.draw_networkx_labels(grafo, pos, font_size=15, font_family="sans-serif")
    nx.draw_networkx_edges(grafo, pos, width=2, arrowstyle="-", arrowsize=30)
    plt.axis("off")
    plt.show()

### Secuencia de Eventos ###
elementos = obtener_elementos()
respuesta = input("¿Deseas ingresar la relación manualmente? (s/n)")
if respuesta.lower() == "s":
    relacion = obtener_relacion(elementos)
else:
    p = float(input("Ingresa la probabilidad de que dos elementos estén relacionados (entre 0 y 1): "))
    relacion = generar_relacion_aleatoria(list(elementos), p)

print("Producto cartesiano:", producto_cartesiano(elementos))
print("La relación es:", relacion)
print("Es reflexiva:", es_reflexiva(elementos, relacion))
print("Es irreflexiva:", es_irreflexiva(elementos, relacion))
print("Es simétrica:", es_simetrica(relacion))
print("Es asimétrica:", es_asimetrica(relacion))
print("Es antisimétrica:", es_antisimetrica(relacion))
print("Es transitiva:", es_transitiva(relacion))
print("Es una relación de equivalencia:", es_equivalencia(elementos, relacion))
print("Es un orden parcial:", es_orden_parcial(elementos, relacion))
if es_orden_parcial(elementos, relacion)==True:
  diagrama_hasse(elementos, relacion)

if es_equivalencia(elementos, relacion)==True:
  print("El conjunto cociente es:", obtener_conjunto_cociente(elementos, relacion))

while True:
    continuar = input("Presione 'Enter' para salir.")
    if continuar == '':
        break

os.system('cls' if os.name=='nt' else 'clear')

grupo = "Grupo 5"
integrantes = ["Luis Herrera", "Joseph Alexis", "Silvana Alvarez", "Daniella Vargas", "Juan Pablo Guija"]
profesor = "Jhonathan Suarez"
curso = "Matemática Discreta"

border = "*" * 60
print(border)

print(f"{'Curso:':<20}{curso:>35}")
print(f"{'Profesor:':<20}{profesor:>32}")
print(f"{'Grupo:':<20}{grupo:>36}")

print("\nIntegrantes:")
for integrante in integrantes:
    print(f"{'- ' + integrante:<45}")

print(border)

tema = "Relaciones"

# Crea el borde
borde = "*" * 50 + "\n"

# Crea la pantalla de salida
output = f"{borde}"
output += f"{'*':^48}\n"
output += f"{'*':^48}\n"
output += f"{'*':^15} Tema: {tema:<25} {'*':^8}\n"
output += f"{'*':^48}\n"
output += f"{'*':^48}\n"
output += f"{borde}"
output += "\n\n"
output += "  /\\_/\\\n"
output += " ( o.o )\n"
output += "  > ^ <\n"
output += "Gracias por usar nuestro programa!\n"

# Imprime la pantalla de salida
print(output)

ascii_art = '''
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@






                                              ..
                                     .*/%&&&&&&&&&&%(/*,.
                                .*(%&&&@@@&&&&&&&&&@@&&&&%(,
                             .(%&&&&@@@@@@@@@@@@@@@@@@@@@&&&%(,.
                           ,(%&@@@@@@@@@@@@@@@@@@@@@@@@@@@@&&@&(*.
                          /%&&@@@@@@@@@@@@@@@@@@@@@@@@@@@&&&&@@@&#*.
                        ./%&@@@@@@@@@@@@&&&%&&&%%%%&&&&&&&@@@@@@@@&(,
                       ./&@@@@@@&&&&&&&&%#(((((((((((####%%&&&@@@@@&/.
                       *&&@@@@&%%#((((##(/////////////((((#%&@@@@@&&(,
                      ./&@@@@&%#(//////////*////*/////////(#%&@@@@@&#*
                      ./&@@@@&%((///////***********///////(#%&@@@@@&#*
                       *&@@@&&#(//((((((////****///((((((((((%&@@@@&#*
                       *&&@@&%(##%%%%%%&&%#(/*//(#%%&&%%%%%###%&@@@%*.
                       ,#&@@&#((##%%&&&%%#((/**/((##%%%%%%##((#&@@&#,
                        .(&@%(///((((((((((///*///(((((////////#%&%*
                         ,#%#///*********/////*//////********///#%/.
                          /((////*******/////***/////******////(((.
                          ./(((///******//(((////((///////////////
                           ,/((///////////((((((((((/////////((/*.
                            .*/(/////////////((((((((/(///////*.
                             .*/(/////((##############((((///,
                              .*/(////(###########(((((((((/.            ,*/////////,
                               ./(((((((((((#####(((((((((*.             /(*     .*(*
                              ./(####(((((((((((((((((((((,          .. ./(,      *(*
                         ..*/#%(/(#########(##########(((/.       .*((*..,*.      *(*
                   .,/(#%&@&&&&(,,/(#################((((*.      ./(#((/(((((/,   *(*
                  ,(&&@@@@@@@@&%,  .*(##############(((*,.         ,*/*. **.      *(*
                    .*#&@@@@@@@&(,    .*/(#((##(((((/,.   .              /(*      *(*
                       .,(%&@@@@%/.      .,/(((((*,.     .*/,            */((((((((/,
                            ,/(%&#*        .*(#*.        ,#&%*.
                                 ..        *#&&%/.       .,.


'''
print(ascii_art)


while True:
    continuar = input("Presione 'Enter' para salir.")
    if continuar == '':
        break



import tkinter
import random
import networkx as nx
import matplotlib.pyplot as plt
#import itertools
import string

###########
# parte de Colab
def producto_cartesiano(A):
    return [(a, b) for a in A for b in A]

def generar_relacion_aleatoria(A, p):
    R = []
    for i in range(len(A)):
        for j in range(len(A)):
            if random.random() <= p: # 0 y 1
                    R.append((A[i], A[j]))
    return R

def es_reflexiva(A, R):
    for a in A:
        if (a, a) not in R:
            return False
    return True

def es_irreflexiva(A, R):
    for a in A:
        if (a, a) in R:
            return False
    return True

def es_simetrica(R):
    for (a, b) in R:
        if (b, a) not in R:
            return False
    return True

def es_asimetrica(R):
    for (a, b) in R:
        if (b, a) in R and a != b:
            return False
    return True

def es_antisimetrica(R):
    for (a, b) in R:
        if (a != b and (a, b) in R and (b, a) in R):
            return False
    return True

def es_transitiva(R):
    for (a, b) in R:
        for (c, d) in R:
            if b == c and (a, d) not in R:
                return False
    return True

def es_equivalencia(A, R):
    return es_reflexiva(A, R) and es_simetrica(R) and es_transitiva(R)

def es_orden_parcial(A, R):
    return es_reflexiva(A, R) and es_antisimetrica(R) and es_transitiva(R)


def obtener_conjunto_cociente(A, R):
    cociente = {}
    for a in A:
        clase = [a]
        for b in A:
            if (a, b) in R:
                clase.append(b)
        cociente[a] = clase
    return cociente


def clasificar_relacion(A, R):
    es_reflexiva = all((a, a) in R for a in A)
    es_irreflexiva = all((a, a) not in R for a in A)
    es_simetrica = all((b, a) in R for (a, b) in R)
    es_asimetrica = all((a, b) not in R for (a, b) in R if a != b)
    es_antisimetrica = all(((a, b) not in R or (b, a) not in R or a == b) for a in A for b in A)
    es_transitiva = all((a, c) in R for (a, b) in R for (c, d) in R if b == c)
    es_equivalencia = es_reflexiva and es_simetrica and es_transitiva
    es_orden_parcial = es_reflexiva and es_antisimetrica and es_transitiva
    return {'reflexiva': es_reflexiva,
            'irreflexiva': es_irreflexiva,
            'simétrica': es_simetrica,
            'asimétrica': es_asimetrica,
            'antisimétrica': es_antisimetrica,
            'transitiva': es_transitiva,
            'equivalencia': es_equivalencia,
            'orden parcial': es_orden_parcial}


def obtener_conjunto_cociente(A, R):
    if not clasificar_relacion(A, R)['equivalencia']:
        return None
    clases = {}
    for a in A:
        clase = None
        for c in clases:
            if (a, c[0]) in R:
                clase = c
                break
        if not clase:
            clase = tuple([a] + [b for b in A if (a, b) in R])
            clases[clase] = True
    return list(clases.keys())

def obtener_elementos(aleatorio=False):
    elementos = set()
    ### NUNCA PASA ###
    if aleatorio:
        elementos_aleatorios = []
        while len(elementos_aleatorios) < 7:
            elemento_aleatorio = random.choice(string.ascii_letters + string.digits)
            if elemento_aleatorio not in elementos_aleatorios:
                elementos_aleatorios.append(elemento_aleatorio)
        elementos = set(elementos_aleatorios)
    #######
    else:
        while True:
            elemento = input("Ingrese un elemento del conjunto o 'salir' para terminar: ")
            if elemento.lower() == "salir":
                 if len(elementos) >= 4:
                   break
            if len(elementos) < 7 and elemento.isalnum():
                elementos.add(elemento)
            else:
                print("Elemento inválido.")
    return elementos

def obtener_relacion(elementos):
    relacion = set()
    for elemento1 in elementos:
        for elemento2 in elementos:
            respuesta = input(f"¿{elemento1} está relacionado con {elemento2}? (s/n)")
            if respuesta.lower() == "s":
                relacion.add((elemento1, elemento2))
    return relacion

def diagrama_hasse(elementos, relacion):
    if isinstance(relacion, set) and all(isinstance(x, tuple) and len(x) == 2 for x in relacion):
        # Eliminar bucles en nodos con si mismos si la relación es reflexiva
        for elemento in elementos:
            relacion.discard((elemento, elemento))
    # remove transitivity
    for a in elementos:
        for b in elementos:
            for c in elementos:
                if (a, b) in relacion and (b, c) in relacion and (a, c) in relacion:
                    relacion.discard((a, c))
    # put a good order
    positions = []
    positions.append([])
    # (1) NUCLEI
    for elemento in elementos:
        isNuclei = True
        for a in elementos:
            if a == elemento:
                continue
            if (a, elemento) in relacion and (elemento, a) not in relacion:
                isNuclei = False
                break
        if isNuclei:
            positions[0].append(elemento)
    #print(positions[0])
    # (HELPER) partners
    partners = []
    for elemento in elementos:
        for a in elementos:
            if a == elemento:
                continue
            if (a, elemento) in relacion and (elemento, a) in relacion and (a, elemento) not in partners:
                partners.append((elemento, a))
    #print(partners)
    # (N) EVERYTHING ELSE
    for i in range(1, len(elementos)):
      positions.append([])
      for elemento in positions[i-1]:
          for a in elementos:
              if (elemento, a) in relacion and (elemento, a) not in partners and (a, elemento) not in partners and a not in positions[i]:
                  positions[i].append(a)
    # now organize them in digraph
    pos = {}
    longestGroup = 0
    for i in range(len(positions)):
        if len(positions[i]) > longestGroup:
            longestGroup = len(positions[i])
    counterOfElements = []
    for i in range(len(positions)):
        counterOfElements.append(1)
    for elemento in elementos:
        for i in range(len(positions)):
            if elemento in positions[i]:
                if (len(positions[i]) == 1):
                    pos.setdefault(elemento, (2 * longestGroup * (counterOfElements[i]), i * 2))
                else:
                    pos.setdefault(elemento, (4 * longestGroup / len(positions[i]) * (counterOfElements[i]), i * 2))
                counterOfElements[i] += 1
    print(positions)
    grafo = nx.DiGraph()
    grafo.add_nodes_from(elementos)
    grafo.add_edges_from(relacion)
    posiciones = nx.spring_layout(grafo)
    nx.draw_networkx_nodes(grafo, pos, node_size=750, node_color="pink")
    nx.draw_networkx_labels(grafo, pos, font_size=15, font_family="sans-serif")
    nx.draw_networkx_edges(grafo, pos, width=2, arrowstyle="-", arrowsize=30)
    plt.axis("off")
    plt.show()
#
###########
###########
###########
###########


window = tkinter.Tk()
window.geometry("500x500")

numElements = 4

buttons = []
relationMatrix = []

def buttonChange(val):
    global buttons
    global relationMatrix
    relationMatrix[val] = not relationMatrix[val]
    buttons[val]['text'] = str(int(relationMatrix[val]))

destructoButton = 0
resultoButton = 0
aleatoButton = 0
names = []
results = 0

def aleatoriacion():
    global numElements
    global buttons
    global relationMatrix
    for i in range(numElements):
        for j in range(numElements):
            if random.random() <= 0.5:
                relationMatrix[i*numElements + j] = True
            else:
                relationMatrix[i*numElements + j] = False
            buttons[i*numElements + j]['text'] = str(int(relationMatrix[i*numElements + j]))



def showResults():
    # error handling
    for i in range(numElements):
        if not names[i].get().isalnum():
            return
    # get elements
    elementos = []
    for i in range(numElements):
        elementos.append('')
    for i in range(numElements):
        elementos[i] = names[i].get()
    # get relation
    relacion = set()
    for i in range(numElements):
        for j in range(numElements):
            if relationMatrix[i * numElements + j] == True:
                relacion.add((elementos[i], elementos[j]))
    # show results
    results = tkinter.Label(text = "", anchor = "w")
    results.grid(row = numElements * 2 + 2 + numElements, column = 0, columnspan = 15)
    print("Producto cartesiano: ", producto_cartesiano(elementos))
    print("La relación es:", relacion)
    print("Es reflexiva:", es_reflexiva(elementos, relacion))
    print("Es irreflexiva:", es_irreflexiva(elementos, relacion))
    print("Es simétrica:", es_simetrica(relacion))
    print("Es asimétrica:", es_asimetrica(relacion))
    print("Es antisimétrica:", es_antisimetrica(relacion))
    print("Es transitiva:", es_transitiva(relacion))
    print("Es una relación de equivalencia:", es_equivalencia(elementos, relacion))
    print("Es un orden parcial:", es_orden_parcial(elementos, relacion))
    if es_orden_parcial(elementos, relacion)==True:
        diagrama_hasse(elementos, relacion)
    if es_equivalencia(elementos, relacion)==True:
        print("El conjunto cociente es:", obtener_conjunto_cociente(elementos, relacion))


def recreate(numElem_Sel):
    global numElements
    global destructoButton
    global resultoButton
    global aleatoButton
    if int(numElem_Sel.get()) > 7 or int(numElem_Sel.get()) < 1:
        return
    # destroy
    ## buttons
    for i in range(numElements):
        for j in range(numElements):
            buttons[0].destroy()
            buttons.pop(0)
            relationMatrix.pop(0)
    ## destructoButton
    destructoButton.destroy()
    ## resultoButton
    resultoButton.destroy()
    ## aleatoButton
    aleatoButton.destroy()
    ## names
    for i in range(numElements):
        names[0].destroy()
        names.pop(0)
    ## results
    results.destroy()
    # new params
    numElements = int(numElem_Sel.get())
    # create
    ## buttons
    for i in range(numElements):
        for j in range(numElements):
            e = tkinter.Button(window, text = "0", command = (lambda i=i, j=j: buttonChange(i*numElements + j)))
            e.grid(row=2*i + 1,column=j,padx=2,pady=2)
            buttons.append(e)
            relationMatrix.append(False)
    ## destructoButton
    destructoButton = tkinter.Button(window, text = "R", command = lambda: recreate(numElem_Sel))
    destructoButton.grid(row = numElements * 2, column = 0)
    ## resultoButton
    resultoButton = tkinter.Button(window, text = "G", command = lambda: showResults())
    resultoButton.grid(row = numElements * 2, column = 1)
    ## aleatoButton
    aleatoButton = tkinter.Button(window, text = "A", command = lambda: aleatoriacion())
    aleatoButton.grid(row = numElements * 2, column = 2)
    ## names
    for i in range(numElements):
        s = tkinter.Entry()
        s.grid(row = numElements * 2 + 1 + i,column=0, columnspan = 7,padx=2,pady=2)
        names.append(s)

numElem_Text = tkinter.Label(text = "Numero de Elementos:")
numElem_Text.grid(row = 0, column = 0, columnspan = 7, sticky = tkinter.W+tkinter.E)
numElem_Sel = tkinter.Entry()
numElem_Sel.grid(row = 0, column = 7)




for i in range(numElements):
    for j in range(numElements):
        e = tkinter.Button(window, text = "0", command = (lambda i=i, j=j: buttonChange(i*numElements + j)))
        e.grid(row=2*i + 1,column=j,padx=2,pady=2)
        buttons.append(e)
        relationMatrix.append(False)

destructoButton = tkinter.Button(window, text = "R", command = lambda: recreate(numElem_Sel))
destructoButton.grid(row = numElements * 2, column = 0)

resultoButton = tkinter.Button(window, text = "G", command = lambda: showResults())
resultoButton.grid(row = numElements * 2, column = 1)

aleatoButton = tkinter.Button(window, text = "A", command = lambda: aleatoriacion())
aleatoButton.grid(row = numElements * 2, column = 2)


for i in range(numElements):
    s = tkinter.Entry()
    s.grid(row = numElements * 2 + 1 + i,column=0, columnspan = 7,padx=2,pady=2)
    names.append(s)

elementos = []
# just for the beginning
for i in range(numElements):
    elementos.append('')
elementos[0] = 'a'
elementos[1] = 'b'
elementos[2] = 'c'
elementos[3] = 'd'
names[0].insert(0, 'a')
names[1].insert(0, 'b')
names[2].insert(0, 'c')
names[3].insert(0, 'd')

results = tkinter.Label(text = "", anchor = "w")
results.grid(row = numElements * 2 + 2 + numElements, column = 0, columnspan = 15)





window.mainloop()
