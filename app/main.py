from fastapi import FastAPI, status
from app.schemas import SymptomInput, EchoResponse, DiagnosisResponse, DiagnosisHistory
from datetime import datetime
from typing import List

# In-memory storage (temporary - we'll use PostgreSQL in Week 3)
diagnosis_history: List[DiagnosisHistory] = []
diagnosis_counter = 0

# Create the FastAPI app instance
app = FastAPI(
    title='Asclepius API',
    description='Learning FastAPI with a medical symptom checker',
    version='0.1.0'
)

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "🚀 Asclepius API is running!",
        "status": "running",
        "version": "0.1.0"
    }

# Health-check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "asclepius-api"
    }

# Echo endpoint - accepts POST requests
@app.post("/echo", response_model=EchoResponse)
async def echo_symptoms(symptom_data: SymptomInput):
    """
    Echo back the symptom data we received.
    This teaches us how to accept POST requests with validation.
    """
    return EchoResponse(
        received_symptoms=symptom_data.symptoms,  # Fixed typo: received not recieved
        received_duration=symptom_data.duration,
        received_severity=symptom_data.severity,
        message=f"✅ Received your symptoms: {symptom_data.symptoms[:50]}..."
    )

# Diagnosis endpoint - simulates AI analysis
@app.post("/diagnose", response_model=DiagnosisResponse)
async def diagnose_symptoms(symptom_data: SymptomInput):
    """
    Analyse symptoms and provide a basic diagnosis.
    Later I'll connect it to real AI model.
    """
    global diagnosis_counter
    
    # Simple keyword-based logic (I'll replace this with AI later)
    symptoms_lower = symptom_data.symptoms.lower()
    
    # Check for emergency keywords
    emergency_keywords = ["chest pain", "can't breathe", "severe bleeding", "stroke"]
    if any(keyword in symptoms_lower for keyword in emergency_keywords):
        result = DiagnosisResponse(
            severity="emergency",
            recommendation="🚨 Call 112 immediately or go to the nearest emergency room",
            confidence=0.95,
            analyzed_symptoms=symptom_data.symptoms
        )
    # Check severity from user input
    elif symptom_data.severity and symptom_data.severity >= 8:
        result = DiagnosisResponse(
            severity="severe",
            recommendation="Seek medical attention within 4 hours",
            confidence=0.80,
            analyzed_symptoms=symptom_data.symptoms
        )
    elif symptom_data.severity and symptom_data.severity >= 5:
        result = DiagnosisResponse(
            severity="moderate",
            recommendation="Consider seeing a doctor within 24-48 hours",
            confidence=0.70,
            analyzed_symptoms=symptom_data.symptoms
        )
    else:
        result = DiagnosisResponse(
            severity="mild",
            recommendation="Monitor symptoms. Rest and stay hydrated. See a doctor if symptoms worsen.",
            confidence=0.65,
            analyzed_symptoms=symptom_data.symptoms
        )
    
    # Save to history
    diagnosis_counter += 1
    history_entry = DiagnosisHistory(
        id=diagnosis_counter,
        symptoms=symptom_data.symptoms,
        severity=result.severity,
        recommendation=result.recommendation,
        timestamp=datetime.now()
    )
    diagnosis_history.append(history_entry)
    
    return result

# History endpoint - get all past diagnoses
@app.get("/history", response_model=List[DiagnosisHistory])
async def get_diagnosis_history():
    """
    Get all past diagnosis records.
    In Week 3, this will query from PostgreSQL database.
    """
    return diagnosis_history

# Clear history endpoint (useful for testing)
@app.delete("/history", status_code=status.HTTP_204_NO_CONTENT)
async def clear_history():
    """
    Clear all diagnosis history (for testing purposes).
    """
    global diagnosis_counter
    diagnosis_history.clear()
    diagnosis_counter = 0