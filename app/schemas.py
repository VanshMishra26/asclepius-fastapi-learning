from pydantic import BaseModel, Field, field_validator, model_validator, computed_field, ConfigDict
from typing import Optional, Literal, List
from datetime import datetime
import re



class VitalSigns(BaseModel):
    """Custom type for vital signs with validation"""
    heart_rate: Optional[int] = Field(None, ge=40, le=200, description="Heart rate in BPM")
    blood_pressure: Optional[str] = Field(None, description="Format: systolic/diastolic (e.g., 120/80)")
    temperature: Optional[float] = Field(None, ge=95.0, le=108.0, description="Body temp in Fahrenheit")
    
    @field_validator('blood_pressure')
    @classmethod
    def validate_bp_format(cls, v):
        if v is None:
            return v
        # Check format: systolic/diastolic (e.g., 120/80)
        if not re.match(r'^\d{2,3}/\d{2,3}$', v):
            raise ValueError('Blood pressure must be in format: systolic/diastolic (e.g., 120/80)')
        
        systolic, diastolic = map(int, v.split('/'))
        
        if not (70 <= systolic <= 200):
            raise ValueError('Systolic pressure must be between 70-200 mmHg')
        if not (40 <= diastolic <= 130):
            raise ValueError('Diastolic pressure must be between 40-130 mmHg')
        if systolic <= diastolic:
            raise ValueError('Systolic must be greater than diastolic')
        
        return v



class SymptomInput(BaseModel):
    """Enhanced schema for symptom input with advanced validation"""
    symptoms: str = Field(..., min_length=20, description="Description of symptoms (minimum 20 characters)")
    duration: Optional[Literal["hours", "1 day", "2-3 days", "week+"]] = Field(
        None, 
        description="How long symptoms have lasted"
    )
    severity: Optional[int] = Field(None, ge=1, le=10, description="Severity on scale 1-10")
    age: Optional[int] = Field(None, ge=1, le=120, description="Patient age")
    
    # Optional vital signs
    heart_rate: Optional[int] = Field(None, ge=40, le=200, description="Heart rate in BPM")
    blood_pressure: Optional[str] = Field(None, description="Format: 120/80")
    temperature: Optional[float] = Field(None, ge=95.0, le=108.0, description="Body temperature in Fahrenheit")
    
  
    
    @field_validator('symptoms')
    @classmethod
    def validate_symptoms_not_spam(cls, v: str) -> str:
        """Detect spam, test data, and meaningless input"""
        v_lower = v.strip().lower()
        
        # Check for common test phrases
        spam_phrases = ['test', 'testing', 'asdf', 'qwerty', 'none', 'n/a', 'dummy']
        if any(phrase in v_lower for phrase in spam_phrases):
            raise ValueError('Please provide real symptom description, not test data')
        
        # Check for repeated words (e.g., "pain pain pain pain")
        words = v_lower.split()
        if len(words) > 3:
            unique_words = set(words)
            if len(unique_words) / len(words) < 0.4:  # Less than 40% unique words
                raise ValueError('Please provide varied symptom description')
        
        # Check for excessive punctuation
        if v.count('!') > 3 or v.count('?') > 3:
            raise ValueError('Please use normal punctuation')
        
        return v.strip()
    
    @field_validator('blood_pressure')
    @classmethod
    def validate_blood_pressure(cls, v):
        """Validate blood pressure format and ranges"""
        if v is None:
            return v
        
        if not re.match(r'^\d{2,3}/\d{2,3}$', v):
            raise ValueError('Blood pressure must be in format: 120/80')
        
        systolic, diastolic = map(int, v.split('/'))
        
        if not (70 <= systolic <= 200):
            raise ValueError('Systolic pressure must be between 70-200 mmHg')
        if not (40 <= diastolic <= 130):
            raise ValueError('Diastolic pressure must be between 40-130 mmHg')
        if systolic <= diastolic:
            raise ValueError('Systolic must be greater than diastolic')
        
        return v
    
    @field_validator('age')
    @classmethod
    def validate_age_realistic(cls, v):
        """Validate age and provide warnings"""
        if v is not None:
            if v < 1:
                raise ValueError('Age must be at least 1')
            if v > 120:
                raise ValueError('Age seems unrealistic')
        return v
    
    
    @model_validator(mode='after')
    def validate_age_symptom_compatibility(self):
        """Check if age and symptoms make sense together"""
        if self.age and self.symptoms:
            symptoms_lower = self.symptoms.lower()
            
            # Pediatric checks (age < 12)
            if self.age < 12:
                adult_keywords = ['pregnancy', 'menopause', 'prostate', 'erectile', 'viagra']
                if any(keyword in symptoms_lower for keyword in adult_keywords):
                    raise ValueError(f'Symptoms not appropriate for age {self.age}')
            
            # Geriatric checks (age > 70)
            if self.age > 70 and self.severity and self.severity < 3:
                # Elderly patients rarely self-report low severity for serious conditions
                if any(word in symptoms_lower for word in ['chest pain', 'stroke', 'fall']):
                    raise ValueError('Severity seems low for reported symptoms in elderly patient')
        
        return self
    
    @model_validator(mode='after')
    def validate_severity_matches_description(self):
        """Ensure severity matches symptom description"""
        if self.severity and self.symptoms:
            symptoms_lower = self.symptoms.lower()
            
            # High severity should have serious keywords
            if self.severity >= 8:
                serious_keywords = ['severe', 'extreme', 'intense', 'unbearable', 'can\'t', 'unable']
                if not any(keyword in symptoms_lower for keyword in serious_keywords):
                    raise ValueError('High severity (8+) should be described with words like "severe", "intense", etc.')
            
            # Low severity shouldn't have emergency keywords
            if self.severity <= 3:
                emergency_keywords = ['severe', 'extreme', 'unbearable', 'emergency']
                if any(keyword in symptoms_lower for keyword in emergency_keywords):
                    raise ValueError('Low severity (1-3) conflicts with emergency-level symptom description')
        
        return self
    
    
    @computed_field
    @property
    def risk_score(self) -> int:
        """
        Calculate risk score based on age, severity, and vital signs
        Range: 0-100
        """
        score = 0
        
        # Age component (0-30 points)
        if self.age:
            if self.age < 1:
                score += 20
            elif self.age < 5:
                score += 15
            elif self.age > 70:
                score += 25
            elif self.age > 60:
                score += 15
            else:
                score += 5
        
        # Severity component (0-40 points)
        if self.severity:
            score += self.severity * 4
        
        # Vital signs component (0-30 points)
        if self.heart_rate:
            if self.heart_rate > 100 or self.heart_rate < 60:
                score += 15
        
        if self.temperature:
            if self.temperature > 100.4 or self.temperature < 97:
                score += 15
        
        return min(score, 100)  # Cap at 100
    
    @computed_field
    @property
    def urgency_level(self) -> str:
        """
        Determine urgency based on risk score
        """
        if self.risk_score >= 70:
            return "CRITICAL"
        elif self.risk_score >= 50:
            return "HIGH"
        elif self.risk_score >= 30:
            return "MODERATE"
        else:
            return "LOW"
    
    @computed_field
    @property
    def patient_category(self) -> str:
        """Categorize patient by age"""
        if not self.age:
            return "UNKNOWN"
        if self.age < 2:
            return "INFANT"
        elif self.age < 12:
            return "PEDIATRIC"
        elif self.age < 18:
            return "ADOLESCENT"
        elif self.age < 65:
            return "ADULT"
        else:
            return "GERIATRIC"
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "symptoms": "I have a persistent severe headache with dizziness and nausea",
                "duration": "2-3 days",
                "severity": 7,
                "age": 35,
                "heart_rate": 95,
                "blood_pressure": "140/90",
                "temperature": 99.5
            }
        }
    )



class EchoResponse(BaseModel):
    """What we send back to the user"""
    received_symptoms: str
    received_duration: Optional[str]
    received_severity: Optional[int]
    message: str
    risk_score: int
    urgency_level: str
    patient_category: str


class DiagnosisResponse(BaseModel):
    """AI diagnosis response"""
    severity: str = Field(..., description="Severity level: mild, moderate, severe, emergency")
    recommendation: str = Field(..., description="What the patient should do")
    confidence: float = Field(..., ge=0, le=1, description="Confidence score 0-1")
    analyzed_symptoms: str
    risk_score: int = Field(..., description="Calculated risk score 0-100")
    urgency_level: str = Field(..., description="Urgency level based on risk")
    patient_category: str = Field(..., description="Patient age category")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "severity": "moderate",
                "recommendation": "Consider seeing a doctor within 24 hours",
                "confidence": 0.75,
                "analyzed_symptoms": "headache, dizziness",
                "risk_score": 45,
                "urgency_level": "MODERATE",
                "patient_category": "ADULT"
            }
        }
    )


class DiagnosisHistory(BaseModel):
    """Store diagnosis history"""
    id: int
    symptoms: str
    severity: str
    recommendation: str
    risk_score: int
    timestamp: datetime
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": 1,
                "symptoms": "headache and dizziness",
                "severity": "moderate",
                "recommendation": "See a doctor within 24 hours",
                "risk_score": 45,
                "timestamp": "2024-02-16T10:30:00"
            }
        }
    )