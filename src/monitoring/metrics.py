import csv
import time
from datetime import datetime
from pathlib import Path
from functools import wraps
import sys

# Ajouter le répertoire racine au path
ROOT_DIR = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

from config.settings import ROOT_DIR, PROCESSED_DATA_DIR
from database.postgresql.crud import create_prediction,create_feedback
from utils.temp_file import save_image
# Fichier CSV pour stocker les métriques
MONITORING_FILE = PROCESSED_DATA_DIR / "monitoring_inference.csv"

def ensure_monitoring_file():
    """Créer le fichier CSV avec les headers si nécessaire"""
    if not MONITORING_FILE.exists():
        with open(MONITORING_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                'timestamp',
                'inference_time_ms',
                'success'
            ])

def log_inference_time(inference_time_ms: float, success: bool = True):
    """Enregistrer une métrique d'inférence dans le CSV"""
    ensure_monitoring_file()
    
    timestamp = datetime.now().isoformat()
    
    with open(MONITORING_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            timestamp,
            round(inference_time_ms, 2),
            success
        ])

def log_inference(file_path,inference_time,prediction=None,success:bool = True):
    """Une fonction pour logger dans la base de donnée une prediction effectuer"""
    #Sauvegarde le fichier dans un dossier temporaire TODO

    filepath = file_path
    date = datetime.now().isoformat()
    #Creer la prediction
    prediction = create_prediction(file_path=filepath,prediction=prediction,predictiontime=inference_time,predictiondate=date,success=success)
    return prediction.prediction_id

def log_feedback(predictionid,value):
    """Fonction pour logger le feedback. Version qui fait appel a la base de donnée"""
    feedback=create_feedback(predictionid,value)
    return feedback.feedback_id

def time_inference(func):
    """Décorateur pour mesurer le temps d'inférence"""
    @wraps(func)
    async def wrapper(file,*args, **kwargs):
        start_time = time.perf_counter()
        filepath=None
        try:
            result = await func(file,*args, **kwargs)
            end_time = time.perf_counter()
            
            # Calculer le temps en millisecondes
            inference_time_ms = (end_time - start_time) * 1000
            await file.seek(0)
            image_data = file.read()
            filepath = save_image(imagedata=image_data,imagename=file.name)
            # Extraire les informations du résultat si possible
            if hasattr(result, 'body'):
                # FastAPI Response object
                import json
                try:
                    response_data = json.loads(result.body)
                    prediction = response_data["prediction"]
                    prediction_id = log_inference(file_path=filepath,
                        prediction=prediction,
                        inference_time=inference_time_ms,
                        success=True
                    )
                    response_data["prediction_id"]=prediction_id
                    result.body = json.dumps(response_data)
                except:
                    log_inference(file_path=filepath,inference_time=inference_time_ms,prediction=None,sucess=False)

            else:
                # Dict response
                log_inference(file_path=filepath,inference_time=inference_time_ms,prediction=None,sucess=False)
            return result
            
        except Exception as e:
            end_time = time.perf_counter()
            inference_time_ms = (end_time - start_time) * 1000
            
            # Logger l'erreur
            log_inference(file_path=filepath,inference_time=inference_time_ms,prediction=None,success=False)

            
            raise e
    
    return wrapper