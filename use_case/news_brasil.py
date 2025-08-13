from entity.headlines.uol import Uol
from entity.headlines.r7 import R7
from entity.headlines.valor import Valor
from entity.headlines.infomoney import Infomoney
from entity.headlines.folha_de_sp import FolhaDeSp
from entity.headlines.jovem_pan import JovemPan
from entity.headlines.diario_do_nordeste import DiarioDoNordeste
from entity.headlines.cnn_brasil import CnnBrasil


def news_brasil():
    uol = Uol()
    print(uol.summary)
    #r7 = R7()
    #print(r7.summary)
    valor = Valor()
    print(valor.summary)
    #infomoney = Infomoney()
    #print(infomoney.summary)
    folha_de_sp = FolhaDeSp()
    print(folha_de_sp.summary)
    jovem_pan = JovemPan()
    print(jovem_pan.summary)
    diario_do_nordeste = DiarioDoNordeste()
    print(diario_do_nordeste.summary)
    cnn_brasil = CnnBrasil()
    print(cnn_brasil.summary)
  

    summary = [
        uol.summary,
        #r7.summary,
        valor.summary,
        #infomoney.summary,
        folha_de_sp.summary,
        jovem_pan.summary,
        diario_do_nordeste.summary,
        cnn_brasil.summary
    ]

    summary = ' '.join(summary)

    #speach = Speach(summary)
    #speach.text_to_speach()

    return summary