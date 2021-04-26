import numpy as np
import random
import matplotlib.pyplot as plt
import time

class Grille_bataille_navale:
    VIDE=0
    PORTE_AVION=1
    CROISEUR=2
    CONTRE_TORPILLEUR=3
    SOUS_MARIN=4
    TORPILLEUR=5
    
    def __init__(self):
        self.grille=np.zeros((10,10),dtype=int)
        
    def get_grille(self):
        return self.grille
    
    def taille_bat(bateau):
        taille=0
        if(bateau==Grille_bataille_navale.PORTE_AVION):
            taille=5
        elif(bateau==Grille_bataille_navale.CROISEUR):
            taille=4
        elif(bateau==Grille_bataille_navale.CONTRE_TORPILLEUR):
            taille=3
        elif(bateau==Grille_bataille_navale.SOUS_MARIN):
            taille=3
        elif(bateau==Grille_bataille_navale.TORPILLEUR):
            taille=2
        return taille
    
    def peut_placer(self, bateau, position, direction):
        taille=Grille_bataille_navale.taille_bat(bateau)
        if(direction==1):#1->horizontale
            for x in range(position[0],position[0]+taille):
                if(x<0 or x>=10) or (self.grille[x][position[1]]!=0):
                    return False
            return True
        elif(direction==2):#2-> Verticale
            for y in range(position[1],position[1]+taille):
                if(y<0 or y>=10) or (self.grille[position[0]][y]!=0):
                    return False
            return True
        return False
   
    def place(self, bateau, position, direction):
        taille=Grille_bataille_navale.taille_bat(bateau)
    
        if (self.peut_placer(bateau, position, direction)):
            if(direction==1):#1->horizontale
                for x in range(position[0],position[0]+taille):
                    self.grille[x][position[1]]=bateau
    
            elif(direction==2): #2-> Verticale
                for y in range(position[1],position[1]+taille):
                    self.grille[position[0]][y]=bateau
    
    def place_alea(self, bateau):
        position=[random.randrange(10),random.randrange(10)]
        direction=random.randrange(1,3)
        while(not self.peut_placer(bateau,position,direction)):
            position=[random.randrange(10),random.randrange(10)]
            direction=random.randrange(1,3)
        self.place(bateau,position,direction)
        
    def affiche_chiffres(self):
        s=""
        for x in range(10):
            s=""
            for y in range(10):
                s+=(str)(self.grille[x][y])+" "
            print(s)
            
        
    def affiche(self):
        plt.imshow(self.grille,origin='{lower}')
        plt.show()
    
    def eq(grilleA, grilleB):
        for x in range(10):
            for y in range(10):
                if (grilleA[x][y]!=grilleB[x][y]):
                    return False
        return True
    
    def genere_grille(self,liste_bateau):
        self.grille=np.zeros((10,10),dtype=int)
        for bateau in liste_bateau:
            self.place_alea(bateau)
    
def q2(taille_bateau):
    taille_grille=10
    compteur=0
    for i in range(taille_grille):
        for j in range(taille_grille):
            if(i+taille_bateau<=taille_grille):
                compteur+=1
            if(j+taille_bateau<=taille_grille):
                compteur+=1
    return compteur
    
def annexe_q3(grille,liste_bateau):
    taille_grille=10
    if(len(liste_bateau)==0):
        return 1

    compteur=0
    bateau=liste_bateau[0]
    taille_bateau=Grille_bataille_navale.taille_bat(bateau)
    for i in range(taille_grille):
        for j in range(taille_grille):
            #en position verticale
            k1=True
            for x in range(i,i+taille_bateau):
                grille_copie=grille.copy()
                if(x>=taille_grille or grille[x][j]!=0):
                    #dans ce cas le bateau ne peut pas être placé ici
                    k1=False
                else:
                    #la case grille_copie[x][j] est maintenant occupée
                    grille_copie[x][j]=1
            #on vérifie que la place est valide, si oui on regarde tous les choix possibles avec le bateau à cette place
            if(k1):
                compteur+=annexe_q3(grille_copie,liste_bateau[1:])
                
            #en position horizontale
            k2=True
            for y in range(j,j+taille_bateau):
                grille_copie=grille.copy()
                if(y>=taille_grille or grille[i][y]!=0):
                    k2=False
                else:
                    grille_copie[i][y]=1
            if(k2):
                compteur+=annexe_q3(grille_copie,liste_bateau[1:])
    return compteur

def q3(liste_bateau):#liste_bateau de la forme [taille_bateau1,taille_bateau2...]
    grille=np.zeros((10,10),dtype=int)        
    return annexe_q3(grille,liste_bateau)
    
    
def q4(grille,liste_bateau):
    grille2=Grille_bataille_navale()
    grille2.genere_grille(liste_bateau)
    compteur=1
    while(not Grille_bataille_navale.eq(grille2.get_grille(),grille.get_grille())):
        compteur+=1
        grille2.genere_grille(liste_bateau)
    grille.affiche()
    grille2.affiche()
    return compteur


###TME3

def factorielle(n):
    res=1
    for i in range(1,n+1):
        res*=i
    return res
def i_parmi_n(i,n):
    return factorielle(n)/(factorielle(i)*factorielle(n-i))
    
def bernouilli(k,n,p):
    return i_parmi_n(k,n)*(p**k)*((1-p)**(n-k))
    
def calcul_esperance():
    esperance = 0
    o=2**83
    for n in range(17,101):
        b=n-17
        #proba=i_parmi_n(b,83)/o
        esperance+=proba*n
    return esperance
    
class Bataille:
    def __init__(self):
        self.grille=Grille_bataille_navale()
        self.grille.genere_grille([1,2,3,4,5])
        
    def deja_tire(self,i,j):
        g=self.grille.get_grille()
        return g[i][j]==9
        
    def joue(self,position):
        #la fonction renvoie 0 si la case est vide -1 si touché et le num du bateau si il est coulé
        g=self.grille.get_grille()
        contenu=g[position[0]][position[1]]
        g[position[0]][position[1]]=9
        if(contenu==0):
            return 0
        for i in range(10):
            for j in range(10):
                if(g[i][j]==contenu):
                    return -1
        return contenu
        
    def victoire(self):
        g=self.grille.get_grille()
        for i in range(10):
            for j in range(10):
                if(g[i][j]!=0 and g[i][j]!=9):
                    return False
        return True
        
    def affiche_grille_chiffre(self):
        print("\n")
        self.grille.affiche_chiffres()
        
    def reset(self):
        self.grille=Grille_bataille_navale()
        self.grille.genere_grille([1,2,3,4,5])
        
    def coup_aleatoire_pas_deja_choisi(self):
        i=random.randrange(10)
        j=random.randrange(10)
        while(self.deja_tire(i,j)):
            i=random.randrange(10)
            j=random.randrange(10)
        return[i,j]  
    
        
class Joueur:
    def __init__(self,b):
        self.bataille=b
        
    def taille_bat(self,bateau):
        return Grille_bataille_navale.taille_bat(bateau)
        
    def partie_aleatoire(self):
        compteur_coup=0
        while(not self.bataille.victoire()):
            coup=self.bataille.coup_aleatoire_pas_deja_choisi()
            self.bataille.joue([coup[0],coup[1]])
            compteur_coup+=1
        return compteur_coup
        
    def partie_heuristique(self):
        compteur_coup=0
        while(not self.bataille.victoire()):
            #on commence aléatoirement
            coup=self.bataille.coup_aleatoire_pas_deja_choisi()
            if(self.bataille.joue([coup[0],coup[1]])!=0):
                #on regarde autour de debut_bateau
                for it in [[-1,0],[1,0],[0,-1],[0,1]]:
                    compteur_coup+=self.fct_rec_heuristique(coup[0],coup[1],it)
            compteur_coup+=1
        return compteur_coup
        
    def fct_rec_heuristique(self,i,j,direction):
        compteur_coup=0
        if(not self.bataille.victoire()):
            x=i+direction[0]
            y=j+direction[1]
            if(x>=0 and x<10 and y>=0 and y<10 and not self.bataille.deja_tire(x,y)):
                case=self.bataille.joue([x,y])
                compteur_coup+=1
                if(case!=0):
                    for it in [[-1,0],[1,0],[0,-1],[0,1]]:
                        compteur_coup+=self.fct_rec_heuristique(x,y,it)
        return compteur_coup
        
    def choix_proba(self,grille_proba):
        n_max=-1
        for i in range(len(grille_proba)):
            for j in range(len(grille_proba[i])):
                if(grille_proba[i][j]>n_max):
                    n_max=grille_proba[i][j]
                    i_max=i
                    j_max=j
        return [i_max,j_max]
    
    def peut_placer_joueur(self, bateau, position, direction):
        taille=Grille_bataille_navale.taille_bat(bateau)
        if(direction==1):#1->horizontale
            for x in range(position[0],position[0]+taille):
                if(x<0 or x>=10):
                    return False
            return True
        elif(direction==2):#2-> Verticale
            for y in range(position[1],position[1]+taille):
                if(y<0 or y>=10):
                    return False
            return True
        return False  
          
    def pos_possibles(self,bateau):
        resultat=[]
        for i in range(10):
            for j in range(10):
                for direction in [1,2]:
                    if(self.peut_placer_joueur(bateau,[i,j],direction)):
                        cases_pos=self.annexe_pos_possibles(bateau,[i,j],direction)
                        resultat+=[cases_pos]
        return resultat
        
    def annexe_pos_possibles(self,bateau,position,direction):
        resultat=[]
        if(direction==1):#1->horizontale
            for x in range(position[0],position[0]+self.taille_bat(bateau)):
                resultat+=[[x,position[1]]]
        elif(direction==2):#2->verticale
            for y in range(position[1],position[1]+self.taille_bat(bateau)):
                resultat+=[[position[0],y]]
        return resultat
        
    def intersection_plus(self,positions,pos):   
        resultat=[]
        for p in positions:
            k=0
            for case in p:
                if(case[0]==pos[0] and case[1]==pos[1]):
                    k=1
            if(k==1):
                resultat+=[p]
        return resultat
        
    def intersection_moins(self,positions,pos):   
        resultat=[]
        for p in positions:
            k=0
            for case in p:
                if(case[0]==pos[0] and case[1]==pos[1]):
                    k=1
            if(k==0):
                resultat+=[p]
        return resultat
        
    def ensemble_case(self,liste_pos):
        resultat=[]
        for bateau in range(5):
            for position in liste_pos[bateau]:
                for case in position:
                    k=0
                    for c in resultat:
                        if(case[0]==c[0] and case[1]==c[1]):
                            k=1
                    if(k==0):
                        resultat+=[case]
        return resultat
        
    def proba(self,case,pos_possibles_bateau):
        compteur=0
        denom=0
        for bateau in range(5):
            for position in pos_possibles_bateau[bateau]:
                denom+=1
                for c in position:
                    if (c[0]==case[0] and c[1]==case[1]):
                        compteur+=1
        return compteur/denom
        
    def partie_probabiliste(self):
        compteur=0
        #le type de bateau 1 à la liste d'id 0,le type de bateau 2 à la liste d'id 1...
        liste_tir_bateau=[[] for _ in range(5)]
        #on initialise grille_proba
        grille_proba=np.zeros((10,10))
        #on initialise les positions possibles des bateaux
        pos_possibles_bateaux=[[] for _ in range(5)]
        l=[]
        for bateau in range(1,6):
            pos_possibles_bateaux[bateau-1]=self.pos_possibles(bateau)
            
        while(not self.bataille.victoire()):
            nombre_cases_pos=len(self.ensemble_case(pos_possibles_bateaux))
            for i in range(len(grille_proba)):
                for j in range(len(grille_proba[i])):
                    if(self.bataille.deja_tire(i,j)):
                        proba=0
                    else:
                        proba=self.proba([i,j],pos_possibles_bateaux)
                    grille_proba[i][j]=proba
            position=self.choix_proba(grille_proba)
            case=self.bataille.joue(position)
            compteur+=1
            
            #on filtre les listes des positions possibles des bateaux en fonction de où on a tiré
            for bateau in range(1,6):
                #si on a coulé un bateau
                if(case in [i for i in range(1,6)]):
                    if(case!=bateau):
                        pos_possibles_bateaux[bateau-1]=self.intersection_moins(pos_possibles_bateaux[bateau-1],position)
                #si on a rien touché
                elif(case==0):
                    #on ne garde que les positions qui ne contiennent pas la case "position" 
                    pos_possibles_bateaux[bateau-1]=self.intersection_moins(pos_possibles_bateaux[bateau-1],position)
                #si on a touché un bateau sans le couler
                elif(case==-1):
                    l+=[[position]]

            #self.bataille.affiche_grille_chiffre()
        return compteur
### Bonus Monte-Carlo
    def verif_pos_possibles(self,liste_bateaux,pos_possibles_bateaux):
        #on regarde s'il ya un bateau sans positions possibles
        for bateau in liste_bateaux:
            if(pos_possibles_bateaux[bateau-1]==[]):
                return False
        return True
        
    def verif_contraintes(self,liste_bateaux,grille,liste_tir):
        #on vérifie que toutes les cases touchées sont occupées par un bateau
        for case in liste_tir:
            if(grille[case[0]][case[1]]==0):
                return False
        #on vérifie que tous les bateaux de la liste sont présent sur la grille
        for bateau in liste_bateaux:
            k=0
            for i in range(10):
                if(bateau in grille[i]):
                    k=1
            if(k==0):
                return False
        return True
        
    def grille_aleatoire_rec(self,liste_bateaux,pos_possibles_bateaux,grille,liste_tir):
        if(liste_bateaux==[] or not self.verif_pos_possibles(liste_bateaux,pos_possibles_bateaux)):
            return grille
            
        case_pas_tiree=[-1,-1]
        #on regarde si des cases ou on a tiré sur un bateau sont inoccupées
        for case in liste_tir:
            if(grille[case[0]][case[1]]==0):
                case_pas_tiree=case
        liste_possible=[]
        #si oui alors on prend une position au hasard qui soit sur une des cases qu'on a repéré
        if(case_pas_tiree!=[-1,-1]):
            for i in range(len(liste_bateaux)):
                for i_case_pos in range(len(pos_possibles_bateaux[liste_bateaux[i]-1])):
                    cases=pos_possibles_bateaux[liste_bateaux[i]-1][i_case_pos]
                    for case_pos in cases:
                        if(case_pos[0]==case_pas_tiree[0] and case_pos[1]==case_pas_tiree[1]):
                            liste_possible+=[[i,i_case_pos]]
            if(len(liste_possible)!=0):
                c=random.randrange(len(liste_possible))
                i_bateau=liste_possible[c][0]
                i_pos=liste_possible[c][1]
                bateau=liste_bateaux[i_bateau]
                pos=pos_possibles_bateaux[bateau-1][i_pos]
                    
        #sinon on choisit une position au hasard dans les positions possibles

        if(case_pas_tiree==[-1,-1] or len(liste_possible)==0):
            #on choisit arbitrairement un bateau de la liste
            i_bateau=random.randrange(len(liste_bateaux))
            bateau=liste_bateaux[i_bateau]
            #on choisit arbitrairement une pos dans la liste des positions du bateau choisi
            i_pos=random.randrange(len(pos_possibles_bateaux[bateau-1]))
            pos=pos_possibles_bateaux[bateau-1][i_pos]

        nv_liste_bateaux=liste_bateaux[:i_bateau]+liste_bateaux[i_bateau+1:]
        nv_pos_possibles_bateaux=pos_possibles_bateaux.copy()
        nv_pos_possibles_bateaux[bateau-1]=[]
        grille_copie=grille.copy()
        
        for case in pos:
            grille_copie[case[0]][case[1]]=bateau
            for b in nv_liste_bateaux:
                nv_pos_possibles_bateaux[b-1]=self.intersection_moins(nv_pos_possibles_bateaux[b-1],case)
            
        #bis_pos_possibles_bateaux contient les positions possibles sauf la position qu'on a essayé
        bis_pos_possibles_bateaux=pos_possibles_bateaux.copy()
        l=bis_pos_possibles_bateaux[bateau-1]
        bis_pos_possibles_bateaux[bateau-1]=l[:i_pos]+l[i_pos+1:]
        
        res=self.grille_aleatoire_rec(nv_liste_bateaux,nv_pos_possibles_bateaux,grille_copie,liste_tir)
        if(not self.verif_contraintes(liste_bateaux,res,liste_tir)):
            #si le resultat est invalide, on regarde s'il nous reste des positions pas essayées
            res=self.grille_aleatoire_rec(liste_bateaux,bis_pos_possibles_bateaux,grille,liste_tir)
        return res
        
    def partie_Monte_Carlo(self):
        #nombre de grilles qu'on prend aléatoirement
        n=10
        compteur=0
        liste_tir=[]
        liste_bateau_coule=[]
        #on initialise les positions possibles des bateaux
        pos_possibles_bateaux=[[] for _ in range(5)]
        liste_bateaux=[1,2,3,4,5]
        for bateau in range(1,6):
            pos_possibles_bateaux[bateau-1]=self.pos_possibles(bateau)
        while(not self.bataille.victoire()):
            grille=np.zeros((10,10))
            for i in range(n):
                gr=self.grille_aleatoire_rec(liste_bateaux,pos_possibles_bateaux,np.zeros((10,10)),liste_tir)
                for i in range(10):
                    for j in range(10):
                        b=gr[i][j]
                        if(b!=0 and not ([i,j] in liste_tir)):
                            grille[i][j]+=1/n
            position=self.choix_proba(grille)
            case=self.bataille.joue(position)
            compteur+=1
            #on actualise liste_tir, pos_possibles_bateaux,liste_bateaux
            if(case==-1):
                liste_tir.append(position)
            #on actualise pos_possibles_bateaux
            for bateau in range(1,6):
                #si on a coulé un bateau
                if(case in [i for i in range(1,6)]):
                    pos_possibles_bateaux[bateau-1]=self.intersection_moins(pos_possibles_bateaux[bateau-1],position)
                    pos_possibles_bateaux[case-1]=self.intersection_plus(pos_possibles_bateaux[bateau-1],position)
                #si on a rien touché
                elif(case==0):
                    #on ne garde que les positions qui ne contiennent pas la case "position" 
                    pos_possibles_bateaux[bateau-1]=self.intersection_moins(pos_possibles_bateaux[bateau-1],position)
                #si on a touché un bateau sans le couler
            
        return compteur
  
### main tme2
"""
grille=Grille_bataille_navale()
grille.genere_grille(liste_bateau)
print(q3(liste_bateau))
print(q4(grille,liste_bateau))

print(calcul_esperance())
"""
### main tme3
"""
b=Bataille()
j=Joueur(b)
#print(j.partie_probabiliste())

compteur=0
n=100
liste_aff=[0. for _ in range(n)]
for i in range(n):
    #s=j.partie_heuristique()
    #s=j.partie_aleatoire()
    s=j.partie_probabiliste()
    liste_aff[i]=s
    compteur+=s
    b.reset()

print("moyenne : ",compteur/n)

#avec la fct heuristique on a environ 66 coups à chaque partie
#avec la fct probabiliste on a environ 66 coups à chaque partie aussi

plt.hist(liste_aff,[17+i for i in range(84)])
plt.xlim(17,100)
plt.show() # affiche la figure a l'ecran
"""
### main tme4

b=Bataille()
j=Joueur(b)
p=[[] for _ in range(5)]
"""
for i in range(5):
    p[i]=j.pos_possibles(i+1)
print(j.grille_aleatoire_rec([1,2,3,4,5],p,np.zeros((10,10)),[[8,6]]))
"""
print(j.partie_Monte_Carlo())
