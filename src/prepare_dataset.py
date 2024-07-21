import logging
import pandas as pd
logger = logging.getLogger(__name__);

#Prepare dataset by detect and remove unnecesary or invalid indices and columns etc. 
def prepare(df_target = pd.DataFrame(), unnecesary_cols = []):
    logger.info("Function Started");
    df_target.drop(columns = unnecesary_cols);
    #TODO: Add default unnecesary_cols and add more preperation
    logger.info("Function Ended");

