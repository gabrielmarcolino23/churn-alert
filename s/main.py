import openai
import os
import pandas as pd
from crewai_tools import SerperDevTool
from crewai import Agent, Task

# Carregar variáveis de ambiente
os.environ["SERPER_API_KEY"] = "sua_chave_serper"
os.environ["OPENAI_API_KEY"] = "sua_chave_openai"

search_tool = SerperDevTool()

# Definir agente que realiza a busca
def create_search_agent():
    agent = Agent(
        role='Buscador de Segmentos',
        goal='Determinar o segmento de um ecommerce a partir da URL.',
        tools=[search_tool],
        verbose=True
    )
    return agent

# Função para determinar o segmento de uma URL usando o agente
def get_segment_from_url(agent, url):
    try:
        search_query = f"site:{url} tipo de produto vendido"
        result = agent.run(search_query)
        
        # Implementar lógica para determinar o segmento
        if result:
            content = result.lower()
            if "fashion" in content or "clothing" in content or "moda" in content:
                return "Moda"
            elif "electronics" in content or "eletrônicos" in content:
                return "Eletrônicos"
            elif "food" in content or "alimentos" in content:
                return "Alimentos"
            else:
                return "Outro"
        else:
            return "Indefinido"
    except Exception as e:
        print(f"Erro ao acessar {url}: {e}")
        return "Indefinido"

# Função para preencher a planilha
def fill_segment_column(input_file, output_file):
    # Carregar o arquivo de entrada
    df = pd.read_excel(input_file)
    agent = create_search_agent()

    # Preencher a coluna com o segmento
    df['Segmento'] = df['url'].apply(lambda url: get_segment_from_url(agent, url))

    # Salvando o arquivo de saída
    df.to_excel(output_file, index=False)
    print(f"Processo concluído. A planilha atualizada está salva em '{output_file}'.")

# Uso do código
input_file = 'ecommerce_urls.xlsx'
output_file = 'ecommerce_urls_com_segmento.xlsx'
fill_segment_column(input_file, output_file)
