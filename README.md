# Hexagon BI Case – AdventureWorks

## Objetivo
Construir uma aplicação de Business Intelligence utilizando dados do banco AdventureWorks, com extração via SQL Server, processamento em Python (Pandas) e visualização interativa com Streamlit.

---

## Stack Utilizada
- SQL Server Express (AdventureWorks2022 OLTP)
- Python 3
- Pandas
- pyodbc
- Streamlit
- VS Code

---

## Etapas Executadas

### 1. Conexão com SQL Server
- Restauração do banco AdventureWorks2022 (OLTP)
- Conexão local via `.\\SQLEXPRESS`

### 2. Extração de Dados (SQL)
Consulta utilizando:
- `Sales.SalesOrderHeader`
- `Sales.SalesOrderDetail`
- `Production.Product`
- `Person.Address`
- `Person.StateProvince`

Campos extraídos:
- Data do pedido (OrderDate)
- Valor de venda (LineTotal)
- Produto
- Região

> O campo `TotalDue` não foi utilizado para evitar dupla contagem, garantindo granularidade por item vendido.

---

### 3. Processamento com Pandas
- Carga dos dados via `pyodbc`
- Conversão de datas
- Criação de colunas temporais (ano e mês)
- Base com aproximadamente 121 mil registros

---

### 4. Agregações
- Vendas totais por região
- Vendas totais por produto
- Vendas totais por período (ano/mês)

---

### 5. Filtros Dinâmicos
Implementados via Streamlit:
- Intervalo de datas
- Seleção de produtos
- Seleção de regiões

> Os filtros atuam diretamente sobre a base carregada em Pandas.

---

### 6. Visualização
- Gráfico de barras: vendas por região
- Gráfico de barras: vendas por produto
- Gráfico de linha: vendas ao longo do tempo

---

## Execução do Projeto

1. Instalar dependências:
```bash
pip install pandas pyodbc streamlit

2. Executar a aplicação:
```bash

# Forma padrão
streamlit run app.py

# Alternativa que funcionou em Windows/PowerShell
python -m streamlit run app.py

## Prints do Projeto
![Dashboard Page 1](images/streamlit_print (1).png)
![Dashboard Page 2](images/streamlit_print (2).png)
![Dashboard Page 3](images/streamlit_print (3).png)