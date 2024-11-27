import requests
import random
import os

def pokemon_from_generation(gen: int, count=6) -> list[str]:
    try:
        url = f"https://pokeapi.co/api/v2/generation/{gen}/"
        response = requests.get(url)
        response.raise_for_status()  #Esta línea checkea el status code de la request (~400/500, errores comunes, 200 OK)
        data = response.json()
        
        #Extraer nombres de los pokemons con list comprehension
        species = [pokemon['name'] for pokemon in data['pokemon_species']]
        
        #Asegurarse de que hay al menos 6 pokemons (count)
        if len(species) < count:
            print("No hay suficientes Pokémon para formar un equipo.")
            return []
        
        # Return a flat list of random Pokémon names
        return random.sample(species, count)
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener datos de la API: {e}")
        return []

def get_pokemon_stats(pokemon_name: str) -> int:
    try:
        url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}/" 
        response = requests.get(url)
        response.raise_for_status()  #Gestión de errores
        data = response.json()
        
        #Sumamos los stats
        stats = sum(stat['base_stat'] for stat in data['stats'])
        return stats
    except requests.exceptions.RequestException as e:
        print(f"Error fetching stats for {pokemon_name}: {e}")
        return 0

def calculate_team_mean(team: list[str]) -> float:
    if not team:
        return 0
    stats = [get_pokemon_stats(pokemon) for pokemon in team]
    return sum(stats) / len(stats)

def download_pokemon_image(pokemon_name: str, folder: str) -> None:
    try:
        url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}/"
        response = requests.get(url)
        response.raise_for_status()
        
        data = response.json()
        image_url = data['sprites']['front_default']  #Cogemos el sprite (imagen) frontal
        
        #Checkeo si se encuentra la url
        if image_url:
            image_response = requests.get(image_url)
            image_response.raise_for_status()
            
            #Crear la carpeta si no existe
            if not os.path.exists(folder):
                os.makedirs(folder)
            
            #Guardar la imagen con el nombre del Pokémon
            image_path = os.path.join(folder, f"{pokemon_name}.png")
            with open(image_path, 'wb') as file:
                file.write(image_response.content)
            print(f"Imagen de {pokemon_name} guardada en {image_path}")
        else:
            print(f"No se encontró una imagen para {pokemon_name}.")
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener la imagen de {pokemon_name}: {e}")

def generate_and_battle_teams() -> None:
    print("Bienvenido al generador de equipos Pokémon, elige una generación para crear una batalla Pokémon")
    
    try:
        #Obtenemos el input de generación del usuario
        gen = int(input("Elegir generación (1-9): ").strip())  # Strip spaces and convert to integer
        if gen < 1 or gen > 9:
            raise ValueError("La generación debe ser entre 1 y 9")
        
        print(f"Obteniendo los Pokémon de la generación {gen}...")
        
        #Generamos los equipos
        pokemons1 = pokemon_from_generation(gen)
        pokemons2 = pokemon_from_generation(gen)

        #Imprimimos los equipos
        if pokemons1:
            print("\nEquipo 1:")
            print(", ".join(pokemons1))
        else:
            print("Error: No se pudo generar el Equipo 1.")
        
        if pokemons2:
            print("\nEquipo 2:")
            print(", ".join(pokemons2))
        else:
            print("Error: No se pudo generar el Equipo 2.")
        
        #Calcular y comparar stats de los equipos
        if pokemons1 and pokemons2:
            print("\nCalculando estadísticas de los equipos...")
            
            team1_mean = calculate_team_mean(pokemons1)
            team2_mean = calculate_team_mean(pokemons2)
            
            print(f"\nEstadísticas promedio:")
            print(f"Equipo 1: {team1_mean:.2f}")
            print(f"Equipo 2: {team2_mean:.2f}")
            
            # Determinamos el ganador
            if team1_mean > team2_mean:
                print("\n¡El ganador es el Equipo 1!")
                winner_team = pokemons1
            elif team2_mean > team1_mean:
                print("\n¡El ganador es el Equipo 2!")
                winner_team = pokemons2
            else:
                print("\n¡Es un empate!")

            if winner_team:
                    folder = "Equipo Ganador"
                    for pokemon in winner_team:
                        download_pokemon_image(pokemon, folder)
        else:
            print("No se pudieron generar ambos equipos. No se puede determinar un ganador.")

    except ValueError as e:
        print(f"Entrada inválida: {e}")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")

#Llamamos a la función para iniciar el programa
generate_and_battle_teams()
