# 🌍 Ceará Científico - Extrator de Notícias sobre Mudanças Climáticas

Este projeto extrai notícias relacionadas a mudanças climáticas e prepara dados estruturados para análise com LLMs e geração de gráficos.

## 🚀 Como Usar

### 1. Configuração do Ambiente

```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual (Windows)
venv\Scripts\Activate.ps1

# Instalar dependências
pip install -r requirements.txt
```

### 2. Execução

#### Script Principal (Recomendado)
```bash
python app.py
```

#### API REST
```bash
python main.py
# Acesse: http://localhost:8080/docs
```

## 📁 Estrutura do Projeto

```
ceara_cientifico/
├── app.py                      # Script principal
├── main.py                     # API FastAPI
├── requirements.txt            # Dependências
├── controller/
│   └── noticias.py            # Endpoints da API
├── entity/
│   └── extrator_noticias.py   # Extrator de notícias
└── use_case/
    ├── noticias.py            # Lógica de negócio
    └── summary.py             # Geração de resumos
```

## 🛠️ Funcionalidades

- 🔍 Extração de notícias sobre mudanças climáticas
- 📊 Dados estruturados para LLM
- 📄 Geração de resumos textuais
- 🌐 API REST com endpoints específicos
- 🎯 Filtragem por relevância climática

## 📊 Saída dos Dados

### Arquivos Gerados:
- `dados_para_llm.json` - Dados estruturados para LLM
- `resumo_noticias.md` - Resumo textual das notícias

### Formato JSON para LLM:
```json
{
  "fonte": "CNN BRASIL - MUDANÇAS CLIMÁTICAS",
  "total_noticias": 5,
  "noticias_para_llm": [
    {
      "titulo": "Título da notícia",
      "conteudo_completo": "Conteúdo completo...",
      "relevancia": 85,
      "palavras_chave_detectadas": ["clima", "carbono"],
      "url_original": "https://..."
    }
  ],
  "resumo_executivo": {
    "total_caracteres": 15000,
    "relevancia_media": 78.5,
    "termos_busca_utilizados": ["mudanças climáticas", "cop28"]
  }
}
```

## 🌐 Endpoints da API

- `GET /docs` - Documentação interativa
- `GET /headlines/mudancas_climaticas` - Dados para LLM
- `GET /headlines/mudancas_climaticas/resumo` - Resumo textual
- `POST /headlines/get_news_brasil` - Busca geral

## 🎯 Próximos Passos

1. Execute `python app.py` para extrair notícias
2. Use `dados_para_llm.json` com sua LLM favorita
3. Analise `resumo_noticias.md` para insights
4. Configure execução automática para monitoramento

## 📝 Dependências

- `fastapi` - Framework web
- `uvicorn` - Servidor ASGI
- `beautifulsoup4` - Parser HTML
- `requests` - Cliente HTTP
- `urllib3` - Utilitários HTTP

## 📄 Licença

Veja o arquivo `LICENSE` para detalhes.
Repositório destinado a projeto para participação do Ceará científico 
