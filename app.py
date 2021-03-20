# to do
# show how many people have same name, surname ..
# EDA - top 10 names, most common birthday ..
# find siblings by looking at surname and haeranun
# preprocess input
# add relationship graphs
# autocompelete for taracshrjan
# date finished -> 19.03.21

# import pandas as pd

# from datetime import datetime
# from datetime import date

# df = pd.read_csv('elections_updated.csv')


from flask import Flask, request, render_template
# from search_for_flask import do_all
from main_search import get_info


app = Flask(__name__)


@app.route('/')
def my_form():
    return render_template('form.html')


@app.route('/', methods=['POST'])
def my_form_post():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    middle_name = request.form['middle_name']
    marz = request.form['marz']
    taracashrjan = request.form['taracashrjan'] 

    min_age = request.form['min_age']
    max_age = request.form['max_age']

    df = get_info(first_name, last_name, middle_name, marz, taracashrjan, min_age, max_age)


    if df[0] == 'no results':
        print ('by')
        return f'<h1>{df[1]}</h1>'
    if df[0] == 'one person':
        return f'<h1>{df[1]}</h1><br>  \
                 <h3>Նշված մարդու հետ միասին նույն հասցեով են գրանցված ՝ \
                 {df[2]}</h3> \
                 <h3>Հետևյալ մարդիկ հնարավորա քուր/ախպեր են{df[3]}</h3>'
    if df[0] == 'multiple results':
        return df[1]
    #     @app.context_processor
    #     def inject_globals():
    #         return dict(
    #             processed_text=processed_text,
    #         )

    #     return render_template('search_results.html')
