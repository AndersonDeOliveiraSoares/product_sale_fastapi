import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Móveis ERP - Business Intelligence",
    page_icon="📊",
    layout="wide"
)

# URL base da API (web_fastapi é o nome do serviço no Docker)
API_URL = "http://web_fastapi:8001/api/v1/analytics"

st.title("📊 Painel de Controlo de Vendas - BI")
st.markdown("---")


# --- FUNÇÃO AUXILIAR PARA CARREGAR DADOS ---
def get_data(endpoint):
    try:
        response = requests.get(f"{API_URL}/{endpoint}", timeout=5)
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        # Silenciamos o erro visual para não poluir o dashboard,
        # mas mantemos o log interno
        return None


# --- BLOCO 1: KPI CARDS (DINÂMICOS E SEGUROS) ---
kpis = get_data("kpis")

if kpis:
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            label="Faturamento Total",
            value=f"R$ {kpis.get('total_revenue', 0):,.2f}",
            delta=f"R$ {kpis.get('revenue_delta', 0):,.2f}"
        )
    with col2:
        st.metric(
            label="Total de Vendas",
            value=kpis.get('total_orders', 0),
            delta=kpis.get('orders_delta', 0)
        )
    with col3:
        st.metric(
            label="Ticket Médio",
            value=f"R$ {kpis.get('average_ticket', 0):,.2f}",
            delta=f"R$ {kpis.get('ticket_delta', 0):,.2f}"
        )
else:
    st.error("⚠️ Não foi possível carregar os KPIs principais. Verifique a conexão com a API.")

st.markdown("---")

# --- BLOCO 2: ANÁLISE DE VENDAS E CLIENTES ---
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("🍕 Vendas por Categoria")
    cat_data = get_data("sales-by-category")
    if cat_data:
        df_cat = pd.DataFrame(cat_data)
        if not df_cat.empty:
            fig_pizza = px.pie(df_cat, values='total_sold', names='category', hole=0.3)
            st.plotly_chart(fig_pizza, use_container_width=True)
        else:
            st.info("Sem dados de categorias para exibir.")
    else:
        st.warning("Aguardando dados de categorias...")

with col_right:
    st.subheader("🏆 Top 5 Clientes (Faturamento)")
    cust_data = get_data("top-customers")
    if cust_data:
        df_cust = pd.DataFrame(cust_data)
        if not df_cust.empty:
            fig_bar = px.bar(
                df_cust.head(5),
                x='customer_name',
                y='total_spent',
                color='total_spent',
                labels={'total_spent': 'Total Gasto (R$)', 'customer_name': 'Cliente'}
            )
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.info("Sem dados de clientes para exibir.")
    else:
        st.warning("Aguardando dados de clientes...")

st.markdown("---")

# --- BLOCO 3: FABRICANTES E STOCK ---
col_inf_left, col_inf_right = st.columns(2)

with col_inf_left:
    st.subheader("🏢 Ranking de Fabricantes")
    fab_data = get_data("manufacturer-ranking")
    if fab_data:
        df_fab = pd.DataFrame(fab_data)
        st.dataframe(df_fab, use_container_width=True, hide_index=True)
    else:
        st.info("Carregando ranking de fabricantes...")

with col_inf_right:
    st.subheader("⚠️ Alerta: Stock Baixo")
    stock_data = get_data("low-stock-report")
    if stock_data:
        df_stock = pd.DataFrame(stock_data)
        if not df_stock.empty:
            st.table(df_stock[['name', 'stock_quantity']].rename(columns={'name': 'Produto', 'stock_quantity': 'Qtd'}))
        else:
            st.success("✅ Todo o stock está em níveis normais.")
    else:
        st.info("Carregando relatório de stock...")