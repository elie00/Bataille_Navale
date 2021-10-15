# -*- coding: utf-8 -*-


# --- IMPORTATION DES MODULES ---

# --- Importation modules standards ---
import tkinter, tkinter.messagebox, random

# --- INITIALISATION GÉNÉRALE ---
LST_Joueur = [[None] * 10 for kligne in range(10)]
LST_Python = [[None] * 10 for kligne in range(10)]
LST_Adversaire = []
DCT_Donnees = {"joueur": [0, 0], "python": [0, 0]}


# --- DÉFINITION DES  FONCTIONS ---

# --- Analyse du tir du joueur ---
def FNC_Analyse():
    # --- Conversion des coordonnées ---
    kcolonne = ord(SPI_Colonnes.get()) - 65
    kligne = int(SPI_Lignes.get())

    # --- Analyse de la case choisie ---
    if LST_Python[kcolonne][kligne]["text"] == chr(8776):
        kcase = str(kcolonne) + str(kligne)

        # --- Le tir a touché-coulé un bateau de Python ---
        if kcase in LST_Adversaire:
            LST_Python[kcolonne][kligne]["text"] = chr(10702)
            LST_Adversaire.remove(kcase)
            LAB_Python["text"] = int(LAB_Python["text"]) - 1
            LAB_Message["text"] = "Votre tir\n*** COULE ***"

        # --- Le tir a raté les bateaux de Python ---
        else:
            LST_Python[kcolonne][kligne]["text"] = chr(10008)
            LAB_Message["text"] = "Votre tir\n--- RATE ---."

    if int(LAB_Python["text"]) == 0:
        FNC_Gagne()
    else:
        FNC_Python()


# --- Le joueur a gagné ---
def FNC_Gagne():
    LAB_Message["foreground"] = "red"
    LAB_Message["background"] = "yellow"
    LAB_Message["text"] = "FELICITATION\nc'est gagné."
    FNC_Termine()


# --- Le joueur a perdu ---
def FNC_Perdu():
    LAB_Message["foreground"] = "lime"
    LAB_Message["background"] = "black"
    LAB_Message["text"] = "CALAMITE\nc'est perdu."
    for kbateau in LST_Adversaire:
        kcolonne = int(kbateau[0])
        kligne = int(kbateau[1])
        LST_Python[kcolonne][kligne]["foreground"] = "yellow"
        LST_Python[kcolonne][kligne]["background"] = "red"
        LST_Python[kcolonne][kligne]["text"] = chr(10699)
    FNC_Termine()


# --- Placement des bateaux ---
def FNC_Placement():
    # --- Placement des bateaux du joueur ---
    kcolonne = ord(SPI_Colonnes.get()) - 65
    kligne = int(SPI_Lignes.get())
    if LST_Joueur[kcolonne][kligne]["text"] != chr(10699):
        LST_Joueur[kcolonne][kligne]["text"] = chr(10699)
        LST_Joueur[kcolonne][kligne]["foreground"] = "blue"
        LST_Joueur[kcolonne][kligne]["background"] = "aqua"
        LAB_Joueur["text"] = int(LAB_Joueur["text"]) + 1
        kaccord = "bateau" if int(LAB_Joueur["text"]) == 10 else "bateaux"
        LAB_Message["text"] = f"Il vous reste {10 - int(LAB_Joueur['text'])}\n{kaccord} à placer."
    else:
        LAB_Message["text"] = "### ERREUR ###\ncase occupée."

    # --- Placement (aléatoire) des bateaux de Python ---
    if int(LAB_Joueur["text"]) == 10:
        for kbateau in range(10):
            while True:
                kcolonne = random.choice(range(10))
                kligne = random.choice(range(10))
                kposition = str(kcolonne) + str(kligne)
                if kposition in LST_Adversaire: continue
                LST_Adversaire.append(kposition)
                break

        # --- Basculement en phase jouer ---
        LAB_Python["text"] = 10
        LAB_Phase["text"] = "phase\nJOUER"
        LAB_Message["text"] = "Choisissez une case\net valider votre tir."
        TKI_Principal.geometry("+200+200")
        FRM_Python.grid()
        FNC_Visualiser()


# --- Tir(aléatoire) de Python ---
def FNC_Python():
    # --- Initialisation du tir de python ---
    LST_Joueur[DCT_Donnees["python"][0]][DCT_Donnees["python"][1]]["foreground"] = "blue"
    LST_Joueur[DCT_Donnees["python"][0]][DCT_Donnees["python"][1]]["background"] = "aqua"
    kmessage = "Python choisi la\ncase "
    kicone = "info"
    kencre = "aqua"
    kfond = "blue"

    # --- Recherche d'un tir (aléatoire) possible pour Python ---
    while True:
        kcolonne = int(random.choice("0123456789"))
        kligne = int(random.choice("0123456789"))
        DCT_Donnees["python"] = [kcolonne, kligne]

        # --- Tir raté de Python ---
        if LST_Joueur[kcolonne][kligne]["text"] == chr(8776):
            LST_Joueur[kcolonne][kligne]["text"] = chr(10008)
            kmessage += f"[ {chr(65 + kcolonne)} - {kligne} ] ...\nC'est un tir raté."
            break

        # --- Le tir au but de Python ---
        if LST_Joueur[kcolonne][kligne]["text"] == chr(10699):
            LST_Joueur[kcolonne][kligne]["text"] = chr(10702)
            LAB_Joueur["text"] = int(LAB_Joueur["text"]) - 1
            kmessage += f"[ {chr(65 + kcolonne)} - {kligne} ] ...\nC'est un tir réussi."
            kicone = "warning"
            kencre = "yellow"
            kfond = "red"
            break

    # --- Finalisation du tir de Python ---
    LST_Joueur[DCT_Donnees["python"][0]][DCT_Donnees["python"][1]]["foreground"] = kencre
    LST_Joueur[DCT_Donnees["python"][0]][DCT_Donnees["python"][1]]["background"] = kfond
    tkinter.messagebox.showinfo(title="Python a joué !", message=kmessage, icon=kicone)
    if int(LAB_Joueur["text"]) == 0:
        FNC_Perdu()
    else:
        FNC_Analyse()


# --- Terminer la partie ---
def FNC_Termine():
    BUT_Valider["state"] = "disabled"
    SPI_Colonnes["state"] = "disabled"
    SPI_Lignes["state"] = "disabled"


# --- Aiguillage du bouton de validation ---
def FNC_Valider():
    if "PLACEMENT" in LAB_Phase["text"]:
        FNC_Placement()
    else:
        FNC_Analyse()


# --- Visualisation de la case sélectionnée ---
def FNC_Visualiser():
    kcolonne = ord(SPI_Colonnes.get()) - 65
    kligne = int(SPI_Lignes.get())
    kgrille = LST_Joueur if "PLACEMENT" in LAB_Phase["text"] else LST_Python
    kencre = "blue" if "PLACEMENT" in LAB_Phase["text"] else "navy"
    kfond = "aqua" if "PLACEMENT" in LAB_Phase["text"] else "skyblue"
    kgrille[DCT_Donnees["joueur"][0]][DCT_Donnees["joueur"][1]]["foreground"] = kencre
    kgrille[DCT_Donnees["joueur"][0]][DCT_Donnees["joueur"][1]]["background"] = kfond
    kgrille[kcolonne][kligne]["foreground"] = kfond
    kgrille[kcolonne][kligne]["background"] = kencre
    DCT_Donnees["joueur"] = [kcolonne, kligne]


# --- CRÉATION L'INTERFACE GRAPHIQUE ---

TKI_Principal = tkinter.Tk()
TKI_Principal.title("ON - Bataille Navale 02")
TKI_Principal.geometry("+548+200")

# --- Création des cadres ---
FRM_Joueur = tkinter.LabelFrame(TKI_Principal, text=" *** JOUEUR *** ", labelanchor="n")
FRM_Python = tkinter.LabelFrame(TKI_Principal, text=" *** PYTHON *** ", labelanchor="n")
FRM_Centre = tkinter.Frame(TKI_Principal)

# --- Création des grille de jeu ---
for kligne in range(10):
    tkinter.Label(FRM_Joueur, text=kligne).grid(row=kligne + 1, column=0)
    tkinter.Label(FRM_Joueur, text=kligne).grid(row=kligne + 1, column=11)
    tkinter.Label(FRM_Joueur, text=chr(65 + kligne)).grid(row=0, column=kligne + 1)
    tkinter.Label(FRM_Joueur, text=chr(65 + kligne)).grid(row=11, column=kligne + 1)
    tkinter.Label(FRM_Python, text=kligne).grid(row=kligne + 1, column=0)
    tkinter.Label(FRM_Python, text=kligne).grid(row=kligne + 1, column=11)
    tkinter.Label(FRM_Python, text=chr(65 + kligne)).grid(row=0, column=kligne + 1)
    tkinter.Label(FRM_Python, text=chr(65 + kligne)).grid(row=11, column=kligne + 1)
    for kcolonne in range(10):
        kjoueur = tkinter.Label(FRM_Joueur, text=chr(8776), relief="solid", font=(None, 16), fg="blue", bg="aqua",
                                width=2)
        kpython = tkinter.Label(FRM_Python, text=chr(8776), relief="solid", font=(None, 16), fg="navy", bg="skyblue",
                                width=2)
        kjoueur.grid(row=kligne + 1, column=kcolonne + 1)
        kpython.grid(row=kligne + 1, column=kcolonne + 1)
        LST_Joueur[kcolonne][kligne] = kjoueur
        LST_Python[kcolonne][kligne] = kpython

# --- Création des controles de jeu ---
BUT_Quitter = tkinter.Button(FRM_Centre, text="Quitter", font=(None, 14), command=TKI_Principal.destroy)
LAB_Phase = tkinter.Label(FRM_Centre, text="phase\nPLACEMENT", relief="ridge", bd=4)
LAB_Message = tkinter.Label(FRM_Centre, text="Placez vos\nbateaux.", font=(None, 10), relief="ridge", bd=4, height=2)
FRM_Bateaux = tkinter.Frame(FRM_Centre, relief="ridge", bd=4)
LAB_Joueur = tkinter.Label(FRM_Bateaux, text="0", relief="solid", font=(None, 24), fg="blue", bg="aqua", width=3)
LAB_Python = tkinter.Label(FRM_Bateaux, text="0", relief="solid", font=(None, 24), fg="navy", bg="skyblue", width=3)
tkinter.Label(FRM_Bateaux, text="bateaux restant").grid(row=0, column=0, columnspan=2, sticky="nesw")
tkinter.Label(FRM_Bateaux, text="python", font=(None, 8)).grid(row=1, column=0, sticky="nesw")
tkinter.Label(FRM_Bateaux, text="joueur", font=(None, 8)).grid(row=1, column=1, sticky="nesw")
LAB_Python.grid(row=2, column=0, padx=3, pady=3, sticky="nesw")
LAB_Joueur.grid(row=2, column=1, padx=3, pady=3, sticky="nesw")

FRM_Choix = tkinter.Frame(FRM_Centre, relief="ridge", bd=4)
BUT_Valider = tkinter.Button(FRM_Choix, text="Valider", font=(None, 18), command=FNC_Valider)
SPI_Colonnes = tkinter.Spinbox(FRM_Choix, values=list("ABCDEFGHIJ"), font=(None, 24), justify="center", width=2,
                               command=FNC_Visualiser)
SPI_Lignes = tkinter.Spinbox(FRM_Choix, values=tuple("9876543210"), font=(None, 24), justify="center", width=2,
                             command=FNC_Visualiser)
SPI_Colonnes.grid(row=0, column=0, sticky="nesw")
SPI_Lignes.grid(row=0, column=1, sticky="nesw")
BUT_Valider.grid(row=1, column=0, columnspan=2, sticky="nesw")

LAB_Phase.grid(row=3, column=0, pady=10, sticky="nesw")
FRM_Bateaux.grid(row=4, column=0, sticky="nesw")
FRM_Choix.grid(row=5, column=0, pady=10, sticky="nesw")
LAB_Message.grid(row=6, column=0, sticky="nesw")
BUT_Quitter.grid(row=7, column=0, pady=10, sticky="nesw")

# ---Mise place des panneaux dans la fenetre ---
FRM_Python.grid(row=0, column=0, sticky="nesw")
FRM_Centre.grid(row=0, column=1, padx=10, sticky="nesw")
FRM_Joueur.grid(row=0, column=2, sticky="nesw")

# --- DÉBUT DU PROGRAMME ---
FRM_Python.grid_remove()
FNC_Visualiser()
TKI_Principal.mainloop()

# --- Programme : JFB ---
# --- Mars 2021 ---
# --- Fin ---


