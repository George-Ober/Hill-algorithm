# George A. Ober (c) 2023

import numpy as np

""" Definition de la liste alphabet. """
alphabet = []
for i in range(ord('a'), ord('z') + 1):
    alphabet.append(chr(i))

alphabet.append(" ")

def sanitisation(texte:str):
    """ Cette fonction prend en entrée une chaine de charactères
    et renvoie une chaine de charactères pouvant être utilisée dans les autres fonctions de ce programme. """
    
    chaine_propre = ""
    for lettre in range(len(texte)): 
        minuscule = texte[lettre].lower()
        if minuscule in alphabet:
            chaine_propre += minuscule
        elif minuscule == " ":
            print("Charactere espace ignoré à l'index %s" % lettre)
        else:
            raise ValueError("Texte entré contient le charactère interdit '%s' à  l'index %s" % (texte[lettre], lettre))
    return chaine_propre

def conversion_index(chaine: str):
    """ Cette fonction convertit une chaine de charactères en une liste d'indices correspondant à la liste `alphabet`. """
    
    liste = []
    for i in range(len(chaine)):
        lettre = chaine[i]
        e = alphabet.index(lettre)
        liste.append(e)
    return liste

def conversion_lettres(nombres: list):
    """ Cette fonction convertit une liste d'entiers en lettres, conformément à la liste `alphabet`. """
    
    chaine_finale = ""
    for lettre in nombres:
        chaine_finale += alphabet[lettre]
    return chaine_finale

def separation_syllabes(nombres: list, taille: int, mode_stricte: bool = False, lettre_en_plus: str = 'x'):
    """ Cette fonction groupe une liste d'entiers par groupes de `taille` demandée. 

        Par exemple pour une `taille = 3`:
        `[1, 2, 3, 4, 5, 6, 7, 8, 9] -> [[1, 2, 3], [4, 5, 6], [7, 8, 9]]`

        Si la liste entrée ne contient pas un multiple de `taille`, on rajoute `lettre_en_plus` au dernier groupe, jusqu'à ce qu'il soit complété. Par exemple, pour `taille = 3`, et `lettre_en_plus -> x`:
        `[1, 2, 3, 4] -> [[1, 2, 3], [4, 23, 23]]`
    """

    groupe = list(zip(*(iter(nombres),) * taille))
    mod = len(nombres) % taille
    if mod == 0:
        return groupe
    elif mode_stricte:
        raise ValueError("Le code entré contient %s lettres qui n'est pas multiple de la taille de la matrice, d'ordre %s." % (len(nombres),taille))
    else:
        dernier_groupe = []
        index = -mod
        while len(dernier_groupe) < taille:
            if index < 0:
                dernier_groupe.append(nombres[index])
                index += 1
            else:
                dernier_groupe.append(alphabet.index(lettre_en_plus))
        groupe.append(dernier_groupe)
        return groupe


def chiffrement_hill(syllabes: list, matrice_chiffrement: list):
    """ Cette fonction prend en entriée une liste de nombres, séparées par groupes du même ordre que la `matrice_chiffrement`, et renvoie le produit matriciel successif de chaqun de ces indices modulo la longueur de l'alphabet, conformément à l'algorithme de Hill. """
    resultat = []
    for syllabe in syllabes:
        syllabe_chifree = np.matmul(matrice_chiffrement, syllabe)
        for ligne in syllabe_chifree:
            resultat.append(ligne % len(alphabet))
    return resultat
        
def dechiffrement_hill(syllabes: list, matrice_chiffrement: list):
    """ Cette fonction prend en entriée une liste de nombres, séparées par groupes du même ordre que la `matrice_chiffrement`.
    - Calcule alpha, l'inverse  modulo la taille de l'alphabet du déterminant de la matrice
    - Effectue le produit matriciel entre la matrice auxiliaire B, alpha, et le vecteur vertical correspondant aux lettres de chaque groupe. """

    det = round(np.linalg.det(matrice_chiffrement))
    B = np.matrix.round(np.linalg.inv(matrice_chiffrement) * det, 0)
    
    # alpha = pow(det, -1, len(alphabet))
    alpha = inverse_modulo(det, len(alphabet))
    
    resultat = []
    for syllabe in syllabes:
        partiel = np.matmul(B, syllabe)
        syllabe_dechifree = partiel * alpha
        for ligne in syllabe_dechifree:
            resultat.append(int(ligne % len(alphabet)))
    return resultat

def inverse_modulo(a, m):
    g, x, y = algorithme_euclide(a % m, m)
    if g != 1:
        raise Exception("Le déterminant et la longueur de l'alphabet ne sont pas premiers entre eux.")
    else:
        return x % m

def algorithme_euclide(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = algorithme_euclide(b % a, a)
        return (g, x - (b // a) * y, y)

def chiffrer(texte: str, matrice: list, lettre_en_plus: str = "x"):
    """ Execute la succéssion de fonctions Python permettant le chiffrement de Hill d'une chaine de charactères. """
    taille_syllabe = np.linalg.matrix_rank(matrice)
    converti = conversion_index(sanitisation(texte))
    syllabes = separation_syllabes(converti, taille_syllabe, False, lettre_en_plus)
    chiffre = chiffrement_hill(syllabes, matrice)
    return conversion_lettres(chiffre)
    
def dechiffrer(code: str, matrice: list):
    """ Execute la succéssion de fonctions Python permettant le déchiffrement de Hill d'une chaine de charactères. """
    taille_syllabe = np.linalg.matrix_rank(matrice)
    converti = conversion_index(sanitisation(code))
    syllabes = separation_syllabes(converti, taille_syllabe, True)
    chiffre = dechiffrement_hill(syllabes, matrice)
    return conversion_lettres(chiffre)


A = [[3,2,1],
     [5,6,0],
     [7,1,1]]


""" A = [[11, 3],
     [7, 4]]
 """

print(dechiffrer(chiffrer('lorem ipsum', A),A))