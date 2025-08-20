from fastapi import FastAPI
from controller.noticias import router as noticias_router

app = FastAPI(
    title="Ceará Científico API",
    description="API para extração de notícias sobre mudanças climáticas",
    version="1.0.0"
)

# Registra as rotas
app.include_router(noticias_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
