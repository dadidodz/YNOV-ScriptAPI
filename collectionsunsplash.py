import requests

def get_collections():
    # Remplace "YOUR_ACCESS_KEY" par ta clé d'API Unsplash
    access_key = "iovKAwTjUlesNHFlzGElr24N6R-rYEfxXOcMEe717LU"

    # Paramètres de la requête
    params = {
        "client_id": access_key
    }

    # Requête GET à l'API Unsplash pour récupérer les collections
    response = requests.get("https://api.unsplash.com/collections", params=params)

    if response.status_code == 200:
        # Extraction des données JSON de la réponse
        data = response.json()

        # Affichage des collections
        for collection in data:
            print("Nom de la collection :", collection["title"])
            print("Description de la collection :", collection["description"])
            print("Nombre de photos dans la collection :", collection["total_photos"])
            print("Liens de la collection :", collection["links"])
            print("----------------------------------------------")
    else:
        print("Erreur lors de la requête à l'API Unsplash :", response.status_code)

# Appel de la fonction pour récupérer les collections
get_collections()
