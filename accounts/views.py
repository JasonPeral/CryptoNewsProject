from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login
from .forms import LoginForm
from django.http import HttpResponseNotAllowed
from . import views
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import NewsArticle, UserProfile, CoinAmount
from .forms import CustomUserCreationForm
from django.contrib import messages
from decimal import Decimal, InvalidOperation
from django.contrib.auth import logout
from django import requests



def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
            auth_login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})

@login_required
def add_to_read(request, article_id):
    article_data = request.session['article_data'][str(article_id)]

    article = NewsArticle(
        user=request.user,
        title=article_data['title'],
        description=article_data['description'],
        url=article_data['url'],
        date=article_data['date'],
        domain=article_data['domain'],
    )
    article.save()

    return redirect('home')

@login_required
def delete_from_read(request, article_id):
    article = get_object_or_404(NewsArticle, id=article_id, user=request.user)
    article.delete()
    return redirect('accounts:list')

def get_market_price(coin_id):
    response = requests.get(f'https://api.coincap.io/v2/assets/{coin_id}')
    if response.status_code == 200:
        return response.json()['data']['priceUsd']
    else:
        return None

API_URL = "https://api.coincap.io/v2/assets/"

@login_required
def list(request):
    saved_articles = NewsArticle.objects.filter(user=request.user)
    saved_coin_amounts = CoinAmount.objects.filter(user=request.user)

    coin_amounts_with_market_price = []
    for coin_amount in saved_coin_amounts:
        market_price_usd = get_market_price(coin_amount.coin_id)
        coin_amounts_with_market_price.append({
            'coin_amount': coin_amount,
            'market_price_usd': float(market_price_usd)
        })

    return render(request, 'accounts/list.html', {
        'saved_articles': saved_articles,
        'coin_amounts_with_market_price': coin_amounts_with_market_price,
    })

@login_required
def save_coin_amount(request, coin_id):
    if request.method == 'POST':
        amount = request.POST.get('coin_amount')
        if not amount:
            messages.error(request, "Coin amount cannot be empty.")
            return redirect('home')
        try:
            decimal_amount = Decimal(amount)
        except (InvalidOperation, ValueError):
            messages.error(request, "Invalid coin amount.")
            return redirect('home')

        # Fetch coin data from the API
        response = requests.get(API_URL + coin_id)
        if response.status_code != 200:
            messages.error(request, "Failed to fetch coin data from the API.")
            return redirect('home')

        coin_data = response.json().get('data')
        price_usd = Decimal(coin_data['priceUsd'])
        change_percent_24hr = Decimal(coin_data['changePercent24Hr'])

        # Save coin data
        coin_amount, created = CoinAmount.objects.update_or_create(
            user=request.user,
            coin_id=coin_id,
            defaults={
                'amount': decimal_amount,
                'price_usd': price_usd,
                'change_percent_24hr': change_percent_24hr
            }
        )

        return redirect('home')
    else:
        return HttpResponseNotAllowed(['POST'])
    
def delete_coin_amount(request, coin_amount_id):
    coin_amount = get_object_or_404(CoinAmount, id=coin_amount_id)
    if request.user == coin_amount.user:
        coin_amount.delete()
    return redirect('accounts:list')

def logout_view(request):
    logout(request)
    return redirect('home')