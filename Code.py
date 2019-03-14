from tkinter import*
from random import*
from time import*

fen = Tk()
fen.title(" Snake updated 2.0")
fen.geometry('550x215')
fichier_fond = PhotoImage(file = "fond_vert.gif") # était fond_vert.gif (2015)
fichier_snake = PhotoImage(file = "Snake_skin.gif")
fichier_pomme = PhotoImage(file = "pomme.gif")
fichier_jeu = PhotoImage(file="image_jouer.gif")
fichier_jeu_difficile = PhotoImage(file="image_jouer_difficile.gif")
fichier_score = PhotoImage(file="image_scores.gif")
fichier_quitter = PhotoImage(file="image_quitter.gif")
fichier_pomme_or = PhotoImage(file="pomme d'or.gif")

# On déclare les variables globales
C = Canvas(fen, width=768, height=608) # Ce Canvas utilisé pour le jeu
snake = [] # Liste stockant les images constituant le serpent
coord = [] # Liste contenant les coordonnées du serpent
coord_pomme = [] # Liste contenant les coordonnées de la pomme
coord_pomme_or = [] # Liste contenant les coordonnées de la pomme d'or
d = 0 # Variable indiquant la direction dans laquelle se dirige le serpent (1=haut, 2=bas, 3=droite, 4=gauche)
compteurs = [] # Dès que le serpent mangera une pomme, on ajoutera a cette liste une petite liste contenant la taille du serpent et les coordonnées de la pomme mangée : compteurs.append( [ len(coord) , [xpomme, ypomme] ). Le 'len(coord)' joue le rôle de compte à rebour avant d'ajouer un carré aux coordonnées indiquées.
score = 0 # Cette variable compte le score du joueur
test = True # Quand cette variable passe en 'False', on ne pourra pas donner une autre direction au serpent. On fait cela quand l'utilisateur veut retourner sur ses pas avec le snake ou quand il relance la fonction pour se déplacer dans la direction dans laquelle il se dirige déjà
pseudo = StringVar() # Ici on stock le pseudo du joueur à la fin du jeu grâce à un Entry
pomme = C.create_image(0 , 0) # Création de l'image de la pomme
pomme_or = C.create_image(0, 0) # Création de l'image de la pomme d'or
txt_score = C.create_text(10 ,10) # Création de l'image de la pomme
mod = 0 # Définit le mode de jeu sélectionné, 1=normal 2=difficile
lst_obstacles = [] # Contient les coordonnées des obstacles sous forme de tuples (car on a pas besoin de les modifier)
stop = False # Indique si le jeu est mis en pause
d_test = False # Joue un rôle dans la pause et la reprise du déplacement
test_fond = False # Indique si il y a une image en place dans le menu à droite



# Ceci est la fonction principale du programme, contenant toutes les autres.
# On a eu besoin de faire une fonction de ce genre afin de pouvoir faire un retour au menu et rejouer encore et encore.
def main():
    global mod
    global d
    global compteurs
    global score
    global test
    global lst_obstacles
    global obstacles
    global pseudo

# Ici on remet à leur état initial toutes les variables utilisées pendant le jeu pour repartir à zéro
    fen.geometry('772x215')
    d = 0
    compteurs = []
    mod = 0
    score = 0
    test = True
    pseudo = StringVar()
    obstacles = []
    lst_obstacles = []
    A = Canvas(fen, width=200, height=200)


# Fonction de détection de la pomme d'or, elle ajoute aussi +3 au score
    def manger_or():
        global score
        # On execute la suite que si la pomme existe, c'est à dire si elle a des coordonées
        if len(coord_pomme_or) > 0 :
            if (coord[0][0] == coord_pomme_or[0]) and (coord[0][1] == coord_pomme_or[1]):
                score += 3
                C.itemconfig(txt_score, text= "SCORE : " + str(score))
                despawn_or()


# Cette fonction fait disparaitre la pomme d'or et déclenche un compte a rebour avant d'en faire réapparaitre une autre
    def despawn_or():
        global coord_pomme_or
        global pomme_or
        if len(coord_pomme_or) > 0 :
            C.delete(pomme_or)
            coord_pomme_or = []
            fen.after(randrange(8000, 15000), spawn_or)


# Cette fonction fait apparaitre la pomme d'or et déclenche un compte a rebour avant de la faire disparaitre
    def spawn_or():
        global coord_pomme_or
        global pomme_or
        coord_pomme_or = spawn()
        pomme_or = C.create_image(coord_pomme_or[0], coord_pomme_or[1], image=fichier_pomme_or, anchor='nw')
        fen.after(randrange(3000, 6000), despawn_or)


# Dans le menu, si on enlève la souris d'un bouton, on fait disparaitre l'image du canvas A
    def fd_leave_bis():
        global test_fond
        if test_fond == True :
            A.delete(ALL)
            A.forget()
            test_fond = False
    def fd_leave(evt):
        return fd_leave_bis()
    
# Les 4 fonctions à venir font apparaitre une image dans le menu
    def fd_jeu(evt):
        global test_fond
        if test_fond  == False :
            A.place(x=565, y=4)
            fond_score = A.create_image(2, 2, image= fichier_jeu, anchor = 'nw')
            test_fond = True
    def fd_jeu_difficile(evt):
        global test_fond
        if test_fond  == False :
            A.place(x=565, y=4)
            fond_score = A.create_image(2, 2, image= fichier_jeu_difficile, anchor = 'nw')
            test_fond = True
    def fd_score(evt):
        global test_fond
        if test_fond  == False :
            A.place(x=565, y=4)
            fond_score = A.create_image(2, 2, image= fichier_score, anchor = 'nw')
            test_fond = True
    def fd_quitter(evt):
        global test_fond
        if test_fond  == False :
            A.place(x=565, y=4)
            fond_score = A.create_image(2, 2, image= fichier_quitter, anchor = 'nw')
            test_fond = True
   

    def pause(evt):
        global stop
        if test == True and stop == False :
            stop = True
            def reprendre():
                global stop
                global d_test
                # Quand stop est en True, le snake s'arrête d'avancer, donc on le remet en False pour que le jeu puisse reprendre
                stop = False
                d_test = True
                bou7.destroy()
            bou7 = Button(fen, text='Reprendre', command=reprendre)
            bou7.place(x=386, y=306)
        

    def destruction():
        bou1.destroy()
        bou2.destroy()
        bou3.destroy()
        txt.destroy()
        bou6.destroy()


    def nb(a, i):
        e = 0   # Quand on récupère les scores lignes par lignes dans le fichier texte,
                # il nous faut connaitre l'index à partir du quel on passe du score au
                # pseudo du joueur, par exemple : dans "30, Joueur" , on retournera 3-1
        test3 = True    # Cette variable contrôle la boule while, quand on détecte qu'on arrive au pseudo du joueur, on arrête la boucle
        while test3 == True :
            for f in range(10):
                if list(a[i][e])[0] == str(f):
                    test3 = False
            if test3 == False:
                test3 = True
            else :
                test3 = False
            e += 1
        return e-1


# Dans cette fonction on ajoute notre score et notre pseudo au fichier scores.txt
    def fin():
        global pseudo
        def ajouter():
            fichier_score = open("Scores.txt", "r")
            lst = fichier_score.readlines()
            fichier_score.close()
            if len(lst) > 0 :
                fichier_score = open("Scores.txt", "r")
                i = 0
                test2 = True
                while (i < len(lst)) and (test2 == True):
                    if (score >= int(lst[i][:nb(lst, i)])):
                        lst.insert(i, str(score)+', '+pseudo.get()+'\n')
                        test2 = False
                    i += 1
                if test2 == True :
                    lst.append(str(score)+', '+pseudo.get()+'\n')
                "".join(lst)
                fichier_score.close()
                fichier_score = open("Scores.txt", "w")
                fichier_score.writelines(lst)
                fichier_score.close()
            else :
                fichier_score = open("Scores.txt", "w")
                fichier_score.writelines(str(score)+', '+pseudo.get()+'\n')
                fichier_score.close()
            bou4.destroy()
            txt2.destroy()
            txt3.destroy()
            E.destroy()
            return main()
        fen.geometry('400x650')
        bou4 = Button(fen, text='Valider', anchor='center', command=ajouter)

        bou4.place(x=160, y=300)
        pseudo = StringVar()
        txt2 = Label(fen, text='Votre pseudo :')
        txt2.place(x=150, y=240)
        txt3 = Label(fen, text='SCORE : '+str(score))
        txt3.place(x=160, y=150)
        E = Entry(fen , textvariable = pseudo, width=30)
        E.place(x=70, y=270)


    def kill():
        global test
        C.delete(ALL)
        C.destroy()
        test = False
        return fin()


    def collision():
        if mod == 1 and ((coord[0][0] == 2) or (coord[0][1] == 2) or (coord[0][0] == 754) or (coord[0][1] == 594)):
            return kill()
        elif test_obstacles() == True :
            return kill()
        elif len(coord) > 4:
            for i in range(4, len(coord)):
                # En effet, on ne peut se mordre la queue que si le serpent fait 5 cases ou plus
                if (coord[i][0] == coord[0][0]) and (coord[i][1] == coord[0][1]) :
                    return kill()


# Cette fonction détecte si l'objet va apparaitre au même endroit qu'un autre objet
    def test_spawn(x, y):
        if len(coord_pomme) > 0:    # Objet et pomme
            if (coord_pomme[0] == x) and (coord_pomme[1] == y): 
                return True
        if len(coord_pomme_or) > 0:     # Objet et pomme d'or
            if (coord_pomme_or[0] == x) and (coord_pomme_or[1] == y):
                return True
        if len(coord) > 0 :     # Objet et serpent
            for i in coord :
                if (i[0] == x) and (i[1] == y):
                    return True
        for i in lst_obstacles :    # Objet et obstacles
            if (i[0] == x) and (i[1] == y):
                return True
        return False
        

# La fonction d'apparition de la pomme, de la pomme d'or et du snake
    def spawn():
        place = True   # Si place devient True, c'est que l'objet a été placé sans problèmes
        x = randrange(18, 739, 16)
        y = randrange(18, 579, 16)
        while place == True :
            place = test_spawn(x, y)
            if place == True :
                x = randrange(18, 739, 16)
                y = randrange(18, 595, 16)
        return [x, y]

    # La fonction de détection de la collision entre une pomme(rouge) et le serpent, elle ajoute aussi +1 au score
    def manger():
        global score
        global coord_pomme
        global compteurs
        if (coord[0][0] == coord_pomme[0]) and (coord[0][1] == coord_pomme[1]):
            score += 1
            C.itemconfig(txt_score, text= "SCORE : " + str(score))
            compteurs.append([len(coord), [coord_pomme[0], coord_pomme[1]]])
            coord_pomme = spawn()
            C.coords(pomme, coord_pomme[0], coord_pomme[1])
            

    def obstacles():
        global lst_obstacles
        lst_obstacles.append((114, 114))
        lst_obstacles.append((114, 482))
        lst_obstacles.append((642, 114))
        lst_obstacles.append((642, 482))
        for i in range(16, 81, 16):
            lst_obstacles.append((114+i, 114))
            lst_obstacles.append((114, 114+i))
            lst_obstacles.append((642, 114+i))
            lst_obstacles.append((642-i, 114))
            lst_obstacles.append((114, 482-i))
            lst_obstacles.append((114+i, 482))
            lst_obstacles.append((642-i, 482))
            lst_obstacles.append((642, 482-i))
        for i in lst_obstacles :
            C.create_image(i[0], i[1], image=fichier_snake, anchor='nw')

    def test_obstacles():
        for i in lst_obstacles:
            if (i[0] == coord[0][0]) and (i[1] == coord[0][1]):
                return True
        return False
            

            # Déplacement vers le haut
    def Hbis():
        global coord
        global compteurs
        global snake
        if d == 1 :
            coord.insert(0, coord[0][::])
            coord[0][1] -= 16
            del(coord[len(coord)-1])
            print(compteurs)
            if len(compteurs)>0 :   # Si une pomme a été mangée précédemment
                if (compteurs[0][0] == 1):  # Comme dit en début de programme, compteurs est une liste de taille variable contenant des sous
                                            # listes de taille 2. Dans ces sous listes on trouve un compte à rebours (au début égale à
                                            # len(coord)) qui diminue de 1 à chaque fois que le serpent se déplace, et les coordonées de la
                                            # pomme mangée. Ces sous listes peuvent s'acumuler dans 'compteurs'. Si le compte à rebours de la
                                            # première sous liste est réduit à 1, alors on ajoute un carré au serpent à l'endroit où il a
                                            # mangé la pomme dont on a stocké les coordonnées (c'est à dire à l'arrière du serpent)
                    coord.append(compteurs[0][1])
                    snake.append(C.create_image(compteurs[0][1][0] , compteurs[0][1][1] , image=fichier_snake, anchor='nw'))
                    del(compteurs[0])
                # Ensuite, on enlève 1 aux compte à rebours :
                for i in compteurs :
                    i[0] -= 1
            # Ici on regarde si il n'y a pas de bordures (mod=0) et alors on regarde si le serpent est sorti de l'écran
            if mod == 0 and (coord[0][1] < 0) :
                coord[0][1] = 594
            # On test si il arrive sur une pomme
            manger_or()
            manger()
            # On actualise la position du serpent
            for i in range(len(coord)):
                C.coords(snake[i], coord[i][0] , coord[i][1])
            # Est-il rentré dans un mur ?
            collision()
            # Si on a ni mis sur pause, ni passé test en False :
            if test == True and stop == False :
                fen.after(70, Hbis)
    def H(evt):
        global d
        global test     # Uniquement utile au bloquage de Hbis
        global d_test   # Permet de ne pas reprendre en allant vers l'arrière après une pause
        if (d_test == False and d == 1) or d == 2 :     # (d==2) car dans tous les cas on ne veux pas pouvoir faire demi tour
                                                        # (d_test == False and d == 1) car si la partie n'est pas en pause et si on re-appuie
                                                        # sur la touche 'haut', on ne veux pas pouvoir enclencher deux fois Hbis en même temps
            test = False
        else :
            d = 1
            d_test = False
        if test == True and stop == False :
            Hbis()
        test = True

    # Déplacement vers le bas
    def Bbis():
        global coord
        global compteurs
        global snake
        if d == 2 :
            coord.insert(0, coord[0][::])
            coord[0][1] += 16
            del(coord[len(coord)-1])
            if len(compteurs)>0 :
                if (compteurs[0][0] == 1):
                    coord.append(compteurs[0][1])
                    snake.append(C.create_image(compteurs[0][1][0] , compteurs[0][1][1] , image=fichier_snake, anchor='nw'))
                    del(compteurs[0])
                for i in compteurs :
                    i[0] -= 1
            if mod == 0 and (coord[0][1] > 594):
                coord[0][1] = 2
            manger_or()
            manger()
            for i in range(len(coord)):
                C.coords(snake[i], coord[i][0] , coord[i][1])
            collision()
            if test == True and stop == False :
                fen.after(70, Bbis)
    def B(evt):
        global d
        global test
        global d_test
        if (d_test == False and d == 2) or d == 1 :
            test = False
        else :
            d = 2
            d_test = False
        if test == True and stop == False :
            Bbis()
        test = True

    # Déplacement vers la droite
    def Dbis():
        global coord
        global compteurs
        global snake
        if d == 3 :
            coord.insert(0, coord[0][::])
            coord[0][0] += 16
            del(coord[len(coord)-1])
            if len(compteurs)>0 :
                if (compteurs[0][0] == 1):
                    coord.append(compteurs[0][1])
                    snake.append(C.create_image(compteurs[0][1][0] , compteurs[0][1][1] , image=fichier_snake, anchor='nw'))
                    del(compteurs[0])
                for i in compteurs :
                    i[0] -= 1
            if mod == 0 and (coord[0][0] == 770):
                coord[0][0] = 2
            manger_or()
            manger()
            for i in range(len(coord)):
                C.coords(snake[i], coord[i][0] , coord[i][1])
            collision()
            if test == True and stop == False :
                fen.after(70, Dbis)
    def D(evt):
        global d
        global test
        global d_test
        if (d_test == False and d == 3) or d == 4 :
            test = False
        else :
            d = 3
            d_test = False
        if test == True and stop == False :
            Dbis()
        test = True

    # Déplacement vers la gauche
    def Gbis():
        global coord
        global compteurs
        global snake
        if d == 4 :
            coord.insert(0, coord[0][::])
            coord[0][0] -= 16
            del(coord[len(coord)-1])
            if len(compteurs)>0 :
                if (compteurs[0][0] == 1):
                    coord.append(compteurs[0][1])
                    snake.append(C.create_image(compteurs[0][1][0] , compteurs[0][1][1] , image=fichier_snake, anchor='nw'))
                    del(compteurs[0])
                for i in compteurs :
                    i[0] -= 1
            if mod == 0 and (coord[0][0] < 0):
                coord[0][0] = 770
            manger_or()
            manger()
            for i in range(len(coord)):
                C.coords(snake[i], coord[i][0] , coord[i][1])
            collision()
            if test == True and stop == False :
                
                fen.after(70, Gbis)
    def G(evt):
        global d
        global test
        global d_test
        if (d_test == False and d == 4) or d == 3 :
            test = False
        else :
            d = 4
            d_test = False
        if test == True and stop == False :
            Gbis()
        test = True



    # Première option du menu : Jouer

    def jeu():
        global coord_pomme
        global C
        global coord
        global snake
        global pomme
        global txt_score

        destruction()
        
        fen.geometry('772x612')
     
        C = Canvas(fen, width=768, height=608)
        C.place(x=0, y=0)

        fd_leave_bis()

        # On crée les obstacles-
        obstacles()

        # Les coordonnées du serpent sont rangées dans une liste car on devra ajouter plein d'autres coordonnées
        coord = [spawn()]

        coord_pomme = spawn()

        fen.after(randrange(10000, 20000), spawn_or)

        # Création du fond
        fond = C.create_image(2,2, image= fichier_fond, anchor = 'nw')
        C.tag_lower(fond)

        # On stock tous les carrés qui constituent le serpent dans cette liste (pour le moment il n'y en a qu'un mais elle vas se remplir)
        snake = [C.create_image(coord[0][0] , coord[0][1] , image=fichier_snake, anchor='nw')]

        # On crée la pomme
        pomme = C.create_image(coord_pomme[0] , coord_pomme[1] , image=fichier_pomme, anchor='nw')

        # Affichage du score
        txt_score = C.create_text(10 ,10, text= "SCORE : " + str(score), anchor='nw')
        
            
        fen.bind_all('<Up>', H)
        fen.bind_all('<Down>', B)
        fen.bind_all('<Right>', D)
        fen.bind_all('<Left>', G)
        fen.bind_all('<space>', pause)

        
    def jeu_bordures():
        global C
        global coord_pomme
        global mod
        global coord
        global snake
        global pomme
        global txt_score

        destruction()
        
        fen.geometry('772x612')
     
        C = Canvas(fen, width=768, height=608, bg='black')
        C.place(x=0, y=0)

        fd_leave_bis()

        mod = 1

        # Les coordonnées du serpent sont rangées dans une liste car on devra ajouter plein d'autres coordonnées
        coord = [spawn()]

        coord_pomme = spawn()

        fen.after(randrange(10000, 20000), spawn_or)
        
        #Création du fond
        fond = C.create_image(2,2, image= fichier_fond, anchor = 'nw')

        # On stock tous les carrés qui constituent le serpent dans cette liste (pour le moment il n'y en a qu'un mais elle vas se remplir)
        snake = [C.create_image(coord[0][0] , coord[0][1] , image=fichier_snake, anchor='nw')]

        # On crée la pomme
        pomme = C.create_image(coord_pomme[0] , coord_pomme[1] , image=fichier_pomme, anchor='nw')

        # Affichage du score
        txt_score = C.create_text(20 ,20, text= "SCORE : " + str(score), anchor='nw')


        for i in range(2,769,16):
            bord_haut = C.create_image( i, 2, image=fichier_snake, anchor='nw')
            bords_bas = C.create_image( i, 594, image=fichier_snake, anchor='nw')
            
        for i in range(2,595,16):
            bord_gauche = C.create_image( 2, i, image=fichier_snake, anchor='nw')
            bord_droit = C.create_image( 754, i, image=fichier_snake, anchor='nw')

        obstacles()

        fen.bind_all('<Up>', H)
        fen.bind_all('<Down>', B)
        fen.bind_all('<Right>', D)
        fen.bind_all('<Left>', G)
        fen.bind_all('<space>', pause)
        


    def tableau_scores():
        destruction()
        fen.geometry('400x650')
        fichier_score = open("Scores.txt", "r")
        a = fichier_score.readlines()
        D = Canvas(fen, width=396, height=646, bg='white')
        D.place(x=0, y=0)
        D.create_text(180, 10, text="TOP 10")
        D.create_text(100, 40, text="Score :")
        D.create_text(250, 40, text="Pseudo :")
        if len(a) < 10 :
            b = len(a)
        else :
            b = 10
        for i in range(b):
            D.create_text(100, 80+i*50, text=a[i][:nb(a, i)])
            D.create_text(250, 80+i*50, text=a[i][2+nb(a, i):len(a[i])-1])
            def retour():
                bou5.destroy()
                D.delete(ALL)
                D.destroy()
                main()
        bou5 = Button(fen, text="Menu", anchor = 'nw', command=retour)
        bou5.place(x=190, y=600)

       

        # Bouton Jouer
    bou1 = Button(fen, text="Jouer\n(normal)", anchor = 'nw', command=jeu)
    bou1.place(x=10, y=10)
    bou1.bind('<Enter>', fd_jeu)
    bou1.bind('<Leave>', fd_leave)
    bou6 = Button(fen, text="Jouer\n(difficile)", anchor = 'nw', command=jeu_bordures)
    bou6.place(x=10, y=65)
    bou6.bind('<Enter>', fd_jeu_difficile)
    bou6.bind('<Leave>', fd_leave)
    # Bouton Score
    bou2 = Button(fen, text="Scores", anchor = 'nw', command=tableau_scores)
    bou2.place(x=10, y=125)
    bou2.bind('<Enter>', fd_score)
    bou2.bind('<Leave>', fd_leave)
    # Bouton Quitter
    bou3 = Button(fen, text="Quitter", anchor = 'nw', command=fen.destroy)
    bou3.place(x=10, y=170)
    bou3.bind('<Enter>', fd_quitter)
    bou3.bind('<Leave>', fd_leave)
    # Annonce au joueur
    txt = Label(fen ,text=      """
                
Programmeurs :
Alexandre Bonavita et Corto Callerisa

Dans ce jeu, vous êtes un serpent et le but du jeu est de manger 
un maximum de pommes pour grandir. 

La partie est terminée quand vous vous mangez la queue.
Déplacez vous avec les flèches directionnelles du clavier
et mettez le jeu en pause avec Espace.

Amusez vous bien ! !"""
                )
    txt.place(x=120, y=2)


# Début
main()

fen.mainloop()
