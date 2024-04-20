import requests
import random
import os
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image, ImageOps, ImageFilter
from io import BytesIO

def get_random_image(query):
    # Remplace "YOUR_ACCESS_KEY" par ta clé d'API Unsplash
    access_key = "iovKAwTjUlesNHFlzGElr24N6R-rYEfxXOcMEe717LU"
    
    # Paramètres de la requête
    if query == "":
        params = {
            # "query": "random",
            "client_id": access_key,
            # "orientation": "landscape",  # Assure-toi d'avoir une image de paysage
            # "per_page": 10  # Nombre maximum d'images à récupérer
        }
        # Requête GET à l'API Unsplash sans mot-clé spécifié
        # response = requests.get("https://api.unsplash.com/search/photos", params=params)
        response = requests.get("https://api.unsplash.com/photos/random", params=params)

        if response.status_code == 200:
            # Extraction des données JSON de la réponse
            data = response.json()
            
            # Récupération de l'URL de l'image aléatoire
            image_url = data["urls"]["regular"]
            
            return image_url
        else:
            print("Erreur lors de la requête à l'API Unsplash:", response.status_code)
            return None
        # print("LA")
    else:
        params = {
            "query": query,
            "client_id": access_key,
            # "orientation": "landscape",  # Assure-toi d'avoir une image de paysage
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

def get_new_image(word="random") :
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


def traitement_image(param):
    global image, photo, label

    match param:
        case "Noir et blanc" :
            # Convertir l'image en noir et blanc
            bw_image = image.convert("L")
        case "Miroir" :
            bw_image = ImageOps.mirror(image)
        case "Inversion" :
            bw_image = ImageOps.invert(image)
        case "Flip" :
            bw_image = ImageOps.flip(image)
        case "Accent" :
            # bw_image = image.filter(ImageFilter.UnsharpMask(radius=2, percent=150, threshold=3))
            bw_image = image.filter(ImageFilter.SHARPEN)
        case "Contraste" :
            bw_image = ImageOps.equalize(image, mask=None)
        case _:
            print("Error")
    
    
    
    # Mettre à jour l'image affichée
    photo = ImageTk.PhotoImage(bw_image)
    label.config(image=photo)


def apply_filters():
    # Applique les filtres sélectionnés sur l'image
    # Obtenez l'image d'origine
    image_filtered = image.copy()

    # Appliquer le filtre noir et blanc si la case est cochée
    if bw_var.get():
        image_filtered = ImageOps.grayscale(image_filtered)

    # Appliquer le filtre d'inversion de couleurs si la case est cochée
    if invert_var.get():
        image_filtered = ImageOps.invert(image_filtered)

    photo = ImageTk.PhotoImage(image_filtered)
    label.config(image=photo)
    label.image = photo  # Garde une référence pour éviter la suppression par le garbage collector





def reset():
    global image, photo, label


    image_path = "images\downloaded_image.jpg"  # Chemin vers l'image
    image = Image.open(image_path)
    photo = ImageTk.PhotoImage(image)

    # Mettre à jour l'image affichée
    label.config(image=photo)

def update_image():
    global image, photo, label, image_path, last_modified
    
    # Vérifie si le fichier image a été modifié
    if os.path.getmtime(image_path) != last_modified:
        # Met à jour l'image affichée
        image = Image.open(image_path)

        # photo = resize_image(image)

        # photo = ImageTk.PhotoImage(photo)

        photo = ImageTk.PhotoImage(image)

        label.config(image=photo)
        # Met à jour le timestamp de dernière modification
        last_modified = os.path.getmtime(image_path)
    
    # Programme le prochain appel à cette fonction dans 1000 ms (1 seconde)
    gui.after(1000, update_image)


# Fonction pour redimensionner une image tout en conservant le ratio hauteur / largeur
def resize_image(image, max_width=800, max_height=600):
    width, height = image.size
    aspect_ratio = width / height
    
    # Redimensionne l'image en fonction de la largeur maximale tout en conservant le ratio
    if width > max_width:
        width = max_width
        height = int(width / aspect_ratio)
    
    # Redimensionne l'image en fonction de la hauteur maximale tout en conservant le ratio
    if height > max_height:
        height = max_height
        width = int(height * aspect_ratio)
    
    return image.resize((width, height))


if __name__ == "__main__":
    # Paramètre de la fenêtre
    gui = tk.Tk()
    gui.title("API Application")
    gui.geometry("1500x900") # Taille de la fenêtre


    #Création du Notebook (widget contenant les onglets)
    notebook = ttk.Notebook(gui)
    notebook.pack(pady=10, padx=10)

    # Création des différents cadres (onglets) à ajouter au Notebook
    frame1 = tk.Frame(notebook, width=400, height=300)
    frame2 = tk.Frame(notebook, width=400, height=300)
    frame3 = tk.Frame(notebook, width=400, height=300)


    # Ajout des cadres (onglets) au Notebook avec un titre pour chaque onglet
    notebook.add(frame1, text='Onglet 1')
    notebook.add(frame2, text='Onglet 2')
    notebook.add(frame3, text='Onglet 3')


    


    # Chargement de l'image
    image_path = "images\downloaded_image.jpg"  # Chemin vers l'image
    image = Image.open(image_path)

    # photo = resize_image(image)

    # photo = ImageTk.PhotoImage(photo)

    photo = ImageTk.PhotoImage(image)


    searchInLabel = tk.StringVar()

    


    # Création d'un widget Label pour afficher l'image
    label = tk.Label(frame1, image=photo)
    # label.grid(row=7, column=4)
    label.pack(side=tk.TOP)

    label1 = tk.Label(frame1, text = "Recherche")
    label.pack(side=tk.TOP)
    # label1.grid(row=0, column=0)

    # label2 = tk.Label(gui, text = "Recherche")
    # label2.grid(row=1, column=0)

    # label3 = tk.Label(gui, text = "Recherche")
    # label3.grid(row=1, column=1)

    entry = tk.Entry(frame1, textvariable = searchInLabel)
    entry.pack()
    # entry.grid(row=2, column=3)

    scanButton = tk.Button(frame1, text="Image aléatoire", command = lambda: get_new_image(searchInLabel.get()))
    scanButton.config(width=20, height=2)
    scanButton.pack(side=tk.LEFT, padx=25)
    # scanButton.grid(row=6, column=3)
    
    

    scanButton1 = tk.Button(frame1, text="Noir et blanc", command = lambda: traitement_image("Noir et blanc"))
    scanButton1.config(width=20, height=2)
    scanButton1.pack(side=tk.LEFT, padx=25)
    # scanButton1.grid(row=7, column=3)

    # Créez des variables de contrôle pour chaque filtre
    bw_var = tk.BooleanVar()
    bw_checkbox = tk.Checkbutton(frame1, text="Noir et blanc", variable=bw_var, command=apply_filters)
    bw_checkbox.pack()


    # Créez une variable de contrôle pour le filtre Inversion de couleurs
    invert_var = tk.BooleanVar()

    # Créez une case à cocher pour le filtre Inversion de couleurs
    invert_checkbox = tk.Checkbutton(frame1, text="Inversion de couleurs", variable=invert_var, command=apply_filters)
    invert_checkbox.pack()



    # scanButton3 = tk.Button(frame1, text="Miroir", command = lambda: traitement_image("Miroir"))
    # scanButton3.config(width=20, height=2)
    # scanButton3.pack(side=tk.LEFT, padx=25)

    # scanButton4 = tk.Button(frame1, text="Inversion", command = lambda: traitement_image("Inversion"))
    # scanButton4.config(width=20, height=2)
    # scanButton4.pack(side=tk.LEFT, padx=25)

    # scanButton5 = tk.Button(frame1, text="Flip", command = lambda: traitement_image("Flip"))
    # scanButton5.config(width=20, height=2)
    # scanButton5.pack(side=tk.LEFT, padx=25)

    # scanButton6 = tk.Button(frame1, text="Accent", command = lambda: traitement_image("Accent"))
    # scanButton6.config(width=20, height=2)
    # scanButton6.pack(side=tk.LEFT, padx=25)

    # scanButton7 = tk.Button(frame1, text="Contraste", command = lambda: traitement_image("Contraste"))
    # scanButton7.config(width=20, height=2)
    # scanButton7.pack(side=tk.LEFT, padx=25)

    scanButton2 = tk.Button(frame1, text="Réinitialiser", command = reset)
    scanButton2.config(width=20, height=2)
    scanButton2.pack(side=tk.LEFT, padx=25)

    last_modified = os.path.getmtime(image_path)

    # Lance la fonction pour détecter les modifications d'image
    update_image()

    gui.mainloop()
