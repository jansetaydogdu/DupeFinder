import re
import sys
from bs4 import BeautifulSoup
import urllib.request
import urllib.error
import pandas as pd
import time

sys.path.append("../data")
import dataHandler

webHeader = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)' };
targetLink = "https://www.ewg.org/skindeep/browse/category/Personal_Care/";

def getHtml(strLink="www.google.com"):
    req = urllib.request.Request(strLink, headers=webHeader);
    try:
        response = urllib.request.urlopen(req);
        return response.read();
    except urllib.error.HTTPError as e:
        print(e.code, e.reason);
        return ""

def extractLinks( htmlPage ):
    linkOut = set();
    soup = BeautifulSoup(htmlPage, 'html.parser');
    for link in soup.find_all('a'):
        if re.search("/products/", str(link.get('href')) ):
            linkOut.add( link.get('href') );
    return linkOut;

def getLinks(intPageStart, intPageEnd):
    fp = open("links.txt", "w")
    for i in range(intPageStart, intPageEnd):
        currentLink = targetLink + "?category=Personal+Care&page="+str(i);
        print( f'Getting {i}/{intPageEnd-1}:\n{currentLink}\n' );
        currentHtml = getHtml(currentLink);
        targetLinks = extractLinks(currentHtml);
        for link in targetLinks:
            fp.write( str(link) + "\n" );

def extractIngredients( soup ):
    targetSection = soup.find( 'section', {"id": "label-information"} );
    if( targetSection ):
        ingredientsTag = targetSection.find("p");
        if( ingredientsTag ):
            ingredients = ingredientsTag.text;
            ingredients = ingredients.replace("Active ingr dient: ", "");
            ingredients = ingredients.replace("Inactive ingredients: ", "");
            ingredients = ingredients.replace(".\n", ", ");
            return ingredients.split(',');
    return [None];

def extractCategories( soup ):
    targetClass = soup.find( "div", {"class": "product-lower"} )
    if( targetClass ):
        categoryTag = targetClass.find("a");
        if(categoryTag):
            return categoryTag.text.replace("\n", "");

def extractName( soup ):
    if(soup.error):
        return;
    if(not soup.text):
        return;
    return soup.title.text.replace("EWG Skin Deep® | ", "");

def fillData( linkPath="links.txt", outPath = "../data.csv" ):
    open(outPath, "w")
    open("save.csv", "a");

    linkFile = open(linkPath, "r");
    dfOut = pd.read_csv("save.csv");
    saveIndex = dfOut.shape[0];

    if linkFile.closed:
        print(f"Couldn't open {linkPath}");
        linkFile.close();
        return;

    intCount = 0;
    for currentLink in linkFile:
        print(f"Processing {intCount}:\n{currentLink}\n");
        intCount+=1;
        if(saveIndex > intCount):
            continue;
        
        targetHtml = getHtml( currentLink );
        soup = BeautifulSoup(targetHtml, 'html.parser');
        
        ingredients = extractIngredients(soup);
        categories = extractCategories(soup);
        name = extractName(soup);

        currentProduct = dataHandler.Product(name, categories, ingredients).toDict();
        dfDictionary = pd.DataFrame( [currentProduct] )
        dfOut = pd.concat( [dfOut, dfDictionary], ignore_index=True );
        print(dfOut.shape);
        dfOut.to_csv("save.csv", index=False);
        time.sleep(1.5); # Ratelimit

    if dfOut.empty:
        print("WARNING: scraper.py, dfOut is empty");
        linkFile.close();
        return;

    dfOut.to_csv(outPath);
    linkFile.close();

def handleArgs(argc=0, argv=[]):
    strHelp = """
    args        :   Shows this help page
    getLinks #N :   Extract N page links into links.txt, DO NOT REPEATEDLY DO THIS.
    fillData    :   Parse through links.txt and fill the data.csv in ../../data 
    """
    
    match(argv[1]):
        case "args": print(strHelp);
        case "getLinks":
            try:
                if(argc < 3):
                    print("Please specify a number N");
                    return False;
                if(int(argv[2]) < 0): 
                    print("Invalid N");
                    return False;
                getLinks(1, int( argv[2])+1 );
                return True;
            except:
                print("Invalid input")
                return False;
        case "fillData":
            fillData();
            return True;
        case _:
            print("Unrecognized arg.");
            print("Please use 'python scraper.py args' to see available args");
            return False;

def scrape():
    argc = len(sys.argv);
    if(argc < 2 or argc > 3): 
        print("Usage: python scraper.py <arg>");
        print("Ex. python scraper.py args   :   Shows possible args")
        return;
    return handleArgs(argc, sys.argv);

scrape();
