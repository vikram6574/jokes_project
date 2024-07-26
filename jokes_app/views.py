import requests
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.shortcuts import render

BASE_URL = 'https://v2.jokeapi.dev/joke'
CATEGORIES_URL = 'https://v2.jokeapi.dev/categories'

def index(request):
    try:
        categories_response = requests.get(CATEGORIES_URL)
        categories_response.raise_for_status()
        categories_data = categories_response.json()
        print("Categories data:", categories_data)  # Debug print
        categories = categories_data.get('categories', [])
        print("Categories:", categories)  # Debug print
        return render(request, 'jokes_app/index.html', {'categories': categories})
    except requests.RequestException as e:
        print(f"Error fetching categories: {e}")  # Debug print
        return render(request, 'jokes_app/index.html', {'categories': []})

@require_http_methods(["GET"])
def get_joke(request):
    # Parse parameters from request
    category = request.GET.get('category', 'Any')
    blacklist_flags = request.GET.getlist('blacklist')
    joke_type = request.GET.get('type', 'single')
    
    # Construct API URL
    url = f"{BASE_URL}/{category}"
    params = {
        'type': joke_type,
        'blacklistFlags': ','.join(blacklist_flags) if blacklist_flags else None,
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        joke = response.json()
        return JsonResponse(joke)
    except requests.RequestException as e:
        return JsonResponse({'error': str(e)}, status=400)

@require_http_methods(["GET"])
def get_categories(request):
    try:
        response = requests.get(CATEGORIES_URL)
        response.raise_for_status()
        categories = response.json()
        return JsonResponse(categories)
    except requests.RequestException as e:
        return JsonResponse({'error': str(e)}, status=400)