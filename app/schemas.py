from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import Optional,Literal
from datetime import datetime

class SymptomInput(BaseModel):
    """Schema for symptom input from user"""
    symptoms: str = Field(..., min_length=20, description="Description of symptoms (minimum 20 characters)")
    duration: Optional[Literal["hours", "1 day", "2-3 days", "week+"]] = Field(
        None, 
        description="How long symptoms have lasted"
    )
    severity: Optional[int] = Field(None, ge=1, le=10, description="Severity on scale 1-10")
    age: Optional[int] = Field(None, ge=1, le=120, description="Patient age")
    
    @field_validator('symptoms')
    @classmethod
    def symptoms_must_be_meaningful(cls, v: str) -> str:
        """Ensure symptoms aren't just filler text"""
        if v.strip().lower() in ['test', 'testing', 'asdf', 'none']:
            raise ValueError('Please provide real symptom description')
        return v.strip()
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "symptoms": "I have a persistent headache and feel dizzy when standing up",
                "duration": "2-3 days",
                "severity": 6,
                "age": 35
            }
        }
    )

class EchoResponse(BaseModel):
    """What we send back to the user"""
    received_symptoms: str
    received_duration: Optional[str]
    received_severity: Optional[int]
    message: str

class DiagnosisResponse(BaseModel):
    """AI diagnosis response"""
    severity: str = Field(..., description="Severity level: mild, moderate, severe, emergency")
    recommendation: str = Field(..., description="What the user should do")
    confidence: float = Field(..., ge=0, le=1, description="Confidence score 0-1")
    analyzed_symptoms: str
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "severity": "moderate",
                "recommendation": "Consider seeing a doctor within 24 hours",
                "confidence": 0.75,
                "analyzed_symptoms": "headache, dizziness"
            }
        }
    )

class DiagnosisHistory(BaseModel):
    """Store diagnosis history"""
    id: int
    symptoms: str
    severity: str
    recommendation: str
    timestamp: datetime
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": 1,
                "symptoms": "headache and dizziness",
                "severity": "moderate",
                "recommendation": "See a doctor within 24 hours",
                "timestamp": "2024-02-16T10:30:00"
            }
        }
    )