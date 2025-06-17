import yaml
import os

# Carregar configurações do arquivo YAML
CONFIG_FILE = "config.yaml"

def load_config():
    """Carrega as configurações do arquivo YAML"""
    with open(CONFIG_FILE, "r") as file:
        return yaml.safe_load(file)

# Configuração global
config = load_config() 