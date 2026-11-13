from fastapi import FastAPI

app = FastAPI(title="IntelliCareer API")


@app.get("/health")
def health():
    return {"status": "ok"}
