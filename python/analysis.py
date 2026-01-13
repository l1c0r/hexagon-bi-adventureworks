import pandas as pd
import pyodbc

# -------------------------
# Conexão com SQL Server
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
    sp.StateProvinceID,
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

# -------------------------
# Carga dos dados
# -------------------------
df = pd.read_sql(query, conn)

# -------------------------
# Tratamento temporal
# -------------------------
df["OrderDate"] = pd.to_datetime(df["OrderDate"])
df["year"] = df["OrderDate"].dt.year
df["month"] = df["OrderDate"].dt.month

# -------------------------
# Parâmetros de filtro (simulação do usuário)
# -------------------------
start_date = "2012-01-01"
end_date = "2013-12-31"
selected_products = ["Road-650 Red, 44", "Road-650 Red, 52"]
selected_regions = ["Ontario", "Georgia"]

# -------------------------
# Aplicação dos filtros
# -------------------------
df_filtered = df[
    (df["OrderDate"] >= start_date) &
    (df["OrderDate"] <= end_date) &
    (df["ProductName"].isin(selected_products)) &
    (df["StateProvinceName"].isin(selected_regions))
]

# -------------------------
# Agregações
# -------------------------
sales_by_region = df_filtered.groupby("StateProvinceName", as_index=False).agg(total_sales=("SalesAmount", "sum"))
sales_by_product = df_filtered.groupby("ProductName", as_index=False).agg(total_sales=("SalesAmount", "sum"))
sales_by_time = df_filtered.groupby(["year", "month"], as_index=False).agg(total_sales=("SalesAmount", "sum"))

# -------------------------
# Debug mínimo
# -------------------------
print("Pipeline executado com sucesso")
print("Base original:", df.shape)
print("Base filtrada:", df_filtered.shape)
print(df_filtered.head())
