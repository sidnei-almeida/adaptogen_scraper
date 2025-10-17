#!/usr/bin/env python3
"""
Adaptogen URL Collector
Coleta URLs de produtos das diferentes categorias do site Adaptogen.
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import logging
from typing import List, Dict

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Constantes
BASE_URL = "https://adaptogen.com.br"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
}
REQUEST_DELAY = 2  # segundos entre requisições


def get_page(url: str) -> BeautifulSoup:
    """
    Faz requisição HTTP e retorna o objeto BeautifulSoup.
    
    Args:
        url: URL da página a ser requisitada
        
    Returns:
        BeautifulSoup: Objeto soup da página
        
    Raises:
        requests.RequestException: Se houver erro na requisição
    """
    try:
        logger.info(f"Acessando: {url}")
        response = requests.get(url, headers=HEADERS, timeout=30)
        response.raise_for_status()
        time.sleep(REQUEST_DELAY)  # Delay para não sobrecarregar o servidor
        return BeautifulSoup(response.content, 'lxml')
    except requests.RequestException as e:
        logger.error(f"Erro ao acessar {url}: {e}")
        raise


def extract_product_urls(soup: BeautifulSoup, base_url: str = BASE_URL) -> List[str]:
    """
    Extrai URLs de produtos de uma página.
    
    Args:
        soup: Objeto BeautifulSoup da página
        base_url: URL base para completar URLs relativas
        
    Returns:
        List[str]: Lista de URLs de produtos
    """
    urls = []
    
    # Procura por links de produtos - geralmente em elementos com class product
    # Adaptando para a estrutura do site Adaptogen
    product_links = soup.find_all('a', class_='woocommerce-LoopProduct-link')
    
    if not product_links:
        # Tenta outras classes comuns
        product_links = soup.find_all('a', href=True)
        product_links = [link for link in product_links if '/produto/' in link.get('href', '')]
    
    for link in product_links:
        href = link.get('href')
        if href:
            # Garante URL absoluta
            if href.startswith('http'):
                urls.append(href)
            elif href.startswith('/'):
                urls.append(f"{base_url}{href}")
            else:
                urls.append(f"{base_url}/{href}")
    
    # Remove duplicatas mantendo a ordem
    seen = set()
    unique_urls = []
    for url in urls:
        if url not in seen:
            seen.add(url)
            unique_urls.append(url)
    
    return unique_urls


def scrape_pre_treino() -> List[str]:
    """
    Coleta URLs de produtos de pré-treino.
    
    Returns:
        List[str]: Lista de URLs de produtos
    """
    logger.info("Coletando URLs de Pré-treinos...")
    url = f"{BASE_URL}/pre-treino"
    
    try:
        soup = get_page(url)
        urls = extract_product_urls(soup)
        logger.info(f"Encontrados {len(urls)} produtos de pré-treino")
        return urls
    except Exception as e:
        logger.error(f"Erro ao coletar pré-treinos: {e}")
        return []


def scrape_snacks() -> List[str]:
    """
    Coleta URLs de produtos de snacks proteicos.
    
    Returns:
        List[str]: Lista de URLs de produtos
    """
    logger.info("Coletando URLs de Snacks...")
    url = f"{BASE_URL}/proteinas/snacks-proteicos/"
    
    try:
        soup = get_page(url)
        urls = extract_product_urls(soup)
        logger.info(f"Encontrados {len(urls)} produtos de snacks")
        return urls
    except Exception as e:
        logger.error(f"Erro ao coletar snacks: {e}")
        return []


def scrape_creatinas() -> List[str]:
    """
    Coleta URLs de produtos de creatina.
    
    Returns:
        List[str]: Lista de URLs de produtos
    """
    logger.info("Coletando URLs de Creatinas...")
    url = f"{BASE_URL}/creatina/"
    
    try:
        soup = get_page(url)
        urls = extract_product_urls(soup)
        logger.info(f"Encontrados {len(urls)} produtos de creatina")
        return urls
    except Exception as e:
        logger.error(f"Erro ao coletar creatinas: {e}")
        return []


def scrape_proteinas() -> List[str]:
    """
    Coleta URLs de produtos de proteínas com paginação.
    Continua até encontrar "Nenhum produto encontrado".
    
    Returns:
        List[str]: Lista de URLs de produtos
    """
    logger.info("Coletando URLs de Proteínas (com paginação)...")
    all_urls = []
    page = 1
    
    while True:
        url = f"{BASE_URL}/proteinas/?sf_paged={page}"
        
        try:
            soup = get_page(url)
            
            # Verifica se chegou ao fim (sem produtos)
            no_products = soup.find('h3', string='Nenhum produto encontrado')
            if no_products:
                logger.info(f"Fim da paginação na página {page}")
                break
            
            # Extrai URLs da página atual
            urls = extract_product_urls(soup)
            
            if not urls:
                # Se não encontrou produtos, pode ser fim da paginação
                logger.info(f"Nenhum produto encontrado na página {page}")
                break
            
            all_urls.extend(urls)
            logger.info(f"Página {page}: {len(urls)} produtos encontrados")
            page += 1
            
        except Exception as e:
            logger.error(f"Erro ao coletar proteínas página {page}: {e}")
            break
    
    # Remove duplicatas
    all_urls = list(set(all_urls))
    logger.info(f"Total de {len(all_urls)} produtos de proteína coletados")
    return all_urls


def save_to_json(data: Dict[str, List[str]], filepath: str) -> None:
    """
    Salva os dados coletados em arquivo JSON.
    
    Args:
        data: Dicionário com categorias e URLs
        filepath: Caminho do arquivo JSON
    """
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        logger.info(f"Dados salvos em {filepath}")
    except Exception as e:
        logger.error(f"Erro ao salvar JSON: {e}")
        raise


def main():
    """
    Função principal que orquestra a coleta de todas as categorias.
    """
    logger.info("Iniciando coleta de URLs de produtos Adaptogen...")
    
    # Coleta URLs de cada categoria
    produtos_urls = {
        "pre-treino": scrape_pre_treino(),
        "snacks": scrape_snacks(),
        "proteinas": scrape_proteinas(),
        "creatinas": scrape_creatinas()
    }
    
    # Estatísticas
    total_urls = sum(len(urls) for urls in produtos_urls.values())
    logger.info(f"\n{'='*50}")
    logger.info("RESUMO DA COLETA:")
    logger.info(f"{'='*50}")
    for categoria, urls in produtos_urls.items():
        logger.info(f"{categoria.capitalize()}: {len(urls)} produtos")
    logger.info(f"Total: {total_urls} produtos")
    logger.info(f"{'='*50}\n")
    
    # Salva em JSON
    output_path = "json/produtos_urls.json"
    save_to_json(produtos_urls, output_path)
    
    logger.info("Coleta finalizada com sucesso!")


if __name__ == "__main__":
    main()

