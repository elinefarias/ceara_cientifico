import os
import re
import json
import time
import hashlib
from datetime import datetime

import requests
from bs4 import BeautifulSoup


class BBCMudancasClimaticas:
    """Extrator focado nas notícias de clima da BBC Brasil."""
    
    BBC_URL = 'https://www.bbc.com/portuguese/topics/cr50y580rjxt'
    BBC_RSS_URL = 'https://feeds.bbci.co.uk/portuguese/rss.xml'  # Feed RSS geral da BBC Brasil
    
    def __init__(self):
        self.name = 'EXTRATOR MUDANÇAS CLIMÁTICAS - BBC BRASIL'
        self.noticias = []
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        
    def _safe_filename(self, text: str) -> str:
        base = re.sub(r'[^0-9a-zA-Z\-_]', '_', text)[:80]
        h = hashlib.sha1(text.encode('utf-8')).hexdigest()[:10]
        return f"bbc_{base}_{h}.json"
        
    def _extrair_conteudo_simples(self, url: str) -> str:
        try:
            print(f"[DEBUG BBC] Extraindo conteúdo de: {url}")
            resp = requests.get(url, headers=self.headers, timeout=15)
            if resp.status_code != 200:
                print(f"[DEBUG BBC] Erro na requisição: {resp.status_code}")
                return ''
                
            print(f"[DEBUG BBC] Tamanho do conteúdo: {len(resp.text)} bytes")
            soup = BeautifulSoup(resp.text, 'html.parser')
            
            # Tenta diferentes estratégias para encontrar o conteúdo principal
            
            # 1. Estratégia: Procura o corpo do artigo
            article_body = soup.find(['article', 'main'])
            
            # 2. Estratégia: Procura div com classe que indique conteúdo
            if not article_body:
                article_body = soup.find('div', class_=lambda c: c and ('story-body' in c or 'article' in c or 'content' in c))
            
            # 3. Estratégia: Usa toda a página
            if not article_body:
                article_body = soup.body
                
            if not article_body:
                print("[DEBUG BBC] Não encontrou corpo do artigo")
                return ''
                
            # Extrai os parágrafos do artigo, priorizando tags de conteúdo
            paragrafos = []
            
            # Primeiro tenta encontrar elementos específicos de conteúdo
            for p in article_body.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'figcaption', 'blockquote']):
                if p.text.strip():
                    # Ignora elementos de navegação, copyright, etc
                    text = p.text.strip()
                    if len(text) > 10 and not ('cookies' in text.lower() or 'direitos' in text.lower() 
                                             or 'copyright' in text.lower() or 'navegação' in text.lower()):
                        paragrafos.append(text)
            
            # Se não encontrou nada, pega qualquer texto
            if not paragrafos:
                print("[DEBUG BBC] Tentando estratégia alternativa para extrair texto")
                for elem in article_body.find_all(text=True):
                    text = elem.strip()
                    if len(text) > 20:  # Apenas textos significativos
                        paragrafos.append(text)
                    
            conteudo = ' '.join(paragrafos)
            conteudo = re.sub(r'\s+', ' ', conteudo).strip()
            
            print(f"[DEBUG BBC] Caracteres extraídos: {len(conteudo)}")
            if len(conteudo) < 100:
                print("[DEBUG BBC] Conteúdo muito curto, pode indicar falha na extração")
                
            return conteudo
        except Exception as e:
            print(f"[DEBUG BBC] Erro ao extrair conteúdo: {str(e)}")
            return ''
            
    def _buscar_via_rss(self, max_items: int = 10) -> list:
        """Busca notícias via RSS feed da BBC."""
        try:
            print(f"[DEBUG BBC] Tentando via RSS: {self.BBC_RSS_URL}")
            resp = requests.get(self.BBC_RSS_URL, headers=self.headers, timeout=10)
            
            if resp.status_code != 200:
                print(f"[DEBUG BBC] Falha na requisição RSS: {resp.status_code}")
                return []
            
            soup = BeautifulSoup(resp.text, 'xml')
            items = soup.find_all('item')[:max_items]
            
            print(f"[DEBUG BBC] Encontrados {len(items)} items no RSS")
            
            noticias = []
            for item in items:
                title = item.find('title').get_text().strip() if item.find('title') else ''
                link = item.find('link').get_text().strip() if item.find('link') else ''
                pub_date = item.find('pubDate').get_text().strip() if item.find('pubDate') else ''
                
                # Filtra apenas notícias relacionadas a clima/meio ambiente
                if not any(termo in title.lower() for termo in ['clima', 'ambiente', 'carbon', 'emiss', 'poluição', 
                                                               'temperatura', 'global', 'cop', 'desmatamento']):
                    continue
                
                conteudo = self._extrair_conteudo_simples(link) if link else ''
                
                noticia = {
                    'titulo': title,
                    'link': link,
                    'conteudo': conteudo,
                    'data_publicacao': pub_date,
                    'data_extracao': datetime.now().isoformat(),
                    'caracteres_conteudo': len(conteudo),
                    'fonte': 'BBC Brasil (RSS)'
                }
                
                noticias.append(noticia)
                time.sleep(0.5)
            
            return noticias
        except Exception as e:
            print(f"[DEBUG BBC] Erro ao buscar via RSS: {str(e)}")
            return []

    def buscar_noticias(self, max_items: int = 10) -> list:
        """Busca as notícias sobre clima da BBC Brasil e popula self.noticias."""
        try:
            resp = requests.get(self.BBC_URL, headers=self.headers, timeout=10)
            if resp.status_code != 200:
                print(f"[DEBUG BBC] Falha na requisição web: {resp.status_code}")
                # Se a página principal falhar, tenta o RSS
                return self._buscar_via_rss(max_items)
                
            soup = BeautifulSoup(resp.text, 'html.parser')
            
            # Vamos imprimir algumas informações para debug
            print(f"[DEBUG BBC] URL: {self.BBC_URL}")
            print(f"[DEBUG BBC] Status code: {resp.status_code}")
            print(f"[DEBUG BBC] Tamanho do HTML: {len(resp.text)} bytes")
            
            # Vamos tentar diferentes seletores para encontrar as notícias
            # 1. Tentativa: artigos ou promos
            noticias_items = soup.find_all(['article', 'div'], class_=['media', 'gs-o-media', 'gs-c-promo'])
            
            # 2. Tentativa: links dentro da main area
            if not noticias_items:
                main_content = soup.find('main')
                if main_content:
                    noticias_items = main_content.find_all('a', href=True)
            
            # 3. Tentativa: qualquer div que pareça uma notícia
            if not noticias_items:
                noticias_items = soup.find_all('div', class_=lambda c: c and ('promo' in c.lower() or 'headline' in c.lower()))
                
            print(f"[DEBUG BBC] Encontrados {len(noticias_items)} possíveis items")
            
            items = noticias_items[:max_items]
            
            noticias = []
            for item in items:
                # Extrai título e link com estratégias diferentes dependendo do elemento
                title = ""
                link = ""
                
                # Se o item for um link (a)
                if item.name == 'a':
                    link_href = item.get('href', '')
                    title = item.get_text().strip()
                    
                    # Pega o texto do título se tiver algum heading
                    heading = item.find(['h1', 'h2', 'h3', 'h4'])
                    if heading:
                        title = heading.get_text().strip()
                    
                # Se for artigo ou div
                else:
                    # Procura título em qualquer heading
                    titulo_element = item.find(['h1', 'h2', 'h3', 'h4'])
                    if titulo_element:
                        title = titulo_element.get_text().strip()
                    
                    # Procura link
                    link_element = item.find('a')
                    if link_element:
                        link_href = link_element.get('href', '')
                    else:
                        link_href = ""
                
                # Se não encontrou título ou link, pula
                if not title or not link_href:
                    continue
                    
                # Limpa o título de espaços extras
                title = re.sub(r'\s+', ' ', title).strip()
                
                # A BBC usa links relativos, então precisamos completar a URL
                if link_href.startswith('/'):
                    link = f"https://www.bbc.com{link_href}"
                else:
                    link = link_href
                
                print(f"[DEBUG BBC] Encontrado: {title[:50]}... | {link}")
                    
                # Tenta extrair a data, mas é complexo na BBC
                date_element = item.find('time', {'data-testid': 'timestamp'})
                pub_date = date_element.get('datetime') if date_element else datetime.now().isoformat()
                
                # Extrai conteúdo
                conteudo = self._extrair_conteudo_simples(link)
                
                noticia = {
                    'titulo': title,
                    'link': link,
                    'conteudo': conteudo,
                    'data_publicacao': pub_date,
                    'data_extracao': datetime.now().isoformat(),
                    'caracteres_conteudo': len(conteudo),
                    'fonte': 'BBC Brasil'
                }
                
                noticias.append(noticia)
                time.sleep(0.5)  # Pausa entre requisições para não sobrecarregar o servidor
                
            self.noticias = noticias
            
            # Se não encontrou notícias na página web, tenta o feed RSS
            if not noticias:
                print("[DEBUG BBC] Não encontrou notícias na página principal, tentando RSS")
                noticias = self._buscar_via_rss(max_items)
                self.noticias = noticias
                
            return noticias
        except Exception as e:
            print(f"[DEBUG BBC] Erro ao buscar notícias: {str(e)}")
            # Em caso de erro, tenta o RSS como fallback
            noticias = self._buscar_via_rss(max_items)
            self.noticias = noticias
            return noticias
            
    def _pasta_dados(self) -> str:
        raiz = os.path.dirname(os.path.dirname(__file__))
        pasta = os.path.join(raiz, 'dados-noticias')
        os.makedirs(pasta, exist_ok=True)
        return pasta
        
    def salvar_em_json(self) -> list:
        pasta = self._pasta_dados()
        salvados = []
        for n in self.noticias:
            nome = self._safe_filename(n.get('titulo') or n.get('link') or datetime.now().isoformat())
            caminho = os.path.join(pasta, nome)
            try:
                with open(caminho, 'w', encoding='utf-8') as f:
                    json.dump(n, f, ensure_ascii=False, indent=2)
                salvados.append(caminho)
            except Exception:
                continue
        return salvados
        
    def obter_dados_para_llm(self) -> dict:
        if not self.noticias:
            self.buscar_noticias()
            
        if not self.noticias:
            return {
                'fonte': self.name,
                'total_noticias': 0,
                'data_extracao': datetime.now().isoformat(),
                'noticias_para_llm': [],
                'arquivos_salvos': []
            }
            
        arquivos = self.salvar_em_json()
        
        return {
            'fonte': self.name,
            'total_noticias': len(self.noticias),
            'data_extracao': datetime.now().isoformat(),
            'noticias_para_llm': self.noticias,
            'arquivos_salvos': arquivos
        }


class NoticiasMudancasClimaticas:
    """Extrator focado no feed RSS do G1 - Meio Ambiente."""

    RSS_URL = 'https://g1.globo.com/rss/g1/meio-ambiente/'

    def __init__(self):
        self.name = 'EXTRATOR MUDANÇAS CLIMÁTICAS - G1 RSS'
        self.noticias = []
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }

    def _safe_filename(self, text: str) -> str:
        base = re.sub(r'[^0-9a-zA-Z\-_]', '_', text)[:80]
        h = hashlib.sha1(text.encode('utf-8')).hexdigest()[:10]
        return f"{base}_{h}.json"

    def _extrair_conteudo_simples(self, url: str) -> str:
        try:
            resp = requests.get(url, headers=self.headers, timeout=10)
            if resp.status_code != 200:
                return ''
            soup = BeautifulSoup(resp.text, 'html.parser')
            paragrafos = [p.get_text().strip() for p in soup.find_all('p') if p.get_text().strip()]
            conteudo = ' '.join(paragrafos)
            conteudo = re.sub(r'\s+', ' ', conteudo).strip()
            return conteudo  # Removendo o limite de 3000 caracteres para pegar todo o conteúdo
        except Exception:
            return ''

    def buscar_noticias(self, max_items: int = 10) -> list:
        """Busca o RSS do G1 Meio Ambiente e popula self.noticias."""
        try:
            resp = requests.get(self.RSS_URL, headers=self.headers, timeout=10)
            if resp.status_code != 200:
                return []

            soup = BeautifulSoup(resp.text, 'xml')
            items = soup.find_all('item')[:max_items]

            noticias = []
            for item in items:
                title = item.find('title').get_text().strip() if item.find('title') else ''
                
                # Obtém o link diretamente do GUID, que normalmente tem a URL completa
                link = ''
                guid = item.find('guid')
                if guid:
                    link = guid.get_text().strip()
                
                # Se não conseguiu pelo GUID, tenta pelo elemento link
                if not link:
                    link_element = item.find('link')
                    if link_element:
                        link = link_element.get_text().strip()
                
                pub_date = item.find('pubDate').get_text().strip() if item.find('pubDate') else ''

                # Obtém conteúdo da página
                conteudo = self._extrair_conteudo_simples(link) if link else ''
                
                noticia = {
                    'titulo': title,
                    'link': link,
                    'conteudo': conteudo,
                    'data_publicacao': pub_date,
                    'data_extracao': datetime.now().isoformat(),
                    'caracteres_conteudo': len(conteudo)
                }
                noticias.append(noticia)
                time.sleep(0.3)

            self.noticias = noticias
            return noticias
        except Exception:
            return []

    def _pasta_dados(self) -> str:
        raiz = os.path.dirname(os.path.dirname(__file__))
        pasta = os.path.join(raiz, 'dados-noticias')
        os.makedirs(pasta, exist_ok=True)
        return pasta

    def salvar_em_json(self) -> list:
        pasta = self._pasta_dados()
        salvados = []
        for n in self.noticias:
            nome = self._safe_filename(n.get('titulo') or n.get('link') or datetime.now().isoformat())
            caminho = os.path.join(pasta, nome)
            try:
                with open(caminho, 'w', encoding='utf-8') as f:
                    json.dump(n, f, ensure_ascii=False, indent=2)
                salvados.append(caminho)
            except Exception:
                continue
        return salvados

    def obter_dados_para_llm(self) -> dict:
        if not self.noticias:
            self.buscar_noticias()

        if not self.noticias:
            return {
                'fonte': self.name,
                'total_noticias': 0,
                'data_extracao': datetime.now().isoformat(),
                'noticias_para_llm': [],
                'arquivos_salvos': []
            }

        arquivos = self.salvar_em_json()

        return {
            'fonte': self.name,
            'total_noticias': len(self.noticias),
            'data_extracao': datetime.now().isoformat(),
            'noticias_para_llm': self.noticias,
            'arquivos_salvos': arquivos
        }

