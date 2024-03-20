from tkinter import *
from ai_utils import run
import pickle

app = Tk()

app.geometry('400x400')
app.title('Projet Python')
app['bg'] = 'grey'
app.resizable(height=True, width=True)



#Sauvergarder l'historique dans un fichier
def sauvegarder_historique():
    with open('historique.pkl','wb') as fichier:
        pickle.dump(historique, fichier)

#Charger l'historique depuis un fichier
def charger_historique():
    try:
        with open('historique.pkl', 'rb') as fichier:
            return pickle.load(fichier)
    except FileNotFoundError:
        return []


#Chargel'historique au demarrage de lapplication
historique = charger_historique()


#Widget pour les reponses non modifiable
reponse =  Label(app, text="", width=50, height = 10)
reponse.pack() 



#Permet d'afficher le resultat de la question lorsqu'on clique sur Envoyer
def afficher_reponse():
    question_actuelle = ma_question.get()
    response_complete = run(question_actuelle)
    
    
    if question_actuelle != "":
        h = {"question" : question_actuelle , "reponse": response_complete}
        historique.append(h)
        sauvegarder_historique()
        ajouter_a_mon_histotique()
        
        reponse['text'] = response_complete
    
    
    #L'utilisateur doit saisir un texte
    else:
        reponse['text'] = "Veuillez poser votre question"

    ma_question.set("")


def ajouter_a_mon_histotique():
    historique_listbox.delete(0,END) #Effacer la liste actuelle

    #Ajouter une question à la liste
    for question in historique:
        historique_listbox.insert(END, question)

#Permet de selectionner la question précedente dans l'historique et affiche la reponse à celle-ci
def selectionner_question(event):
    selected_index = historique_listbox.curselection()
    if selected_index:
        selected_index = selected_index[0]
        selected_question = historique[selected_index]
        ma_question.set(selected_question["question"])
        reponse.config(text = selected_question["reponse"])
        run(ma_question.get())


ma_question = StringVar()



#bouton pour soumettre la question
bouton1 = Button(app, text="Envoyer", command=afficher_reponse)
bouton1.pack()

#Zone de saisi des questions
entree = Entry(app, textvariable=ma_question, width=60)
entree.pack()


historique_label = Label(app, text="Historique:") 
historique_label.pack(pady=20) 

#barre de défilement
scrollbar = Scrollbar(app)
scrollbar.pack(side=RIGHT, fill=Y)

#Historique : Liste des questions précédentes
historique_listbox = Listbox(app, yscrollcommand=scrollbar.set, width=60)
historique_listbox.pack()

#Configuration bar de défilement avec Listbox
scrollbar.config(command=historique_listbox.yview)

ajouter_a_mon_histotique()

#permet d'afficher la reponse a la question séléctionnée dans la liste par un clic
historique_listbox.bind("<ButtonRelease-1>", selectionner_question)


app.mainloop()

