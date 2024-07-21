import pandas as pd
import logging

LOGFORMAT = '%(levelname)-2s\tTime:%(asctime)s\tFunction:%(funcName)-10s\t%(message)s'
logger = logging.getLogger(__name__)
logging.basicConfig(filename='logs/logs.txt', level=logging.INFO, format=LOGFORMAT);



def main():
    logger.info("PROGRAM STARTED")

    df_ingredients = pd.read_csv("datasets/ingredients.csv");
    print("Columns:\n", df_ingredients.columns, "\n\n");
    
    print("Column examples:\t")
    for col in df_ingredients.columns:
        print(f"{col:<35}\t{df_ingredients[col][0]}");
    print("\nDataset head:\n", df_ingredients.head());

    logger.info("PROGRAM ENDED\n")


main()



