USE AdventureWorks2022;
GO
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
