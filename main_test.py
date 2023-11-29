import uvicorn as uvicorn
from fastapi import FastAPI, APIRouter, Request

app = FastAPI()
router = APIRouter()

@router.post("/")
async def main():
    return {'status': 'success'}


app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)

