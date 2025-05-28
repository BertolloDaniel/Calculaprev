# Arquivo: app_aposentadoria_carlos.py

import streamlit as st
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np

# Funções auxiliares
def calcular_idade(nascimento, referencia):
    return referencia.year - nascimento.year - ((referencia.month, referencia.day) < (nascimento.month, nascimento.day))

def calcular_valores(saldo, saque_pct, beneficio_pct):
    valor_saque = saldo * saque_pct / 100
    saldo_restante = saldo - valor_saque
    beneficio_mensal = saldo_restante * beneficio_pct / 100
    return valor_saque, beneficio_mensal, saldo_restante

def verificar_margem(beneficio_mensal, parcela_emprestimo):
    margem = beneficio_mensal * 0.30
    return parcela_emprestimo <= margem, margem

def simular_investimento(saldo, taxa_juros_anual, anos):
    return saldo * ((1 + taxa_juros_anual) ** anos)

def calcular_ir(valor, regime):
    if regime == "Regressivo":
        return valor * 0.10
    else:
        if valor <= 2112:
            return 0
        elif valor <= 2826.65:
            return valor * 0.075
        elif valor <= 3751.05:
            return valor * 0.15
        elif valor <= 4664.68:
            return valor * 0.225
        else:
            return valor * 0.275

# Título do App
st.title("Simulador de Aposentadoria - Caso Carlos")

# Dados fixos do caso Carlos
data_nascimento = datetime.strptime("1969-09-04", "%Y-%m-%d")
data_saida = datetime.strptime("2025-01-15", "%Y-%m-%d")

# Entradas do usuário
saldo_total = st.number_input("Saldo acumulado (R$)", value=3833803.91)
emprestimo_mensal = st.number_input("Parcela de empréstimo (R$)", value=7399.62)
percentual_saque = st.slider("Percentual de saque (%)", 0, 100, 25)
percentual_beneficio = st.slider("Percentual de benefício mensal (%)", 0.1, 3.0, 1.4, step=0.1)
regime_tributario = st.radio("Regime de tributação", ["Progressivo", "Regressivo"])

# Cálculos principais
idade = calcular_idade(data_nascimento, data_saida)
elegivel = idade >= 50

valor_saque, beneficio_mensal, saldo_restante = calcular_valores(
    saldo_total, percentual_saque, percentual_beneficio
)

emprestimo_ok, margem_emprestimo = verificar_margem(beneficio_mensal, emprestimo_mensal)

# Resultados
st.subheader("1. Elegibilidade")
st.write(f"Idade na data de saída: {idade} anos")
if elegivel:
    st.success("Carlos é elegível ao benefício de aposentadoria.")
else:
    st.error("Carlos não é elegível ao benefício.")

st.subheader("2. Simulação de Saque e Benefício")
st.write(f"Saque ({percentual_saque}%): R$ {valor_saque:,.2f}")
st.write(f"Saldo remanescente: R$ {saldo_restante:,.2f}")
st.write(f"Benefício mensal: R$ {beneficio_mensal:,.2f}")

st.subheader("3. Empréstimo e Margem de Desconto")
st.write(f"Parcela do empréstimo: R$ {emprestimo_mensal:,.2f}")
st.write(f"Margem permitida (30%): R$ {margem_emprestimo:,.2f}")
if emprestimo_ok:
    st.success("Parcela está dentro da margem permitida.")
else:
    st.error("Parcela excede a margem permitida. Avaliar opções de amortização.")

st.subheader("4. Simulação: Manter Saldo Investido")
taxa_juros_anual = st.slider("Taxa de retorno anual estimada (%)", 0.0, 15.0, 6.0, step=0.5) / 100
anos_investimento = st.slider("Período de investimento (anos)", 1, 30, 5)
saldo_futuro = simular_investimento(saldo_total, taxa_juros_anual, anos_investimento)
st.write(f"Saldo projetado após {anos_investimento} anos: R$ {saldo_futuro:,.2f}")
