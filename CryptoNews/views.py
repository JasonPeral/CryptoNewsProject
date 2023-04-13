from django import requests
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def home(request):
    api_url = "https://cryptopanic.com/api/v1/posts/?auth_token=e53346a5cfee7b972f0429fdcf0f06a80f57ee1d"
    response = requests.get(api_url)
    data = response.json()

    # Add this code to get coins data
    coins_api_url = "https://api.coincap.io/v2/assets"
    coins_response = requests.get(coins_api_url)
    coins_data = coins_response.json()
    coins = coins_data['data'][:10]

    articles = data['results'][:5]
    request.session['article_data'] = {}
    for article in articles:
        request.session['article_data'][str(article['id'])] = {
            'title': article['title'],
            'description': article['title'],
            'url': article['url'],
            'date': article['created_at'],
            'domain': article['domain'],
        }

    context = {'articles': articles, 'is_authenticated': request.user.is_authenticated, 'coins': coins}
    return render(request, 'home.html', context)

