import socket
import base64
import re

# Paramètres de connexion
HOST = "challenge01.root-me.org"
PORT = 52023

def solve():
    # 1. Création de la socket et connexion
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((HOST, PORT))
        print(f"[+] Connecté à {HOST}:{PORT}")

        # 2. Réception des données
        # On reçoit 1024 octets (suffisant pour ce challenge)
        data = s.recv(1024).decode('utf-8')
        print(f"[<] Reçu du serveur : {data}")

        # 3. Extraction de la chaîne à décoder
        # Le serveur envoie souvent : "my string is 'CHAINECODEE'"
        # On utilise une regex pour capturer ce qui est entre les quotes '...'
        match = re.search(r"'(.*?)'", data)
        
        if match:
            encoded_string = match.group(1)
            print(f"[*] Chaîne extraite : {encoded_string}")

            # 4. Décodage (Base64)
            decoded_bytes = base64.b64decode(encoded_string)
            decoded_string = decoded_bytes.decode('utf-8')
            print(f"[*] Chaîne décodée : {decoded_string}")

            # 5. Envoi de la réponse
            # Attention : envoyer un retour à la ligne '\n' est souvent nécessaire
            response = decoded_string + "\n"
            s.send(response.encode('utf-8'))
            print(f"[>] Réponse envoyée : {decoded_string}")

            # 6. Lire la réponse finale (le flag)
            final_response = s.recv(1024).decode('utf-8')
            print(f"[SUCCESS] Réponse du serveur :\n{final_response}")
        else:
            print("[!] Impossible de trouver la chaîne encodée dans la réponse.")

    except Exception as e:
        print(f"[!] Erreur : {e}")
    finally:
        s.close()

if __name__ == "__main__":
    solve()