from flask import Flask, request, render_template
import requests
from countryguess import guess_country
import pycountry
import os
from dotenv import load_dotenv

load_dotenv()

api_url = os.getenv('API_URL')  
api_key = os.getenv('API_KEY')

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    language = 'en'

    countries = [country.name for country in pycountry.countries]
    countries.sort()

    if request.method == 'GET':  
        params = {
            'apikey': api_key,
            'language': language,
            'prioritydomain': 'top',
        }

        response = requests.get(api_url, params=params)

        data = response.json()

        if response.status_code != 200 or data.get('status') != 'success':
            return render_template('error.html', error="Failed to fetch news")
        
        total_results = data.get('totalResults', 0)

        articles = data.get('results', [])

        first_article = articles[0] if articles else None

        context = {
            'first_article': first_article,
            'articles': articles[1:11],
            'countries': countries,
            'total_results': total_results,
        }

        return render_template('index.html', **context)

    if request.method == 'POST':
        country = request.form.get("country", "").strip()

        country_name = guess_country(country)
        if country_name:
            country_name = country_name['iso2'].lower()

        q = request.form.get("search", "").strip().lower()

        category = request.form.get("category", "").lower()

        params = {
            'apikey': api_key,
            'language': language,
            "prioritydomain": "top",
        }

        if country_name:
            params['country'] = country_name

        if q:
            params['q'] = q

        if category:
            params['category'] = category

        response = requests.get(api_url, params=params)

        data = response.json()

        if response.status_code != 200 or data.get('status') != 'success':
            return render_template('error.html', error="Failed to fetch news")
        
        total_results = data.get('totalResults', 0)

        articles = data.get('results', [])

        first_article = articles[0] if articles else None

        context = {
            'first_article': first_article,
            'articles': articles[1:11],
            'total_results': total_results,
            'countries' : countries,
        }

        return render_template('index.html', **context)
    


if __name__ == "__main__":
    app.run(debug=True)