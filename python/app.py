import pandas as pd
import pyodbc
import streamlit as st

st.set_page_config(page_title="Hexagon BI – AdventureWorks", layout="wide")
st.title("Sales Analysis – AdventureWorks")

# -------------------------
# Conexão SQL Server
# -------------------------
conn = pyodbc.connect(
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=.\\SQLEXPRESS;"
    "Database=AdventureWorks2022;"
    "Trusted_Connection=yes;"
)

# -------------------------
# Query SQL
# -------------------------
query = """
SELECT
    soh.OrderDate,
    sod.LineTotal AS SalesAmount,
    p.Name AS ProductName,
    sp.Name AS StateProvinceName
FROM Sales.SalesOrderHeader AS soh
INNER JOIN Sales.SalesOrderDetail AS sod
    ON soh.SalesOrderID = sod.SalesOrderID
INNER JOIN Production.Product AS p
    ON sod.ProductID = p.ProductID
INNER JOIN Person.Address AS a
    ON soh.ShipToAddressID = a.AddressID
INNER JOIN Person.StateProvince AS sp
    ON a.StateProvinceID = sp.StateProvinceID;
"""

df = pd.read_sql(query, conn)

# -------------------------
# Tratamento temporal
# -------------------------
df["OrderDate"] = pd.to_datetime(df["OrderDate"])
df["year"] = df["OrderDate"].dt.year
df["month"] = df["OrderDate"].dt.month
df["YearMonth"] = df["OrderDate"].dt.to_period("M").astype(str)  # coluna única para gráfico

# -------------------------
# Filtros no sidebar
# -------------------------
st.sidebar.header("Filtros")

min_date = df["OrderDate"].min()
max_date = df["OrderDate"].max()

date_range = st.sidebar.date_input(
    "Período",
    [min_date, max_date],
    min_value=min_date,
    max_value=max_date
)

products = st.sidebar.multiselect(
    "Produto",
    sorted(df["ProductName"].unique())
)

regions = st.sidebar.multiselect(
    "Região",
    sorted(df["StateProvinceName"].unique())
)

df_filtered = df.copy()

if date_range:
    df_filtered = df_filtered[
        (df_filtered["OrderDate"] >= pd.to_datetime(date_range[0])) &
        (df_filtered["OrderDate"] <= pd.to_datetime(date_range[1]))
    ]

if products:
    df_filtered = df_filtered[df_filtered["ProductName"].isin(products)]

if regions:
    df_filtered = df_filtered[df_filtered["StateProvinceName"].isin(regions)]

# -------------------------
# Debug mínimo
# -------------------------
st.write("Base filtrada (primeiros 5 registros):")
st.write(df_filtered.head())
st.write("Número de registros após filtros:", df_filtered.shape[0])

# -------------------------
# Agregações
# -------------------------
sales_by_region = df_filtered.groupby("StateProvinceName", as_index=False).agg(total_sales=("SalesAmount", "sum"))
sales_by_product = df_filtered.groupby("ProductName", as_index=False).agg(total_sales=("SalesAmount", "sum"))
sales_by_time = df_filtered.groupby("YearMonth", as_index=False).agg(total_sales=("SalesAmount", "sum"))

# -------------------------
# Visualizações
# -------------------------
st.subheader("Vendas Totais por Região")
if not sales_by_region.empty:
    st.bar_chart(sales_by_region.set_index("StateProvinceName"))
else:
    st.info("Sem dados para exibir por Região.")

st.subheader("Vendas Totais por Produto")
if not sales_by_product.empty:
    st.bar_chart(sales_by_product.set_index("ProductName"))
else:
    st.info("Sem dados para exibir por Produto.")

st.subheader("Vendas ao Longo do Tempo")
if not sales_by_time.empty:
    st.line_chart(sales_by_time.set_index("YearMonth"))
else:
    st.info("Sem dados para exibir ao Longo do Tempo.")
