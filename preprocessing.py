# Import the necessary packages
import pandas as pd
import re
import numpy as np
from sklearn.preprocessing import MultiLabelBinarizer

ingredients = pd.read_csv('data/ingredients.csv')

unique_ingredients = ingredients.drop_duplicates(subset='name')
unique_ingredients_array = np.array(unique_ingredients['name'])

recipes = pd.read_csv('data/recipes.csv')



# Remove quotes from ingredients so that when we one-hot encode, we get proper column names
l = []
offending_character = recipes['ingredients'][0].strip("][")[0]
offending_character2 = '"'

for item in recipes['ingredients']:
    item_list = item.strip("][").replace(offending_character, '').replace(offending_character2, '').split(', ')
    l.append(item_list)

formatted_ingredient = pd.Series(l)

recipes['ingredients'] = formatted_ingredient



# One hot encode ingredients
mlb = MultiLabelBinarizer(sparse_output=True)

recipes = recipes.join(
            pd.DataFrame.sparse.from_spmatrix(
                mlb.fit_transform(recipes.pop('ingredients')),
                index=recipes.index,
                columns=mlb.classes_))


for col in recipes.columns[5:]:
    b = col in unique_ingredients_array
    if b == False:
        recipes.pop(col)

recipes.pop('Unnamed: 0')


# Remove quotes from tags
l1 = []
offending_character = "'"
offending_character2 = '"'

for item in recipes['tags']:
    item_list = item.strip("][").replace(offending_character, '').replace(offending_character2, '').split(', ')
    l1.append(item_list)

formatted_tags = pd.Series(l1)
recipes['tags'] = formatted_tags

# One hot encode tags
mlb = MultiLabelBinarizer()

recipes = recipes.join(
            pd.DataFrame(
                mlb.fit_transform(recipes.pop('tags')),
                index=recipes.index,
                columns=mlb.classes_))


# List of common ingredients and erroneous ingredients to ignore
ignore_ingredients = ['water', 'salt', 'kosher salt', 'sea salt', 'pepper', 'black peppercorn', 'Equal', 'oil',
                     'Garnish:']


# Pop branded ingredient names and those that form part of the above list
for col in recipes.columns[3:-22]:
    if col[0].isupper():
        recipes.pop(col)
    try:
        if col in ignore_ingredients:
            recipes.pop(col)
    except:
        print(f'Already popped {col}')


# Takes a really long time to run
recipes.to_csv('data/recipes_cleaned.csv', chunksize=100)

unique_ingredients.to_csv('data/ingredients_cleaned.csv', chunksize=100)
