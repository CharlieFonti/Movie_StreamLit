import streamlit as st
import requests
import datetime
import matplotlib
matplotlib.use("agg") 
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd





api_key = "14e9eb80a218ca240f9e72fd0bfe2c64"


def search_movies(query):
    base_url = "https://api.themoviedb.org/3/search/movie"
    params = {"api_key": api_key, "query": query}

    response = requests.get(base_url, params=params)
    data = response.json()

    return data.get("results", [])


# noinspection PyShadowingNames
def get_movie_details(movie_id):
    base_url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    params = {"api_key": api_key}

    response = requests.get(base_url, params=params)
    data = response.json()

    return data


# noinspection PyShadowingNames
def display_movie_page(movie_id):
    movie_data = get_movie_details(movie_id)

    # Display movie details
    st.header(movie_data["title"])
    st.subheader("Description:")
    st.write(movie_data["overview"])

    st.subheader("Rating:")
    st.write(movie_data["vote_average"])

    st.subheader("Actors:")
    credits_url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits"
    credits_params = {"api_key": api_key}
    credits_response = requests.get(credits_url, params=credits_params)
    credits_data = credits_response.json()

    actors = credits_data.get("cast", [])[:5]  # Displaying only the first 5 actors
    for actor in actors:
        st.write(f"- {actor['name']}")

# Trending page

def get_popular_movies(api_key, language="en-US", page=1):
    base_url = "https://api.themoviedb.org/3/movie/popular"
    params = {"api_key": api_key, "language": language, "page": page}
    response = requests.get(base_url, params=params)
    data = response.json()
    return data.get("results", [])

def get_popular_shows(api_key, language="en-US", page=1):
    base_url = "https://api.themoviedb.org/3/tv/popular"
    params = {"api_key": api_key, "language": language, "page": page}
    response = requests.get(base_url, params=params)
    data = response.json()
    return data.get("results", [])

st.set_page_config(
    page_title="BoxOffice"
)

page = st.sidebar.selectbox(
    "Pick a page",
    ["Search Page", "Watchlist Page", "Trending Page"]
)

if page == "Search Page":
    st.title("Search Page")

    # Search bar
    search_query = st.text_input("Search for a movie:")
    if st.button("Search"):
        if search_query:
            movies = search_movies(search_query)
            if movies:
                st.success(f"Found {len(movies)} movies:")
                selected_movie = st.selectbox("Select a movie", [movie['title'] for movie in movies])

                for movie in movies:
                    if selected_movie == movie['title']:
                        # Display movie details
                        st.header(movie["title"])
                        st.subheader("Description:")
                        st.write(movie["overview"])

                        poster_path = movie.get("poster_path")
                        if poster_path:
                            poster_url = f"https://image.tmdb.org/t/p/w500/{poster_path}"
                            st.image(poster_url, caption=movie["title"], use_column_width=True)

                        st.subheader("Rating:")
                        st.write(movie["vote_average"])

                        st.subheader("Actors:")
                        credits_url = f"https://api.themoviedb.org/3/movie/{movie['id']}/credits"
                        credits_params = {"api_key": api_key}
                        credits_response = requests.get(credits_url, params=credits_params)
                        credits_data = credits_response.json()

                        actors = credits_data.get("cast", [])[:5]  # Displaying only the first 5 actors
                        for actor in actors:
                            st.write(f"- {actor['name']}")
            else:
                st.warning("No movies found.")
        else:
            st.warning("Please enter a search query.")
            
   



elif page == "Watchlist Page":
    st.write("Under Construction")


elif page == "Trending Page":
    st.title("Trending Movies and Tv Shows")
   
        
    
    # Get popular movies and TV shows
    popular_movies_data = get_popular_movies(api_key)[:5]  # Limit to 5 movies
    popular_shows_data = get_popular_shows(api_key)[:5]  # Limit to 5 shows

    # Calculate the width of each column based on the number of items
    col1_width = 0.5
    col2_width = 0.5
        
 # Calculate the width of each column based on the number of items
# col1_width = len(popular_movies_data) / (len(popular_movies_data) + len(popular_shows_data))
# col2_width = 1 - col1_width

# Create columns with specified width
    col1, col2 = st.columns((col1_width, col2_width))

# Display popular movies in the first column
    with col1:
        st.subheader("Popular Movies:")
        for movie in popular_movies_data:
            poster_path = movie.get('poster_path', '')
            if poster_path:
                st.image(f"https://image.tmdb.org/t/p/w500/{poster_path}", caption=f"{movie.get('title', '')} (Rating: {movie.get('vote_average', '')}/10)", use_column_width=True)

    # Display popular TV shows in the second column
    with col2:
        st.subheader("Popular TV Shows:")
        for show in popular_shows_data:
            poster_path = show.get('poster_path', '')
            title = show.get('name', 'Title not available')  # Adjust 'title' to 'name' if that's the correct key
            if poster_path:
                st.image(f"https://image.tmdb.org/t/p/w500/{poster_path}", caption=f"{title} (Rating: {show.get('vote_average', '')}/10)", use_column_width=True)