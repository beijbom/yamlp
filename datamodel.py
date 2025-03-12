from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from sqlmodel import Field, Relationship, SQLModel


class BoundingBox(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    center_x: float
    center_y: float
    width: float
    height: float
    label_name: str
    annotator_name: str
    image_id: int = Field(foreign_key="image.id")
    created_at: datetime = Field(default_factory=datetime.now)
    image: "Image" = Relationship(back_populates="boxes")


class Image(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    filename: str
    width: int
    height: int
    created_at: datetime = Field(default_factory=datetime.now)
    boxes: list[BoundingBox] = Relationship(back_populates="image")


class ImageDetectionSample(BaseModel):
    image_url: str
    image_width: int
    image_height: int
    boxes: list[BoundingBox]
