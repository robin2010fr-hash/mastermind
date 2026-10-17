import random 
import tkinter as tk

app = tk.Tk()
app.title("Mastermind")
app.geometry("400x500")

def ecran_acceuil():
    global titre_mode, bouton_m1, bouton_m2
    
    titre_mode = tk.Label(app, text="=== MASTERMIND ===")
    titre_mode.pack(pady=20)
    
    bouton_m1 = tk.Button(app, text="Tu devines le code" ,command=lambda: mode(1))
    bouton_m1.pack(pady=10)
    
    bouton_m2 = tk.Button(app, text="L'ordinateur devine le tien" ,command=lambda: mode(2))
    bouton_m2.pack(pady=10)
    
def ecran_difficulte():
    global titre_diff, bouton_facile, bouton_difficile
    
    titre_diff = tk.Label(app, text="=== CHOIX DU MODE ===")
    titre_diff.pack(pady=20)
    
    bouton_facile = tk.Button(app, text="Mode facile (sans répétition)" ,command=lambda: lancer_jeu(1))
    bouton_facile.pack(pady=10)
    
    bouton_difficile = tk.Button(app, text="Mode difficile (répétition potentielle)" ,command=lambda: lancer_jeu(2))
    bouton_difficile.pack(pady=10)

def mode(mode):
    titre_mode.pack_forget()
    bouton_m1.pack_forget()
    bouton_m2.pack_forget()
    if mode == 1:
        ecran_difficulte()
    else:
        print("En développement")

tentative_en_cours = []

def lancer_jeu(mode):
    global solution_secrete, bouton_valider, historique_label, label_consigne, essais_restants
    global label_combinaison_actuelle
    
    titre_diff.pack_forget()
    bouton_facile.pack_forget()
    bouton_difficile.pack_forget()
    
    solution_secrete = choix_reponse("n",mode)
    essais_restants = 12
    
    titre_jeu = tk.Label(app, text="=== PLATEAU DE JEU ===", font="bold")
    titre_jeu.pack(pady=10)

    label_consigne = tk.Label(app, text="Cliquez sur 4 couleurs pour choisir votre proposition")
    label_consigne.pack(pady=5)
    
    label_combinaison_actuelle = tk.Label(app, text="Votre choix actuel :")
    label_combinaison_actuelle.pack(pady=10)
    
    cadre_boutons = tk.Frame(app)
    cadre_boutons.pack(pady=10)
    
    lettres = ("B","R","J","V","O","N")
    couleurs_tk = ("blue","red","yellow","green","orange","black")
    couleurs_texte = ("white", "white", "black", "white", "black", "white")
    
    
    for i in range(len(lettres)):
        btn = tk.Button(
            cadre_boutons,
            text=lettres[i],
            bg=couleurs_tk[i],
            fg=couleurs_texte[i],
            command=lambda lettre=lettres[i]: ajouter_couleur(lettre)
        )
        btn.pack(side="left", padx=3)
            
    actions = tk.Frame(app)
    actions.pack(pady=10)
    
    bouton_valider = tk.Button(app, text="Valider", command=verifier_proposition)
    bouton_valider.pack(pady=5)

    bouton_effacer = tk.Button(app, text="Effacer", command=effacer_selection)
    bouton_effacer.pack(pady=5)

    historique_label = tk.Label(app, text=texte_historique + f"Il vous reste {essais_restants} essais.", justify="left")
    historique_label.pack(pady=10)
    
def ajouter_couleur(lettre_couleur):
    global tentative_en_cours
    if len(tentative_en_cours) < 4:
        tentative_en_cours.append(lettre_couleur)
        label_combinaison_actuelle.config(text=f"Votre choix actuel : {tentative_en_cours}")

def effacer_selection():
    if len(tentative_en_cours) > 0:
        tentative_en_cours.pop(-1)
        label_combinaison_actuelle.config(text=f"Votre choix actuel : {tentative_en_cours}")
    if len(tentative_en_cours) == 0:
        label_combinaison_actuelle.config(text="Votre choix actuel : (vide)")

texte_historique = "Historique des essais :\n"

def verifier_proposition():
    global essais_restants, texte_historique, tentative_en_cours
    
    bien_places, mal_places = comparaison(tentative_en_cours,solution_secrete)
    
    saisie_texte = f"{tentative_en_cours}"
    
    essais_restants -= 1
    texte_historique += f"Essai {12 - essais_restants}/12 : {saisie_texte} | BP: {bien_places} | MP: {mal_places}\n"
    
    if tentative_en_cours == solution_secrete:
        historique_label.config(text=f"{texte_historique}\n Bravo ! Tu as réussi en {12 - essais_restants} essai(s) !", fg="green")
        bouton_valider.pack_forget() # On cache le bouton pour bloquer le jeu
        bouton_effacer.pack_forget()
    elif essais_restants == 0:
        historique_label.config(text=f"{texte_historique}\n Perdu ! La réponse était {solution_secrete}", fg="red")
        bouton_valider.pack_forget() # On cache le bouton pour bloquer le jeu
        bouton_effacer.pack_forget()
    else:
        historique_label.config(text=texte_historique + f"\nIl vous reste {essais_restants} essais")
        tentative_en_cours = []
        label_combinaison_actuelle.config(text="Votre choix actuel : (vide)")
        
def choix_reponse(choisir,difficulte):
    reponse = []
    couleurs = ("B","R","J","V","O","N")
    if choisir == "o":
        liste_couleurs_choisies = choix_combinaison_utilisateur()
        for i in range(len(liste_couleurs_choisies)):
            reponse.append(liste_couleurs_choisies[i])
    elif choisir == "n":
        if difficulte == 1:
            while len(reponse) < 4:
                n = random.randint(0,5)
                if couleurs[n] not in reponse:
                    reponse.append(couleurs[n])
        elif difficulte == 2:
            for i in range(4):
                reponse.append(couleurs[random.randint(0,5)])
    return reponse

def comparaison(test,solution):
    bien_placés = 0
    mal_placés = 0
    test_temp = []
    soluce_temp = []
    for i in range(len(test)):
        if test[i] == solution[i]:
            bien_placés += 1
        else:
            test_temp.append(test[i])
            soluce_temp.append(solution[i])
    for i in range(len(test_temp)):
        if test_temp[i] in soluce_temp:
            mal_placés += 1
            nouvelle_soluce = []
            deja_enleve = False
            for j in range (len(soluce_temp)):
                if test_temp[i] == soluce_temp[j] or deja_enleve:
                    deja_enleve = True
                else:
                    nouvelle_soluce.append(soluce_temp[j])
    return bien_placés, mal_placés

ecran_acceuil()
app.mainloop()