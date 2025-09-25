from .models import Prediction,FeedBack
from .db_connection import get_session




def create_prediction(file_path,success,prediction=None,predictiontime=None,predictiondate=None):
    #Si le filepath est un objet path de pathlib
    if not isinstance(file_path,str):
        file_path = str(file_path)
    kargs = {"file_path":file_path,"prediction":prediction,"prediction_time":predictiontime,"prediction_date":predictiondate,"success":success}
    with get_session() as session:
        prediction = Prediction(**kargs)
        session.add(prediction)
        session.flush()
        return prediction.prediction_id

def get_prediction(prediction_id):
    with get_session() as session:
        query = session.query(Prediction).filter(Prediction.prediction_id==prediction_id)
        result = query.one_or_none()
    if not result:
        raise ValueError(f"Impossible de récuperer la prédiction {prediction_id}")
    return result


def create_feedback(predictionid,value):
    kargs = {"prediction_id":predictionid,"feedback_value":value}
    with get_session() as session:
        try:
            prediction = get_prediction(predictionid)
        except ValueError as e:
            raise ValueError(f"Impossible de récuperer la prédiction {predictionid} lors de la creation du feedback")

        feedback = FeedBack(**kargs)
        session.add(feedback)
        session.flush()
        return feedback.feedback_id
    