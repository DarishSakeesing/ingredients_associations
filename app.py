import dash
import dash_daq as daq
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from mlxtend.frequent_patterns import apriori, fpmax, fpgrowth, association_rules
import numpy as np


external_stylesheets = ['assets/app.css', dbc.themes.BOOTSTRAP]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

recipes = pd.read_csv('data/recipes_cleaned.csv')
ingredients = pd.read_csv('data/ingredients_cleaned.csv')

categories = ingredients.category.unique()

# common_ingredients = ['salt', 'pepper', 'black pepper', 'black peppercorn', 'garlic', 'onion', 'soy sauce', 'bean sprout']

first_card = dbc.Card(
	dbc.CardBody(
	[
	html.H5("Support", className="card-title"),
	html.P("Support is an indication of how frequently the itemset appears in the dataset. For example if X = {Apple}, then supp(X) = X/n, where n is the number of recipes in the dataset being considered."),
	html.P('Similarly, we can find the support of itemsets that contains multiple items. If Y = {Milk, Egg}, then supp(Y) indicates the number of recipes that include both Milk and Egg as a proportion of the size of the dataset. Support values will always range from 0 to 1 since it is a proportion'),
	html.P('Therefore, support can be thought of as the probability of the intersection of Event X and Event Y, where Event X and Event Y are the events that a recipe contains Itemset X and Itemset Y respectively.'),
	dbc.Button("Wiki", href='https://en.wikipedia.org/wiki/Association_rule_learning#Support', color="info"),
	]
	)
)


second_card = dbc.Card(
    dbc.CardBody(
        [
            html.H5("Confidence", className="card-title"),
            html.P('Confidence tries to answer the following question: What is the probability of finding Itemset Y in the recipe given that Itemset X is already in the recipe. The values also range from 0 to 1'),
            html.P('However, the confidence metric can be misleading. For example, if we find conf(X -> Y) is equal to 1, we can say that every single time that Itemset X appears in the recipe, Itemset Y also appears in that recipe. But just from looking at the confidence metric, we cannot say that they have a strong relationship. It could be that Itemset Y is just popular and appears in every recipes.'),
            dbc.Button("Wiki", href='https://en.wikipedia.org/wiki/Association_rule_learning#Confidence', color="info"),
        ]
    )
)

Third_card = dbc.Card(
    dbc.CardBody(
        [
            html.H5("Lift", className="card-title"),
            html.P('Lift corrects the mistakes of Confidence by taking into account the popularity of Itemset Y. It divides confidence(X -> Y) by the supp(Y). '),
            html.P('Lift can take any value from 0 to infinity. A Lift value of < 1 indicates that the two itemsets being considered are substitutes of each other.'),
            html.P('A lift value of 1 indicates that both itemsets being considered are independent of each other.'),
            html.P('A lift value of > 1 lets us know the degree to which those two occurrences are dependent on one another, and makes those rules potentially useful for predicting the consequent in future data sets. '),
            dbc.Button("Wiki", href='https://en.wikipedia.org/wiki/Association_rule_learning#Lift', color="info"),
        ]
    )
)

# ----------------------- APP LAYOUT-------------------------------------
# -----------------------------------------------------------------------
app.layout = html.Div([

	#html.H1('Ingredients Associations from Popular Cuisines'),

	dbc.Jumbotron(
    [
        html.H1("Ingredients Associations from Popular Cuisines", className="display-3"),
        html.P(
            "Data Analysis by Darish Sakeesing",
            className="lead",
        ),
        html.Hr(className="my-2"),
        html.P(
            "Association rule mining is a rule-based machine learning method for " + 
	 	"discovering interesting relations between variables in large databases. It is intended " + 
	 	"to identify strong rules discovered in databases using some measures of interestingness."
        ),
        html.P(dbc.Button("Learn more", href='https://en.wikipedia.org/wiki/Association_rule_learning', color="info"), className="lead"),
    ]
	),



	dbc.Row([dbc.Col(first_card, width=4), dbc.Col(second_card, width=4), dbc.Col(Third_card, width=4)]),

	html.Br(),



	# html.P('Association rule learning is a rule-based machine learning method for ' + 
	# 	'discovering interesting relations between variables in large databases. It is intended ' + 
	# 	'to identify strong rules discovered in databases using some measures of interestingness.', className='intro'),


	dcc.Dropdown(
		id='list_of_cuisines',
		options=[
			{'label': 'American', 'value': 'american'},
			{'label': 'Chinese', 'value': 'chinese'},
			{'label': 'Mexican', 'value': 'mexican'},
			{'label': 'Italian', 'value': 'italian'},
			{'label': 'Japanese', 'value': 'japanese'},
			{'label': 'Greek', 'value': 'greek'},
			{'label': 'French', 'value': 'french'},
			{'label': 'Thai', 'value': 'thai'},
			{'label': 'Spanish', 'value': 'spanish'},
			{'label': 'Indian', 'value': 'indian'},
			{'label': 'Mediterranean', 'value': 'mediterranean'}],
		multi=True,
		value=["american"],
		style={'margin-left': '3px', 'margin-right': '3px'}),
	
	html.Div(
		children = [
			dcc.Checklist(
			id='food_category',
			options=[
				{'label': 'Dairy', 'value': 'Dairy'},
				{'label': 'Produce', 'value': 'Produce'},
				{'label': 'Frozen Foods', 'value': 'Frozen Foods'},
				{'label': 'Pasta & Grains', 'value': 'Pasta & Grains'},
				{'label': 'Condiments', 'value': 'Condiments'},
				{'label': 'Global Foods', 'value': 'Global Foods'},
				{'label': 'Meat', 'value': 'Meat'},
				{'label': 'Baking & Cooking', 'value': 'Baking & Cooking'},
				{'label': 'Snack Foods', 'value': 'Snack Foods'},
				{'label': 'Drinks', 'value': 'Drinks'},
				{'label': 'Alcohol', 'value': 'Alcohol'},
				{'label': 'Canned Goods & Soups', 'value': 'Canned Goods & Soups'},
				{'label': 'Seafood', 'value': 'Seafood'},
				{'label': 'Breakfast Foods', 'value': 'Breakfast Foods'},
				{'label': 'Bakery', 'value': 'Bakery'},
				{'label': 'Deli', 'value': 'Deli'},
				{'label': 'Packaged Meals & Side Dishes', 'value': 'Packaged Meals & Side Dishes'},
				{'label': 'Coffee & Tea', 'value': 'Coffee & Tea'},
				{'label': 'Frozen Desserts', 'value': 'Frozen Desserts'},
				{'label': 'Soy Products', 'value': 'Soy Products'},
				{'label': 'Vegetables', 'value': 'Vegetables'},
				{'label': 'Other', 'value': 'Other'},
				{'label': 'Floral', 'value': 'Floral'},
				{'label': 'Pharmacy & First-Aid', 'value': 'Pharmacy & First-Aid'}
			],
			value=['Produce', 'Dairy', 'Condiments', 'Meat'],
			style = {'display': 'grid'}),     

			dcc.Graph(id='apriori_plot', figure={}, style={'display': 'inline-block', 'width': '-webkit-fill-available'})
			
	],
	style={'display':'flex'}
	)
	
])
# ------------------------ CALLBACK FUNCTIONS--------------------------------------
# ---------------------------------------------------------------------------------
@app.callback(
	Output(component_id='apriori_plot', component_property='figure'),
	Input(component_id='list_of_cuisines', component_property='value'),
	Input(component_id='food_category', component_property='value')
)
def update_output_graph(list_of_cuisines, food_category):

	recipes_copy = filter_by_cuisine(list_of_cuisines)

	recipes_copy = filter_by_category(recipes_copy, food_category)

	print(food_category)


	rules = rules_table(recipes_copy, 0.01, 1.2)

	fig = px.scatter(rules, x="support", y="confidence", color="lift", hover_data=['antecedents', 'consequents'])

	return fig


def filter_by_cuisine(l):
	recipes_copy = recipes.copy()

	cuisines = l
	print(cuisines)

	series_list = []

	for cuisine in cuisines:
		ser = recipes['cuisine'].eq(cuisine)
		series_list.append(ser)

	result = False
	for se in range(len(series_list)):
		result = result | series_list[se]


	recipes_copy = recipes_copy[result]

	recipes_copy = recipes_copy.iloc[:,4:-22]

	return recipes_copy

def rules_table(df, minimum_support, min_lift):
	frequent_itemsets = fpgrowth(df, min_support=minimum_support, use_colnames=True)

	rules = association_rules(frequent_itemsets, metric='lift', min_threshold=min_lift)

	rules["antecedents"] = rules["antecedents"].apply(lambda x: list(x)[0]).astype("unicode")
	rules["consequents"] = rules["consequents"].apply(lambda x: list(x)[0]).astype("unicode")

	return rules


def filter_by_category(df, l):
	df_copy = df.copy()

	list_of_categories = l

	result = False
	for c in list_of_categories:
		result = (ingredients['category'] == c) | result

	list_of_ingredients = np.array(ingredients[result].name.unique())

	arr = []
	for col in recipes.columns:
		if col in list_of_ingredients:
			arr.append(col) 

	return df_copy[arr]

if __name__ == '__main__':
	app.run_server(debug=True)






























