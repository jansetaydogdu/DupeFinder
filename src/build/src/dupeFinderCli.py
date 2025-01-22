import sys;
import pandas as pd;
import numpy as np;
from data import dataHandler;
from usrInput import inputHandler;

df_products = pd.read_csv("../src/data/data.csv"); 

# mathemathical "sets" containing available ingredients and categories.
setAvailableProducts = np.load('../src/lists/products.npy', allow_pickle=True);
setAvailableCategories = np.load('../src/lists/categories.npy', allow_pickle=True); 
setAvailableIngredients = np.load('../src/lists/ingredients.npy', allow_pickle=True);

def updateList(listPath = '../src/lists'):
    setAvailableCategories = inputHandler.getAvailableCategories(df_products); 
    setAvailableIngredients = inputHandler.getAvailableIngredients(df_products);
    setAvailableProducts = df_products['Product'].unique();
    np.save( listPath+'/'+'products.npy', setAvailableProducts );
    np.save( listPath+'/'+'categories.npy', setAvailableCategories );
    np.save( listPath+'/'+'ingredients.npy', setAvailableIngredients );

def writeLists(listPath = '../src/lists'):
    with open( (listPath+'/'+'products.txt') , "w") as f:
        for product in setAvailableProducts: 
            f.write( str(product) + "\n" );
    with open( (listPath+'/'+'categories.txt') , "w" ) as f:
        for category in setAvailableCategories: 
            f.write( str(category) + "\n" );
    with open( (listPath+'/'+'ingredients.txt') , "w" ) as f: 
        f.write( str(setAvailableIngredients) + "\n" );

def search(argc, argv):
    dataHandler.initSql("../src/data/data.csv", dbPath = '../src/data/products.db');
    if(argc < 3): 
        inputHandler.invalidInput("Use 'python dupeFinderCli.py help search' for help");

    searchParams = argv[2:];
    searchCategories = [];
    searchIngredients = [];
    for param in searchParams:
        found = False;
        for categoryName in setAvailableCategories:
            if( param.lower() in str(categoryName).lower() ):
                searchCategories.append(param);
                found = True;
                break;

        if(found): continue;
        for ingredientName in setAvailableIngredients.tolist():
            if( len(ingredientName) <= 0 ): continue;
            if( param.lower() in str(ingredientName).lower() ):
                searchIngredients.append(param);
                found = True;
                break;

        if(not found): 
            print(f"Warning. {param} not found. Looking directly into db instead")

    if( len(searchCategories) <= 0 ): searchCategories.append("");
    results = dataHandler.filter(searchCategories, searchIngredients, '../src/data/products.db');
    return results.head(100);

def main(argc = len(sys.argv), argv = sys.argv):
    if(argc <= 1): argv = ["dupeFinderCli.py", "help"];

    match(argv[1]):
        case "help": inputHandler.help(argc, argv);
        case "search": print( search(argc, argv) );
        case "searchToCsv": search(argc, argv).to_csv("../src/data/searchResults.csv", index=False, header=False);
        case "updateList": updateList() if argc < 3 else updateList(argv[2]);
        case _: inputHandler.invalidInput(f" Unkown arg '{argv[1]}' ");

    return 0;

if __name__ == "__main__":
    main();
