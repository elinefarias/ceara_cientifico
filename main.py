from fastapi import FastAPI
from controller import noticias

app = FastAPI(
    title="Ceará Científico - API de Notícias Climáticas",
    version="1.0",
    description="API para extrair e analisar notícias sobre mudanças climáticas."
)

app.include_router(noticias.router)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
