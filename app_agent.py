"""
Agente de IA para análise de dados de recibos
Refatorado para melhor organização e manutenibilidade
"""

import logging
from typing import Dict, Any, Optional
from flask import Flask, request, jsonify

# Importar módulos criados
from config import config
from database import db_manager
from ai_processor import ai_processor
from memory_manager import memory_manager
from file_processor import unzip_files

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def initialize_app():
    """Inicializa a aplicação"""
    try:
        logger.info("Iniciando configuração da aplicação...")
        
        # Descompactar arquivos se necessário
        logger.info("Verificando arquivos ZIP...")
        unzip_files()
        
        # Criar banco de dados
        logger.info("Criando banco de dados...")
        db_manager.create_database()
        
        logger.info("Aplicação inicializada com sucesso!")
        return True
        
    except Exception as e:
        logger.error(f"Erro ao inicializar aplicação: {str(e)}")
        return False

# Criar aplicação Flask
app = Flask(__name__)

@app.route('/ask', methods=['POST'])
def ask():
    """Endpoint principal para processar perguntas"""
    data = request.get_json()
    
    if not data or "question" not in data:
        return jsonify({"error": "Forneça 'question' na requisição."}), 400

    question = data["question"]
    client_id = data.get("client_id", "default")
    
    try:
        logger.info(f"Processando pergunta do cliente {client_id}: {question}")
        
        # Obter schema do banco
        schema = db_manager.get_schema()
        
        # Gerar query SQL
        sql_query = ai_processor.generate_sql_from_question(question, schema)
        logger.info(f"Query SQL gerada: {sql_query}")
        
        # Executar a query
        result = db_manager.execute_query(sql_query)
        
        # Gerar resposta humana
        human_answer = ai_processor.generate_human_response(question, sql_query, result)
        
        logger.info(f"Resposta gerada com sucesso para cliente {client_id}")
        
        return jsonify({
            "answer": human_answer,
            "sql_query": sql_query,
            "client_id": client_id
        })
        
    except Exception as e:
        logger.error(f"Erro ao processar pergunta: {str(e)}")
        return jsonify({"error": f"Erro interno do servidor: {str(e)}"}), 500

if __name__ == '__main__':
    # Inicializar aplicação
    if not initialize_app():
        logger.error("Falha na inicialização da aplicação. Encerrando...")
        exit(1)
    
    logger.info(f"Iniciando servidor com modelo: {config['model']['name']}")
    logger.info(f"Banco de dados: {config['database']['name']}")
    
    app.run(
        host='0.0.0.0',
        port=5001, 
        debug=True
    )
