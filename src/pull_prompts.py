"""
Script para fazer pull de prompts do LangSmith Prompt Hub.

Este script:
1. Conecta ao LangSmith usando credenciais do .env
2. Faz pull dos prompts do Hub
3. Salva localmente em prompts/bug_to_user_story_v1.yml

SIMPLIFICADO: Usa serialização nativa do LangChain para extrair prompts.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from langchain import hub
from utils import save_yaml, check_env_vars, print_section_header

load_dotenv()


def pull_prompts_from_langsmith():
    print_section_header("PULL DE PROMPTS DO LANGSMITH HUB")

    required_vars = ["LANGSMITH_API_KEY"]
    if not check_env_vars(required_vars):
        return False

    prompts_to_pull = [
        {
            "source": "leonanluppi/bug_to_user_story_v1",
            "output_file": "prompts/bug_to_user_story_v1.yml",
        }
    ]

    success = True

    for prompt_config in prompts_to_pull:
        source = prompt_config["source"]
        output_file = prompt_config["output_file"]

        print(f"Fazendo pull de: {source}")

        try:
            prompt = hub.pull(source)

            messages = prompt.messages
            system_prompt = ""
            user_prompt = ""

            for msg in messages:
                role = msg.__class__.__name__.lower()
                if "system" in role:
                    system_prompt = msg.prompt.template if hasattr(msg, "prompt") else str(msg)
                elif "human" in role:
                    user_prompt = msg.prompt.template if hasattr(msg, "prompt") else str(msg)

            prompt_name = source.split("/")[-1]
            prompt_data = {
                prompt_name: {
                    "description": f"Prompt pulled from LangSmith Hub: {source}",
                    "system_prompt": system_prompt,
                    "user_prompt": user_prompt,
                    "version": "v1",
                    "source": source,
                    "tags": ["bug-analysis", "user-story", "product-management"],
                }
            }

            if save_yaml(prompt_data, output_file):
                print(f"   Salvo em: {output_file}")
            else:
                print(f"   Erro ao salvar {output_file}")
                success = False

        except Exception as e:
            print(f"   Erro ao fazer pull de {source}: {e}")
            success = False

    return success


def main():
    """Função principal"""
    result = pull_prompts_from_langsmith()

    if result:
        print("\nPull concluído com sucesso!")
        print("Próximo passo: otimize os prompts e execute push_prompts.py")
        return 0
    else:
        print("\nErro durante o pull dos prompts.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
