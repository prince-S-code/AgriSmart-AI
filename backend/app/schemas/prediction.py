from pydantic import BaseModel, ConfigDict, Field


class CropInput(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    nitrogen: float = Field(ge=0, le=500, alias="N")
    phosphorus: float = Field(ge=0, le=500, alias="P")
    potassium: float = Field(ge=0, le=500, alias="K")
    temperature: float = Field(ge=-10, le=60)
    humidity: float = Field(ge=0, le=100)
    ph: float = Field(ge=3, le=11, alias="pH")
    rainfall: float = Field(ge=0, le=500)


class CropRecommendation(BaseModel):
    crop: str
    score: float


class CropResponse(BaseModel):
    recommended_crop: str
    alternatives: list[CropRecommendation]
    model_used: str
