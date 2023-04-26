import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt




# To set a webpage title, header and subtitle
st.set_page_config(page_title = "Movies analysis",layout = 'wide')
st.header("Tabaleau de Bord Interactif")
st.subheader("Interagissez avec ce tableau de bord à l'aide des widgets de la barre latérale")


#read in the file
movies_data = pd.read_csv("https://raw.githubusercontent.com/danielgrijalva/movie-stats/7c6a562377ab5c91bb80c405be50a0494ae8e582/movies.csv")
movies_data.info()
movies_data.duplicated()
movies_data.count()
movies_data.dropna()


# Creating sidebar widget filters from movies dataset
year_list = movies_data['year'].unique().tolist()
score_rating = movies_data['score'].unique().tolist()
genre_list = movies_data['genre'].unique().tolist()


# Add the filters. Every widget goes in here
with st.sidebar:
    st.write("Sélectionnez une plage sur le curseur (il représente la partition du film) pour afficher le nombre total de films dans un genre qui se situe dans cette plage ")
    #create a slider to hold user scores
    new_score_rating = st.slider(label = "Choisir une valeur:",
                                  min_value = 1.0,
                                  max_value = 10.0,
                                 value = (3.0,4.0))


    st.write("Sélectionnez votre ou vos genres préférés et l'année pour voir les films sortis cette année-là et sur ce genre")
    #create a multiselect option that holds genre
    new_genre_list = st.multiselect('Choisir un Genre:',
                                        genre_list, default = ['Animation', 'Horror', 'Fantasy', 'Romance'])

    #create a selectbox option that holds all unique years
    year = st.selectbox('Choisir une année', year_list, 0)

#Configure the slider widget for interactivity
score_info = (movies_data['score'].between(*new_score_rating))



#Configure the selectbox and multiselect widget for interactivity
new_genre_year = (movies_data['genre'].isin(new_genre_list)) & (movies_data['year'] == year)


#VISUALIZATION SECTION
#group the columns needed for visualizations
col1, col2 = st.columns([2,3])
with col1:
    st.write("""#### Listes de films filtrés par année et genre """)
    dataframe_genre_year = movies_data[new_genre_year].groupby(['name', 'genre'])['year'].sum()
    dataframe_genre_year = dataframe_genre_year.reset_index()
    st.dataframe(dataframe_genre_year, width = 400)

with col2:
    st.write("""#### Score utilisateur des films et leur genre """)
    rating_count_year = movies_data[score_info].groupby('genre')['score'].count()
    rating_count_year = rating_count_year.reset_index()
    figpx = px.line(rating_count_year, x = 'genre', y = 'score')
    st.plotly_chart(figpx)




 # creating a bar graph with matplotlib
st.write("""
Budget moyen du film, regroupé par genre
    """)
avg_budget = movies_data.groupby('genre')['budget'].mean().round()
avg_budget = avg_budget.reset_index()
genre = avg_budget['genre']
avg_bud = avg_budget['budget']

fig = plt.figure(figsize = (19, 10))

plt.bar(genre, avg_bud, color = 'maroon')
plt.xlabel('genre')
plt.ylabel('budget')
plt.title('Graphique à barres Matplotlib montrant le budget moyen des films dans chaque genre')
st.pyplot(fig)

