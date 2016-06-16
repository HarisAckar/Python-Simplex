# -*- coding: utf-8 -*-
"""
Elektrotehnički fakultet
Univerzitet u Sarajevu
Predmet: Optimalno upravljanje
Tema: Implementacija simpleksnog algoritma
Nastavnik: Vanr. prof. dr Samim Konjicija
Asistenti: Mr Nedim Osmić, dipl. ing. el. i Kapetanović Nadir, MSc of EE
Student: Haris Ačkar
"""

import numpy as np

def inicijalizacija():
###############################################################################
# Funkcija inicijalizira broj varijabli i broj ograničenja problema linearnog
# programiranja čiji optimum želimo naći
###############################################################################
    br_var = input("Unesite broj varijabli problema: ")
    if isinstance(br_var, int):
        br_ogr = input("Unesite broj ogranicenja problema: ")
        if isinstance(br_ogr, int):
            return br_var, br_ogr
        else:
            print "Broj ogranicenja nije cijeli broj!"
            return -1
    else:
        print "Broj varijabli nije cijeli broj!"
        return -1

def init_fiju_kriterija(br_var):
###############################################################################
# Funkcija inicijalizira koeficijente funkcije kriterija datog problema
###############################################################################
    string = "P(x) = "
    koef_krit = []
    for i in range(br_var):
        string = string + "a" + str(i+1) + "x" + str(i+1)
        if i < br_var - 1:
            string = string + " + "
    print string
    for i in range(br_var):
        koef_krit.append(input("Unesite " + "a" + str(i+1) + ": "))
    return koef_krit

def init_ogranicenja(br_ogr, br_var):
###############################################################################
# Funkcija inicijalizira koeficijente ograničenja datog problema
###############################################################################
    koef_ogr = [[None]*(br_var + 1) for _ in range(br_ogr)]
    for i in range(br_ogr):
        print "Unesite koeficijente " + str(i+1) + "-og ogranicenja: "
        string = ""
        for k in range(br_var):
            string = string + "a" + str(k+1) + "x" + str(k+1) 
            if k < br_var - 1:
                string = string + " + "
        print string + " <= b"

        for j in range(br_var):
            koef_ogr[i][j] = (input("Unesite " + "a" + str(j+1) + ": "))
        koef_ogr[i][br_var] =(input("Unesite b: "))
    return koef_ogr

def A(koef_ogr, br_var, br_ogr):
###############################################################################
# Funkcija inicijalizira koeficijente matrice 'A'
###############################################################################
    A = [[] for _ in range(br_ogr)]
    for i in range(br_ogr):
        for j in range(br_var):
            A[i].append(koef_ogr[i][j])
    return A
   
def C(koef_krit, br_ogr):
###############################################################################
# Funkcija inicijalizira koeficijente matrice 'C'
###############################################################################
    C = []
    for i in range(len(koef_krit)):
        C.append(koef_krit[i])
    return C

def b(koef_ogr, br_ogr, br_var):
###############################################################################
# Funkcija inicijalizira koeficijente matrice 'b'
###############################################################################
    b = []
    for i in range(br_ogr):
        b.append(koef_ogr[i][br_var])
    return b


def index_max(x):
###############################################################################
# Funkcija nalazi index najveceg clana u vektora
###############################################################################
    temp = x[0]
    index = 0
    for i in range(len(x)):
        if temp < x[i]:
            temp = x[i]
            index = i
    return index

def index_min(x):
###############################################################################
# Funkcija nalazi index najmanjeg clana u vektoru
###############################################################################
    temp = x[0]
    index = 0
    for i in range(0,len(x)):
        if temp > x[i]:
            temp = x[i]
            index = i
    return index

def suma_vnula(x):
###############################################################################
# Funkcija nalazi sumu svih elemenata vektora koji su veci od nule
###############################################################################
    temp = 0
    for i in range(len(x)):
        if x[i] > 0:
            temp += x[i]
    return temp
    

def simpleks(A,b,c):
###############################################################################
# Funkcija simpleksnog algoritma, kao rezultat vraca maximum funkcije
# i tacke u kojima se maksimum nalazi
###############################################################################
    simplex_table = A
    simplex_table = np.column_stack([simplex_table, np.eye(len(b))])
    simplex_table = np.column_stack([simplex_table, b])
    vekt = []
    for i in range(len(c)):
        vekt.append(c[i])
    for i in range(len(b)+1):
        vekt.append(0)
    simplex_table = np.vstack([simplex_table, vekt])
    base = np.linspace(len(c)+1, len(c)+len(b), len(b))
    for h in range(len(base)):
        base[h] -= 1
    rows, columns = simplex_table.shape
    rows = int(rows)
    columns = int(columns)
    temp = 0
    vect = 0
    uslov = True
    while uslov:
        j = index_max(simplex_table[rows-1,:])
        temp = np.divide(simplex_table[0:rows-1,columns-1], simplex_table[0:rows-1, j])
        for u in range(len(temp)):
            if temp[u] < 0:
                temp[u] = float('Inf')
        i = index_min(temp)
        base[i] = j
        vect = simplex_table[i,:]
        div = simplex_table[i,j]
        for h in range(len(vect)):
            vect[h] = float(vect[h])/div
        simplex_table[i,:] = vect
        for k in range(rows):
            if k != i:
                simplex_table[k,:] = simplex_table[k,:] - simplex_table[k,j] * simplex_table[i,:]
        uslov = not(suma_vnula(simplex_table[rows-1,:]) == False)
    f_opt = -simplex_table[rows-1, columns-1]
    x_opt = np.zeros(len(c) + len(b))
    for k in range(0,len(base)):
        x_opt[base[k]] = simplex_table[k, columns-1]
    
    return f_opt, x_opt        
    
###############################################################################
#---------------------------------- MAIN --------------------------------------
###############################################################################
br_var, br_ogr = inicijalizacija()
koef_krit = init_fiju_kriterija(br_var)
koef_ogr = init_ogranicenja(br_ogr, br_var)
A = A(koef_ogr, br_var, br_ogr)
C = C(koef_krit, br_ogr)
b = b(koef_ogr, br_ogr, br_var)
f_opt, x_opt = simpleks(A,b,C)
print "Maximum funkcije je: ", f_opt
x_optn = []
for i in range(br_var):
    x_optn.append(x_opt[i])
print "Maximum je u tački:", x_optn