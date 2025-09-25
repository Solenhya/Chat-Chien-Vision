import sys
from pathlib import Path
import uuid
# Ajouter les chemins nécessaires
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from config.settings import TEMP_FOLDER

def save_image(imagedata,imagename,addedpath=None):
    
    path = Path(TEMP_FOLDER)

    if(addedpath):
        path = path / addedpath
    
    path.mkdir(parents=True,exist_ok=True)

    file_id = f"{uuid.uuid4()}_{imagename}"

    file_path = path/file_id
    
        # Write binary data to disk
    file_path.write_bytes(imagedata)

    return file_path