import os
import zipfile
import pandas as pd
from config import config

def unzip_files():
    """Descompacta arquivo ZIP para a pasta de destino especificada"""
    try:
        caminho_zip = config["files"]["zip"] + "/202401_NFs.zip"
        pasta_destino = config["files"]["unzip"]

        # Verifica se o arquivo ZIP existe
        if not os.path.exists(caminho_zip):
            print(f"Arquivo {caminho_zip} não encontrado!")
            return
        
        # Cria a pasta de destino se ela não existir
        os.makedirs(pasta_destino, exist_ok=True)
        
        # Abre o arquivo ZIP e extrai todo o conteúdo
        with zipfile.ZipFile(caminho_zip, 'r') as zip_ref:
            zip_ref.extractall(pasta_destino)
            
    except Exception as e:
        print(f"Ocorreu um erro ao descompactar: {e}")

def normalize_column_names(df):
    """Normaliza nomes das colunas removendo espaços e caracteres especiais"""
    return df.columns.str.replace(' ', '_').str.replace('Ç', 'C').str.replace('Ã', 'A').str.replace('Õ', 'O')

def load_csv_files():
    """Carrega os arquivos CSV e retorna os DataFrames"""
    unzip_folder_path = config["files"]["unzip"]
    
    # Carregar os dados
    df_cabecalho = pd.read_csv(unzip_folder_path + "/202401_NFs_Cabecalho.csv")
    df_itens = pd.read_csv(unzip_folder_path + "/202401_NFs_Itens.csv")
    
    # Normalizar nomes das colunas
    df_cabecalho.columns = normalize_column_names(df_cabecalho)
    df_itens.columns = normalize_column_names(df_itens)
    
    return df_cabecalho, df_itens 