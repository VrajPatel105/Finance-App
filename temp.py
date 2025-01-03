import requests

def get_stock_news(symbol):
            
            
            API_KEY = "e92fe2a711264deea18ed1db329d7e15"
            url = f"https://newsapi.org/v2/everything?q={symbol}+stock&apiKey={API_KEY}&language=en&sortBy=publishedAt"
            
            response = requests.get(url)
            data = response.json()
            
            if data.get('articles'):
                formatted_news = []
                for item in data['articles'][:10]:
                    news_item = {
                        'title': item.get('title', 'No Title Available'),
                        'publisher': item.get('source', {}).get('name', 'Unknown Publisher'),
                        'link': item.get('url', '#'),
                        'published': item.get('publishedAt', '').replace('T', ' ').replace('Z', ''),
                        'summary': item.get('description', ''),
                        'image': item.get('urlToImage')
                    }
                    formatted_news.append(news_item)
                return formatted_news
            return None
        
a = get_stock_news('NVDA')
print(a)