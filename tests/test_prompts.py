"""
Testes automatizados para validação de prompts.
"""
import pytest
import yaml
import sys
from pathlib import Path

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from utils import validate_prompt_structure

def load_prompts(file_path: str):
    """Carrega prompts do arquivo YAML."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

PROMPT_FILE = str(Path(__file__).parent.parent / "prompts" / "bug_to_user_story_v2.yml")
PROMPT_KEY = "bug_to_user_story_v2"


@pytest.fixture(scope="module")
def prompt_data():
    prompts = load_prompts(PROMPT_FILE)
    assert PROMPT_KEY in prompts, f"Chave '{PROMPT_KEY}' não encontrada no YAML"
    return prompts[PROMPT_KEY]


class TestPrompts:
    def test_prompt_has_system_prompt(self, prompt_data):
        """Verifica se o campo 'system_prompt' existe e não está vazio."""
        system_prompt = prompt_data.get("system_prompt", "")
        assert system_prompt, "system_prompt está vazio ou ausente"
        assert len(system_prompt.strip()) > 50, "system_prompt é muito curto"

    def test_prompt_has_role_definition(self, prompt_data):
        """Verifica se o prompt define uma persona (ex: 'Você é um Product Manager')."""
        system_prompt = prompt_data.get("system_prompt", "")
        role_keywords = ["você é", "voce e", "você é um", "you are"]
        assert any(kw in system_prompt.lower() for kw in role_keywords), \
            "system_prompt não define uma persona/role (ex: 'Você é um Product Manager')"

    def test_prompt_mentions_format(self, prompt_data):
        """Verifica se o prompt exige formato Markdown ou User Story padrão."""
        system_prompt = prompt_data.get("system_prompt", "")
        format_keywords = ["como um", "eu quero", "para que", "critérios de aceitação", "user story", "dado que", "quando", "então"]
        matches = [kw for kw in format_keywords if kw in system_prompt.lower()]
        assert len(matches) >= 3, \
            f"system_prompt não especifica formato de User Story adequadamente. Encontrados: {matches}"

    def test_prompt_has_few_shot_examples(self, prompt_data):
        """Verifica se o prompt contém exemplos de entrada/saída (técnica Few-shot)."""
        system_prompt = prompt_data.get("system_prompt", "")
        example_keywords = ["exemplo", "input:", "output:", "**input**", "**output**"]
        assert any(kw in system_prompt.lower() for kw in example_keywords), \
            "system_prompt não contém exemplos de Few-shot (Input/Output)"

    def test_prompt_no_todos(self, prompt_data):
        """Garante que não há [TODO] no texto."""
        system_prompt = prompt_data.get("system_prompt", "")
        user_prompt = prompt_data.get("user_prompt", "")
        full_text = system_prompt + user_prompt
        assert "[TODO]" not in full_text and "[todo]" not in full_text.lower(), \
            "Prompt contém marcadores [TODO] não resolvidos"

    def test_minimum_techniques(self, prompt_data):
        """Verifica se pelo menos 2 técnicas foram listadas nos metadados do YAML."""
        techniques = prompt_data.get("techniques_applied", [])
        assert isinstance(techniques, list), "techniques_applied deve ser uma lista"
        assert len(techniques) >= 2, \
            f"Mínimo de 2 técnicas requeridas, encontradas: {len(techniques)} — {techniques}"

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])