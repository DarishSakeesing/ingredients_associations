import urllib, json
import pandas as pd

# Top 11 cuisines in the United States 
cuisines = ['chinese', 'mexican', 'italian', 'japanese', 'greek', 'french', 'thai', 'spanish', 'indian', 'mediterranean', 'american']

# Dictionaries to hold the data; appending data to a dictionary is faster than appendind to a dataframe
collected_recipe_data = {'recipe_id':[], 'cuisine':[], 'ingredients':[], 'tags':[], 'course':[]}
collected_ingredient_data = {'name':[], 'category':[]}

#number of recipes for each cuisine
number_of_recipes = 1000 



for cuisine in cuisines:
    
    with urllib.request.urlopen(f"https://mapi.yummly.com/mapi/v19/content/search?solr.seo_boost=new&q={cuisine}&ignore-taste-pref%3F=true&start=0&maxResult={number_of_recipes}&fetchUserCollections=false&allowedContent=single_recipe&allowedContent=suggested_search&allowedContent=related_search&allowedContent=article&allowedContent=video&allowedContent=generic_cta&guided-search=true&solr.view_type=search_internal") as url:
        web_data = json.loads(url.read().decode())
    
    for i in range(number_of_recipes):
        try:
            collected_recipe_data['cuisine'].append(cuisine)
        except:
            print(f"Error with {cuisine}")
        
        try:
            name = web_data['feed'][i]['tracking-id']
            collected_recipe_data['recipe_id'].append(name)
        except:
            collected_recipe_data['recipe_id'].append(None)
            print(f"Error with {i}th recipe")
            
        
        
        
        try:
            collected_recipe_data['course'].append(web_data['feed'][i]['content']['tags']['course'][0]['display-name'])
        except:
            collected_recipe_data['course'].append(None)
            print(f"No course data for {name}")
            
        
        
        
        
        tags = []
        
        try:
            for tag in web_data['feed'][i]['content']['tags']['nutrition']:
                tags.append(tag['display-name'])
        except:
            print(f"No Nutrition tags for {name}")

        collected_recipe_data['tags'].append(tags)

        
        
        ingredient_list = []
        
        try:
            for ingredient in web_data['feed'][i]['content']['ingredientLines']:
                collected_ingredient_data['category'].append(ingredient['category'])
                collected_ingredient_data['name'].append(ingredient['ingredient'])

                ingredient_list.append(ingredient['ingredient'])
        except:
            print(f"problem with the ingredients for {name}")
            
        collected_recipe_data['ingredients'].append(ingredient_list)



# Writing the dictionaries to dataframes
recipe = pd.DataFrame(collected_recipe_data)
ingredient = pd.DataFrame(collected_ingredient_data)


# Saving the dataframes as csv files for future use
recipe.to_csv('data/recipes.csv')
ingredient.to_csv('data/ingredients.csv')
