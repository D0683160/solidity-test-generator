from fastapi import FastAPI
from pydantic import BaseModel
from backend.generator import generate_test_code
from backend.tester import run_tests
import requests

app = FastAPI()

class TestRequest(BaseModel):
    mode: str
    model: str
    filename: str
    contract_code: str
    use_rag: bool  # <<<<<< 加這一行！

@app.get("/list_models")
def list_models():
    try:
        response = requests.get("http://localhost:11434/api/tags")
        response.raise_for_status()
        data = response.json()
        model_list = [model["name"] for model in data["models"]]
        return {"models": model_list}
    except Exception as e:
        return {"models": [], "error": str(e)}

@app.post("/generate_test")
def generate_test(req: TestRequest):
    test_code = generate_test_code(
        selected_mode=req.mode,
        contract_code=req.contract_code,
        model_name=req.model,
        filename=req.filename,
        use_rag=req.use_rag
    )
    return {"test_code": test_code}

@app.post("/run_tests")
def run_tests_api():
    test_result, coverage_result = run_tests()
    return {
        "test_result": test_result,
        "coverage_result": coverage_result
    }

@app.get("/health")
def health_check():
    return {"status": "ok"}

