"""Kit da Atividade 02 — O Painel de Comando do Seu Negócio.

Cenário: alguns meses se passaram desde o Raio-X (Atividade 01, em outro
repositório-template — `cdn-ppi-lab`). O **mesmo** negócio — mesmo nome,
mesma cidade, mesma categoria — cresceu, e cresceu rápido demais para
decisões "no olho". Você, fundador(a), monta agora um painel de comando: um
conjunto de regras automáticas que decidem, sozinhas, o que fazer em sete
frentes do dia a dia — estoque, atendimento, avaliação de clientes,
logística, expansão, caixa e repasse a prestadores.

O notebook do aluno usa seis funções, e é só isso::

    iniciar(matricula, nome)      liga o kit e cria os seus dados
    prever(**respostas)           carimba a sua previsão antes de revelar
    registrar(etapa, nota)        marca uma etapa no diário de bordo
    conferir(etapa, **respostas)  devolve um retorno sobre o que você resolveu
    diario()                      mostra o seu ritmo de trabalho
    assinatura()                  emite a linha de entrega

Nada aqui usa rede, arquivo externo ou biblioteca de terceiros.

**Nível de estruturas: 2** — a Atividade 01 cobriu só escalares e operadores;
esta cobre `if`/`elif`/`else`, `match`/`case`, estruturas aninhadas e
`try`/`except`/`raise` (Módulos 6 e 7). **Ainda sem laços** (`for`, `while`)
nem listas, tuplas ou dicionários — essas ferramentas chegam nos módulos
seguintes.

A identidade do negócio (nome, UF, categoria) em `_IDENTIDADES` é uma
**cópia** das três primeiras colunas do painel de `kit_a01.py` no
repositório da Atividade 01 — cada atividade é o seu próprio
repositório-template no GitHub (`git clone`/"Use this template" não têm
nenhuma relação de sincronia entre si depois de criados), então não há como
importar entre os dois. A cópia garante que a mesma matrícula sempre caia
no mesmo negócio nas duas atividades. ⚠️ Se o painel da Atividade 01 for
alterado (nova linha, categoria diferente), replique a mudança aqui à mão.

Os números **operacionais** desta atividade são sorteados de forma
independente da Atividade 01 (semente própria, tema ``"a02"``) — é assim
que o `core.semente` garante que a dificuldade de uma atividade não "vaza"
para a próxima.

Este arquivo é legível de propósito: se você quiser entender de onde saem os
seus números, abra e leia — é Python comum, sem mágica. A mecânica
compartilhada (semente, diário, assinatura) mora em ``core.py``.
"""

from . import core
from .core import checar_bool, checar_igual, checar_numero

ATIVIDADE = "a02"
VERSAO = "1.0"

# ---------------------------------------------------------------- identidade
# (nome, UF, categoria) — cópia exata, na MESMA ORDEM, das três primeiras
# colunas do painel `_PAINEL` de `kit_a01.py` (repositório da Atividade 01).
# 43 linhas, como lá, para preservar a ausência de colisão na turma.
_IDENTIDADES = [
    ("Ateliê Flor de Lis", "SP", "moda"),
    ("Trama Urbana", "RJ", "moda"),
    ("Closet da Ana", "MG", "moda"),
    ("Verve Streetwear", "PE", "moda"),
    ("Patinhas Felizes", "SP", "pet"),
    ("Miau & Cia", "RS", "pet"),
    ("Cão Doido Pet Shop", "PR", "pet"),
    ("Bicho Solto", "BA", "pet"),
    ("Sabor Express", "SP", "delivery"),
    ("Fominha Delivery", "RJ", "delivery"),
    ("Panela de Barro Delivery", "BA", "delivery"),
    ("Prato Rápido", "CE", "delivery"),
    ("Aprendex Cursos", "MG", "educação"),
    ("Fluência Fácil Idiomas", "SP", "educação"),
    ("Academia do Código", "PB", "educação"),
    ("Notas & Acordes Música", "RS", "educação"),
    ("Studio Bela Face", "SP", "beleza"),
    ("Barbearia Navalha de Ouro", "RJ", "beleza"),
    ("Espaço Renove Estética", "PE", "beleza"),
    ("Tinta na Pele Tatuagem", "PR", "beleza"),
    ("Respira Yoga Studio", "SP", "fitness"),
    ("Corpo em Movimento Pilates", "MG", "fitness"),
    ("PersonalFit Online", "RS", "fitness"),
    ("Vitalis Academia", "CE", "fitness"),
    ("Casa Encantada Decor", "SP", "casa"),
    ("Papelaria Girassol", "PB", "casa"),
    ("Lar Doce Lar Ateliê", "BA", "casa"),
    ("Cantinho Zen Decorações", "PR", "casa"),
    ("ReBoot Eletrônicos", "SP", "tecnologia"),
    ("TechNova Usados", "RJ", "tecnologia"),
    ("Circuito Reuso", "MG", "tecnologia"),
    ("GadgetLar", "DF", "tecnologia"),
    ("Brechó Retrô Vibe", "SP", "artesanato"),
    ("Mãos que Criam Artesanato", "PB", "artesanato"),
    ("Segunda Vida Brechó", "RS", "artesanato"),
    ("Fio & Arte", "PE", "artesanato"),
    ("Café das Letras", "SP", "gastronomia"),
    ("Sorveteria Polar Doce", "CE", "gastronomia"),
    ("Doceria da Vovó", "MG", "gastronomia"),
    ("Confeitaria Flor de Açúcar", "BA", "gastronomia"),
    ("Lava & Leva Lavanderia", "SP", "serviços"),
    ("Faxina Já", "RJ", "serviços"),
    ("Oficina do Seu Zé", "PR", "serviços"),
]

# ---------------------------------------------------------------- exercício 4
# modal: (frete-base em R$, prazo em dias úteis, valor mínimo p/ frete grátis)
_FRETE = {
    "moto": (8.90, 1, 80.0),
    "bike": (5.50, 1, 60.0),
    "van": (15.00, 2, 300.0),
    "correios": (22.00, 7, 500.0),
}

# ---------------------------------------------------------------- exercício 5
CORTE_PORTE_EXPANSAO = 60_000.0       # faturamento médio trimestral mínimo
CORTE_MARGEM_EXPANSAO = 8.0           # margem líquida média mínima (%)
CORTE_ENDIVIDAMENTO_EXPANSAO = 40.0   # endividamento máximo (%)
PRATICAS_MINIMAS_EXPANSAO = 2         # de 3 práticas operacionais

# ---------------------------------------------------------------- exercício 2
LIMITE_ESPERA_ESCALONAR = 10          # minutos

# ---------------------------------------------------------------- exercício 7
_COMISSOES_PLATAFORMA = {
    "limpeza": 0.20,
    "beleza": 0.25,
    "reparos": 0.18,
    "aulas": 0.15,
}
RETENCAO_AUTONOMO = 0.11               # simplificação didática do INSS


# ------------------------------------------------------------ geração
def _gerar(matricula, ger):
    """Deriva os dados personalizados do aluno a partir da matrícula.

    A **ordem dos sorteios** abaixo é parte do contrato: mudá-la muda os
    dados de toda a turma e invalida as assinaturas já emitidas. Se precisar
    alterar, suba ``VERSAO``.
    """
    nome, uf, categoria = _IDENTIDADES[
        core.indice_sem_colisao(matricula, len(_IDENTIDADES))
    ]

    # Exercício 1 — estoque
    estoque_minimo = ger.randrange(20, 200)
    estoque_atual = round(core.perturbar(estoque_minimo, ger, 0.8, minimo=0))

    # Exercício 2 — atendimento
    tempo_espera_min = ger.randrange(1, 40)
    chamado_vip = ger.random() < 0.3

    # Exercício 3 — avaliação de clientes
    nota_avaliacao = round(ger.uniform(1.0, 5.0), 1)

    # Exercício 4 — logística
    modal_entrega = ger.choice(list(_FRETE.keys()))
    valor_pedido = round(ger.uniform(25.0, 650.0), 2)

    # Exercício 5 — comitê de expansão
    faturamento_trimestre = round(ger.uniform(15_000.0, 160_000.0), 2)
    margem_liquida_media = round(ger.uniform(-5.0, 25.0), 1)
    endividamento_pct = round(ger.uniform(5.0, 85.0), 1)
    tem_sistema_gestao = ger.random() < 0.55
    contabilidade_em_dia = ger.random() < 0.70
    gerente_treinado = ger.random() < 0.45

    # Exercício 6 — caixa (chega como TEXTO de propósito)
    valor_caixa = round(ger.uniform(50.0, 5_000.0), 2)
    tipo_lancamento = ger.choice(["entrada", "saida"])
    quantidade_itens = ger.randrange(1, 500)

    # Exercício 7 — repasse a prestadores
    tipo_servico_plataforma = ger.choice(list(_COMISSOES_PLATAFORMA.keys()))
    regime_prestador = ger.choice(["autonomo", "mei"])
    valor_servico = round(ger.uniform(80.0, 4_000.0), 2)

    # Parte 1 — previsão (sempre em "pico de demanda": ver Passo 0)
    pedidos_hoje = ger.randrange(55, 141)

    return {
        "MEU_NEGOCIO": nome,
        "MINHA_UF": uf,
        "MINHA_CATEGORIA": categoria,
        "MEUS_PEDIDOS_HOJE": pedidos_hoje,
        "MEU_ESTOQUE_ATUAL": estoque_atual,
        "MEU_ESTOQUE_MINIMO": estoque_minimo,
        "MEU_TEMPO_ESPERA_MIN": tempo_espera_min,
        "MEU_CHAMADO_VIP": chamado_vip,
        "MINHA_NOTA_AVALIACAO": nota_avaliacao,
        "MEU_MODAL_ENTREGA": modal_entrega,
        "MEU_VALOR_PEDIDO": valor_pedido,
        "MEU_FATURAMENTO_TRIMESTRE": faturamento_trimestre,
        "MINHA_MARGEM_LIQUIDA_MEDIA": margem_liquida_media,
        "MEU_ENDIVIDAMENTO_PCT": endividamento_pct,
        "MEU_TEM_SISTEMA_GESTAO": tem_sistema_gestao,
        "MINHA_CONTABILIDADE_EM_DIA": contabilidade_em_dia,
        "MEU_GERENTE_TREINADO": gerente_treinado,
        "MEU_VALOR_CAIXA_TEXTO": f"{valor_caixa:.2f}",
        "MEU_TIPO_LANCAMENTO_TEXTO": tipo_lancamento,
        "MINHA_QUANTIDADE_ITENS_TEXTO": str(quantidade_itens),
        "MEU_TIPO_SERVICO_PLATAFORMA": tipo_servico_plataforma,
        "MEU_REGIME_PRESTADOR": regime_prestador,
        "MEU_VALOR_SERVICO": valor_servico,
    }


def _apresentar(d):
    """Imprime o briefing do fundador no Passo 0."""
    print(f"🚀  {d['MEU_NEGOCIO']} ({d['MINHA_UF']}) — {d['MINHA_CATEGORIA']}")
    print("    (mesmo negócio da Atividade 01 — números novos aqui)")
    print()
    print("📈  Parte 1 — carga do dia")
    print(f"    MEUS_PEDIDOS_HOJE ....... {d['MEUS_PEDIDOS_HOJE']} pedidos")
    print()
    print("📦  Exercício 1 — estoque")
    print(f"    MEU_ESTOQUE_ATUAL ....... {d['MEU_ESTOQUE_ATUAL']} un.")
    print(f"    MEU_ESTOQUE_MINIMO ...... {d['MEU_ESTOQUE_MINIMO']} un.")
    print()
    print("☎️  Exercício 2 — atendimento")
    print(f"    MEU_TEMPO_ESPERA_MIN .... {d['MEU_TEMPO_ESPERA_MIN']} min")
    print(f"    MEU_CHAMADO_VIP ......... {d['MEU_CHAMADO_VIP']}")
    print()
    print("⭐  Exercício 3 — avaliação de clientes")
    print(f"    MINHA_NOTA_AVALIACAO .... {d['MINHA_NOTA_AVALIACAO']} / 5.0")
    print()
    print("🛵  Exercício 4 — logística")
    print(f"    MEU_MODAL_ENTREGA ....... {d['MEU_MODAL_ENTREGA']}")
    print(f"    MEU_VALOR_PEDIDO ........ R$ {d['MEU_VALOR_PEDIDO']:.2f}")
    print()
    print("🏗️  Exercício 5 — comitê de expansão")
    print(f"    MEU_FATURAMENTO_TRIMESTRE  R$ {d['MEU_FATURAMENTO_TRIMESTRE']:.2f}")
    print(f"    MINHA_MARGEM_LIQUIDA_MEDIA {d['MINHA_MARGEM_LIQUIDA_MEDIA']}%")
    print(f"    MEU_ENDIVIDAMENTO_PCT ... {d['MEU_ENDIVIDAMENTO_PCT']}%")
    print(f"    MEU_TEM_SISTEMA_GESTAO .. {d['MEU_TEM_SISTEMA_GESTAO']}")
    print(f"    MINHA_CONTABILIDADE_EM_DIA {d['MINHA_CONTABILIDADE_EM_DIA']}")
    print(f"    MEU_GERENTE_TREINADO .... {d['MEU_GERENTE_TREINADO']}")
    print()
    print("💵  Exercício 6 — caixa (tudo TEXTO)")
    print(f"    MEU_VALOR_CAIXA_TEXTO ... {d['MEU_VALOR_CAIXA_TEXTO']!r}")
    print(f"    MEU_TIPO_LANCAMENTO_TEXTO {d['MEU_TIPO_LANCAMENTO_TEXTO']!r}")
    print(f"    MINHA_QUANTIDADE_ITENS_TEXTO {d['MINHA_QUANTIDADE_ITENS_TEXTO']!r}")
    print()
    print("🧾  Exercício 7 — repasse a prestadores")
    print(f"    MEU_TIPO_SERVICO_PLATAFORMA {d['MEU_TIPO_SERVICO_PLATAFORMA']}")
    print(f"    MEU_REGIME_PRESTADOR .... {d['MEU_REGIME_PRESTADOR']}")
    print(f"    MEU_VALOR_SERVICO ....... R$ {d['MEU_VALOR_SERVICO']:.2f}")


# ------------------------------------------------------------ as réguas
# Estas funções são a "resposta" do professor. Existem separadas das
# checagens para que a regra fique escrita uma vez só — e para que o
# gabarito e a conferência nunca divirjam.
def classificar_avaliacao(nota):
    if nota >= 4.5:
        return "🏆 Destaque — usar em marketing"
    if nota >= 4.0:
        return "😀 Positiva — sem ação"
    if nota >= 3.0:
        return "😐 Neutra — pedir feedback"
    return "🚨 Crítica — abrir plano de recuperação"


def frete_e_prazo(modal, valor_pedido):
    if modal not in _FRETE:
        raise ValueError(f"Modal desconhecido: {modal!r}")
    frete_base, prazo_dias, minimo_gratis = _FRETE[modal]
    frete_final = 0.0 if valor_pedido >= minimo_gratis else frete_base
    return frete_final, prazo_dias


def decisao_expansao(d):
    porte_ok = d["MEU_FATURAMENTO_TRIMESTRE"] >= CORTE_PORTE_EXPANSAO
    saude_ok = (
        d["MINHA_MARGEM_LIQUIDA_MEDIA"] > CORTE_MARGEM_EXPANSAO
        and d["MEU_ENDIVIDAMENTO_PCT"] <= CORTE_ENDIVIDAMENTO_EXPANSAO
    )
    praticas = (
        int(d["MEU_TEM_SISTEMA_GESTAO"])
        + int(d["MINHA_CONTABILIDADE_EM_DIA"])
        + int(d["MEU_GERENTE_TREINADO"])
    )
    if porte_ok and saude_ok and praticas >= PRATICAS_MINIMAS_EXPANSAO:
        decisao = "✅ ABRIR segunda unidade"
    else:
        decisao = "❌ ADIAR EXPANSÃO"
    return praticas, decisao


def comissao_e_repasse(tipo_servico, regime, valor_servico):
    if valor_servico <= 0:
        raise ValueError(f"Valor de serviço inválido: R$ {valor_servico:.2f}")
    if tipo_servico not in _COMISSOES_PLATAFORMA:
        raise ValueError(f"Tipo de serviço desconhecido: {tipo_servico!r}")
    comissao_pct = _COMISSOES_PLATAFORMA[tipo_servico]
    comissao_valor = valor_servico * comissao_pct
    valor_apos_comissao = valor_servico - comissao_valor
    if regime == "autonomo":
        retencao = valor_apos_comissao * RETENCAO_AUTONOMO
    elif regime == "mei":
        retencao = 0.0
    else:
        raise ValueError(f"Regime desconhecido: {regime!r}")
    valor_repasse = valor_apos_comissao - retencao
    return comissao_valor, retencao, valor_repasse


# ------------------------------------------------------------ checagens
def _checagens(etapa, r, d):
    """Monta a lista de checagens de uma etapa: ``[(ok, mensagem), ...]``."""

    if etapa == "exercicio-1":
        diferenca = d["MEU_ESTOQUE_ATUAL"] - d["MEU_ESTOQUE_MINIMO"]
        precisa_repor = d["MEU_ESTOQUE_ATUAL"] < d["MEU_ESTOQUE_MINIMO"]
        return [
            checar_numero(
                "diferenca", r.get("diferenca"), diferenca,
                "estoque atual − estoque mínimo (pode ser negativo).",
                tolerancia=0,
            ),
            checar_bool(
                "precisa_repor", r.get("precisa_repor"), precisa_repor,
                "compare MEU_ESTOQUE_ATUAL com MEU_ESTOQUE_MINIMO — sem if.",
            ),
        ]

    if etapa == "exercicio-2":
        escalar = (
            d["MEU_TEMPO_ESPERA_MIN"] > LIMITE_ESPERA_ESCALONAR
            or d["MEU_CHAMADO_VIP"]
        )
        fila = "🚨 Supervisor" if escalar else "💬 Atendente padrão"
        return [
            checar_bool(
                "escalar_supervisor", r.get("escalar_supervisor"), escalar,
                f"o limite é {LIMITE_ESPERA_ESCALONAR} min — mas um chamado "
                "VIP escala mesmo dentro do limite (é um `or`).",
            ),
            checar_igual(
                "fila_destino", r.get("fila_destino"), fila,
                "if/else sobre o escalar_supervisor que você acabou de calcular.",
            ),
        ]

    if etapa == "exercicio-3":
        classificacao = classificar_avaliacao(d["MINHA_NOTA_AVALIACAO"])
        return [
            checar_igual(
                "classificacao", r.get("classificacao"), classificacao,
                f"nota {d['MINHA_NOTA_AVALIACAO']} — releia os quatro cortes "
                "(4.5 / 4.0 / 3.0) na ORDEM em que aparecem no enunciado.",
            ),
        ]

    if etapa == "exercicio-4":
        frete_final, prazo_dias = frete_e_prazo(
            d["MEU_MODAL_ENTREGA"], d["MEU_VALOR_PEDIDO"]
        )
        return [
            checar_numero(
                "frete_final", r.get("frete_final"), frete_final,
                f"modal {d['MEU_MODAL_ENTREGA']!r}, pedido de "
                f"R$ {d['MEU_VALOR_PEDIDO']:.2f} — confira o mínimo de frete "
                "grátis DESSE modal, dentro do case certo.",
            ),
            checar_numero(
                "prazo_dias", r.get("prazo_dias"), prazo_dias,
                f"prazo do modal {d['MEU_MODAL_ENTREGA']!r}.", tolerancia=0,
            ),
        ]

    if etapa == "exercicio-5":
        praticas, decisao = decisao_expansao(d)
        return [
            checar_numero(
                "praticas_prontidao", r.get("praticas_prontidao"), praticas,
                "some os três bools de prontidão operacional com int(...).",
                tolerancia=0,
            ),
            checar_igual(
                "decisao_expansao", r.get("decisao_expansao"), decisao,
                f"porte ≥ R$ {CORTE_PORTE_EXPANSAO:.0f}? saúde OK (margem > "
                f"{CORTE_MARGEM_EXPANSAO}% e endividamento ≤ "
                f"{CORTE_ENDIVIDAMENTO_EXPANSAO}%)? prontidão "
                f"{praticas}/3 ≥ {PRATICAS_MINIMAS_EXPANSAO}? Os três filtros "
                "são aninhados — o segundo só é olhado se o primeiro passar.",
            ),
        ]

    if etapa == "exercicio-6":
        valor = float(d["MEU_VALOR_CAIXA_TEXTO"])
        quantidade = int(d["MINHA_QUANTIDADE_ITENS_TEXTO"])
        tipo = d["MEU_TIPO_LANCAMENTO_TEXTO"]
        valor_unitario = valor / quantidade
        sinal = 1 if tipo == "entrada" else -1
        impacto_caixa = valor * sinal
        return [
            checar_numero(
                "valor_unitario", r.get("valor_unitario"), valor_unitario,
                "valor do lançamento ÷ quantidade de itens.",
            ),
            checar_numero(
                "impacto_caixa", r.get("impacto_caixa"), impacto_caixa,
                f"MEU_TIPO_LANCAMENTO_TEXTO é {tipo!r} — entrada soma, saída "
                "subtrai do caixa.",
            ),
        ]

    if etapa == "exercicio-7":
        comissao_valor, retencao, valor_repasse = comissao_e_repasse(
            d["MEU_TIPO_SERVICO_PLATAFORMA"],
            d["MEU_REGIME_PRESTADOR"],
            d["MEU_VALOR_SERVICO"],
        )
        return [
            checar_numero(
                "comissao_valor", r.get("comissao_valor"), comissao_valor,
                f"tipo {d['MEU_TIPO_SERVICO_PLATAFORMA']!r} — confira a "
                "comissão-base no case certo.",
            ),
            checar_numero(
                "retencao", r.get("retencao"), retencao,
                f"regime {d['MEU_REGIME_PRESTADOR']!r} — só 'autonomo' retém "
                f"{RETENCAO_AUTONOMO*100:.0f}% sobre o valor após comissão.",
            ),
            checar_numero(
                "valor_repasse", r.get("valor_repasse"), valor_repasse,
                "valor do serviço − comissão − retenção.",
            ),
        ]

    return [(False, f"❓ etapa desconhecida: {etapa!r}")]


# ---------------------------------------------------------------- montagem
_KIT = core.Kit(
    atividade=ATIVIDADE,
    titulo="Atividade 02 — O Painel de Comando do Seu Negócio",
    versao=VERSAO,
    gerar_dados=_gerar,
    apresentar=_apresentar,
    checagens=_checagens,
)

iniciar = _KIT.iniciar
prever = _KIT.prever
registrar = _KIT.registrar
conferir = _KIT.conferir
diario = _KIT.diario
limpar_diario = _KIT.limpar_diario
assinatura = _KIT.assinatura
dados_de = _KIT.dados_de


def distribuicao(matriculas):
    """Mostra o negócio e os indicadores de cada matrícula da turma.

    Ferramenta **do professor**, não do aluno::

        from scripts.kit_a02 import distribuicao
        distribuicao(["20261234500", "20261234501", "20261234502"])

    ⚠️ Nunca versione a lista de matrículas: é dado pessoal do aluno e este
    repositório é público.
    """
    return _KIT.distribuicao(
        matriculas,
        colunas=[
            ("negócio", "MEU_NEGOCIO", "<18"),
            ("modal", "MEU_MODAL_ENTREGA", "<10"),
            ("nota aval.", "MINHA_NOTA_AVALIACAO", ">10.1f"),
            ("faturamento", "MEU_FATURAMENTO_TRIMESTRE", ">12.2f"),
            ("serviço", "MEU_TIPO_SERVICO_PLATAFORMA", "<10"),
            ("regime", "MEU_REGIME_PRESTADOR", "<10"),
        ],
    )
