from pydantic import BaseModel, ConfigDict

import json
import uuid
import time

from sqlalchemy import Column, String, BigInteger, Boolean, Text

from apps.webui.internal.db import Base, get_db, engine

####################
# Annotation DB Schema
####################

class Annotation(Base):
    __tablename__ = 'annotation'

    id = Column(String, primary_key=True)
    user_id = Column(String)
    chat_id = Column(String)
    message_id = Column(String)
    annotation = Column(Text)  # Save Annotation JSON as Text

    created_at = Column(BigInteger)
    updated_at = Column(BigInteger)

    archived = Column(Boolean, default=False)

class AnnotationModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    user_id: str
    chat_id: str
    message_id: str
    annotation: str

    created_at: int  # timestamp in epoch
    updated_at: int  # timestamp in epoch

    archived: bool = False

class AnnotationTable:
    def insert_or_update_annotation(self, user_id: str, chat_id: str, message_id: str, annotation):
        with (get_db() as db):
            existing_annotation = (
                db.query(Annotation)
                .filter_by(user_id=user_id, message_id=message_id)
                .first()
            )
            if existing_annotation:
                existing_annotation.annotation = json.dumps(annotation)
                existing_annotation.updated_at = int(time.time())
                db.commit()
                db.refresh(existing_annotation)

                return AnnotationModel.model_validate(existing_annotation)
            else:
                id = str(uuid.uuid4())
                annotation = AnnotationModel(
                    **{
                        'id': id,
                        "user_id": user_id,
                        "chat_id": chat_id,
                        "message_id": message_id,
                        "annotation": json.dumps(annotation),
                        "created_at": int(time.time()),
                        "updated_at": int(time.time()),
                    }
                )
                result = Annotation(**annotation.model_dump())
                db.add(result)
                db.commit()
                db.refresh(result)
                return AnnotationModel.model_validate(result) if result else None

    def get_annotation_map_by_chat_id_and_user_id(self, chat_id: str, user_id: str):
        annotation_list = self.get_annotation_list_by_chat_id_and_user_id(chat_id, user_id)
        if annotation_list is None:
            return None
        return {ann.message_id: json.loads(ann.annotation) for ann in annotation_list}

    def get_annotation_list_by_chat_id(self, chat_id: str):
        try:
            with get_db() as db:
                all_annotations = (
                    db.query(Annotation)
                    .filter_by(chat_id=chat_id)
                    .all()
                )
                return [AnnotationModel.model_validate(annotation) for annotation in all_annotations]
        except Exception as e:
            return None

    def get_annotation_list_by_chat_id_and_user_id(self, chat_id: str, user_id: str):
        try:
            with get_db() as db:
                all_annotations = (
                    db.query(Annotation)
                    .filter_by(chat_id=chat_id, user_id=user_id)
                    .all()
                )
                return [AnnotationModel.model_validate(annotation) for annotation in all_annotations]
        except Exception as e:
            return None

# 创建 annotation 表
# Base.metadata.create_all(engine)

Annotations = AnnotationTable()