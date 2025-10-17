#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🧪 ADAPTOGEN SCRAPER - Interface CLI
====================================
Interface profissional para coleta e extração de dados nutricionais da Adaptogen

Desenvolvido por: Sidnei Almeida (github.com/sidnei-almeida)
"""

import os
import sys
import time
import glob
from datetime import datetime
from typing import List, Dict, Optional

# ============================================================================
# 🎨 SISTEMA DE CORES ANSI PARA TERMINAL
# ============================================================================
class Cores:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    VERDE = '\033[92m'
    AZUL = '\033[94m'
    AMARELO = '\033[93m'
    VERMELHO = '\033[91m'
    CIANO = '\033[96m'
    MAGENTA = '\033[95m'
    BRANCO = '\033[97m'

# ============================================================================
# 🛠️ FUNÇÕES UTILITÁRIAS
# ============================================================================
def limpar_terminal():
    """Limpa o terminal"""
    os.system('clear' if os.name == 'posix' else 'cls')

def mostrar_banner():
    """Exibe o banner principal do programa"""
    banner = f"""
{Cores.CIANO}{Cores.BOLD}
╔══════════════════════════════════════════════════════════════╗
║              🧪 ADAPTOGEN SCRAPER - v1.0                     ║
║                                                              ║
║        Extrator de Dados Nutricionais da Adaptogen          ║
║                                                              ║
║  📊 Coleta de URLs de Produtos                               ║
║  🎯 Extração de Tabelas Nutricionais                         ║
║  📝 Exportação para JSON e CSV                               ║
╚══════════════════════════════════════════════════════════════╝
{Cores.RESET}"""
    print(banner)

def mostrar_barra_progresso(texto: str, duracao: float = 2.0):
    """Exibe uma barra de progresso animada"""
    print(f"\n{Cores.AMARELO}⏳ {texto}...{Cores.RESET}")
    barra_tamanho = 40
    for i in range(barra_tamanho + 1):
        progresso = i / barra_tamanho
        barra = "█" * i + "░" * (barra_tamanho - i)
        porcentagem = int(progresso * 100)
        print(f"\r{Cores.VERDE}[{barra}] {porcentagem}%{Cores.RESET}", end="", flush=True)
        time.sleep(duracao / barra_tamanho)
    print()

def mostrar_menu():
    """Exibe o menu principal"""
    menu = f"""
{Cores.AZUL}{Cores.BOLD}═══════════════════ MENU PRINCIPAL ═══════════════════{Cores.RESET}

{Cores.VERDE}🚀 OPERAÇÕES PRINCIPAIS:{Cores.RESET}
  {Cores.AMARELO}1.{Cores.RESET} 🔗 {Cores.BRANCO}Coletar URLs{Cores.RESET} - Coleta URLs de produtos
  {Cores.AMARELO}2.{Cores.RESET} 📊 {Cores.BRANCO}Extrair Tabelas Nutricionais{Cores.RESET} - Extrai dados nutricionais
  {Cores.AMARELO}3.{Cores.RESET} 🚀 {Cores.BRANCO}Executar Fluxo Completo{Cores.RESET} - Coleta + Extração

{Cores.VERDE}📁 GERENCIAR DADOS:{Cores.RESET}
  {Cores.AMARELO}4.{Cores.RESET} 📋 {Cores.BRANCO}Ver Arquivos{Cores.RESET} - Lista arquivos gerados
  {Cores.AMARELO}5.{Cores.RESET} 🗑️  {Cores.BRANCO}Limpar Dados{Cores.RESET} - Remove arquivos antigos

{Cores.VERDE}ℹ️  INFORMAÇÕES:{Cores.RESET}
  {Cores.AMARELO}6.{Cores.RESET} 📖 {Cores.BRANCO}Sobre o Programa{Cores.RESET} - Informações e estatísticas
  {Cores.AMARELO}7.{Cores.RESET} ❌ {Cores.BRANCO}Sair{Cores.RESET} - Encerrar programa

{Cores.AZUL}══════════════════════════════════════════════════════{Cores.RESET}
"""
    print(menu)

def obter_escolha() -> str:
    """Obtém a escolha do usuário"""
    try:
        escolha = input(f"{Cores.MAGENTA}👉 Digite sua opção (1-7): {Cores.RESET}").strip()
        return escolha
    except KeyboardInterrupt:
        print(f"\n\n{Cores.AMARELO}⚠️  Programa interrompido pelo usuário{Cores.RESET}")
        sys.exit(0)

# ============================================================================
# 🎯 FUNÇÕES ESPECÍFICAS DO ADAPTOGEN SCRAPER
# ============================================================================

def coletar_urls():
    """Executa a coleta de URLs de produtos"""
    print(f"\n{Cores.CIANO}{Cores.BOLD}🔗 COLETAR URLs DE PRODUTOS{Cores.RESET}")
    print(f"{Cores.AZUL}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Cores.RESET}")
    
    print(f"\n{Cores.VERDE}✅ Categorias a serem coletadas:{Cores.RESET}")
    print(f"   📊 Pré-treinos: {Cores.AMARELO}https://adaptogen.com.br/pre-treino{Cores.RESET}")
    print(f"   🍫 Snacks: {Cores.AMARELO}https://adaptogen.com.br/proteinas/snacks-proteicos/{Cores.RESET}")
    print(f"   💪 Proteínas: {Cores.AMARELO}https://adaptogen.com.br/proteinas/ (com paginação){Cores.RESET}")
    print(f"   ⚡ Creatinas: {Cores.AMARELO}https://adaptogen.com.br/creatina/{Cores.RESET}")
    
    print(f"\n{Cores.VERDE}📁 Saída:{Cores.RESET} {Cores.AMARELO}json/produtos_urls.json{Cores.RESET}")
    
    confirmar = input(f"\n{Cores.MAGENTA}🤔 Continuar com a coleta? (s/N): {Cores.RESET}").lower()
    
    if confirmar in ['s', 'sim', 'y', 'yes']:
        try:
            mostrar_barra_progresso("Iniciando coleta de URLs", 1.5)
            
            # Importa e executa o url_collector
            print(f"\n{Cores.VERDE}🚀 Executando coleta...{Cores.RESET}\n")
            print(f"{Cores.AZUL}{'='*60}{Cores.RESET}")
            
            import url_collector
            url_collector.main()
            
            print(f"{Cores.AZUL}{'='*60}{Cores.RESET}")
            print(f"\n{Cores.VERDE}✅ Coleta de URLs concluída com sucesso!{Cores.RESET}")
            
        except Exception as e:
            print(f"\n{Cores.VERMELHO}❌ Erro durante coleta: {e}{Cores.RESET}")
    else:
        print(f"{Cores.AMARELO}⏭️  Operação cancelada{Cores.RESET}")

def extrair_dados_nutricionais():
    """Executa a extração de dados nutricionais"""
    print(f"\n{Cores.CIANO}{Cores.BOLD}📊 EXTRAIR TABELAS NUTRICIONAIS{Cores.RESET}")
    print(f"{Cores.AZUL}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Cores.RESET}")
    
    # Verifica se o arquivo de URLs existe
    if not os.path.exists('json/produtos_urls.json'):
        print(f"\n{Cores.VERMELHO}❌ ERRO: Arquivo json/produtos_urls.json não encontrado!{Cores.RESET}")
        print(f"{Cores.AMARELO}💡 Execute primeiro a opção 1 (Coletar URLs){Cores.RESET}")
        return
    
    print(f"\n{Cores.AMARELO}⚠️  ATENÇÃO:{Cores.RESET}")
    print(f"   • Esta operação pode demorar {Cores.VERMELHO}vários minutos{Cores.RESET}")
    print(f"   • Cada produto será acessado individualmente")
    print(f"   • Um delay de 2 segundos é aplicado entre requisições")
    
    print(f"\n{Cores.VERDE}📁 Entrada:{Cores.RESET} {Cores.AMARELO}json/produtos_urls.json{Cores.RESET}")
    print(f"{Cores.VERDE}📁 Saída:{Cores.RESET} {Cores.AMARELO}dados_extraidos/produtos_nutricionais.csv{Cores.RESET}")
    
    confirmar = input(f"\n{Cores.MAGENTA}🤔 Continuar com a extração? (s/N): {Cores.RESET}").lower()
    
    if confirmar in ['s', 'sim', 'y', 'yes']:
        try:
            mostrar_barra_progresso("Preparando extração de dados", 1.5)
            
            # Importa e executa o nutritional_scraper
            print(f"\n{Cores.VERDE}🚀 Executando extração...{Cores.RESET}\n")
            print(f"{Cores.AZUL}{'='*60}{Cores.RESET}")
            
            import nutritional_scraper
            nutritional_scraper.main()
            
            print(f"{Cores.AZUL}{'='*60}{Cores.RESET}")
            print(f"\n{Cores.VERDE}✅ Extração de dados concluída!{Cores.RESET}")
            
        except Exception as e:
            print(f"\n{Cores.VERMELHO}❌ Erro durante extração: {e}{Cores.RESET}")
    else:
        print(f"{Cores.AMARELO}⏭️  Operação cancelada{Cores.RESET}")

def executar_fluxo_completo():
    """Executa o fluxo completo: coleta + extração"""
    print(f"\n{Cores.CIANO}{Cores.BOLD}🚀 EXECUTAR FLUXO COMPLETO{Cores.RESET}")
    print(f"{Cores.AZUL}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Cores.RESET}")
    
    print(f"\n{Cores.VERDE}📋 Etapas do fluxo:{Cores.RESET}")
    print(f"   1️⃣  Coletar URLs de produtos")
    print(f"   2️⃣  Extrair tabelas nutricionais")
    
    print(f"\n{Cores.AMARELO}⚠️  Este processo pode demorar bastante tempo!{Cores.RESET}")
    
    confirmar = input(f"\n{Cores.MAGENTA}🤔 Executar fluxo completo? (s/N): {Cores.RESET}").lower()
    
    if confirmar in ['s', 'sim', 'y', 'yes']:
        try:
            inicio = time.time()
            
            # Etapa 1: Coletar URLs
            print(f"\n{Cores.CIANO}{'='*60}{Cores.RESET}")
            print(f"{Cores.BOLD}ETAPA 1/2: COLETA DE URLs{Cores.RESET}")
            print(f"{Cores.CIANO}{'='*60}{Cores.RESET}\n")
            
            import url_collector
            url_collector.main()
            
            print(f"\n{Cores.VERDE}✅ Etapa 1 concluída!{Cores.RESET}")
            time.sleep(2)
            
            # Etapa 2: Extrair dados
            print(f"\n{Cores.CIANO}{'='*60}{Cores.RESET}")
            print(f"{Cores.BOLD}ETAPA 2/2: EXTRAÇÃO DE DADOS NUTRICIONAIS{Cores.RESET}")
            print(f"{Cores.CIANO}{'='*60}{Cores.RESET}\n")
            
            import nutritional_scraper
            nutritional_scraper.main()
            
            fim = time.time()
            tempo_total = fim - inicio
            
            # Resumo final
            print(f"\n{Cores.VERDE}{Cores.BOLD}{'='*60}{Cores.RESET}")
            print(f"{Cores.VERDE}{Cores.BOLD}✅ FLUXO COMPLETO CONCLUÍDO COM SUCESSO!{Cores.RESET}")
            print(f"{Cores.VERDE}{Cores.BOLD}{'='*60}{Cores.RESET}")
            print(f"\n{Cores.CIANO}⏱️  Tempo total: {Cores.AMARELO}{tempo_total/60:.1f} minutos{Cores.RESET}")
            print(f"{Cores.CIANO}📁 Arquivos gerados:{Cores.RESET}")
            print(f"   • {Cores.VERDE}json/produtos_urls.json{Cores.RESET}")
            print(f"   • {Cores.VERDE}dados_extraidos/produtos_nutricionais.csv{Cores.RESET}")
            
        except Exception as e:
            print(f"\n{Cores.VERMELHO}❌ Erro durante execução: {e}{Cores.RESET}")
    else:
        print(f"{Cores.AMARELO}⏭️  Operação cancelada{Cores.RESET}")

def listar_arquivos_gerados():
    """Lista arquivos gerados pelo programa"""
    print(f"\n{Cores.CIANO}{Cores.BOLD}📋 ARQUIVOS GERADOS{Cores.RESET}")
    print(f"{Cores.AZUL}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Cores.RESET}")
    
    total_arquivos = 0
    
    # Lista JSONs
    print(f"\n{Cores.VERDE}{Cores.BOLD}📊 ARQUIVOS JSON:{Cores.RESET}")
    pasta_json = "json"
    
    if os.path.exists(pasta_json):
        arquivos_json = glob.glob(f"{pasta_json}/*.json")
        
        if arquivos_json:
            for i, arquivo in enumerate(sorted(arquivos_json, reverse=True), 1):
                nome_arquivo = os.path.basename(arquivo)
                tamanho = os.path.getsize(arquivo)
                data_modificacao = datetime.fromtimestamp(os.path.getmtime(arquivo))
                
                # Calcula o tamanho em formato legível
                if tamanho < 1024:
                    tamanho_str = f"{tamanho} B"
                elif tamanho < 1024 * 1024:
                    tamanho_str = f"{tamanho / 1024:.1f} KB"
                else:
                    tamanho_str = f"{tamanho / (1024 * 1024):.1f} MB"
                
                print(f"\n{Cores.AMARELO}{i:2d}.{Cores.RESET} {Cores.BRANCO}{nome_arquivo}{Cores.RESET}")
                print(f"     📅 {data_modificacao.strftime('%d/%m/%Y %H:%M:%S')}")
                print(f"     📏 {tamanho_str}")
                total_arquivos += 1
        else:
            print(f"   {Cores.AMARELO}📄 Nenhum arquivo JSON encontrado{Cores.RESET}")
    else:
        print(f"   {Cores.AMARELO}📁 Pasta 'json/' não encontrada{Cores.RESET}")
    
    # Lista CSVs
    print(f"\n{Cores.VERDE}{Cores.BOLD}📈 ARQUIVOS CSV:{Cores.RESET}")
    pasta_csv = "dados_extraidos"
    
    if os.path.exists(pasta_csv):
        arquivos_csv = glob.glob(f"{pasta_csv}/*.csv")
        
        if arquivos_csv:
            for i, arquivo in enumerate(sorted(arquivos_csv, reverse=True), 1):
                nome_arquivo = os.path.basename(arquivo)
                tamanho = os.path.getsize(arquivo)
                data_modificacao = datetime.fromtimestamp(os.path.getmtime(arquivo))
                
                # Calcula o tamanho em formato legível
                if tamanho < 1024:
                    tamanho_str = f"{tamanho} B"
                elif tamanho < 1024 * 1024:
                    tamanho_str = f"{tamanho / 1024:.1f} KB"
                else:
                    tamanho_str = f"{tamanho / (1024 * 1024):.1f} MB"
                
                print(f"\n{Cores.AMARELO}{i:2d}.{Cores.RESET} {Cores.BRANCO}{nome_arquivo}{Cores.RESET}")
                print(f"     📅 {data_modificacao.strftime('%d/%m/%Y %H:%M:%S')}")
                print(f"     📏 {tamanho_str}")
                total_arquivos += 1
        else:
            print(f"   {Cores.AMARELO}📄 Nenhum arquivo CSV encontrado{Cores.RESET}")
    else:
        print(f"   {Cores.AMARELO}📁 Pasta 'dados_extraidos/' não encontrada{Cores.RESET}")
    
    print(f"\n{Cores.CIANO}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Cores.RESET}")
    print(f"{Cores.VERDE}📊 Total de arquivos: {total_arquivos}{Cores.RESET}")

def limpar_dados_antigos():
    """Remove arquivos antigos"""
    print(f"\n{Cores.CIANO}{Cores.BOLD}🗑️  LIMPAR DADOS ANTIGOS{Cores.RESET}")
    print(f"{Cores.AZUL}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Cores.RESET}")
    
    # Conta arquivos
    arquivos_json = glob.glob("json/*.json") if os.path.exists("json") else []
    arquivos_csv = glob.glob("dados_extraidos/*.csv") if os.path.exists("dados_extraidos") else []
    total_arquivos = len(arquivos_json) + len(arquivos_csv)
    
    if total_arquivos == 0:
        print(f"\n{Cores.VERDE}✅ Nenhum arquivo para limpar{Cores.RESET}")
        return
    
    print(f"\n{Cores.AMARELO}⚠️  ATENÇÃO:{Cores.RESET}")
    print(f"   • Serão removidos {Cores.VERMELHO}{total_arquivos} arquivos{Cores.RESET}")
    print(f"     - {len(arquivos_json)} arquivo(s) JSON")
    print(f"     - {len(arquivos_csv)} arquivo(s) CSV")
    print(f"   • Esta ação {Cores.VERMELHO}NÃO PODE ser desfeita{Cores.RESET}")
    
    confirmar = input(f"\n{Cores.MAGENTA}🤔 Tem certeza? Digite 'CONFIRMAR' para prosseguir: {Cores.RESET}")
    
    if confirmar == "CONFIRMAR":
        try:
            removidos = 0
            
            for arquivo in arquivos_json + arquivos_csv:
                os.remove(arquivo)
                removidos += 1
                print(f"{Cores.AMARELO}🗑️  Removido: {os.path.basename(arquivo)}{Cores.RESET}")
            
            print(f"\n{Cores.VERDE}✅ {removidos} arquivo(s) removido(s) com sucesso!{Cores.RESET}")
        except Exception as e:
            print(f"\n{Cores.VERMELHO}❌ Erro ao remover arquivos: {e}{Cores.RESET}")
    else:
        print(f"{Cores.AMARELO}⏭️  Operação cancelada{Cores.RESET}")

def mostrar_sobre():
    """Exibe informações sobre o programa"""
    sobre = f"""
{Cores.CIANO}{Cores.BOLD}📖 SOBRE O ADAPTOGEN SCRAPER{Cores.RESET}
{Cores.AZUL}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Cores.RESET}

{Cores.VERDE}🎯 OBJETIVO:{Cores.RESET}
   Coletar e extrair automaticamente informações nutricionais de produtos
   do site Adaptogen (adaptogen.com.br), facilitando a análise e comparação
   de dados nutricionais de suplementos.

{Cores.VERDE}📊 FUNCIONALIDADES:{Cores.RESET}
   • Coleta automática de URLs de produtos em 4 categorias
   • Suporte a paginação automática (categoria Proteínas)
   • Extração inteligente de tabelas nutricionais
   • Exportação de dados em formato JSON e CSV
   • Tratamento de valores ausentes (converte para 0)
   • Registro de data/hora da coleta

{Cores.VERDE}🛠️  TECNOLOGIAS:{Cores.RESET}
   • Python 3.13+
   • requests - Requisições HTTP
   • beautifulsoup4 - Parsing HTML
   • lxml - Parser rápido
   • csv - Manipulação de CSV

{Cores.VERDE}📂 ARQUIVOS GERADOS:{Cores.RESET}
   • Formato JSON: json/produtos_urls.json
   • Formato CSV: dados_extraidos/produtos_nutricionais.csv
   • Estrutura: Nome, URL, Porção, Macros, Data, Categoria

{Cores.VERDE}⚡ CARACTERÍSTICAS:{Cores.RESET}
   • Headers personalizados para simular navegador real
   • Delay de 2s entre requisições para respeitar o servidor
   • Logging detalhado do progresso e erros
   • Interface CLI colorida e intuitiva
   • Tratamento robusto de erros HTTP

{Cores.VERDE}📝 DESENVOLVIDO POR:{Cores.RESET}
   • Sidnei Almeida
   • GitHub: github.com/sidnei-almeida
   • Versão: 1.0
   • Data: {datetime.now().strftime('%B %Y')}

{Cores.AZUL}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Cores.RESET}
"""
    print(sobre)

def pausar():
    """Pausa o programa aguardando input do usuário"""
    input(f"\n{Cores.CIANO}⏯️  Pressione Enter para continuar...{Cores.RESET}")

# ============================================================================
# 🚀 FUNÇÃO PRINCIPAL
# ============================================================================
def main():
    """Função principal do programa"""
    try:
        while True:
            limpar_terminal()
            mostrar_banner()
            mostrar_menu()
            
            escolha = obter_escolha()
            
            if escolha == "1":
                coletar_urls()
                pausar()
                
            elif escolha == "2":
                extrair_dados_nutricionais()
                pausar()
                
            elif escolha == "3":
                executar_fluxo_completo()
                pausar()
                
            elif escolha == "4":
                listar_arquivos_gerados()
                pausar()
                
            elif escolha == "5":
                limpar_dados_antigos()
                pausar()
                
            elif escolha == "6":
                mostrar_sobre()
                pausar()
                
            elif escolha == "7":
                print(f"\n{Cores.VERDE}👋 Obrigado por usar o Adaptogen Scraper!{Cores.RESET}")
                print(f"{Cores.CIANO}🚀 Até a próxima!{Cores.RESET}\n")
                break
                
            else:
                print(f"\n{Cores.VERMELHO}❌ Opção inválida! Por favor, escolha entre 1-7{Cores.RESET}")
                time.sleep(2)
                
    except KeyboardInterrupt:
        print(f"\n\n{Cores.AMARELO}👋 Programa encerrado pelo usuário. Até logo!{Cores.RESET}\n")
    except Exception as e:
        print(f"\n{Cores.VERMELHO}❌ Erro inesperado: {e}{Cores.RESET}")

if __name__ == "__main__":
    main()

