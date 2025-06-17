from langchain.memory import ConversationBufferMemory

class MemoryManager:
    def __init__(self):
        self.client_memories = {}
    
    def get_memory(self, client_id):
        """Obtém ou cria a memória para um cliente específico"""
        if client_id not in self.client_memories:
            self.client_memories[client_id] = ConversationBufferMemory(
                memory_key="chat_history", 
                return_messages=True
            )
        return self.client_memories[client_id]
    
    def clear_memory(self, client_id):
        """Limpa a memória de um cliente específico"""
        if client_id in self.client_memories:
            del self.client_memories[client_id]
    
    def clear_all_memories(self):
        """Limpa todas as memórias"""
        self.client_memories.clear()

# Instância global do gerenciador de memória
memory_manager = MemoryManager() 