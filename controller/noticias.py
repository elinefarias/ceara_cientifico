from fastapi import APIRouter
from fastapi.responses import JSONResponse

# Ajusta o import para funcionar tanto quando executado diretamente quanto pelo app.py
import sys
import os
# Adiciona o diretório raiz do projeto ao path se não estiver lá
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from use_case.noticias import noticias, noticias_bbc

router = APIRouter(
    prefix="/api",
    tags=['Notícias']
)

@router.get('/noticias/clima')
async def extrair_noticias_climaticas():
    """
    Extrai notícias sobre mudanças climáticas e salva em JSON.
    Retorna os dados extraídos e informações sobre os arquivos salvos.
    """
    try:
        dados = noticias()
        return JSONResponse(
            content={
                "status": "success",
                "data": dados,
                "message": f"Extraídas {dados['total_noticias']} notícias e salvas em {len(dados['arquivos_salvos'])} arquivos"
            },
            status_code=200
        )
    except Exception as e:
        return JSONResponse(
            content={
                "status": "error",
                "message": str(e)
            },
            status_code=500
        )

@router.get('/noticias/bbc')
async def extrair_noticias_bbc():
    """
    Extrai notícias sobre mudanças climáticas da BBC Brasil e salva em JSON.
    Retorna os dados extraídos e informações sobre os arquivos salvos.
    """
    try:
        dados = noticias_bbc()
        return JSONResponse(
            content={
                "status": "success",
                "data": dados,
                "message": f"Extraídas {dados['total_noticias']} notícias da BBC e salvas em {len(dados['arquivos_salvos'])} arquivos"
            },
            status_code=200
        )
    except Exception as e:
        return JSONResponse(
            content={
                "status": "error",
                "message": str(e)
            },
            status_code=500
        )

