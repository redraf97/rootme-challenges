import socket
import re
import codecs

# Configuration
HOST = "challenge01.root-me.org"
PORT = 52021

def solve():
    try:
        # 1. Connexion
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((HOST, PORT))
        print(f"[+] Connecté à {HOST}:{PORT}")

        # 2. Réception
        data = client.recv(1024).decode()
        print(f"[<] Reçu du serveur : {data.strip()}")

        # 3. Extraction de la chaîne (entre les simples quotes'')
        match = re.search(r"'(.*?)'", data)
        
        if match:
            encoded_str = match.group(1)
            print(f"[*] Chaîne chiffrée : {encoded_str}")

            # 4. Décodage ROT13
            # Python a un codec natif pour ça !
            decoded_str = codecs.decode(encoded_str, 'rot_13')
            print(f"[*] Chaîne décodée : {decoded_str}")

            # 5. Envoi de la réponse
            response = f"{decoded_str}\n"
            client.send(response.encode())
            print(f"[>] Réponse envoyée.")

            # 6. Récupération du flag
            final_response = client.recv(1024).decode()
            print(f"[SUCCESS] Réponse finale :\n{final_response}")
            
        else:
            print("[!] Impossible de trouver la chaîne entre quotes.")

    except Exception as e:
        print(f"[!] Erreur : {e}")
    finally:
        client.close()

if __name__ == "__main__":
    solve()