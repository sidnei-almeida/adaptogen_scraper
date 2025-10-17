# Adaptogen Scraper

O Adaptogen Scraper é um coletor de dados automatizado desenvolvido em Python para extrair, tratar e armazenar informações de diferentes fontes relacionadas a produtos e suplementos naturais.

## 🚀 Quick Start

```bash
# 1. Clone o repositório
git clone https://github.com/sidnei-almeida/adaptogen_scraper.git
cd adaptogen_scraper

# 2. Instale as dependências
pip install -r requirements.txt

# 3. Execute a interface CLI
python main.py
```

Pronto! Use a opção **3 (Executar Fluxo Completo)** para coletar e extrair todos os dados automaticamente.

## Instalação Detalhada

1. Clone o repositório:
```bash
git clone https://github.com/sidnei-almeida/adaptogen_scraper.git
cd adaptogen_scraper
```

2. Crie um ambiente virtual (recomendado):
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Uso

### Interface CLI Principal (Recomendado)

O projeto inclui uma interface CLI bonita e intuitiva para facilitar o uso:

```bash
python main.py
```

A interface oferece:
- 🔗 **Coletar URLs** - Coleta URLs de produtos de todas as categorias
- 📊 **Extrair Tabelas Nutricionais** - Extrai dados nutricionais de cada produto
- 🚀 **Executar Fluxo Completo** - Executa coleta + extração automaticamente
- 📋 **Ver Arquivos** - Lista JSONs e CSVs gerados com detalhes
- 🗑️ **Limpar Dados** - Remove arquivos antigos com segurança
- 📖 **Sobre o Programa** - Informações detalhadas do projeto

**Vantagens da Interface CLI:**
- ✨ Interface colorida e intuitiva
- 🎯 Menu fácil de navegar
- ⚡ Barras de progresso animadas
- 🛡️ Confirmações de segurança para operações críticas
- 📊 Estatísticas em tempo real
- ❌ Tratamento de erros amigável

### 1. URL Collector (Uso Individual)

O script `url_collector.py` coleta URLs de produtos das seguintes categorias:
- Pré-treinos
- Snacks proteicos
- Proteínas (com paginação automática)
- Creatinas

Para executar:
```bash
python url_collector.py
```

Os resultados serão salvos em `json/produtos_urls.json` com a seguinte estrutura:
```json
{
  "pre-treino": ["url1", "url2", ...],
  "snacks": ["url1", "url2", ...],
  "proteinas": ["url1", "url2", ...],
  "creatinas": ["url1", "url2", ...]
}
```

### 2. Nutritional Scraper

O script `nutritional_scraper.py` extrai tabelas nutricionais de cada produto coletado anteriormente e salva em CSV.

**Pré-requisito:** Execute primeiro o `url_collector.py` para gerar o arquivo `json/produtos_urls.json`.

Para executar:
```bash
python nutritional_scraper.py
```

O script irá:
- Carregar todas as URLs do JSON
- Acessar cada página de produto
- Extrair a tabela nutricional
- Salvar os dados em `dados_extraidos/produtos_nutricionais.csv`

**Estrutura do CSV gerado:**
- `nome`: Nome do produto
- `url`: URL do produto
- `porcao`: Porção (ex: "25 g (1 unidade)")
- `calorias`: Valor energético em kcal
- `carboidratos`: Carboidratos em g
- `proteinas`: Proteínas em g
- `gorduras`: Gorduras totais em g
- `gorduras_saturadas`: Gorduras saturadas em g
- `fibras`: Fibras alimentares em g
- `acucares`: Açúcares totais em g
- `sodio`: Sódio em mg
- `data_coleta`: Data e hora da coleta
- `categoria`: Categoria do produto

## Estrutura do Projeto

```
adaptogen_scraper/
├── main.py                   # 🎯 Interface CLI principal (use este!)
├── url_collector.py          # Script de coleta de URLs
├── nutritional_scraper.py    # Script de extração de dados nutricionais
├── template_main.py          # Template para criar CLIs bonitos
├── json/                     # Pasta para armazenar os JSONs
│   └── produtos_urls.json
├── dados_extraidos/          # Pasta para armazenar os CSVs
│   └── produtos_nutricionais.csv
├── requirements.txt          # Dependências do projeto
└── README.md                # Este arquivo
```

## Funcionalidades

### URL Collector
- ✅ Coleta automática de URLs de produtos
- ✅ Suporte a paginação automática (categoria Proteínas)
- ✅ Remoção automática de URLs duplicadas
- ✅ Saída em JSON estruturado por categoria

### Nutritional Scraper
- ✅ Extração de tabelas nutricionais de produtos
- ✅ Parsing inteligente de valores nutricionais
- ✅ Tratamento de valores ausentes (converte para 0)
- ✅ Exportação em formato CSV
- ✅ Registro de data/hora da coleta
- ✅ Associação de categoria a cada produto

### Geral
- ✅ Headers personalizados para simular navegador real
- ✅ Delay entre requisições para respeitar o servidor
- ✅ Logging detalhado do progresso
- ✅ Tratamento robusto de erros HTTP

## Requisitos

- Python 3.13+ (recomendado) ou 3.7+
- requests
- beautifulsoup4
- lxml

## Autor

**Sidnei Almeida**
- GitHub: [@sidnei-almeida](https://github.com/sidnei-almeida)

## Licença

Este projeto é de código aberto e está disponível para uso pessoal e educacional.
