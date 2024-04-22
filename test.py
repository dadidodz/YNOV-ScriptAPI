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

            # resize_image_to_fit_window()
            resize_im()
        else:
            print("Impossible de télécharger l'image.")
    else:
        print("Impossible de récupérer l'image.")


def apply_filters():
    # Applique les filtres sélectionnés sur l'image
    # Obtenez l'image d'origine
    # image_filtered = image.copy()
    image_filtered = Image.open(image_path)

    # Appliquer le filtre noir et blanc si la case est cochée
    if bw_var.get():
        image_filtered = ImageOps.grayscale(image_filtered)

    # Appliquer le filtre d'inversion de couleurs si la case est cochée
    if invert_var.get():
        image_filtered = ImageOps.invert(image_filtered)

    # Appliquer le filtre d'inversion de couleurs si la case est cochée
    if flipy_var.get():
        image_filtered = ImageOps.mirror(image_filtered)
    
    if flipx_var.get():
        image_filtered = ImageOps.flip(image_filtered)

    if equalize_var.get():
        image_filtered = ImageOps.equalize(image_filtered, mask=None)

    if blur_var.get():
        # image_filtered = image_filtered.filter(ImageFilter.BLUR)
        image_filtered = image_filtered.filter(ImageFilter.GaussianBlur(radius=5))
    
    if contour_var.get():
        image_filtered = image_filtered.filter(ImageFilter.CONTOUR)

    if detail_var.get():
        image_filtered = image_filtered.filter(ImageFilter.DETAIL)

    if edge_enhance_var.get():
        image_filtered = image_filtered.filter(ImageFilter.EDGE_ENHANCE)
    
    if emboss_var.get():
        image_filtered = image_filtered.filter(ImageFilter.EMBOSS)
    
    if find_edges_var.get():
        image_filtered = image_filtered.filter(ImageFilter.FIND_EDGES)
    
    if sharpen_var.get():
        image_filtered = image_filtered.filter(ImageFilter.SHARPEN)

    photo = ImageTk.PhotoImage(image_filtered)
    label.config(image=photo)
    label.image = photo  # Garde une référence pour éviter la suppression par le garbage collector

def reset():
# if os.path.getmtime(image_path) == last_modified:
    bw_var.set(False)
    invert_var.set(False)
    flipy_var.set(False)
    flipx_var.set(False)
    sharpen_var.set(False)
    equalize_var.set(False)
    blur_var.set(False)
    contour_var.set(False)
    detail_var.set(False)
    edge_enhance_var.set(False)
    emboss_var.set(False)
    find_edges_var.set(False)
    sharpen_var.set(False)
    # Appliquer les filtres à nouveau
    apply_filters()

def update_image():
    global last_modified
    
    # Vérifie si le fichier image a été modifié
    if os.path.getmtime(image_path) != last_modified:
        # Met à jour l'image affichée
        image = Image.open(image_path)

        photo = ImageTk.PhotoImage(image)
        label.config(image=photo)
        label.image = photo
        # Met à jour le timestamp de dernière modification
        last_modified = os.path.getmtime(image_path)
    
    # Programme le prochain appel à cette fonction dans 1000 ms (1 seconde)
    gui.after(1000, update_image)



def resize_im():

    image = Image.open(image_path)

    # Obtient les dimensions de l'image
    image_width, image_height = image.size

    frame_width = frame1.winfo_width()
    frame_height = frame1.winfo_height()

    # Calcul des dimensions de la fenêtre (80% de la taille de l'écran)
    max_width = int(frame_width * 0.9)
    max_height = int(frame_height * 0.9)

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

if __name__ == "__main__":
    # Paramètre de la fenêtre
    gui = tk.Tk()
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
    notebook = ttk.Notebook(gui)
    notebook.pack(pady=10, padx=10)

    # Création des différents cadres (onglets) à ajouter au Notebook
    frame1 = tk.Frame(notebook, width=1400, height=800)
    frame2 = tk.Frame(notebook, width=1400, height=800)
    frame3 = tk.Frame(notebook, width=1400, height=800)


    # Ajout des cadres (onglets) au Notebook avec un titre pour chaque onglet
    notebook.add(frame1, text='Onglet 1')
    notebook.add(frame2, text='Onglet 2')
    notebook.add(frame3, text='Onglet 3')

    # Chargement de l'image
    image_path = "images\downloaded_image.jpg"  # Chemin vers l'image
    image = Image.open(image_path)

    # original_width, original_height = image.size
    
    photo = ImageTk.PhotoImage(image)
    
    # Création d'un widget Label pour afficher l'image
    label = tk.Label(frame1, image=photo)
    label.grid(row=0, column=0, columnspan=15)


    # Créez un cadre pour la checkbox
    bw_checkbox_frame = tk.Frame(frame1, bg="#FF00FF")
    bw_checkbox_frame.grid(row=1, column=0, sticky="ew")  # Utilisez 'sticky="ew"' pour étendre le cadre sur toute la largeur

    # Créez la checkbox à l'intérieur du cadre
    bw_var = tk.BooleanVar()
    bw_checkbox = tk.Checkbutton(bw_checkbox_frame, text="Noir et blanc", variable=bw_var, command=apply_filters, bg="#FF00FF")
    bw_checkbox.pack(fill="both", expand=True)  # Utilisez 'fill="both"' et 'expand=True' pour remplir tout l'espace disponible dans le cadre


    # Créez une variable de contrôle pour le filtre Inversion de couleurs
    invert_var = tk.BooleanVar()
    # Créez une case à cocher pour le filtre Inversion de couleurs
    invert_checkbox = tk.Checkbutton(frame1, text="Inversion de couleurs", variable=invert_var, command=apply_filters)
    invert_checkbox.grid(row=1, column=1)

    # Créez une variable de contrôle pour le filtre Inversion de couleurs
    flipy_var = tk.BooleanVar()
    # Créez une case à cocher pour le filtre Inversion de couleurs
    flipy_checkbox = tk.Checkbutton(frame1, text="Miroir", variable=flipy_var, command=apply_filters)
    flipy_checkbox.grid(row=1, column=2)

    flipx_var = tk.BooleanVar()
    # Créez une case à cocher pour le filtre Inversion de couleurs
    flipx_checkbox = tk.Checkbutton(frame1, text="FlipX", variable=flipx_var, command=apply_filters)
    flipx_checkbox.grid(row=1, column=3)

    

    equalize_var = tk.BooleanVar()
    # Créez une case à cocher pour le filtre Inversion de couleurs
    equalize_checkbox = tk.Checkbutton(frame1, text="Equalize", variable=equalize_var, command=apply_filters)
    equalize_checkbox.grid(row=1, column=4)

    blur_var = tk.BooleanVar()
    # Créez une case à cocher pour le filtre Inversion de couleurs
    blur_checkbox = tk.Checkbutton(frame1, text="Blur", variable=blur_var, command=apply_filters)
    blur_checkbox.grid(row=1, column=5)

    contour_var = tk.BooleanVar()
    # Créez une case à cocher pour le filtre Inversion de couleurs
    contour_checkbox = tk.Checkbutton(frame1, text="Contour", variable=contour_var, command=apply_filters)
    contour_checkbox.grid(row=1, column=6)

    detail_var = tk.BooleanVar()
    # Créez une case à cocher pour le filtre Inversion de couleurs
    detail_checkbox = tk.Checkbutton(frame1, text="Detail", variable=detail_var, command=apply_filters)
    detail_checkbox.grid(row=1, column=7)

    edge_enhance_var = tk.BooleanVar()
    # Créez une case à cocher pour le filtre Inversion de couleurs
    edge_enhance_checkbox = tk.Checkbutton(frame1, text="Edge enhance", variable=edge_enhance_var, command=apply_filters)
    edge_enhance_checkbox.grid(row=1, column=8)

    emboss_var = tk.BooleanVar()
    # Créez une case à cocher pour le filtre Inversion de couleurs
    emboss_checkbox = tk.Checkbutton(frame1, text="Emboss", variable=emboss_var, command=apply_filters)
    emboss_checkbox.grid(row=1, column=9)

    find_edges_var = tk.BooleanVar()
    # Créez une case à cocher pour le filtre Inversion de couleurs
    find_edges_checkbox = tk.Checkbutton(frame1, text="Find Edges", variable=find_edges_var, command=apply_filters)
    find_edges_checkbox.grid(row=1, column=10)

    sharpen_var = tk.BooleanVar()
    # Créez une case à cocher pour le filtre Inversion de couleurs
    sharpen_checkbox = tk.Checkbutton(frame1, text="Sharpen", variable=sharpen_var, command=apply_filters)
    sharpen_checkbox.grid(row=1, column=11)

    scanButton2 = tk.Button(frame1, text="Réinitialiser", command = reset)
    scanButton2.config(width=15, height=1)
    scanButton2.grid(row=3, column=0)

    searchInLabel = tk.StringVar()
    entry = tk.Entry(frame1, textvariable = searchInLabel)
    entry.grid(row=2, column=1)

    scanButton3 = tk.Button(frame1, text="Nouvelle image", command = lambda: get_new_image(searchInLabel.get()))
    scanButton3.config(width=15, height=1)
    scanButton3.grid(row=2, column=0, sticky='ew')

    # Créer un bouton Quitter
    bouton_quitter = tk.Button(frame1, text="Quitter", command=quitter)
    bouton_quitter.grid(row=4, column=3)
    
    last_modified = os.path.getmtime(image_path)

    # Lance la fonction pour détecter les modifications d'image
    update_image()

    for i in range(10):
        frame1.grid_columnconfigure(i, minsize=100)

    gui.resizable(False, False)

    gui.mainloop()


# autocontrast(image, cutoff=0, ignore=None)
# colorize(image, black, white)
# crop(image, border=0)
# deform(image, quad, meshSize=0, resample=0, fill=0)
# expand(image, border, fill=None)
# fit(image, size, method=3, bleed=0.0, centering=(0.5, 0.5))
# flip(image)
# grayscale(image, weights=None)
# invert(image)
# mirror(image)
# posterize(image, bits)
# solarize(image, threshold=128)
# resize(image, size, resample=3, box=None)
# rotate(image, angle, resample=0, expand=0, center=None, translate=None)
# shear(image, xShear, yShear, resample=0, fill=0)
# transpose(image)
# transverse(image)
# equalize(image, mask=None)
# offset(image, xoffset, yoffset)
# pad(image, border, color=0)
# premultiplied_alpha(image)
# unpremultiplied_alpha(image)