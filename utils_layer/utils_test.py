"""Modulo de testes das funcoes uteis"""

import utils


def test_cpf_mask():
    """Teste CPF formatado"""
    result = utils.cpf_mask("00110119207")
    assert result == "001.101.192-07"
