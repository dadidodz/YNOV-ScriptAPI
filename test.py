import requests
import random
import os
import datetime
from tkinter import *
from tkinter.ttk import *
from PIL import ImageTk, Image, ImageOps, ImageFilter
# from io import BytesIO

def get_random_image(query):
    # Remplace "YOUR_ACCESS_KEY" par ta clé d'API Unsplash
    access_key = "iovKAwTjUlesNHFlzGElr24N6R-rYEfxXOcMEe717LU"
    
    # Paramètres de la requête
    if query == "":
        params = {
            # "query": "random",
            "client_id": access_key,
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
            
            return None

    else:
        params = {
            "query": query,
            "client_id": access_key,
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
            t = "Erreur lors de la requête à l'API Unsplash:" + response.status_code
            modif_texte(t)
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
        t = "Erreur lors du téléchargement de l'image:" + response.status_code
        modif_texte(t)

        return None

def get_new_image(word="random") :
    image_url = get_random_image(word)
    if image_url:
        print("Image téléchargée:", image_url)
        image_path = download_image(image_url)
        if image_path:
            texte_variable = "L'image a été téléchargée avec succès: " + image_path
            modif_texte(texte_variable)
            resize_im()
        else:
            modif_texte("Impossible de télécharger l'image.")
            # print("Impossible de télécharger l'image.")
    else:
        modif_texte("Impossible de récupérer l'image.")
        # print("Impossible de récupérer l'image.")

def modif_texte(texte: str): 
    global reset_texte_after_id

    # Annuler l'appel précédent à reset_texte si disponible
    if reset_texte_after_id:
        gui.after_cancel(reset_texte_after_id)
        textmodif.config(text=texte)
    else:
        textmodif.config(text=texte)
    
    # Programmer l'appel à reset_texte après 3000 ms
    reset_texte_after_id = gui.after(2000, reset_texte)

def reset_texte():
    textmodif.config(text="")


def apply_filters():
    # Applique les filtres sélectionnés sur l'image
    # Obtenez l'image d'origine
    image_filtered = Image.open(image_path)

    # Appliquer le filtre noir et blanc si la case est cochée
    if nb_var.get():
        image_filtered = ImageOps.grayscale(image_filtered)
        
    # Appliquer le filtre d'inversion de couleurs si la case est cochée
    if inversion_var.get():
        image_filtered = ImageOps.invert(image_filtered)

    # Appliquer le filtre d'inversion de couleurs si la case est cochée
    if miroiry_var.get():
        image_filtered = ImageOps.mirror(image_filtered)
    
    if miroirx_var.get():
        image_filtered = ImageOps.flip(image_filtered)

    if egaliser_var.get():
        image_filtered = ImageOps.equalize(image_filtered, mask=None)

    if flou_var.get():
        image_filtered = image_filtered.filter(ImageFilter.GaussianBlur(radius=5))
    
    if contour_var.get():
        image_filtered = image_filtered.filter(ImageFilter.CONTOUR)

    if detail_var.get():
        image_filtered = image_filtered.filter(ImageFilter.DETAIL)

    if amelioration_var.get():
        image_filtered = image_filtered.filter(ImageFilter.EDGE_ENHANCE)
    
    if gaufrage_var.get():
        image_filtered = image_filtered.filter(ImageFilter.EMBOSS)
    
    if bords_var.get():
        image_filtered = image_filtered.filter(ImageFilter.FIND_EDGES)

    if nettete_var.get():
        image_filtered = image_filtered.filter(ImageFilter.SHARPEN)

    photo = ImageTk.PhotoImage(image_filtered)
    label.config(image=photo)
    label.image = photo  # Garde une référence pour éviter la suppression par le garbage collector

def reset():
    for i, var in enumerate((amelioration_var, bords_var, contour_var, detail_var, egaliser_var, flou_var, gaufrage_var,
                                inversion_var, miroiry_var, miroirx_var, nb_var, nettete_var)):
        var.set(False)

    apply_filters()


def update_image():
    global last_modified_img
    
    # Vérifie si le fichier image a été modifié
    if os.path.getmtime(image_path) != last_modified_img:
        # Met à jour l'image affichée
        image = Image.open(image_path)

        photo = ImageTk.PhotoImage(image)
        label.config(image=photo)
        label.image = photo
        # Met à jour le timestamp de dernière modification
        last_modified_img = os.path.getmtime(image_path)
    
    # Programme le prochain appel à cette fonction dans 1000 ms (1 seconde)
    gui.after(1000, update_image)



def resize_im():

    image = Image.open(image_path)

    # Obtient les dimensions de l'image
    image_width, image_height = image.size

    frame_width = frame1.winfo_width()
    frame_height = frame1.winfo_height()

    # Calcul des dimensions de la fenêtre (80% de la taille de l'écran)
    max_width = int(frame_width * 0.85)
    max_height = int(frame_height * 0.85)

    # Vérifie si l'image est plus grande que la fenêtre
    if image_width > max_width or image_height > max_height:
        # Calculer le ratio hauteur/largeur de l'image
        image_ratio = image_width / image_height

        # Redimensionne l'image en fonction de la plus grande dimension (largeur ou hauteur)
        if image_width > image_height:
            new_width = max_width
            new_height = int(max_width / image_ratio)
        else:
            new_height = max_height
            new_width = int(max_height * image_ratio)

        resized_image = ImageOps.fit(image, (new_width, new_height), method=0, bleed=0.0, centering=(0.5, 0.5))
        resized_image.save("images\downloaded_image.jpg")

def quitter():
    gui.quit()

def telecharger_image_filtree():
    # Appliquer d'abord le filtre blur à une copie de l'image originale
    image_originale = Image.open(image_path)
    image_filtree = image_originale.copy()

    if nb_var.get():
        image_filtree = ImageOps.grayscale(image_filtree)

    # Appliquer le filtre d'inversion de couleurs si la case est cochée
    if inversion_var.get():
        image_filtree = ImageOps.invert(image_filtree)

    # Appliquer le filtre d'inversion de couleurs si la case est cochée
    if miroiry_var.get():
        image_filtree = ImageOps.mirror(image_filtree)
    
    if miroirx_var.get():
        image_filtree = ImageOps.flip(image_filtree)

    if egaliser_var.get():
        image_filtree = ImageOps.equalize(image_filtree, mask=None)

    if flou_var.get():
        # image_filtree = image_filtree.filter(ImageFilter.BLUR)
        image_filtree = image_filtree.filter(ImageFilter.GaussianBlur(radius=5))
    
    if contour_var.get():
        image_filtree = image_filtree.filter(ImageFilter.CONTOUR)

    if detail_var.get():
        image_filtree = image_filtree.filter(ImageFilter.DETAIL)

    if amelioration_var.get():
        image_filtree = image_filtree.filter(ImageFilter.EDGE_ENHANCE)
    
    if gaufrage_var.get():
        image_filtree = image_filtree.filter(ImageFilter.EMBOSS)
    
    if bords_var.get():
        image_filtree = image_filtree.filter(ImageFilter.FIND_EDGES)
    
    if nettete_var.get():
        image_filtree = image_filtree.filter(ImageFilter.SHARPEN)

    # Télécharger l'image filtrée
    image_filtree_path = "images/image_filtree_apres_blur.jpg"  # Chemin de l'image filtrée après le filtre blur
    # label.image.save(image_filtree_path)
    image_filtree.save(image_filtree_path)  # Enregistrer l'image filtrée après le filtre blur
    print("Image filtrée après blur téléchargée avec succès:", image_filtree_path)

if __name__ == "__main__":
    # Paramètre de la fenêtre
    gui = Tk()
    gui.title("API Application")

    # Obtention des dimensions de l'écran
    screen_width = gui.winfo_screenwidth()
    screen_height = gui.winfo_screenheight()

    # Calcul des dimensions de la fenêtre (80% de la taille de l'écran)
    window_width = int(screen_width * 0.9)
    window_height = int(screen_height * 0.9)

    # Définition des dimensions de la fenêtre
    gui.geometry(f"{window_width}x{window_height}")

    #Création du Notebook (widget contenant les onglets)
    notebook = Notebook(gui)
    notebook.pack(pady=10, padx=10)

    # Obtention des dimensions de l'écran
    window_width = gui.winfo_screenwidth()
    window_height = gui.winfo_screenheight()

    # Calcul des dimensions de la fenêtre (80% de la taille de l'écran)
    window_width = int(screen_width * 0.7)
    window_height = int(screen_height * 0.7)

    # Création des différents cadres (onglets) à ajouter au Notebook
    frame1 = Frame(notebook, width=1400, height=800)
    frame2 = Frame(notebook, width=1400, height=800)
    frame3 = Frame(notebook, width=1400, height=800)


    # Ajout des cadres (onglets) au Notebook avec un titre pour chaque onglet
    notebook.add(frame1, text='Api Unsplash')
    notebook.add(frame2, text='Onglet 2')
    notebook.add(frame3, text='Onglet 3')

    

    # Chargement de l'image
    image_path = "images\downloaded_image.jpg"  # Chemin vers l'image
    image = Image.open(image_path)
    photo = ImageTk.PhotoImage(image)

    


    # Création d'un widget Label pour afficher l'image
    label = Label(frame1, image=photo)
    label.grid(row=0, column=0, columnspan=15)

    #--------------------Création de toutes les variables des checkboxes--------------------#
    amelioration_var = BooleanVar()
    bords_var = BooleanVar()
    contour_var = BooleanVar()
    detail_var = BooleanVar()
    egaliser_var = BooleanVar()
    flou_var = BooleanVar()
    gaufrage_var = BooleanVar()
    inversion_var = BooleanVar() # Créez une variable de contrôle pour le filtre Inversion de couleurs
    miroiry_var = BooleanVar() # Créez une variable de contrôle pour le filtre Inversion de couleurs
    miroirx_var = BooleanVar()
    nb_var = BooleanVar() # Créez une variable de contrôle pour le filtre Inversion de couleurs
    nettete_var = BooleanVar()

    #--------------------Création des checkboxes--------------------#

    # Définir une liste de noms de variables correspondant à bw_var, invert_var, etc.
    ck_names = ["Amelioration", "Bords", "Contour", "Détail", "Égaliser", 
             "Flou", "Gaufrage", "Inversion", "Miroir Y", 
             "Miroir X", "Noir et Blanc", "Netteté"]

    for i, var in enumerate((amelioration_var, bords_var, contour_var, detail_var, egaliser_var, flou_var, gaufrage_var,
                             inversion_var, miroiry_var, miroirx_var, nb_var, nettete_var)):
        Checkbutton(frame1, text=ck_names[i], variable=var, command=apply_filters).grid(row=1, column=i)

    
    #--------------------Création des Style--------------------#
    #--------------------Boutons--------------------#
    # Créez une instance de la classe Style()
    buttons_style = Style()
    buttons_style.configure("TButton",
                foreground="black",  # Couleur du texte
                font=("Arial", 10),  # Police de caractères
                bordercolor="black",  # Couleur de la bordure
                padding=3,  # Espace entre le contenu et la bordure
                width=15,  # Largeur du bouton
                height=5,  # Hauteur du bouton
                anchor="center",  # Alignement du contenu
                justify="center",  # Alignement horizontal du texte
                )

    button_names = ["Réinitialiser", "Nouvelle image", "Quitter", "Télécharger"]

    searchInLabel = StringVar()
    entry = Entry(frame1, textvariable = searchInLabel)
    entry.grid(row=2, column=2)

    

    # Créez le bouton avec le style personnalisé
    Button(frame1, text="Nouvelle image", command=lambda:[get_new_image(searchInLabel.get()), reset() ]).grid(row=2, column=0, sticky="ew", columnspan=2)
    Button(frame1, text="Réinitialiser", command=reset).grid(row=3, column=0,  sticky="ew",columnspan=2)
    Button(frame1, text="Télécharger", command=telecharger_image_filtree).grid(row=4, column=0,  sticky="ew",columnspan=2)
    Button(frame1, text="Quitter", command=quitter).grid(row=4, column=3,  sticky="ew",columnspan=2)

    # Créer une variable pour le texte
    texte_variable = ""
    # Créer un Label pour afficher le texte
    textmodif = Label(frame1, text=texte_variable)
    textmodif.grid(row=2, column=2, sticky="e", columnspan=8)

    reset_texte_after_id = None
    
    last_modified_img = os.path.getmtime(image_path)

    # Lance la fonction pour détecter les modifications d'image
    update_image()
    # apply_filters()

    for i in range(len(ck_names)):
        frame1.grid_columnconfigure(i, minsize=110)

    gui.resizable(False, False)

    gui.mainloop()