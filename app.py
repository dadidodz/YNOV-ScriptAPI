import requests
import random
import os
from tkinter import *
from PIL import ImageTk, Image

def get_random_image(query):
    # Remplace "YOUR_ACCESS_KEY" par ta clé d'API Unsplash
    access_key = "iovKAwTjUlesNHFlzGElr24N6R-rYEfxXOcMEe717LU"
    
    # Paramètres de la requête
    params = {
        "query": query,
        "client_id": access_key,
        "orientation": "landscape",  # Assure-toi d'avoir une image de paysage
        "per_page": 10  # Nombre maximum d'images à récupérer
    }
    
    # Requête GET à l'API Unsplash
    response = requests.get("https://api.unsplash.com/search/photos", params=params)
    
    # Vérification de la réponse
    if response.status_code == 200:
        # Extraction des données JSON de la réponse
        data = response.json()
        
        # Choix aléatoire d'une image parmi celles retournées
        random_image = random.choice(data["results"])
        
        # Récupération de l'URL de l'image
        image_url = random_image["urls"]["regular"]
        
        return image_url
    else:
        print("Erreur lors de la requête à l'API Unsplash:", response.status_code)
        return None

def download_image(url, folder="images", filename="downloaded_image.jpg"):
    # Crée le dossier s'il n'existe pas
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    # Télécharge l'image
    response = requests.get(url)
    if response.status_code == 200:
        # Chemin complet du fichier
        filepath = os.path.join(folder, filename)
        with open(filepath, 'wb') as f:
            f.write(response.content)
        return filepath
    else:
        print("Erreur lors du téléchargement de l'image:", response.status_code)
        return None

def work(word) :
    image_url = get_random_image(word)
    if image_url:
        print("Image téléchargée:", image_url)
        image_path = download_image(image_url)
        if image_path:
            print("L'image a été téléchargée avec succès:", image_path)
        else:
            print("Impossible de télécharger l'image.")
    else:
        print("Impossible de récupérer l'image.")


def sendInput():
    word = searchInLabel.get()
    work(word)

def update_image():
    global image, photo, label, image_path, last_modified
    
    # Vérifie si le fichier image a été modifié
    if os.path.getmtime(image_path) != last_modified:
        # Met à jour l'image affichée
        image = Image.open(image_path)
        photo = ImageTk.PhotoImage(image)
        label.config(image=photo)
        # Met à jour le timestamp de dernière modification
        last_modified = os.path.getmtime(image_path)
    
    # Programme le prochain appel à cette fonction dans 1000 ms (1 seconde)
    gui.after(1000, update_image)

if __name__ == "__main__":
    gui = Tk()

    gui.title("Application")

    #Taille de la fenêtre
    gui.geometry("1500x900")

    label1 = Label(gui, text = "Recherche")
    # label.pack(side = TOP)
    label1.grid(row=0, column=0)

    label2 = Label(gui, text = "Recherche")
    label2.grid(row=1, column=0)

    label3 = Label(gui, text = "Recherche")
    label3.grid(row=1, column=1)

    searchInLabel = StringVar()

    entry = Entry(gui, textvariable = searchInLabel)
    # entry.pack()
    entry.grid(row=2, column=3)

    scanButton = Button(gui, text="Go", command = sendInput)
    scanButton.config(width=20, height=2)
    # scanButton.pack()
    scanButton.grid(row=6, column=3)

    # Chargement de l'image
    image_path = "images\downloaded_image.jpg"  # Chemin vers l'image
    image = Image.open(image_path)
    photo = ImageTk.PhotoImage(image)

    # Création d'un widget Label pour afficher l'image
    label = Label(gui, image=photo)
    label.grid(row=7, column=4)


    scanButton = Button(gui, text="Go", command = sendInput)
    scanButton.config(width=20, height=2)
    # scanButton.pack()
    scanButton.grid(row=7, column=3)


    last_modified = os.path.getmtime(image_path)

    # Lance la fonction pour détecter les modifications d'image
    update_image()

    gui.mainloop()
