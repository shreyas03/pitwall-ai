import requests
import pandas as pd

BASE_URL = "https://api.jolpi.ca/ergast/f1"

def get_historical_driver_standings(year: int) -> str:
    """Fetches finalized driver standings for a specific historical season."""
    url = f"{BASE_URL}/{year}/driverStandings.json"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        # Parse the highly nested JSON response
        standings = data['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings']
        
        # Use pandas to flatten and format the data
        df = pd.json_normalize(standings)
        
        # Extract the constructor name
        df['Constructor'] = df['Constructors'].apply(lambda x: x[0]['name'] if x else 'Unknown')
        
        # Keep only the columns the AI will need
        clean_df = df[['position', 'points', 'wins', 'Driver.givenName', 'Driver.familyName', 'Constructor']]
        clean_df.columns = ['Position', 'Points', 'Wins', 'First Name', 'Last Name', 'Team']
        
        return clean_df.to_string(index=False)
        
    except Exception as e:
        return f"Error fetching {year} F1 standings: {str(e)}"

def get_historical_constructor_standings(year: int) -> str:
    """Fetches finalized constructor (team) standings for a specific historical year."""
    url = f"{BASE_URL}/{year}/constructorStandings.json"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        standings = data['MRData']['StandingsTable']['StandingsLists'][0]['ConstructorStandings']
        df = pd.json_normalize(standings)
        
        # Keep only the team data
        clean_df = df[['position', 'points', 'wins', 'Constructor.name']]
        clean_df.columns = ['Position', 'Points', 'Wins', 'Team']
        
        return clean_df.to_string(index=False)
        
    except Exception as e:
        return f"Error fetching {year} constructor standings: {str(e)}"