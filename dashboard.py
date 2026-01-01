import streamlit as st
import pandas as pd
import plotly.express as px
import asyncio
import httpx

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Móveis ERP - Business Intelligence",
    page_icon="📊",
    layout="wide"
)

# URL base da API
API_URL = "http://web_fastapi:8001/api/v1/analytics"

st.title("📊 Painel de Controlo de Vendas - BI (Async)")
st.markdown("---")

# --- FUNÇÃO ASSÍNCRONA PARA CARREGAR DADOS ---
async def get_data_async(client: httpx.AsyncClient, endpoint: str):
    """Realiza chamadas HTTP assíncronas à API."""
    try:
        response = await client.get(f"{API_URL}/{endpoint}", timeout=10)
        if response.status_code == 200:
            return response.json()
        return None
    except Exception:
        return None

async def load_all_dashboard_data():
    """Executa todas as chamadas de API em paralelo."""
    async with httpx.AsyncClient() as client:
        tasks = [
            get_data_async(client, "kpis"),
            get_data_async(client, "sales-by-category"),
            get_data_async(client, "top-customers"),
            get_data_async(client, "manufacturer-ranking"),
            get_data_async(client, "low-stock-report")
        ]
        # O gather faz com que as 5 chamadas ocorram ao mesmo tempo
        return await asyncio.gather(*tasks)

# --- EXECUÇÃO E MAPEAMENTO DOS DADOS ---
# Rodamos o loop assíncrono dentro do Streamlit
try:
    results = asyncio.run(load_all_dashboard_data())
    kpis, cat_data, cust_data, fab_data, stock_data = results
except Exception as e:
    st.error(f"Erro crítico ao conectar com a API: {e}")
    st.stop()

# --- BLOCO 1: KPI CARDS ---
if kpis:
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(
            label="Faturamento Total",
            value=f"R$ {kpis.get('total_revenue', 0):,.2f}",
            delta=f"R$ {kpis.get('revenue_delta', 0):,.2f}"
        )
    with col2:
        st.metric(label="Total de Vendas", value=kpis.get('total_orders', 0), delta=kpis.get('orders_delta', 0))
    with col3:
        st.metric(
            label="Ticket Médio",
            value=f"R$ {kpis.get('average_ticket', 0):,.2f}",
            delta=f"R$ {kpis.get('ticket_delta', 0):,.2f}"
        )
else:
    st.error("⚠️ Não foi possível carregar os KPIs principais.")

st.markdown("---")

# --- BLOCO 2: ANÁLISE DE VENDAS E CLIENTES ---
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("🍕 Vendas por Categoria")
    if cat_data:
        df_cat = pd.DataFrame(cat_data)
        if not df_cat.empty:
            fig_pie = px.pie(df_cat, values='total_sold', names='category', hole=0.3)
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.info("Sem dados de categorias.")
    else:
        st.warning("Erro ao carregar categorias.")

with col_right:
    st.subheader("🏆 Top 5 Clientes (Faturamento)")
    if cust_data:
        df_cust = pd.DataFrame(cust_data)
        if not df_cust.empty:
            fig_bar = px.bar(
                df_cust.head(5), x='customer_name', y='total_spent',
                color='total_spent', labels={'total_spent': 'R$', 'customer_name': 'Cliente'}
            )
            st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.warning("Erro ao carregar clientes.")

st.markdown("---")

# --- BLOCO 3: FABRICANTES E STOCK ---
col_inf_left, col_inf_right = st.columns(2)

with col_inf_left:
    st.subheader("🏢 Ranking de Fabricantes")
    if fab_data:
        st.dataframe(pd.DataFrame(fab_data), use_container_width=True, hide_index=True)
    else:
        st.info("Erro ao carregar fabricantes.")

with col_inf_right:
    st.subheader("⚠️ Alerta: Stock Baixo")
    if stock_data:
        df_stock = pd.DataFrame(stock_data)
        if not df_stock.empty:
            st.table(df_stock[['name', 'stock_quantity']].rename(columns={'name': 'Produto', 'stock_quantity': 'Qtd'}))
        else:
            st.success("✅ Stock em níveis normais.")