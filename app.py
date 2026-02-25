import streamlit as st
import pickle
import pandas as pd
import requests
import joblib
import os
import gdown

file_id = "1NV3tGw8hvlGNXP0ATH4HtCoeAXuyzzvN"
url = f"https://drive.google.com/uc?id={file_id}"

if not os.path.exists("similarity.pkl"):
    gdown.download(url, "similarity.pkl", quiet=False)

movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies=pd.DataFrame(movies_dict)

similarity = joblib.load('similarity.pkl')

def fetch_poster(movie_id):
    response=requests.get('https://api.themoviedb.org/3/movie/{}?api_key=600c30fbc89644650e8e4fe3639f4f35&language=en-US'.format(movie_id))
    data=response.json()
    return "https://image.tmdb.org/t/p/w500/"+data['poster_path']

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distance = sorted(list(enumerate(similarity[movie_index])), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies=[]
    recommended_movies_posters=[]
    for i in distance:
        # Fetch Poster of movie
        recommended_movies.append(movies.iloc[i[0]].title)
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters

st.title('Movie Recommendation System')
selected_movie_name=st.selectbox(
    "How would you like to be contacted?",
    movies['title'].values,)

if st.button('Recommend'):
    names, posters=recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(names[0])
        st.image(posters[0])

    with col2:
        st.text(names[1])
        st.image(posters[1])

    with col3:
        st.text(names[2])
        st.image(posters[2])

    with col4:
        st.text(names[3])
        st.image(posters[3])

    with col5:
        st.text(names[4])
        st.image(posters[4])