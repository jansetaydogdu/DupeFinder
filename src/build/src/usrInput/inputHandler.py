import pandas

manual = {
        "search":
        f"""
        search <optional:Category> <Ingredients>
        'python dupeFinderCli.py search Toothpaste water glycerin': 
        Search and list Toothpaste in order of matching to ingredients water and glycerin
        """,

        "searchToCsv":
        f"""
        searchToCsv <optional:Category> <Ingredients>
        'python dupeFinderCli searchToCsv "Toothpaste, water, glycerin":
        Search Toothpaste in order of matching ingredients to water and glycerin, then write results to output.csv
        """,

        "updateLists":
        """
        updateLists <optional:outputPath>
        'python dupeFinderCli.py updateLists':
        Update the lists that contain and manage available Ingredients and whatnot. For contributors mostly.
        If an outputPath is not given it will write the list to default reading path lists/lists.txt. 
        """,

        "help":
        f"""
        help <optional:arg>
        'python dupeFinderCli.py help':
        Displays the help page
        If an arg is given it tell you how to use that arg.
        """,
};

def getAvailableCategories(df_products):
    return df_products.Category.unique();

def getAvailableIngredients(df_products):
    outSet = set();
    for ingredients in df_products.Ingredients:
        listIngredients = str(ingredients).split("  ");
        for ingredient in listIngredients:
            outSet.add( ingredient );
    return outSet;
def invalidInput(msg):
    print(msg);
    exit(1);

def help(argc, argv):
    helpPage = f"""
        Cli version of dupeFinder to use from commandline.
        Usage:      python dupeFinderCli.py <arg>
        Example:    python dupeFinderCli.py search "Toothpaste, water, glycerin"
        
        Valid args: help, search, searchToCsv, updateLists
                        'python dupeFinderCli.py help <arg> for info about a given arg'
    """

    if(argc <= 2): 
        print(helpPage);
    elif(argc < 4):
        print( manual.get(argv[2]) if argv[2] in manual else f"Unkown arg {argv[2]}");
    else: invalidInput("Can't display multiple help pages at the same time");

