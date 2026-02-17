# Asclepius FastAPI Learning

>  Learning FastAPI by building a medical symptom triage API - Week 2 of Project Asclepius

A mini-project built while following a 16-week journey to create an AI-powered medical triage system. This repository represents Week 2 (FastAPI & Pydantic fundamentals).

##  What I Learned

- FastAPI basics and routing
- Pydantic v2 for data validation
- RESTful API design patterns
- Request/response models
- Interactive API documentation
- In-memory data storage

##  Features

### Current Endpoints

- **GET `/`** - API status and information
- **GET `/health`** - Health check endpoint
- **POST `/echo`** - Echo back symptom data (practice endpoint)
- **POST `/diagnose`** - Analyze symptoms and provide triage recommendations
- **GET `/history`** - Retrieve diagnosis history
- **DELETE `/history`** - Clear diagnosis history

### Data Validation

- Symptoms must be at least 20 characters
- Duration restricted to: `hours`, `1 day`, `2-3 days`, `week+`
- Severity scale: 1-10
- Age validation: 1-120 years
- Custom validators for meaningful input

### Diagnosis Logic

Currently uses keyword-based logic (will be replaced with AI in Weeks 4-6):
- **Emergency**: Detects critical symptoms (chest pain, severe bleeding, etc.)
- **Severe**: High severity score (8-10)
- **Moderate**: Medium severity (5-7)
- **Mild**: Low severity (1-4)

##  Tech Stack

- **Python 3.10+**
- **FastAPI** - Modern web framework
- **Pydantic v2** - Data validation
- **Uvicorn** - ASGI server

##  Installation

1. **Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/asclepius-fastapi-learning.git
cd asclepius-fastapi-learning
```

2. **Create virtual environment**
```bash
python -m venv venv

# Activate it:
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the server**
```bash
uvicorn app.main:app --reload
```

5. **Open the interactive docs**
```
http://127.0.0.1:8000/docs
```

##  Usage Examples

### Diagnose Mild Symptoms
```bash
curl -X POST "http://127.0.0.1:8000/diagnose" \
  -H "Content-Type: application/json" \
  -d '{
    "symptoms": "I have a slight runny nose and minor cough today",
    "duration": "1 day",
    "severity": 3,
    "age": 30
  }'
```

### Diagnose Emergency
```bash
curl -X POST "http://127.0.0.1:8000/diagnose" \
  -H "Content-Type: application/json" \
  -d '{
    "symptoms": "I have crushing chest pain radiating to my left arm",
    "duration": "hours",
    "severity": 10,
    "age": 55
  }'
```

### Get History
```bash
curl http://127.0.0.1:8000/history
```

## 📖 API Documentation

Once the server is running, visit:
- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc
- **OpenAPI JSON**: http://127.0.0.1:8000/openapi.json

##  Project Structure
```
asclepius-fastapi-learning/
├── app/
│   ├── __init__.py
│   ├── main.py           # FastAPI app and endpoints
│   └── schemas.py        # Pydantic models
├── venv/                 # Virtual environment (gitignored)
├── requirements.txt      # Python dependencies
├── .gitignore
└── README.md
```

##  Learning Milestones

- [x] Set up Python virtual environment
- [x] Create FastAPI application
- [x] Build GET and POST endpoints
- [x] Implement Pydantic v2 validation
- [x] Add custom field validators
- [x] Create in-memory data storage
- [x] Auto-generated API documentation
- [ ] Add CORS middleware (Week 2, Day 2)
- [ ] Connect to PostgreSQL (Week 3)
- [ ] Integrate AI model (Weeks 4-6)

##  Important Disclaimers

**This is a learning project and NOT for medical use:**
- No real medical diagnoses
- Not a substitute for professional medical advice
- Emergency detection is basic keyword matching
- Always consult healthcare professionals for medical concerns

##  Future Enhancements (Upcoming Weeks)

- **Week 3**: PostgreSQL database integration with SQLAlchemy
- **Week 4-6**: AI model integration (vLLM + Llama 3)
- **Week 7-8**: Docker containerization
- **Week 9-11**: Flutter mobile app
- **Week 12-13**: Authentication and security
- **Week 14-16**: Production deployment

## Learning Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic v2 Documentation](https://docs.pydantic.dev/)
- [Asclepius 16-Week Learning Guide](link-to-your-guide)

##  Part of Project Asclepius

This repository is part of a 16-week learning journey to build a complete AI-powered medical triage system. See the full project roadmap in the main Asclepius repository.

##  License

MIT License - Feel free to use this for your own learning!

##  Acknowledgments

Built following the Asclepius 16-Week YouTube Learning Path, with tutorials from:
- ArjanCodes
- freeCodeCamp.org
- Corey Schafer
- Tech With Tim

---

**Day 1 Status**:  Complete  
**Current Week**: Week 2 - FastAPI & Pydantic  
**Next Up**: CORS Middleware & Testing
