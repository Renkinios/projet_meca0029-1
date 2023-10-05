import numpy as np
import matplotlib.pyplot as plt
import math

def read_data (file_name) : 
    """ Lit le fichier "fichier" contenant la liste des coordonnées des noeuds, et les éléments
        Arguments : 
            - fichier : nom du fichier texte
        Return : 
            - nodes : la liste des coordonnées des noeuds 
            - elements : la liste des éléments
    """

    # Initialiser les listes
    nodes = []
    elements = []

    # Ouvrir le fichier en mode lecture
    with open(file_name, 'r') as file:
        lines = file.readlines()

    # Ignorer la première ligne (Number of nodes)
    lines = lines[1:]
    cumpt = 0 

    # Parcourir les lignes restantes et insérer les coordonnées dans la nodes
    for line in lines:
        # Séparer la ligne en tokens en utilisant l'espace comme délimiteur
        if("Number of elements :\n" == line):
            break
        tokens = line.split()
        cumpt += 1
        coordonnees = [float(tokens[2]), float(tokens[3]), float(tokens[4])]
        nodes.append(coordonnees)
    for line in range(cumpt+1, len(lines)):
        # Séparer la ligne en tokens en utilisant l'espace comme délimiteur
        tokens = lines[line].split()
        elem_nodes = [int(tokens[2]), int(tokens[3])]
        elements.append(elem_nodes)

    return nodes, elements

# print("éléments : ", elements)
# print("nodes : ", nodes)
# print("coordonnees :",nodes[elements[30][0]][0])

def new_nodes(nodes, elements):
    """ Crée des nouveaux noeuds en divisant chaque éléments en deux 
        Arguments : 
            - matrix : matrice contenant les noeuds initiaux    
        Return : 
            - new_matrix : matrice contenant les noeuds initiaux et les nouveaux noeuds
    """

    new_matrix = []
    for i in range(len(elements)):
        x = (nodes[elements[i][0]][0] + nodes[elements[i][1]][0])/2
        y = (nodes[elements[i][0]][1] + nodes[elements[i][1]][1])/2
        z = (nodes[elements[i][0]][2] + nodes[elements[i][1]][2])/2
        nodes.append([x, y, z])
        new_element_1 = [elements[i][0], len(nodes)-1]
        new_element_2 = [len(nodes)-1, elements[i][1]]
        new_matrix.append(new_element_1)
        new_matrix.append(new_element_2)
    return new_matrix

# elements = new_nodes(elements)

def writing_nodes_element_file(nodes,elements, file_name):
    """ Ecrit les nouveaux éléments créés dans un fichier texte
        Arguments : 
            - nodes : liste des noeuds
            - elements : liste des éléments 
        Return : 
            - Rien
    """

    with open(file_name, 'w') as fichier:
        fichier.write("Number of nodes " + str(len(nodes)) + " :\n")
        for i in range(len(nodes)):
            fichier.write("\t" + str(i) + " : " + str(nodes[i][0]) + " " + str(nodes[i][1]) + " " + str(nodes[i][2]) + "\n")
        fichier.write("Number of elements :\n")
        for i in range(len(elements)):
            fichier.write("\t"+ str(i) + " : " + str(elements[i][0]) + " " + str(elements[i][1]) + "\n")

# writing_nodes_element_file(nodes,elements)

def plot_nodes(nodes, elements) : 
    """ Plot la structure avec les noeuds et les éléments
        Arguments : 
            - noeud : liste des noeuds
            - elements : liste des éléments
        Return : 
            - Rien
    """

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    for i in elements:
        x = [nodes[i[0]][0], nodes[i[1]][0]]
        y = [nodes[i[0]][1], nodes[i[1]][1]]
        z = [nodes[i[0]][2], nodes[i[1]][2]]
        ax.plot(x, y, z, 'b-')
    for node in nodes:
        ax.plot(node[0], node[1], node[2], 'ro')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('Maillage de droites en 3D')
    ax.set_zlim(0,25000)
    plt.show()

# plot_nodes(nodes, elements)

def euclidian_distance(elem, elements, nodes) : 
    """ Calcule la longueur de l'élément via la formule de la distance euclidienne
        Argument : 
            - elem : scalaire donnant l'index de l'élément dans la liste elements
            - elements : la liste des éléments
            - nodes : la liste des coordonnées de chaque noeud
        Return : 
            - elem_len : la longueur de l'élément
    """

    node_1 = elements[elem][0]
    node_2 = elements[elem][1]
    coord_1 = nodes[node_1]
    coord_2 = nodes[node_2]

    elem_len = math.sqrt(((coord_1[0]-coord_2[0])**2)+((coord_1[1]-coord_2[1])**2)+((coord_1[2]-coord_2[2])**2))

    return elem_len

def elem_matrixes(beam_param) : 
    """ Crée les matrices élémentaires
        Arguements : 
            - beam_param : une array contenant les paramètres de la poutre : [A, r, h, E, Iz, Iy, Jx, G]
        Return : 
            - M_el : la matrice élémentaire de masse
            - K_el : la matrice élémentaire d'énergie cinétique
    """
    A = beam_param[0]; r = beam_param[1]; h=beam_param[2]; E=beam_param[3]; Iz=beam_param[4]; Iy=beam_param[5]; Jx=beam_param[6]; G=beam_param[7]
    r = 1
    a = (11*h)/210
    b = (13*h)/420
    c = (h**2)/105
    d = (r**2)/3
    e = (h**2)/140
    M_el = [[  1/3,     0,     0,     0,     0,     0,   1/6,     0,     0,     0,     0,     0], 
            [    0, 13/35,     0,     0,     0,     a,     0,  9/70,     0,     0,     0,    -b],
            [    0,     0, 13/35,     0,    -a,     0,     0,     0,  9/70,     0,     b,     0], 
            [    0,     0,     0,     d,     0,     0,     0,     0,     0,   d/2,     0,     0],
            [    0,     0,    -b,     0,     c,     0,     0,     0,    -b,     0,    -e,     0], 
            [    0,     a,     0,     0,     0,     c,     0,     b,     0,     0,     0,    -e],
            [  1/6,     0,     0,     0,     0,     0,   1/3,     0,     0,     0,     0,     0],
            [    0,  9/70,     0,     0,     0,     b,     0, 13/35,     0,     0,     0,    -a],
            [    0,     0,  9/70,     0,    -b,     0,     0,     0, 13/35,     0,     a,     0],
            [    0,     0,     0,   d/2,     0,     0,     0,     0,     0,     d,     0,     0],
            [    0,     0,     b,     0,    -e,     0,     0,     0,     a,     0,     c,     0],
            [    0,    -b,     0,     0,     0,    -e,     0,    -a,     0,     0,     0,     c]]
    
    f = (E*A)/h
    g = (12*E*Iz)/(h**3)
    i = (6*E*Iz)/(h**2)
    j = (12*E*Iy)/(h**3)
    k = (6*E*Iy)/(h**2)
    m = (G*Jx)/h
    n = (2*E*Iz)/h
    o = (2*E*Iy)/h
    K_el = [[    f,     0,     0,     0,     0,     0,    -f,     0,     0,     0,     0,     0], 
            [    0,     g,     0,     0,     0,     i,     0,    -g,     0,     0,     0,     i],
            [    0,     0,     j,     0,    -k,     0,     0,     0,    -j,     0,    -k,     0], 
            [    0,     0,     0,     m,     0,     0,     0,     0,     0,     m,     0,     0],
            [    0,     0,    -k,     0,   2*o,     0,     0,     0,     k,     0,     o,     0], 
            [    0,     i,     0,     0,     0,   2*n,     0,    -i,     0,     0,     0,     n],
            [   -f,     0,     0,     0,     0,     0,     f,     0,     0,     0,     0,     0],
            [    0,    -g,     0,     0,     0,    -i,     0,     g,     0,     0,     0,    -i],
            [    0,     0,    -j,     0,     k,     0,     0,     0,     j,     0,     k,     0],
            [    0,     0,     0,    -m,     0,     0,     0,     0,     0,     m,     0,     0],
            [    0,     0,    -k,     0,     o,     0,     0,     0,     k,     0,   2*o,     0],
            [    0,     i,     0,     0,     0,     n,     0,    -i,     0,     0,     0,   2*n]]
    
    return M_el, K_el
    