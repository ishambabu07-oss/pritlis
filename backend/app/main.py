from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router as api_router, refresh_catalog
from app.services.risk_scorer import is_model_loaded

app = FastAPI(
    title="Space Debris Tracking & Collision Risk Engine",
    description="Astrodynamics SGP4 propagation and conjunction assessment API",
    version="1.0.0"
)

# Enable CORS for frontend dashboard
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production (e.g., ["http://localhost:3000"])
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")

@app.on_event("startup")
def startup_event():
    if not is_model_loaded():
        raise RuntimeError(
            "Risk model is unavailable. Build and deploy "
            "ml_pipeline/models/risk_xgboost_v1.pkl before starting the API."
        )

    print("[INIT] Booting orbital engine and caching starter TLEs...")
    try:
        # Pre-load satellite catalog on startup
        refresh_catalog("stations")  # Loads space stations & primary payloads as starter catalog
    except Exception as e:
        print(f"[WARN] Could not pre-fetch TLE catalog: {e}")

@app.get("/")
def root():
    return {"message": "Orbital Conjunction & Space Debris API is running"}
