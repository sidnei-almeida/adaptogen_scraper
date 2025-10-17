#!/usr/bin/env python3
"""
Adaptogen Nutritional Scraper
Extrai tabelas nutricionais de produtos e salva em CSV.
"""

import requests
from bs4 import BeautifulSoup
import json
import csv
import time
import logging
from datetime import datetime
from typing import Dict, List, Optional
import re

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Constantes
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
}
REQUEST_DELAY = 2  # segundos entre requisições

# Colunas do CSV
CSV_COLUMNS = [
    'nome', 'url', 'porcao', 'calorias', 'carboidratos', 'proteinas',
    'gorduras', 'gorduras_saturadas', 'fibras', 'acucares', 'sodio',
    'data_coleta', 'categoria'
]


def load_product_urls(filepath: str = 'json/produtos_urls.json') -> Dict[str, List[str]]:
    """
    Carrega URLs de produtos do arquivo JSON.
    
    Args:
        filepath: Caminho do arquivo JSON
        
    Returns:
        Dict[str, List[str]]: Dicionário com categorias e URLs
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        logger.info(f"URLs carregadas de {filepath}")
        return data
    except Exception as e:
        logger.error(f"Erro ao carregar URLs: {e}")
        raise


def get_page(url: str) -> Optional[BeautifulSoup]:
    """
    Faz requisição HTTP e retorna o objeto BeautifulSoup.
    
    Args:
        url: URL da página a ser requisitada
        
    Returns:
        BeautifulSoup: Objeto soup da página ou None se houver erro
    """
    try:
        logger.info(f"Acessando: {url}")
        response = requests.get(url, headers=HEADERS, timeout=30)
        response.raise_for_status()
        time.sleep(REQUEST_DELAY)  # Delay para não sobrecarregar o servidor
        return BeautifulSoup(response.content, 'lxml')
    except requests.RequestException as e:
        logger.error(f"Erro ao acessar {url}: {e}")
        return None


def extract_product_name(soup: BeautifulSoup) -> str:
    """
    Extrai o nome do produto da página.
    
    Args:
        soup: Objeto BeautifulSoup da página
        
    Returns:
        str: Nome do produto
    """
    # Tenta diferentes seletores comuns para nome de produto
    selectors = [
        'h1.product_title',
        'h1.product-title',
        'h1',
        '.product-title',
        '.product_title'
    ]
    
    for selector in selectors:
        element = soup.select_one(selector)
        if element:
            return element.get_text(strip=True)
    
    return "Nome não encontrado"


def clean_numeric_value(value: str) -> float:
    """
    Limpa e converte valor numérico de string para float.
    
    Args:
        value: Valor em string
        
    Returns:
        float: Valor numérico ou 0 se inválido
    """
    if not value or value.strip() == '':
        return 0
    
    # Remove espaços e substitui vírgula por ponto
    cleaned = value.strip().replace(',', '.')
    
    # Extrai apenas números e ponto decimal
    match = re.search(r'[\d.]+', cleaned)
    if match:
        try:
            return float(match.group())
        except ValueError:
            return 0
    
    return 0


def extract_porcao(table) -> str:
    """
    Extrai porção de diferentes locais da tabela com suporte a múltiplos formatos.
    
    Args:
        table: Elemento BeautifulSoup da tabela
        
    Returns:
        str: Porção extraída ou string vazia se não encontrar
    """
    # Padrões regex para diferentes formatos de porção
    patterns = [
        r'Porção:\s*(.+?)(?:\n|<|$)',           # "Porção: 25 g (1 unidade)"
        r'Porção de\s+(.+?)(?:\n|<|$)',         # "Porção de 2 dosadores – 10g"
        r'Porção\s+de\s+(.+?)(?:\n|<|$)',       # "Porção de 10g"
        r'Porção\s+(.+?)(?:\n|<|$)',            # "Porção 10g"
    ]
    
    # 1. Busca no thead
    thead = table.find('thead')
    if thead:
        text = thead.get_text()
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                porcao = match.group(1).strip()
                # Remove quebras de linha extras e limpa o texto
                porcao = ' '.join(porcao.split())
                return porcao
    
    # 2. Busca na primeira linha do tbody (caso especial como Panic Pré-Treino)
    tbody = table.find('tbody')
    if tbody:
        first_row = tbody.find('tr')
        if first_row:
            cells = first_row.find_all(['td', 'th'])
            for cell in cells:
                text = cell.get_text()
                if 'porção' in text.lower():
                    # Tenta os padrões regex
                    for pattern in patterns:
                        match = re.search(pattern, text, re.IGNORECASE)
                        if match:
                            porcao = match.group(1).strip()
                            porcao = ' '.join(porcao.split())
                            return porcao
                    
                    # Se encontrou "porção" mas não matchou padrão específico,
                    # tenta extrair a parte relevante
                    if 'de' in text.lower():
                        # Ex: "Porção de 2 dosadores – 10g"
                        parts = text.split('de', 1)
                        if len(parts) > 1:
                            porcao = parts[1].strip()
                            porcao = ' '.join(porcao.split())
                            return porcao
                    
                    # Última tentativa: retorna o texto limpo removendo "Porção"
                    porcao = text.replace('Porção', '').replace('porção', '').strip()
                    porcao = ' '.join(porcao.split())
                    if porcao:
                        return porcao
    
    return ''


def parse_nutritional_table(soup: BeautifulSoup) -> Optional[Dict]:
    """
    Extrai e processa a tabela nutricional.
    
    Args:
        soup: Objeto BeautifulSoup da página
        
    Returns:
        Dict: Dicionário com dados nutricionais ou None se não encontrar
    """
    # Localiza a div com a tabela
    flow_div = soup.find('div', class_='flow')
    if not flow_div:
        logger.warning("Div 'flow' não encontrada")
        return None
    
    table = flow_div.find('table')
    if not table:
        logger.warning("Tabela não encontrada dentro da div 'flow'")
        return None
    
    # Inicializa dados com valores padrão
    data = {
        'porcao': '',
        'calorias': 0,
        'carboidratos': 0,
        'proteinas': 0,
        'gorduras': 0,
        'gorduras_saturadas': 0,
        'fibras': 0,
        'acucares': 0,
        'sodio': 0
    }
    
    # Extrai porção usando a nova função robusta
    data['porcao'] = extract_porcao(table)
    
    # Mapeia nomes de nutrientes para chaves do dicionário
    nutrient_mapping = {
        'valor energético': 'calorias',
        'carboidratos': 'carboidratos',
        'proteínas': 'proteinas',
        'gorduras totais': 'gorduras',
        'gorduras saturadas': 'gorduras_saturadas',
        'fibras alimentares': 'fibras',
        'açúcares totais': 'acucares',
        'sódio': 'sodio'
    }
    
    # Extrai valores do tbody
    tbody = table.find('tbody')
    if tbody:
        rows = tbody.find_all('tr')
        for row in rows:
            cells = row.find_all('td')
            if len(cells) >= 2:
                nutrient_name = cells[0].get_text(strip=True).lower()
                nutrient_value = cells[1].get_text(strip=True)
                
                # Verifica se o nutriente está no mapeamento
                for key, mapped_key in nutrient_mapping.items():
                    if key in nutrient_name:
                        data[mapped_key] = clean_numeric_value(nutrient_value)
                        break
    
    return data


def scrape_product(url: str, categoria: str) -> Optional[Dict]:
    """
    Faz scraping de um produto individual.
    
    Args:
        url: URL do produto
        categoria: Categoria do produto
        
    Returns:
        Dict: Dados do produto ou None se houver erro
    """
    try:
        soup = get_page(url)
        if not soup:
            return None
        
        # Extrai nome do produto
        nome = extract_product_name(soup)
        
        # Extrai tabela nutricional
        nutritional_data = parse_nutritional_table(soup)
        if not nutritional_data:
            logger.warning(f"Tabela nutricional não encontrada para: {nome} ({url})")
            return None
        
        # Monta dados completos do produto
        product_data = {
            'nome': nome,
            'url': url,
            'porcao': nutritional_data['porcao'],
            'calorias': nutritional_data['calorias'],
            'carboidratos': nutritional_data['carboidratos'],
            'proteinas': nutritional_data['proteinas'],
            'gorduras': nutritional_data['gorduras'],
            'gorduras_saturadas': nutritional_data['gorduras_saturadas'],
            'fibras': nutritional_data['fibras'],
            'acucares': nutritional_data['acucares'],
            'sodio': nutritional_data['sodio'],
            'data_coleta': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'categoria': categoria
        }
        
        logger.info(f"✓ Produto coletado: {nome}")
        return product_data
        
    except Exception as e:
        logger.error(f"Erro ao processar produto {url}: {e}")
        return None


def save_to_csv(data: List[Dict], filepath: str) -> None:
    """
    Salva dados em arquivo CSV.
    
    Args:
        data: Lista de dicionários com dados dos produtos
        filepath: Caminho do arquivo CSV
    """
    try:
        with open(filepath, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS)
            writer.writeheader()
            writer.writerows(data)
        logger.info(f"Dados salvos em {filepath}")
    except Exception as e:
        logger.error(f"Erro ao salvar CSV: {e}")
        raise


def main():
    """
    Função principal que orquestra a coleta de dados nutricionais.
    """
    logger.info("Iniciando coleta de dados nutricionais...")
    
    # Carrega URLs dos produtos
    try:
        produtos_urls = load_product_urls()
    except Exception as e:
        logger.error(f"Não foi possível carregar URLs. Execute url_collector.py primeiro.")
        return
    
    # Lista para armazenar todos os produtos
    all_products = []
    
    # Estatísticas
    total_urls = sum(len(urls) for urls in produtos_urls.values())
    processed = 0
    success = 0
    failed = 0
    
    logger.info(f"\n{'='*60}")
    logger.info(f"Total de produtos a processar: {total_urls}")
    logger.info(f"{'='*60}\n")
    
    # Processa cada categoria
    for categoria, urls in produtos_urls.items():
        logger.info(f"\n{'='*60}")
        logger.info(f"Processando categoria: {categoria.upper()}")
        logger.info(f"Total de URLs: {len(urls)}")
        logger.info(f"{'='*60}\n")
        
        for url in urls:
            processed += 1
            logger.info(f"[{processed}/{total_urls}] Processando...")
            
            product_data = scrape_product(url, categoria)
            
            if product_data:
                all_products.append(product_data)
                success += 1
            else:
                failed += 1
    
    # Salva resultados em CSV
    if all_products:
        output_path = "dados_extraidos/produtos_nutricionais.csv"
        save_to_csv(all_products, output_path)
    
    # Estatísticas finais
    logger.info(f"\n{'='*60}")
    logger.info("RESUMO DA COLETA:")
    logger.info(f"{'='*60}")
    logger.info(f"Total processado: {processed}")
    logger.info(f"Sucesso: {success}")
    logger.info(f"Falhas: {failed}")
    logger.info(f"Taxa de sucesso: {(success/processed*100):.1f}%")
    logger.info(f"{'='*60}\n")
    
    logger.info("Coleta finalizada!")


if __name__ == "__main__":
    main()

