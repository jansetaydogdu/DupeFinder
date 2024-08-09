import sqlite3 as SQL
import pandas as pd

class Product:
    def __init__(self, strName, strCategory, listIngredients):
        self.name = strName;
        self.category = strCategory;
        self.ingredients=listIngredients;

    def toDict(self):
        if(self.name == "" or self.category == "" or len(self.ingredients) <= 0):
            return;
        return {
            "Product": self.name,
            "Category": self.category,
            "Ingredients": " ".join( self.ingredients )
        };

def initSql(csvPath="data.csv", dbPath = "products.db"):
    sqlConnection = SQL.connect(dbPath);
    
    dfProduct = pd.read_csv(csvPath, index_col=False);
    dfProduct.to_sql('products', sqlConnection, index=False, if_exists='replace');

    sqlConnection.commit();
    sqlConnection.close();

def filter(Category=[], ingredients=[], dbPath = "products.db"):
    sqlConnection = SQL.connect(dbPath);

    
    sqlMatchFunction = "";
    ingredientQuery = "";
    categoryQuery = "";

    if(len(Category) <= 0): Category.append('');
    if(len(ingredients) <= 0): ingredients.append('');
    
    for i in ingredients:
        sqlMatchFunction += f"SUM(CASE WHEN Ingredients LIKE '%{i}%' THEN 1 ELSE 0 END) + "
        ingredientQuery += f"Ingredients LIKE '%{i}%' OR "
    for i in Category:
        categoryQuery += f"\n\t    OR Category LIKE '%{i}%'"

    sqlMatchFunction = sqlMatchFunction[:-3]
    ingredientQuery = ingredientQuery[:-4]

    userQuery = f"""
        SELECT Product, Ingredients, Category
        FROM products
        WHERE Category LIKE '%{Category[0]}%'
        AND (True)
        GROUP BY Product
    """;

    if(len(ingredients) > 0):
        userQuery = f"""
            SELECT Product, Category, Ingredients, {sqlMatchFunction} as MatchScore
            FROM products
            WHERE Category LIKE '%{Category[0]}%'
            AND ({ingredientQuery})
            GROUP BY Product
            ORDER BY MatchScore DESC
        """;
    
    if(len(Category) > 1):
        queryUpper = userQuery[:userQuery.find("AND")];
        queryLower = userQuery[userQuery.find("AND"):];
        userQuery = queryUpper + f"{categoryQuery}\n\t    " + queryLower;


    dfResult = pd.read_sql_query(userQuery, sqlConnection);
    sqlConnection.close();

    return dfResult;
