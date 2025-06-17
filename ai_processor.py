import pandas as pd
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from config import config

class AIProcessor:
    def __init__(self):
        self.model = config["model"]["name"]
        self.chat = ChatOpenAI(model_name=self.model, temperature=0.3)
    
    def generate_sql_from_question(self, question, schema):
        """Gera uma query SQL baseada na pergunta do usuário"""
        
        system_prompt = f"""Você é um especialista em SQL e análise de dados. 
        
        Baseado na pergunta do usuário, você deve gerar uma query SQL válida para o banco de dados SQLite.
        
        Schema do banco de dados:
        {schema}
        
        Regras importantes:
        1. Use apenas as tabelas 'receipts' e 'items'
        2. A tabela 'receipts' contém informações das notas fiscais (cabeçalho)
        3. A tabela 'items' contém os itens de cada nota fiscal
        4. As tabelas são relacionadas pela coluna 'CHAVE_DE_ACESSO'
        5. Para contar notas fiscais, use COUNT(*) na tabela receipts
        6. Para valores monetários, use a coluna 'VALOR_NOTA_FISCAL' da tabela receipts
        7. Para datas, use a coluna 'DATA_EMISSAO'
        8. Retorne APENAS a query SQL, sem explicações adicionais
        
        Exemplos de queries comuns:
        - Contar total de notas: SELECT COUNT(*) as total_notas FROM receipts
        - Soma de valores: SELECT SUM(VALOR_NOTA_FISCAL) as valor_total FROM receipts
        - Notas por UF: SELECT UF_EMITENTE, COUNT(*) as total FROM receipts GROUP BY UF_EMITENTE
        """
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=f"Pergunta: {question}\n\nGere uma query SQL para responder esta pergunta:")
        ]
        
        response = self.chat.invoke(messages)
        return response.content.strip()
    
    def generate_human_response(self, question, sql_query, result):
        """Gera uma resposta humana e natural baseada nos resultados da query SQL"""
        
        system_prompt = """Você é um assistente especializado em análise de dados de notas fiscais. 
        
        Sua função é responder perguntas sobre dados de notas fiscais de forma clara, natural e direta.
        
        Regras importantes:
        1. Responda sempre em português brasileiro
        2. Seja natural e conversacional, como se estivesse explicando para um colega
        3. Use linguagem simples e acessível
        4. Seja direto e objetivo - não adicione contexto ou insights extras
        5. Para valores monetários, formate adequadamente (ex: R$ 1.234,56)
        6. Para datas, use formato brasileiro (dd/mm/aaaa)
        7. Se houver muitos resultados, destaque os principais
        8. Não mencione detalhes técnicos como queries SQL a menos que seja necessário
        9. Use expressões naturais como "Encontrei", "Analisando os dados", "Com base nos resultados"
        10. Para percentuais, use formato brasileiro (ex: 45,5%)
        11. Responda apenas o que foi perguntado, sem adicionar informações extras
        
        Exemplos de respostas:
        - "Encontrei um total de 1.234 notas fiscais no período analisado."
        - "O valor total das notas fiscais é de R$ 45.678,90."
        - "As principais UFs emissoras são São Paulo (45%), Rio de Janeiro (30%) e Minas Gerais (25%)."
        - "Analisando os dados, posso ver que..."
        - "Com base nos resultados obtidos..."
        """
        
        # Preparar contexto com os resultados
        context = self._prepare_result_context(result)
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=f"""Pergunta do usuário: {question}

                Query SQL executada: {sql_query}

                Resultados obtidos:
                {context}

                Agora responda de forma natural e direta, explicando apenas os resultados da pergunta feita. 
                Seja amigável e use linguagem do dia a dia, mas seja objetivo e não adicione informações extras:""")
        ]
        
        response = self.chat.invoke(messages)
        return response.content.strip()
    
    def _prepare_result_context(self, result):
        """Prepara o contexto dos resultados para a resposta"""
        if isinstance(result, pd.DataFrame):
            if len(result) == 1 and len(result.columns) == 1:
                # Resultado simples
                return f"Resultado da consulta: {result.iloc[0, 0]}"
            else:
                # Resultado mais complexo - limitar a 10 linhas para não sobrecarregar
                if len(result) > 10:
                    return f"Resultado da consulta (mostrando primeiras 10 linhas de {len(result)}):\n{result.head(10).to_string(index=False)}"
                else:
                    return f"Resultado da consulta:\n{result.to_string(index=False)}"
        else:
            # Erro na execução
            return f"Erro: {result}"

# Instância global do processador de IA
ai_processor = AIProcessor() 