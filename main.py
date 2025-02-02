import json
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routes import items

# Cargar la metadata de los tags desde el archivo JSON
with open("tags_metadata.json") as f:
    tags_metadata = json.load(f)

app = FastAPI(
    title="Tuna Awainan API",
    description="Prueba de API con FastAPI",
    version="0.0.1",
    openapi_tags=tags_metadata
)

app.mount("/test", StaticFiles(directory="test"), name="test")

# Incluir las rutas definidas en items.py
app.include_router(items.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)