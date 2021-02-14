import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from mlxtend.frequent_patterns import apriori, fpmax, fpgrowth, association_rules


app = dash.Dash(__name__)

recipes = pd.read_csv('data/recipes_cleaned.csv')


app.layout = html.Div([

	html.H1('Ingredients Associations from Popular Cuisines'),

	html.P('Association rule learning is a rule-based machine learning method for ' + 
		'discovering interesting relations between variables in large databases. It is intended ' + 
		'to identify strong rules discovered in databases using some measures of interestingness.'),


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
		value=["american"]),


	dcc.Graph(id='apriori_plot', figure={})


	])

@app.callback(
	Output(component_id='apriori_plot', component_property='figure'),
	Input(component_id='list_of_cuisines', component_property='value')
)
def update_output_graph(input_value):

	recipes_copy = recipes.copy()
	cuisines = input_value
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

	frequent_itemsets = fpgrowth(recipes_copy, min_support=0.01, use_colnames=True)

	rules = association_rules(frequent_itemsets, metric='lift', min_threshold=2)

	rules["antecedents"] = rules["antecedents"].apply(lambda x: list(x)[0]).astype("unicode")
	rules["consequents"] = rules["consequents"].apply(lambda x: list(x)[0]).astype("unicode")

	fig = px.scatter(rules, x="support", y="confidence", color="lift", hover_data=['antecedents', 'consequents'])

	return fig



if __name__ == '__main__':
	app.run_server(debug=True)