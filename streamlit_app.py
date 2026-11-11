# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie! :cup_with_straw: ")
st.write(
  """Choose the fruits you want in your custom Smoothie!
  """
)

cnx = st.connection("snowflake")
session = cnx.session()

name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your Smoothie will be:", name_on_order)




my_dataframe = (
    session.table("smoothies.public.fruit_options")
    .select(col("fruit_name"))
    )
    
ingredients_list = st.multiselect(
    label = "Choose up to 5 ingeredients:",
    options = my_dataframe,
    max_selections = 5,
)

if ingredients_list:
    ingredients_string = ''
    
    for fruit in ingredients_list:
        ingredients_string += fruit + ' '

else:
    pass

time_to_insert = st.button(label="Submit Order")

st.write(time_to_insert)

if time_to_insert:
    my_insert_stmt = f"""
        insert into smoothies.public.orders(ingredients, name_on_order)
            values (
                '{ingredients_string}'
                ,'{name_on_order}')
            """
    
    session.sql(my_insert_stmt).collect()
    st.success(f'Your Smoothie is ordered, {name_on_order}!', icon="✅")
