import tkinter as tk
from tkinter import ttk

# Créer une fenêtre
root = tk.Tk()
root.geometry("300x200")

# Créer un style
style = ttk.Style()

# Configurer le style de la checkbox
style.configure('Custom.TCheckbutton', background='blue')  # Changer 'blue' par la couleur désirée

# Créer une checkbox avec le style personnalisé
checkbox = ttk.Checkbutton(root, text="Checkbox", style='Custom.TCheckbutton')
checkbox.pack(pady=20)

# Lancer la boucle principale
root.mainloop()