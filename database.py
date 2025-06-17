import os
import sqlite3
import pandas as pd
from config import config
from file_processor import load_csv_files

class DatabaseManager:
    def __init__(self):
        self.database_path = config["database"]["path"]
        self.db_name = config["database"]["name"]
        self.db_path = os.path.join(self.database_path, self.db_name)
        
    def create_database(self):
        """Cria o banco de dados e carrega os dados dos arquivos CSV"""
        # Criar pasta database se não existir
        os.makedirs(self.database_path, exist_ok=True)
        
        # Carregar dados dos CSV
        df_cabecalho, df_itens = load_csv_files()
        
        # Criar conexão com o banco SQLite
        conn = sqlite3.connect(self.db_path)
        
        # Salvar as tabelas no banco de dados
        df_cabecalho.to_sql('receipts', conn, if_exists='replace', index=False)
        df_itens.to_sql('items', conn, if_exists='replace', index=False)
        
        # Criar índices para melhor performance
        self._create_indexes(conn)
        
        # Fechar conexão
        conn.close()
    
    def _create_indexes(self, conn):
        """Cria índices para melhorar performance das consultas"""
        conn.execute('CREATE INDEX IF NOT EXISTS idx_receipts_chave ON receipts (CHAVE_DE_ACESSO)')
        conn.execute('CREATE INDEX IF NOT EXISTS idx_items_chave ON items (CHAVE_DE_ACESSO)')
    
    def get_schema(self):
        """Retorna o schema do banco de dados"""
        conn = sqlite3.connect(self.db_path)
        
        schema_info = []
        
        # Obter informações das tabelas
        tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
        
        for table in tables:
            table_name = table[0]
            columns = conn.execute(f"PRAGMA table_info({table_name});").fetchall()
            
            table_info = f"Tabela: {table_name}\n"
            table_info += "Colunas:\n"
            for col in columns:
                table_info += f"  - {col[1]} ({col[2]})\n"
            
            schema_info.append(table_info)
        
        conn.close()
        return "\n".join(schema_info)
    
    def execute_query(self, query):
        """Executa uma query SQL e retorna os resultados"""
        try:
            conn = sqlite3.connect(self.db_path)
            
            # Executar a query
            result = pd.read_sql_query(query, conn)
            conn.close()
            
            return result
        except Exception as e:
            return f"Erro na execução da query: {str(e)}"

# Instância global do gerenciador de banco
db_manager = DatabaseManager() 