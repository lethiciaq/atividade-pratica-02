"""Validação do kit_a02: sem colisões, checagens batem com o gerador.

Não é um pacote de testes formal (o repositório não usa framework de
terceiros) — é um script de verificação, no mesmo espírito do
`distribuicao()`. Rode com::

    python3 -m scripts.test_kit_a02
"""

from . import core
from .kit_a02 import (
    _checagens,
    comissao_e_repasse,
    classificar_avaliacao,
    dados_de,
    decisao_expansao,
    frete_e_prazo,
)


def test_sem_colisoes():
    matriculas = [str(20261234500 + i) for i in range(core.TURMA_MAX)]
    vistos = {}
    for m in matriculas:
        d = dados_de(m)
        vistos.setdefault(d["MEU_NEGOCIO"], []).append(m)
    repetidos = {k: v for k, v in vistos.items() if len(v) > 1}
    assert not repetidos, f"negócios repetidos na turma simulada: {repetidos}"
    print(f"✅ sem colisões em {len(matriculas)} matrículas simuladas "
          f"({len(vistos)} negócios distintos)")


def test_pedidos_hoje_sempre_em_pico():
    for m in (str(20261234500 + i) for i in range(core.TURMA_MAX)):
        d = dados_de(m)
        assert d["MEUS_PEDIDOS_HOJE"] > 50, d["MEUS_PEDIDOS_HOJE"]
    print("✅ MEUS_PEDIDOS_HOJE sempre em faixa de pico (> 50) para toda a turma")


def test_checagens_batem_com_gerador():
    d = dados_de("20261234567")

    # Exercício 1
    diferenca = d["MEU_ESTOQUE_ATUAL"] - d["MEU_ESTOQUE_MINIMO"]
    precisa_repor = d["MEU_ESTOQUE_ATUAL"] < d["MEU_ESTOQUE_MINIMO"]
    resultados = _checagens("exercicio-1", dict(
        diferenca=diferenca, precisa_repor=precisa_repor,
    ), d)
    assert all(ok for ok, _ in resultados), resultados

    # Exercício 2
    escalar = d["MEU_TEMPO_ESPERA_MIN"] > 10 or d["MEU_CHAMADO_VIP"]
    fila = "🚨 Supervisor" if escalar else "💬 Atendente padrão"
    resultados = _checagens("exercicio-2", dict(
        escalar_supervisor=escalar, fila_destino=fila,
    ), d)
    assert all(ok for ok, _ in resultados), resultados

    # Exercício 3
    resultados = _checagens("exercicio-3", dict(
        classificacao=classificar_avaliacao(d["MINHA_NOTA_AVALIACAO"]),
    ), d)
    assert all(ok for ok, _ in resultados), resultados

    # Exercício 4
    frete_final, prazo_dias = frete_e_prazo(
        d["MEU_MODAL_ENTREGA"], d["MEU_VALOR_PEDIDO"]
    )
    resultados = _checagens("exercicio-4", dict(
        frete_final=frete_final, prazo_dias=prazo_dias,
    ), d)
    assert all(ok for ok, _ in resultados), resultados

    # Exercício 5
    praticas, decisao = decisao_expansao(d)
    resultados = _checagens("exercicio-5", dict(
        praticas_prontidao=praticas, decisao_expansao=decisao,
    ), d)
    assert all(ok for ok, _ in resultados), resultados

    # Exercício 6
    valor = float(d["MEU_VALOR_CAIXA_TEXTO"])
    quantidade = int(d["MINHA_QUANTIDADE_ITENS_TEXTO"])
    sinal = 1 if d["MEU_TIPO_LANCAMENTO_TEXTO"] == "entrada" else -1
    resultados = _checagens("exercicio-6", dict(
        valor_unitario=valor / quantidade, impacto_caixa=valor * sinal,
    ), d)
    assert all(ok for ok, _ in resultados), resultados

    # Exercício 7
    comissao_valor, retencao, valor_repasse = comissao_e_repasse(
        d["MEU_TIPO_SERVICO_PLATAFORMA"],
        d["MEU_REGIME_PRESTADOR"],
        d["MEU_VALOR_SERVICO"],
    )
    resultados = _checagens("exercicio-7", dict(
        comissao_valor=comissao_valor, retencao=retencao,
        valor_repasse=valor_repasse,
    ), d)
    assert all(ok for ok, _ in resultados), resultados

    print("✅ todas as checagens (exercícios 1–7) batem com o gerador para "
          "a matrícula de teste")


def test_todas_as_matriculas_geram_sem_erro():
    for m in (str(20261234500 + i) for i in range(core.TURMA_MAX)):
        d = dados_de(m)
        frete_e_prazo(d["MEU_MODAL_ENTREGA"], d["MEU_VALOR_PEDIDO"])
        comissao_e_repasse(
            d["MEU_TIPO_SERVICO_PLATAFORMA"],
            d["MEU_REGIME_PRESTADOR"],
            d["MEU_VALOR_SERVICO"],
        )
    print("✅ dados e réguas geram sem erro para toda a turma simulada")


if __name__ == "__main__":
    test_sem_colisoes()
    test_pedidos_hoje_sempre_em_pico()
    test_checagens_batem_com_gerador()
    test_todas_as_matriculas_geram_sem_erro()
    print("OK")
