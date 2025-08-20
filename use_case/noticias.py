from entity.extrator_noticias import NoticiasMudancasClimaticas, BBCMudancasClimaticas

def noticias():
    extrator = NoticiasMudancasClimaticas()
    dados = extrator.obter_dados_para_llm() 
    return dados

def noticias_bbc():
    extrator = BBCMudancasClimaticas()
    dados = extrator.obter_dados_para_llm()
    return dados