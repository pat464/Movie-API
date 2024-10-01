import json
import requests
from fastapi import FastAPI, HTTPException

# Initialize FastAPI app
app = FastAPI()

# Load JSON data with movies
with open("data.json", "r") as file:
    movies_data = json.load(file)

# OMDB API key (replace 'your_api_key' with the actual API key)
OMDB_API_KEY = "http://www.omdbapi.com/?i=tt3896198&apikey=a5475264"
OMDB_API_URL = "http://www.omdbapi.com/"

# Search for a movie in the JSON data and fetch additional details from OMDB API
def search_movie_api(title: str):
    # Query OMDB API for the movie title
    response = requests.get(OMDB_API_URL, params={"t": title, "apikey": OMDB_API_KEY})

    # If the API call fails or movie is not found, raise an error
    if response.status_code != 200 or response.json().get("Response") == "False":
        raise HTTPException(status_code=404, detail=f"Movie '{title}' not found in external API.")

    # Return movie data from the API
    return response.json()

@app.get("/movies/{title}")
def get_movie_details(title: str):
    """
    Get detailed movie information for a specific title from the local JSON file and OMDB API.
    """
    # Search for the movie in the local JSON file
    matching_movie = next((movie for movie in movies_data if movie["title"].lower() == title.lower()), None)
    
    if not matching_movie:
        raise HTTPException(status_code=404, detail=f"Movie '{title}' not found in the local database.")

    # Fetch additional details from the OMDB API
    movie_details = search_movie_api(title)

    # Combine local JSON data with additional details from the OMDB API
    result = {
        "local_data": matching_movie,
        "omdb_data": movie_details
    }
    return result

@app.get("/search/")
def search_movies(query: str):
    """
    Search for movies by title within the local JSON data.
    """
    # Filter the movies based on the search query
    results = [movie for movie in movies_data if query.lower() in movie["title"].lower()]

    if not results:
        raise HTTPException(status_code=404, detail=f"No movies found matching '{query}'.")

    # Return the filtered movies
    return {"results": results}

