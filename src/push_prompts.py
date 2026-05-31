"""
Script para fazer push de prompts otimizados ao LangSmith Prompt Hub.

Este script:
1. Lê os prompts otimizados de prompts/bug_to_user_story_v2.yml
2. Valida os prompts
3. Faz push PÚBLICO para o LangSmith Hub
4. Adiciona metadados (tags, descrição, técnicas utilizadas)

SIMPLIFICADO: Código mais limpo e direto ao ponto.
"""

import os
import sys
from dotenv import load_dotenv
from langchain import hub
from langchain_core.prompts import ChatPromptTemplate
from utils import load_yaml, check_env_vars, print_section_header

load_dotenv()


def push_prompt_to_langsmith(prompt_name: str, prompt_data: dict) -> bool:
    """
    Faz push do prompt otimizado para o LangSmith Hub (PÚBLICO).

    Args:
        prompt_name: Nome do prompt no formato username/nome
        prompt_data: Dados do prompt com system_prompt e user_prompt

    Returns:
        True se sucesso, False caso contrário
    """
    try:
        system_prompt = prompt_data.get("system_prompt", "")
        user_prompt = prompt_data.get("user_prompt", "{bug_report}")

        prompt_template = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", user_prompt),
        ])

        hub.push(prompt_name, prompt_template, new_repo_is_public=True)
        print(f"   Push realizado: {prompt_name}")
        return True

    except Exception as e:
        print(f"   Erro ao fazer push de {prompt_name}: {e}")
        return False


def validate_prompt(prompt_data: dict) -> tuple[bool, list]:
    """
    Valida estrutura básica de um prompt (versão simplificada).

    Args:
        prompt_data: Dados do prompt

    Returns:
        (is_valid, errors) - Tupla com status e lista de erros
    """
    errors = []

    if not prompt_data.get("system_prompt", "").strip():
        errors.append("system_prompt está vazio")

    if "TODO" in prompt_data.get("system_prompt", ""):
        errors.append("system_prompt ainda contém TODOs")

    techniques = prompt_data.get("techniques_applied", [])
    if len(techniques) < 2:
        errors.append(f"Mínimo de 2 técnicas requeridas, encontradas: {len(techniques)}")

    return (len(errors) == 0, errors)


def main():
    """Função principal"""
    print_section_header("PUSH DE PROMPTS OTIMIZADOS AO LANGSMITH HUB")

    required_vars = ["LANGSMITH_API_KEY", "USERNAME_LANGSMITH_HUB"]
    if not check_env_vars(required_vars):
        return 1

    username = os.getenv("USERNAME_LANGSMITH_HUB")

    prompts_to_push = [
        {
            "yaml_file": "prompts/bug_to_user_story_v2.yml",
            "yaml_key": "bug_to_user_story_v2",
            "hub_name": f"{username}/bug_to_user_story_v2",
        }
    ]

    all_success = True

    for config in prompts_to_push:
        yaml_file = config["yaml_file"]
        yaml_key = config["yaml_key"]
        hub_name = config["hub_name"]

        print(f"Carregando: {yaml_file}")

        data = load_yaml(yaml_file)
        if not data:
            print(f"   Erro ao carregar {yaml_file}")
            all_success = False
            continue

        prompt_data = data.get(yaml_key, {})
        if not prompt_data:
            print(f"   Chave '{yaml_key}' não encontrada no YAML")
            all_success = False
            continue

        is_valid, errors = validate_prompt(prompt_data)
        if not is_valid:
            print(f"   Validação falhou:")
            for err in errors:
                print(f"      - {err}")
            all_success = False
            continue

        print(f"Fazendo push: {hub_name}")
        success = push_prompt_to_langsmith(hub_name, prompt_data)
        if not success:
            all_success = False

    if all_success:
        print("\nTodos os prompts publicados com sucesso!")
        print("Próximo passo: execute python src/evaluate.py")
        return 0
    else:
        print("\nErro ao publicar alguns prompts. Verifique os erros acima.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
