
from pieces import *
from aff import *

# 0: Pion
# 1: Fou
# 2: Cavalier
# 3: Tour
# 4: Dame
# 5: Roi

#piece
def p(game, id_camps, id_piece, pos):
    if id_piece == 0: return Pion(game, id_camps, id_piece, pos)
    elif id_piece == 1: return Fou(game, id_camps, id_piece, pos)
    elif id_piece == 2: return Cavalier(game, id_camps, id_piece, pos)
    elif id_piece == 3: return Tour(game, id_camps, id_piece, pos)
    elif id_piece == 4: return Dame(game, id_camps, id_piece, pos)
    elif id_piece == 5: return Roi(game, id_camps, id_piece, pos)

class Game:
    def __init__(self):
        self.tour = 0
        self.plateau = [ [None for _ in range(8)] for _ in range(8)]
        self.p1 = "Blanc"
        self.p2 = "Noir"
        self.joueurs = [self.p1, self.p2]
        self.joueur = 0
        self.prep_plateau()
        self.gagne = None
        self.pris = [[],[]]
        self.pions = [{},{}] # Les positions des pions seront placés dans des sets
        self.prep_plateau()
    
    def prep_plateau(self):
        self.plateau = [ 
[p(self,0,3,(0,0)),p(self,0,2,(1,0)),p(self,0,1,(2,0)),p(self,0,4,(3,0)),p(self,0,5,(4,0)),p(self,0,1,(5,0)),p(self,0,2,(6,0)),p(self,0,3,(7,0))],
[p(self,0,0,(0,1)),p(self,0,0,(1,1)),p(self,0,0,(2,1)),p(self,0,0,(3,1)),p(self,0,0,(4,1)),p(self,0,0,(5,1)),p(self,0,0,(6,1)),p(self,0,0,(7,1))],
[None           , None, None, None, None, None, None, None],
[None           , None, None, None, None, None, None, None],
[None           , None, None, None, None, None, None, None],
[None           , None, None, None, None, None, None, None],
[p(self,1,0,(0,6)),p(self,1,0,(1,6)),p(self,1,0,(2,6)),p(self,1,0,(3,6)),p(self,1,0,(4,6)),p(self,1,0,(5,6)),p(self,1,0,(6,6)),p(self,1,0,(7,6))],
[p(self,1,3,(0,7)),p(self,1,2,(1,7)),p(self,1,1,(2,7)),p(self,1,4,(3,7)),p(self,1,5,(4,7)),p(self,1,1,(5,7)),p(self,1,2,(6,7)),p(self,1,3,(7,7))]
        ]
        self.pions = [
            # Joueur 0 :
            {(0,0), (1,0), (2,0), (3,0), (4,0), (5,0), (6,0), (7,0),
             (0,1), (1,1), (2,1), (3,1), (4,1), (5,1), (6,1), (7,1)},
            # Joueur 1 :
            {(0,6), (1,6), (2,6), (3,6), (4,6), (5,6), (6,6), (7,6),
             (0,7), (1,7), (2,7), (3,7), (4,7), (5,7), (6,7), (7,7)}
        ]
    
    def partie_finie(self):
        print("La partie est finie.")
        print("Vous pouvez relancer le programme si vous voulez rejouer")

    def partie_gagnee(self, vainqueur):
        print(f"Le joueur {self.joueurs[vainqueur]} a gagné !")

    def pieces_prises(self):
        print("Les pieces prises sont : \n")
        for j in [0, 1]:
            print(f"  - Joueur {self.joueurs[j]}\n")
            if len(self.pris[j]) == 0:
                print("    Aucune piece n'a été prise\n")
            else:
                # Compteur
                compteur = {}
                for p in self.pris[j]:
                    if p.nom in compteur.keys():
                        compteur[p.nom] += 1
                    else:
                        compteur[p.nom] = 1
                # On affiche
                virg = False
                txt = "    "
                for k in compteur.keys():
                    if virg:
                        txt += ", "
                    else:
                        virg = True
                    txt += k
                    if compteur[k] > 1:
                        txt += f" x {compteur[k]}"
                print(txt)
        print()
    
    def aide(self):
        print("L'aide est en cour de construction, veuillez revenir plus tard ;)")
        # TODO : 
        #  * afficher la liste des commandes
        #  * détailler plus la syntaxe pour jouer un coup
        print("\nBonne chance !")
    
    def test_echec(self):
        # TODO: afficher si il y a une position d'échec
        # Il faut d'abord récuperer la position du roi
        pos_roi = None
        for pos in self.pions[self.joueur]:
            p = self.plateau[pos[1]][pos[0]]
            if p.nom == "Roi":
                pos_roi = pos
                break
        # Une solution est de parcourir tous les coups possibles des adversaires et de tester s'il peut se déplacer sur le roi
        if pos_roi == None:
            raise UserWarning("Il y a un probleme dans le code !")
        #
        echec = False
        aj = 1 if self.joueur == 0 else 0
        for pos in self.pions[aj]:
            p = self.plateau[pos[1]][pos[0]]
            if p.move(pos_roi):
                echec = True
                break
        if echec:
            print("Votre roi est en échec")

    def jouer_coups(self, c1, c2, plateau, joueur, pris, pions):
        c = plateau[c1[1]][c1[0]]
        if c == None:
            print("Il n'y a pas de pieces !")
            input("\nPress Enter to Continue\n")
            return True, False, plateau, joueur, pris, pions # On retourne jouer
        # On vérifie que c'est bien une pièce du bon joueur
        if c.camps != joueur:
            print("Vous ne pouvez pas bouger les pièces des autres !")
            input("\nPress Enter to Continue\n")
            return True, False, plateau, joueur, pris, pions # On retourne jouer
        # On vérifie si la pièce peut bouger
        if c.move(c2): # Détecte tous les obstacles ;)
            # Si il y a une piece sur la case
            # => On la prend ;)
            p = plateau[c2[1]][c2[0]]
            if p != None:
                aj = 1 if joueur == 0 else 0
                pris[aj].append(p)
                pions[aj].remove((c2[0], c2[1]))
                # On vérifie si c'est le roi qui est prit => 
                if p.nom == "Roi":
                    self.partie_gagnee(joueur)
                    return False, True, plateau, joueur, pris, pions
            # On bouge la piece
            c.pos = c2
            c.compteur_bouge += 1
            plateau[c2[1]][c2[0]] = c
            plateau[c1[1]][c1[0]] = None
            pions[joueur].remove((c1[0], c1[1]))
            pions[joueur].add((c2[0], c2[1]))
        else:
            print("La piece ne peut pas jouer ici !")
            input("\nPress Enter to Continue\n")
            return True, False, plateau, joueur, pris, pions # On retourne jouer
        return False, False, plateau, joueur, pris, pions

    # Malheureusement, on a un problème de récursivité avec python
    # Donc on peut aussi utiliser la méthode itérative
    def jouer(self):
        while True:
            # On affiche le plateau
            aff(self)
            # echec
            self.test_echec()
            # On va prendre les inputs des joueurs
            print("\nSyntaxe : [Case de départ] [Case d'arrivée]. Exemple : B8 C6\n taper 'aide' pour plus d'infos\n")
            j = input(": ")
            # Autres commandes ici : 
            if j.lower() in ["quitter", "exit", "q", "shutdown", "poweroff", "quit", "sortir", "salut !"]:
                break
            elif j.lower() in ["pieces prises", "prises", "butins", "scores", "pieces", "p"]:
                self.pieces_prises()
                input("\nPress Enter to Continue\n")
                continue # On retourne jouer
            elif j.lower() in ["aide", "help", "h", "guide", "aidez moi svp"]:
                self.aide()
                input("\nPress Enter to Continue\n")
                continue # On retourne jouer
            elif j.lower().startswith("coups "):
                l = j.split(" ")
                if len(l) != 2:
                    print("Erreur de syntaxe !")
                    input("\nPress Enter to Continue\n")
                    continue # On retourne jouer
                #
                c = l[1]
                if c[0].upper() not in CX or c[1] not in CY:
                    print("Probleme dans la description des cases !")
                    input("\nPress Enter to Continue\n")
                    continue # On retourne jouer
                c = (CX.index(c[0].upper()), CY.index(c[1]))
                p = self.plateau[c[1]][c[0]]
                if p is None:
                    print("Il n'y a pas de pièces ici !")
                    input("\nPress Enter to Continue\n")
                    continue # On retourne jouer
                
                COUPS = p.coups_pos()
                if len(COUPS) == 0:
                    print("La pièce ne peut pas bouger !")
                    input("\nPress Enter to Continue\n")
                    continue # On retourne jouer
                else:
                    print("La pièce peut bouger sur les cases : ")
                    for c in COUPS:
                        print(f"   - {CX[c[0]]}{CY[c[1]]}")
                    input("\nPress Enter to Continue\n")
                    continue # On retourne jouer

            # Si ce n'est pas une autre commande
            l = j.split(" ")
            #
            if len(l)!=2 or not all([len(p)==2 for p in l]):
                print("Erreur de syntaxe !")
                input("\nPress Enter to Continue\n")
                continue # On retourne jouer
            #
            c1,c2 = l[0], l[1]
            if c1[0].upper() not in CX or c2[0].upper() not in CX \
            or c1[1] not in CY or c2[1] not in CY:
                print("Probleme dans la description des cases !")
                input("\nPress Enter to Continue\n")
                continue # On retourne jouer
            #
            c1 = (CX.index(c1[0].upper()), CY.index(c1[1]))
            c2 = (CX.index(c2[0].upper()), CY.index(c2[1]))
            
            #
            res = self.jouer_coups(c1, c2, self.plateau, self.joueur, self.pris, self.pions)
            cont, brake, self.plateau, self.joueur, self.pris, self.pions = res

            if cont:
                continue
            
            if brake:
                break

            # On a bien bougé le coup
            # Donc on va changer le joueur et continuer la partie jusqu'à la fin.
            if self.joueur == 1:
                self.joueur = 0
                self.tour += 1
            else:
                self.joueur = 1

        aff(self)
        self.partie_finie()

