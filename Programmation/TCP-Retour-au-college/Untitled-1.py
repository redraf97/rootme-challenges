import socket
import re
import math

# Configuration
HOST = "challenge01.root-me.org"
PORT = 52002

def solve():
    try:
        # 1. Connexion
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((HOST, PORT))
        print(f"[+] Connecté à {HOST}:{PORT}")

        # 2. Réception des données
        # On reçoit un bloc suffisamment grand pour avoir toute la question
        data = client.recv(1024).decode()
        print(f"[<] Reçu du serveur :\n{data}")

        # 3. Extraction des nombres (Regex)
        # La phrase typique est : "Calculate the square root of X and multiply by Y"
        # On cherche deux nombres (\d+) séparés par du texte
        match = re.search(r"square root of (\d+) and multiply by (\d+)", data)

        if match:
            num1 = int(match.group(1))
            num2 = int(match.group(2))
            print(f"[*] Nombres trouvés : {num1} et {num2}")

            # 4. Calcul mathématique
            # Racine de num1 * num2
            result = math.sqrt(num1) * num2
            
            # 5. Arrondi (2 chiffres après la virgule)
            result = round(result, 2)
            print(f"[*] Résultat calculé : {result}")

            # 6. Envoi de la réponse
            response = f"{result}\n"
            client.send(response.encode())
            print(f"[>] Réponse envoyée : {response.strip()}")

            # 7. Lecture du flag
            final_response = client.recv(1024).decode()
            print(f"[SUCCESS] Réponse finale :\n{final_response}")
            
        else:
            print("[!] Erreur : Impossible de trouver les nombres dans la réponse.")

    except Exception as e:
        print(f"[!] Erreur : {e}")
    finally:
        client.close()

if __name__ == "__main__":
    solve()