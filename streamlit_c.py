import streamlit as st

st.title("WBSFLIX - Movies Recommendation")
 
st.write("""
### Most popular movies 
""")
import pandas as pd
movies = pd.read_csv('movies.csv').head()
ratings=pd.read_csv('ratings.csv')
movies=pd.read_csv('movies.csv')
links=pd.read_csv('links.csv')
tags=pd.read_csv('tags.csv')

matrix = pd.merge(ratings,movies, how ="inner", on = ["movieId"])
matrix = pd.merge(ratings,movies, how ="inner", on = ["movieId"])
matrix= pd.merge(matrix,tags, how ="inner", on = ["movieId"])
matrix.dropna()
matrix.drop(['timestamp_x','timestamp_y','userId_y'], axis=1, inplace=True )
matix_movies=matrix.copy()


#st.dataframe(matix_movies)
def popularity_based_recommender(data: pd.DataFrame, min_n_ratings: int):
    
    return (
        matrix
        .groupby(['movieId', 'title',  'genres'])
        .agg(
           
            movie_rating_mean = ('rating', 'mean'),
            movie_rating_count = ('rating', 'count')
        )
        .reset_index()
        .sort_values(['movie_rating_count'], ascending=False)
        .query('movie_rating_count > @min_n_ratings')
        .head(5)
        )
hide_table_row_index = """
        <style>
        tbody th {display:none}
        .blank {display:none}
        </style>
        """

# Inject CSS with Markdown
st.markdown(hide_table_row_index, unsafe_allow_html=True)
most_popular = popularity_based_recommender(matrix.copy(),1)
mostPopular = most_popular.filter(['title'])
st.table(mostPopular)

st.write("""
### Movie selection based on Genre
""")
genres = st.selectbox(
    ' ',
     (matix_movies['genres'].unique()))
def popularity_based_recommender_gen(data: pd.DataFrame, genres: str):
    return (
        matrix
        .groupby(['movieId', 'title',  'genres'])
        .agg(
           
            movie_rating_mean = ('rating', 'mean'),
            movie_rating_count = ('rating', 'count')
        )
        .reset_index()
        .sort_values(['movie_rating_count'], ascending=False)
        .query('genres == @genres')
        .head(5)
        )
hide_table_row_index = """
        <style>
        tbody th {display:none}
        .blank {display:none}
        </style>
        """
# Inject CSS with Markdown
st.markdown(hide_table_row_index, unsafe_allow_html=True)
most_popular1 = popularity_based_recommender_gen(matrix.copy(),genres)
mostPopular1 = most_popular1.filter(['title'])
st.table(mostPopular1)

newdf= (
    matrix
    .filter(['userId_x', 'title', 'rating'])
    )
#st.dataframe(newdf)
newdf1 = newdf.drop_duplicates()


user_pref = st.sidebar.number_input("Please enter the user Id", value=0, min_value=0, step=1, max_value=608)
user_pref1 =int(user_pref)
if(user_pref > 0):
    def get_user_prefered_item(newdf1: pd.DataFrame, userId_x: int):
        data=newdf1.copy()
        return(data
        .query('userId_x == @userId_x') 
        .sort_values('rating', ascending=False)
        ['title'].to_list()[:6]
        )
    user_preference = get_user_prefered_item(newdf1,user_pref1)
    st.text("Movies recommended to user ID")
    st.text(user_pref1)
    hide_table_row_index = """
            <style>
            tbody th {display:none}
            .blank {display:none}
            </style>
            """

    # Inject CSS with Markdown
    st.markdown(hide_table_row_index, unsafe_allow_html=True)
    st.table(user_preference)

    
# py function get sparse matrix
def get_sparse_matrix(newdf1: pd.DataFrame): 

    return(
    newdf1
        .pivot(index='userId_x', columns='title', values='rating')
    )

st.text("Select a movie you like ")
movie_name = st.sidebar.selectbox(
    ' ',
     (matix_movies['title'].unique()))
#movie_name = st.sidebar.text_input("Please enter a movie that you like")
if(movie_name != ''):
# py function item based recommender
    def item_based_recommender(dense_matrix: pd.DataFrame, title: str, n: int=5):
        sparse_matrix = get_sparse_matrix(newdf1)
        return(
        sparse_matrix
            
            .corrwith(sparse_matrix[title])
            .sort_values(ascending=False)
            .index
            .to_list()[1:n+1]
        )
    item_preference = item_based_recommender(newdf1, movie_name)
    st.text("Movie Selected : " + movie_name)
    st.text("Movies recommended based on your preference")
    hide_table_row_index = """
        <style>
        tbody th {display:none}
        .blank {display:none}
        </style>
        """
    # Inject CSS with Markdown
    st.markdown(hide_table_row_index, unsafe_allow_html=True)
    st.table(item_preference)

        
