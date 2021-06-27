
def delta(dep, ari):
    return (abs(ari[0]-dep[0]), abs(ari[1]-dep[1]))

def deplac(dep, ari):
    return (ari[0]-dep[0], ari[1]-dep[1])

class Piece:
    def __init__(self, game, camps, id_piece, pos):
        self.game = game
        self.pos = pos
        self.camps = camps
        self.id_piece = id_piece
        self.nom = "Piece"
        self.compteur_bouge = 0


class Pion(Piece):
    def __init__(self, game, camps, id_piece, pos):
        super().__init__(game, camps, id_piece, pos)
        self.nom = "Pion"
    
    def move(self, nv_pos, plateau = None):
        if plateau is None:
            plateau = self.game.plateau
        c = plateau[nv_pos[1]][nv_pos[0]]
        d = deplac(self.pos, nv_pos)
        if self.camps == 0:
            if d == (0, 1):
                return c == None
            elif d == (0, 2):
                return self.pos[1] == 1
            elif d == (1, 1) or d == (-1, 1):
                if c != None:
                    return c.camps != self.camps
        elif self.camps == 1:
            if d == (0, -1):
                return c == None
            elif d == (0, -2):
                return self.pos[1] == 6
            elif d == (1, -1) or d == (-1, -1):
                if c != None:
                    return c.camps != self.camps
        return False
    
    def coups_pos(self, plateau = None):
        if plateau is None:
            plateau = self.game.plateau
        #
        COUPS = []
        #
        if self.camps == 0:
            #
            p = (self.pos[0], self.pos[1]+2)
            if self.pos[1] == 1 and plateau[p[1]][p[0]] is None:
                COUPS.append(p)
            #
            if self.pos[1] + 1 < 8:
                p = (self.pos[0], self.pos[1]+1)
                if plateau[p[1]][p[0]] is None:
                    COUPS.append(p)
                #
                if self.pos[0] + 1 < 8:
                    p = (self.pos[0]+1, self.pos[1]+1)
                    c = plateau[p[1]][p[0]]
                    if c is not None and c.camps != self.camps:
                        COUPS.append(p)
                #
                if self.pos[0]-1 >= 0:
                    p = (self.pos[0]-1, self.pos[1]+1)
                    c = plateau[p[1]][p[0]]
                    if c is not None and c.camps != self.camps:
                        COUPS.append(p)

        elif self.camps == 1:
            #
            p = (self.pos[0], self.pos[1]-2)
            if self.pos[1] == 6 and plateau[p[1]][p[0]] is None:
                COUPS.append(p)
            #
            if self.pos[1] - 1 >= 0:
                p = (self.pos[0], self.pos[1]-1)
                if plateau[p[1]][p[0]] is None:
                    COUPS.append(p)
                #
                if self.pos[0] + 1 < 8:
                    p = (self.pos[0]+1, self.pos[1]-1)
                    c = plateau[p[1]][p[0]]
                    if c is not None and c.camps != self.camps:
                        COUPS.append(p)
                #
                if self.pos[0] - 1 >= 0:
                    p = (self.pos[0]-1, self.pos[1]-1)
                    c = plateau[p[1]][p[0]]
                    if c is not None and c.camps != self.camps:
                        COUPS.append(p)
        #
        return COUPS


class Fou(Piece):
    def __init__(self, game, camps, id_piece, pos):
        super().__init__(game, camps, id_piece, pos)
        self.nom = "Fou"
    
    def move(self, nv_pos, plateau = None):
        if plateau is None:
            plateau = self.game.plateau
        c = plateau[nv_pos[1]][nv_pos[0]]
        d = deplac(self.pos, nv_pos)
        if abs(d[0]) == abs(d[1]): # On est bien sur une diagonale
            # Il faut maintenant regarder s'il y a un pion qui bloque la diagonale
            dx = d[0]/abs(d[0])
            dy = d[1]/abs(d[1])
            X = self.pos[0]+dx
            Y = self.pos[1]+dy
            #
            while X != nv_pos[0]:
                #
                p = plateau[int(Y)][int(X)]
                if p != None:
                    return False
                # On passe a la case suivante
                Y += dy
                X += dx
            #
            return c == None or c.camps != self.camps                    
        return False
    
    def coups_pos(self, plateau = None):
        if plateau is None:
            plateau = self.game.plateau
        #
        COUPS = []
        for (dx, dy) in [(1,1), (1,-1), (-1,1), (-1,-1)]:
            x,y = self.pos
            while x + dx >= 0 and x + dx < 8 and y + dy >= 0 and y + dy < 8:
                x += dx
                y += dy
                c = plateau[y][x]
                if c is None:
                    COUPS.append((x, y))
                else:
                    if c.camps != self.camps:
                        COUPS.append((x, y))
                    break
        #
        return COUPS


class Cavalier(Piece):
    def __init__(self, game, camps, id_piece, pos):
        super().__init__(game, camps, id_piece, pos)
        self.nom = "Cavalier"
    
    def move(self, nv_pos, plateau = None):
        if plateau is None:
            plateau = self.game.plateau
        d = delta(self.pos, nv_pos)
        c = plateau[nv_pos[1]][nv_pos[0]]
        if d == (1, 2) or d == (2, 1):
            return c == None or c.camps != self.camps
        return False
    
    def coups_pos(self, plateau = None):
        if plateau is None:
            plateau = self.game.plateau
        #
        COUPS = []
        #
        for (x,y) in [(2,1), (-2,1), (2,-1), (-2,-1), (1,2), (1, -2), (-1, 2), (-1, -2)]:
            if self.pos[1] + y >= 0 and self.pos[1] + y < 8 and self.pos[0] + x >= 0 and self.pos[0] + x < 8:
                c = plateau[self.pos[1]+y][self.pos[0]+x]
                if c is None or c.camps != self.camps:
                    COUPS.append((self.pos[0]+x, self.pos[1]+y))
        #
        return COUPS


class Tour(Piece):
    def __init__(self, game, camps, id_piece, pos):
        super().__init__(game, camps, id_piece, pos)
        self.nom = "Tour"
    
    def move(self, nv_pos, plateau = None):
        if plateau is None:
            plateau = self.game.plateau
        c = plateau[nv_pos[1]][nv_pos[0]]
        d = deplac(self.pos, nv_pos)
        if (d[0] == 0 or d[1] == 0) and d[0]!=d[1]: # On est bien sur une ligne
            # Il faut maintenant regarder s'il y a un pion qui bloque la ligne
            if d[0] == 0:
                dx = 0
                dy = d[1]/abs(d[1])
            elif d[1] == 0:
                dx = d[0]/abs(d[0])
                dy = 0
            X,Y = self.pos[0]+dx, self.pos[1]+dy
            #
            while X != nv_pos[0] or Y != nv_pos[1]:
                #
                p = plateau[int(Y)][int(X)]
                if p != None:
                    return False
                # On passe a la case suivante
                Y += dy
                X += dx
            #
            return c == None or c.camps != self.camps              
        return False
    
    def coups_pos(self, plateau = None):
        if plateau is None:
            plateau = self.game.plateau
        #
        COUPS = []
        #
        for x in range(self.pos[0]+1, 8):
            c = plateau[self.pos[1]][x]
            if c is None:
                COUPS.append((x, self.pos[1]))
            else:
                if c.camps != self.camps:
                    COUPS.append((x, self.pos[1]))
                break
        #
        for x in range(self.pos[0]-1, -1, -1):
            c = plateau[self.pos[1]][x]
            if c is None:
                COUPS.append((x, self.pos[1]))
            else:
                if c.camps != self.camps:
                    COUPS.append((x, self.pos[1]))
                break
        #
        for y in range(self.pos[1]+1, 8):
            c = plateau[y][self.pos[0]]
            if c is None:
                COUPS.append((self.pos[0], y))
            else:
                if c.camps != self.camps:
                    COUPS.append((self.pos[0], y))
                break
        #
        for y in range(self.pos[1]-1, -1, -1):
            c = plateau[y][self.pos[0]]
            if c is None:
                COUPS.append((self.pos[0], y))
            else:
                if c.camps != self.camps:
                    COUPS.append((self.pos[0], y))
                break
        #
        return COUPS


class Dame(Piece):
    def __init__(self, game, camps, id_piece, pos):
        super().__init__(game, camps, id_piece, pos)
        self.nom = "Dame"
    
    def move(self, nv_pos, plateau = None):
        if plateau is None:
            plateau = self.game.plateau
        c = plateau[nv_pos[1]][nv_pos[0]]
        d = deplac(self.pos, nv_pos)
        if (d[0] == 0 or d[1] == 0) and d[0]!=d[1]: # On est bien sur une ligne
            # Il faut maintenant regarder s'il y a un pion qui bloque la ligne
            if d[0] == 0:
                dx = 0
                dy = d[1]/abs(d[1])
            elif d[1] == 0:
                dx = d[0]/abs(d[0])
                dy = 0
            X,Y = self.pos[0]+dx, self.pos[1]+dy
            #
            while X != nv_pos[0] or Y != nv_pos[1]:
                #
                p = plateau[int(Y)][int(X)]
                if p != None:
                    return False
                # On passe a la case suivante
                Y += dy
                X += dx
            #
            return c == None or c.camps != self.camps

        if abs(d[0]) == abs(d[1]): # On est bien sur une diagonale
            # Il faut maintenant regarder s'il y a un pion qui bloque la diagonale
            dx = d[0]/abs(d[0])
            dy = d[1]/abs(d[1])
            X = self.pos[0]+dx
            Y = self.pos[1]+dy
            #
            while X != nv_pos[0]:
                #
                p = plateau[int(Y)][int(X)]
                if p != None:
                    return False
                # On passe a la case suivante
                Y += dy
                X += dx
            #
            return c == None or c.camps != self.camps                    
        return False
    
    def coups_pos(self, plateau = None):
        if plateau is None:
            plateau = self.game.plateau
        #
        COUPS = []
        return COUPS


class Roi(Piece):    
    def __init__(self, game, camps, id_piece, pos):
        super().__init__(game, camps, id_piece, pos)
        self.nom = "Roi"
    
    def move(self, nv_pos, plateau = None):
        if plateau is None:
            plateau = self.game.plateau
        c = plateau[nv_pos[1]][nv_pos[0]]
        d = deplac(self.pos, nv_pos)
        #
        if d[0] in [-1, 0, 1] and d[1] in [-1, 0, 1] and not(d[0]==0 and d[1]==0):
            return c == None or c.camps != self.camps
        return False
    
    def coups_pos(self, plateau = None):
        if plateau is None:
            plateau = self.game.plateau
        #
        COUPS = []
        for x in range(-1, 2):
            for y in range(-1, 2):
                if not (x == 0 and y == 0):
                    X, Y = self.pos[0] + x, self.pos[1] + y
                    c = plateau[Y][X]
                    if c is None or c.camps != self.camps:
                        COUPS.append((X, Y))
        return COUPS



pieces_id = {
    0: Pion,
    1: Fou,
    2: Cavalier,
    3: Tour,
    4: Dame,
    5: Roi
}


