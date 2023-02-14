from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.automap import automap_base



import os
file_path = os.path.abspath(os.getcwd()) + "/data/zips.db"


app = Flask(__name__)

# /// = relative path, //// = absolute path
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+file_path
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

with app.app_context():
    factors = db.Table('factors', db.metadata, autoload_with = db.engine)


class MakeDictionary:
    def __init__(self, keys, values):
        self.dictionary = {}
        for i, key in enumerate(keys):
            self.dictionary[key] = values[i]

    def get_dictionary(self):
        return self.dictionary

keyz = [
    'ZIP code',
    'Total population',
    'Sex Ratio (males to female)',
    'Median Age',
    'Average household size (persons)',
    'Percent of males never married',
    'Percent of population with educational attainment below 12th grade',
    'Percent of population who lived in a different house last year',
    'Percent of population unemployed',
    'Average income per household ($)',
    'Median annual earnings for workers ($)',
    'Percent of housing units that are vacant',
    'Percent of housing units that are rentals',
    'Percent of houses with more than one occupant per room',
    'Percent of families living below the poverty line'
]



with app.app_context():
    def roundvalues(x):
        if x is None:
            return 'not available'
        elif isinstance(x, float):
             return round(x, 4)
        else:
             return x

@app.route("/")
def home():
    with app.app_context():

        results = db.session.query(factors).filter_by(ZIP='32132').first()
        results = ['Not Available' if x is None else x for x in results]
        results = tuple(roundvalues(x) for x in results)
        factors_dict = MakeDictionary(keyz, results).get_dictionary()


    return render_template("base.html", todo=factors_dict
    )


@app.route("/search", methods=["POST"])
def search():
    title = request.form.get("title")
    results = db.session.query(factors).filter_by(ZIP=title).first()

    if results is None:
        keyz_none = ["message"]
        results_none = ["not a valid ZIP code, please try again"]
        factors_dict = MakeDictionary(keyz_none, results_none).get_dictionary()
    else:
        results = ['Not Available' if x is None else x for x in results]
        results = tuple(roundvalues(x) for x in results)
        factors_dict = MakeDictionary(keyz, results).get_dictionary()


    return render_template("base.html", todo=factors_dict)


if __name__ == "__main__":

    app.run(host='0.0.0.0', port=80)             
             
             
             
             
             
             
