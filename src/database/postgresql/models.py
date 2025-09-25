from sqlalchemy import Integer, String,ForeignKey,Date,Time,DateTime , Boolean,Float
from sqlalchemy.orm import relationship , mapped_column , Mapped
from sqlalchemy.dialects.postgresql import UUID
from .database import Base
import uuid


class Prediction(Base):
    __tablename__="prediction"
    prediction_id:Mapped[uuid.UUID]= mapped_column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4  # génère l’UUID dans le code Python
    )
    file_path = mapped_column(String)
    success= mapped_column(Boolean)
    prediction = mapped_column(String)
    prediction_time=mapped_column(Float)
    prediction_date = mapped_column(DateTime)
    feedback : Mapped["FeedBack"] = relationship(back_populates="prediction")

class FeedBack(Base):
    __tablename__="feedback"
    feedback_id:Mapped[uuid.UUID]=  mapped_column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4  
    )
    prediction_id:Mapped[uuid.UUID]= mapped_column(ForeignKey("prediction.prediction_id"))
    feedback_value: Mapped[Integer]=mapped_column(Integer)
    prediction: Mapped["Prediction"] = relationship(back_populates="feedback")
