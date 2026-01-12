import socket
import re
import base64
import zlib

HOST = "challenge01.root-me.org"
PORT = 52022

def solve():
    try:
        # 1. Connexion
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((HOST, PORT))
        print(f"[+] Connecté à {HOST}:{PORT}")

        while True:
            # 2. Réception des données
            # On reçoit les données dans la boucle car le serveur parle plusieurs fois
            data = client.recv(4096).decode()
            
            # Si on reçoit des données vides, le serveur a coupé
            if not data:
                break
                
            print(f"[<] Reçu : {data}")

            # 3. Vérification de victoire (Flag)
            # Si le mot "flag" ou "Well done" est dans le message, on a gagné
            if "flag" in data.lower() or "well done" in data.lower():
                print("\n[SUCCESS] FLAG TROUVÉ !")
                print(data)
                break

            # 4. Extraction de la chaîne (entre les quotes ')
            match = re.search(r"'(.*?)'", data)
            if match:
                encoded_str = match.group(1)
                
                try:
                    # 5. Traitement (Double couche)
                    # Étape A : Base64 -> Bytes compressés
                    compressed_data = base64.b64decode(encoded_str)
                    
                    # Étape B : Décompression Zlib -> Texte original
                    decoded_bytes = zlib.decompress(compressed_data)
                    decoded_text = decoded_bytes.decode()
                    
                    print(f"[*] Décodé : {decoded_text}")

                    # 6. Envoi de la réponse
                    # On renvoie le texte suivi d'un saut de ligne
                    response = decoded_text + "\n"
                    client.send(response.encode())
                    
                except Exception as e:
                    print(f"[!] Erreur de décodage : {e}")
                    break
            else:
                # Parfois le serveur envoie juste du texte sans question, on continue d'écouter
                pass

    except KeyboardInterrupt:
        print("\n[!] Arrêt par l'utilisateur")
    except Exception as e:
        print(f"[!] Erreur de connexion : {e}")
    finally:
        client.close()

if __name__ == "__main__":
    solve()