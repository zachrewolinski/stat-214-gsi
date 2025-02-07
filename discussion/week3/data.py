import pandas as pd
import numpy as np

def load_gapminder_data(path="data/", filename="gapminder-FiveYearData.csv") -> pd.DataFrame:
    """
    A function to load the gapminder data from a CSV file.
    
    Arguments:
    path: The folder path where the CSV file is located.
    filename: The name of the CSV file.
    
    Returns:
    A DataFrame corresponding to the gapminder data.
    """
    # Extract the file path
    file_path = f"{path}{filename}"
    # Load the gapminder data
    gapminder = pd.read_csv(file_path)
    # Return the loaded data
    return gapminder

def load_percept_data(path="data/", filename="probly.csv") -> pd.DataFrame:
    """
    A function to load the perceptions data from a CSV file.
    
    Arguments:
    path: The folder path where the CSV file is located.
    filename: The name of the CSV file.
    
    Returns:
    A DataFrame corresponding to the perceptions data.
    """
    # Extract the file path
    file_path = f"{path}{filename}"
    # Load the perceptions data
    percept = pd.read_csv(file_path)
    # Return the loaded data
    return percept

def clean_gapminder_data(gapminder_data: pd.DataFrame) -> pd.DataFrame:
    """
    A function to clean the gapminder data.
    
    Arguments:
    gapminder_data: A DataFrame in the format of the output of the loadGapminderData() function
    
    Returns:
    A DataFrame similar to the input `gapminder_data` but with cleaned variable names
    """
    gapminder_data = gapminder_data.rename(columns={
        'lifeExp': 'life_exp',
        'gdpPercap': 'gdp_per_cap',
        'pop': 'population'
    })
    return gapminder_data

def clean_probly_data(probly_orig: pd.DataFrame) -> pd.DataFrame:
    """
    A function to clean the perception probability data.
    
    Arguments:
    probly_orig: A DataFrame in the format of the output of the loadPerceptData(filename = "probly.csv") function
    
    Returns:
    A DataFrame similar to the input `probly_orig` but with cleaned variable names
    """
    # Convert from wide to long format
    probly = probly_orig.reset_index().melt(id_vars='index', var_name='phrase', value_name='prob')
    probly.rename(columns={'index': 'id'}, inplace=True)
    
    # Replace dots with spaces
    probly['phrase'] = probly['phrase'].str.replace('.', ' ', regex=False)
    
    # Convert prob to percentage
    probly['prob'] = probly['prob'] / 100
    
    # Convert id to category
    probly['id'] = probly['id'].astype('category')
    
    # Order phrases
    phrase_order = [
        "Chances Are Slight", "Highly Unlikely", "Almost No Chance", "Little Chance",
        "Probably Not", "Unlikely", "Improbable", "We Doubt", "About Even",
        "Better Than Even", "Probably", "We Believe", "Likely", "Probable",
        "Very Good Chance", "Highly Likely", "Almost Certainly"
    ]
    probly['phrase'] = pd.Categorical(probly['phrase'], categories=phrase_order, ordered=True)
    
    return probly

def clean_numberly_data(numberly_orig: pd.DataFrame) -> pd.DataFrame:
    """
    A function to clean the perception number data.
    
    Arguments:
    numberly_orig: A DataFrame in the format of the output of the loadPerceptData(filename = "numberly.csv") function
    
    Returns:
    A DataFrame similar to the input `numberly_orig` but with cleaned variable names
    """
    # Convert from wide to long format
    numberly = numberly_orig.reset_index().melt(id_vars='index', var_name='phrase', value_name='number')
    numberly.rename(columns={'index': 'id'}, inplace=True)
    
    # Replace dots with spaces
    numberly['phrase'] = numberly['phrase'].str.replace('.', ' ', regex=False)
    
    # Convert id to category
    numberly['id'] = numberly['id'].astype('category')
    
    # Order phrases
    phrase_order = [
        "Hundreds of", "Scores of", "Dozens", "Many", "A lot", "Several",
        "Some", "A few", "A couple", "Fractions of"
    ]
    numberly['phrase'] = pd.Categorical(numberly['phrase'], categories=phrase_order, ordered=True)
    
    return numberly