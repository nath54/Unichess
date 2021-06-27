
CX = "ABCDEFGH"
CY = "12345678"


pions = [
    [9823, 9821, 9822, 9820, 9819, 9818],
    [9817, 9815, 9816, 9814, 9813, 9812]
]

clrs1 = {
    "black": 30,
    "red": 31,
    "green": 32,
    "yellow": 33,
    "blue": 34,
    "pink": 35,
    "cyan": 36,
    "white": 37
}

clrs2 = {
    "black": 40,
    "red": 41,
    "green": 42,
    "yellow": 43,
    "blue": 44,
    "pink": 45,
    "cyan": 46,
    "white": 47
}

ENDC = '\033[m' # reset to the defaults

def cl(cl1, cl2):
    return f'\x1b[6;{clrs1[cl1]};{clrs2[cl2]}m'

def aff(game, clrs = False):
    # Intro
    print("-" * 20)
    print(f"Tour n°{game.tour}")
    print(f"C'est à {game.joueurs[game.joueur]} de jouer")
    print("-" * 20)
    # Tableau
    print(" / " + " ".join(list(CX))+ " \\")
    for y in range(8):
        txt = " "+CY[y]+" "
        for x in range(8):
            if clrs:
                if (x+y) % 2 == 0:
                    txt += cl("black","yellow")
                    bg = "yellow"
                else:
                    txt += cl("black","blue")
                    bg = "blue"
            if game.plateau[y][x] is None:
                txt += "_"
            else:
                p = game.plateau[y][x]
                if clrs:
                    txt += cl(["white","black"][p.camps], bg)
                    txt += chr(pions[0][p.id_piece])
                else:
                    txt += chr(pions[p.camps][p.id_piece])
                
            txt += " " # Pour séparer les pieces
            if clrs:
                txt += ENDC
        txt += ""+CY[y]
        print(txt)
    print(" \\ " + " ".join(list(CX))+ " /")
