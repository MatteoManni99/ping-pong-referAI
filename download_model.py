import urllib.request
import os
import json

# URL del modello
MODEL_NAME = "pose_landmarker.task"

def download_model(model_url: str) -> bool:
    """Scarica il modello pose_landmarker se non esiste già."""
    
    # Controlla se il file esiste già
    if os.path.exists(MODEL_NAME):
        print(f"✓ {MODEL_NAME} esiste già. Download saltato.")
        return True
    
    print(f"Scaricando {MODEL_NAME}...")
    print(f"URL: {model_url}")
    
    try:
        # Scarica il file con barra di progresso
        urllib.request.urlretrieve(model_url, MODEL_NAME)
        
        # Verifica che il file sia stato scaricato
        if os.path.exists(MODEL_NAME):
            file_size = os.path.getsize(MODEL_NAME) / (1024 * 1024)  # Converti in MB
            print(f"✓ Download completato!")
            print(f"✓ File salvato: {os.path.abspath(MODEL_NAME)}")
            print(f"✓ Dimensione: {file_size:.2f} MB")
            return True
        else:
            print("✗ Errore: il file non è stato salvato correttamente.")
            return False
            
    except Exception as e:
        print(f"✗ Errore durante il download: {e}")
        return False

if __name__ == "__main__":
    with open('config.json', 'r') as config_file:
        config_data = json.load(config_file)
    success = download_model(model_url = config_data["MODEL_URL_HEAVY"])
    exit(0 if success else 1)