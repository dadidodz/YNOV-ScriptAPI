import os
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image, ImageOps, ImageFilter
import requests
import random

def get_random_image(query=""):
    access_key = "iovKAwTjUlesNHFlzGElr24N6R-rYEfxXOcMEe717LU"
    url = "https://api.unsplash.com/photos/random"
    if query:
        url = "https://api.unsplash.com/search/photos"
    params = {"client_id": access_key, "query": query, "per_page": 10}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if query:
            return random.choice(data["results"])["urls"]["regular"]
        return data["urls"]["regular"]
    print("Error:", response.status_code)
    return None

def download_image(url, folder="images", filename="downloaded_image.jpg"):
    os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, filename)
    with open(filepath, 'wb') as f:
        f.write(requests.get(url).content)
    return filepath

def apply_filters():
    image_filtered = Image.open(image_path)
    filters = [
        (bw_var, ImageOps.grayscale),
        (invert_var, ImageOps.invert),
        (flipy_var, ImageOps.mirror),
        (flipx_var, ImageOps.flip),
        (equalize_var, ImageOps.equalize),
        (blur_var, lambda img: img.filter(ImageFilter.GaussianBlur(radius=5))),
        (contour_var, ImageFilter.CONTOUR),
        (detail_var, ImageFilter.DETAIL),
        (edge_enhance_var, ImageFilter.EDGE_ENHANCE),
        (emboss_var, ImageFilter.EMBOSS),
        (find_edges_var, ImageFilter.FIND_EDGES),
        (sharpen_var, ImageFilter.SHARPEN)
    ]
    for var, filter_func in filters:
        if var.get():
            if isinstance(filter_func, type):
                image_filtered = image_filtered.filter(filter_func)
            else:
                image_filtered = filter_func(image_filtered)
    photo = ImageTk.PhotoImage(image_filtered)
    label.config(image=photo)
    label.image = photo

def reset():
    for var in (bw_var, invert_var, flipy_var, flipx_var, equalize_var, blur_var, contour_var,
                detail_var, edge_enhance_var, emboss_var, find_edges_var, sharpen_var):
        var.set(False)
    apply_filters()

def update_image():
    global last_modified
    if os.path.getmtime(image_path) != last_modified:
        image = Image.open(image_path)
        photo = ImageTk.PhotoImage(image)
        label.config(image=photo)
        label.image = photo
        last_modified = os.path.getmtime(image_path)
    gui.after(1000, update_image)

def resize_image():
    image = Image.open(image_path)
    frame_width, frame_height = frame1.winfo_width(), frame1.winfo_height()
    max_width, max_height = int(frame_width * 0.9), int(frame_height * 0.9)
    if image.width > max_width or image.height > max_height:
        image = ImageOps.fit(image, (max_width, max_height))
        image.save(image_path)

def quit_app():
    gui.quit()

def download_filtered_image():
    image_originale = Image.open(image_path)
    image_filtree = image_originale.copy()
    apply_filters()
    image_filtree.save("images/image_filtree.jpg")

if __name__ == "__main__":
    gui = tk.Tk()
    gui.title("API Application")
    window_width, window_height = int(gui.winfo_screenwidth() * 0.9), int(gui.winfo_screenheight() * 0.9)
    gui.geometry(f"{window_width}x{window_height}")

    notebook = ttk.Notebook(gui)
    notebook.pack(pady=10, padx=10)

    frame1 = tk.Frame(notebook, width=1400, height=800)
    frame2 = tk.Frame(notebook, width=1400, height=800)
    frame3 = tk.Frame(notebook, width=1400, height=800)
    notebook.add(frame1, text='Onglet 1')
    notebook.add(frame2, text='Onglet 2')
    notebook.add(frame3, text='Onglet 3')

    image_path = "images/downloaded_image.jpg"
    image = Image.open(image_path)
    photo = ImageTk.PhotoImage(image)
    label = tk.Label(frame1, image=photo)
    label.grid(row=0, column=0, columnspan=15)

    bw_var = tk.BooleanVar()
    invert_var = tk.BooleanVar()
    flipy_var = tk.BooleanVar()
    flipx_var = tk.BooleanVar()
    equalize_var = tk.BooleanVar()
    blur_var = tk.BooleanVar()
    contour_var = tk.BooleanVar()
    detail_var = tk.BooleanVar()
    edge_enhance_var = tk.BooleanVar()
    emboss_var = tk.BooleanVar()
    find_edges_var = tk.BooleanVar()
    sharpen_var = tk.BooleanVar()


    # Définir une liste de noms de variables correspondant à bw_var, invert_var, etc.
    var_names = ["Amelioration", "Bords", "Contour", "Détail", "Égaliser", 
             "Flou", "Gaufrage", "Inversion", "Miroir Y", 
             "Miroir X", "Noir et Blanc", "Netteté"]

    for i, var in enumerate((bw_var, invert_var, flipy_var, flipx_var, equalize_var, blur_var, contour_var,
                             detail_var, edge_enhance_var, emboss_var, find_edges_var, sharpen_var)):
        var.set(False)
        tk.Checkbutton(frame1, text=var_names[i], variable=var, command=apply_filters).grid(row=1, column=i)

    tk.Button(frame1, text="Réinitialiser", command=reset).grid(row=3, column=0)
    search_label = tk.StringVar()
    tk.Entry(frame1, textvariable=search_label).grid(row=2, column=1)
    tk.Button(frame1, text="Nouvelle image", command=lambda: [download_image(get_random_image(search_label.get())), reset()]).grid(row=2, column=0, sticky='ew')
    tk.Button(frame1, text="Quitter", command=quit_app).grid(row=4, column=3)
    tk.Label(frame1, text="Texte initial").grid(row=2, column=2, columnspan=5)
    tk.Button(frame1, text="Télécharger", command=download_filtered_image).grid(row=4, column=0)

    last_modified = os.path.getmtime(image_path)
    update_image()
    for i in range(11):
        frame1.grid_columnconfigure(i, minsize=110)
    gui.resizable(False, False)
    gui.mainloop()
