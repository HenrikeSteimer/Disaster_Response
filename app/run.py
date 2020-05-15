import json
import plotly
import plotly.graph_objects as pgo
import pandas as pd

from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

from flask import Flask
from flask import render_template, request, jsonify
from sklearn.externals import joblib
from sqlalchemy import create_engine

#from wrangling_data import return_figures

app = Flask(__name__)

def tokenize(text):
    tokens = word_tokenize(text)
    lemmatizer = WordNetLemmatizer()

    clean_tokens = []
    for tok in tokens:
        clean_tok = lemmatizer.lemmatize(tok).lower().strip()
        clean_tokens.append(clean_tok)

    return clean_tokens

# load data
engine = create_engine('sqlite:///data/DisasterResponse.db')
df = pd.read_sql_table('Messages', engine)

# load model
model = joblib.load("models/classifier.pkl")


# index webpage displays cool visuals and receives user input text for model
@app.route('/')
@app.route('/index')
def index():
    
    # extract data needed for visuals
    genre_counts = df.groupby('genre').count()['message']
    genre_names = list(genre_counts.index)
    
    # create visuals
    graph_one = [] 
    
    graph_one.append(
      pgo.Bar(
        x=genre_names,
        y=genre_counts,
            )
        )

    layout_one = dict(title = 'Distribution of Message Genres',
                xaxis = dict(title = 'Genre'),
                yaxis = dict(title = 'Frequency'),
                )
    
    # second chart 
    graph_two = []
    
    # frequencies of top 5 categories
    y = df.drop(['id','message','original','genre'], axis=1)
    occur = list(y.sum(axis=0).sort_values(ascending=False))
    occur_top5 = occur[:5]
    occur_top5_names = ["related", "aid related", "weather related", "direct report", "request"]
    x_pos = [i for i, _ in enumerate(occur_top5)]

    graph_two.append(
      pgo.Bar(
      x = occur_top5_names,
      y = occur_top5,
            )
        )

    layout_two = dict(title = 'Frequency of top 5 message categories',
                xaxis = dict(title = 'Category'),
                yaxis = dict(title = 'Frequency'),
                )

    # third chart 
    graph_three = []
    
    # frequencies of top 5 categories
    y = df.drop(['id','message','original','genre'], axis=1)
    nbr_cat = y.sum(axis=1).value_counts().sort_index()
    nbr_cat = list(nbr_cat[:10])
    x_pos = list(range(0, 10))

    graph_three.append(
      pgo.Bar(
      x = x_pos,
      y = nbr_cat,
            )
        )

    layout_three = dict(title = 'Number of categories messages classify for',
                xaxis = dict(title = 'Category'),
                yaxis = dict(title = 'Frequency'),
                )
    
    
    # append all charts to the figures list
    graphs = []
    graphs.append(dict(data=graph_one, layout=layout_one))
    graphs.append(dict(data=graph_two, layout=layout_two))
    graphs.append(dict(data=graph_three, layout=layout_three))
    
    # encode plotly graphs in JSON
    ids = ["graph-{}".format(i) for i, _ in enumerate(graphs)]
    graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)
    
    # render web page with plotly graphs
    return render_template('master.html', ids=ids, graphJSON=graphJSON)


# web page that handles user query and displays model results
@app.route('/go')
def go():
    # save user input in query
    query = request.args.get('query', '') 

    # use model to predict classification for query
    classification_labels = model.predict([query])[0]
    classification_results = dict(zip(df.columns[4:], classification_labels))

    # This will render the go.html Please see that file. 
    return render_template(
        'go.html',
        query=query,
        classification_result=classification_results
    )


def main():
    app.run(host='0.0.0.0', port=3001, debug=True)


if __name__ == '__main__':
    main()