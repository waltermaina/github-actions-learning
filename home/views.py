import requests
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.views.decorators.cache import cache_page


def index(request):
    return render(request, 'home/index.html')


@require_http_methods(["GET"])
@cache_page(60 * 5)  # Cache for 5 minutes
def bitcoin_price_api(request):
    """
    API endpoint to fetch Bitcoin price data from CoinGecko
    """
    try:
        # Fetch Bitcoin data from CoinGecko API
        response = requests.get(
            'https://api.coingecko.com/api/v3/coins/bitcoin',
            params={
                'localization': 'false',
                'tickers': 'false',
                'market_data': 'true',
                'community_data': 'false',
                'developer_data': 'false',
                'sparkline': 'false'
            },
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            
            # Extract relevant data with proper validation and sanitization
            market_data = data.get('market_data', {})
            
            # Helper function to safely extract numeric values
            def safe_numeric(value, default=0):
                try:
                    if isinstance(value, (int, float)) and not isinstance(value, bool):
                        # Handle infinity and NaN
                        if value == float('inf') or value == float('-inf') or value != value:  # NaN check
                            return default
                        return float(value)
                    return default
                except (ValueError, TypeError):
                    return default
            
            # Helper function to safely extract string values
            def safe_string(value, default=''):
                try:
                    if isinstance(value, str):
                        # Basic sanitization - remove any HTML/script tags
                        import re
                        cleaned = re.sub(r'<[^>]*>', '', str(value))
                        return cleaned
                    return default
                except (ValueError, TypeError):
                    return default
            
            result = {
                'price': safe_numeric(market_data.get('current_price', {}).get('usd')),
                'high_24h': safe_numeric(market_data.get('high_24h', {}).get('usd')),
                'low_24h': safe_numeric(market_data.get('low_24h', {}).get('usd')),
                'market_cap': safe_numeric(market_data.get('market_cap', {}).get('usd')),
                'volume_24h': safe_numeric(market_data.get('total_volume', {}).get('usd')),
                'price_change_percentage_24h': safe_numeric(market_data.get('price_change_percentage_24h')),
                'last_updated': safe_string(market_data.get('last_updated'))
            }
            
            return JsonResponse(result)
        else:
            return JsonResponse({'error': 'Failed to fetch data from CoinGecko'}, status=500)
            
    except requests.exceptions.RequestException as e:
        return JsonResponse({'error': 'Network error occurred'}, status=500)
    except Exception as e:
        return JsonResponse({'error': 'An unexpected error occurred'}, status=500)
