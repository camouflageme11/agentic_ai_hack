from django.shortcuts import render

# Create your views here.
def home_page(request):
    # f_twitter()
    get_gnews_data()
    scrape_google_news()
    return render(request, 'home.html')

def listener(request):
    return render(request, 'listener.html')

def judge(request):
    return render(request, 'judge.html')

def scanner(request):
    return render(request, 'scanner.html')

def artist(request):
    return render(request, 'artist.html')  

def telescope(request):
    return render(request, 'telescope.html')

def guide(request):
    return render(request, 'guide.html')

def messenger(request):
    return render(request, 'messenger.html')


from django.http import JsonResponse
from django.shortcuts import render

# All your existing views here...
# ...

def mood_data(request):
    # This is static mock data. Replace with real data later.
    data = [
        {"latitude": 12.9716, "longitude": 77.5946, "mood": "happy"},
        {"latitude": 12.9352, "longitude": 77.6142, "mood": "sad"},
        {"latitude": 13.0358, "longitude": 77.5970, "mood": "angry"},
        {"latitude": 12.9876, "longitude": 77.6789, "mood": "calm"},
    ]
    return JsonResponse(data, safe=False)


# _____________ db connection______________________
import requests
from django.http import JsonResponse
# from .firebase_config import db

def fetch_and_store_weather(request):
    # Example: OpenWeatherMap API
    api_key = 'YOUR_API_KEY'
    city = 'Bengaluru'
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'

    response = requests.get(url)
    data = response.json()

    # Store in Firestore
    doc_ref = db.collection('weather_reports').document(city)
    doc_ref.set(data)

    return JsonResponse({'status': 'stored', 'city': city})
# ____________________________________________________________________________


def f_twitter():
#-------------- twitter ______________________________________________________
    bearer_token_twitter = "AAAAAAAAAAAAAAAAAAAAADQE3QEAAAAADeOe%2BzRjSpk555QwGcmaFUcVFto%3D4R32iUIpy1zxwzZSsRje2cuuDAgJFv4Bok2fkB9VUsUol1yYvf"
    import tweepy
    import os

    # Define your Twitter API credentials (use environment variables for safety)
    BEARER_TOKEN = bearer_token_twitter  # Set this in your environment

    # Define the current location as latitude,longitude,radius (Twitter's geo search uses this format)

    current_location = "12.9716,77.5946,20km"

    # Define tags/keywords related to abnormal traffic
    TRAFFIC_KEYWORDS = [
        "accident", "collision", "roadblock", "jam", "traffic", "closed", "pileup",
        "fire", "detour", "delay", "incident", "block", "congestion", "snarled",
        "flooded", "heavy traffic", "crash", "breakdown"
    ]

    # Initialize Tweepy client
    client = tweepy.Client(bearer_token=BEARER_TOKEN)

    def search_tweets_near_location(query_keywords, location_query, max_results=50):
        query = " OR ".join(query_keywords) + f" point_radius:[{location_query}]"
        print(f"Running query: {query}")
        response = client.search_recent_tweets(
            query=query,
            max_results=max_results,
            tweet_fields=["created_at", "text", "author_id", "geo"],
            wait_on_rate_limit=True,
        )

        if not response.data:
            print("No relevant tweets found.")
            return []

        return response.data


    def run_tweets_update():
        # Run the search
        tweets = search_tweets_near_location(TRAFFIC_KEYWORDS, current_location)
        # Output the results
        print(f"\n🚨 Found {len(tweets)} potentially abnormal traffic tweets:\n")
        for tweet in tweets:
            print(f"- [{tweet.created_at}] {tweet.text}\n")
    run_tweets_update()
    #_____________________________________________________________________________

# _______________ GNEW AND GOOGLE NEWS API _______________________________________#

import requests
from django.http import JsonResponse
from datetime import datetime, timedelta

def get_gnews_data():
    # GNews API key (get one from gnews.io)
    API_KEY = "1fa1e62b116287da65f72278444bcd13"
    GNEWS_BASE_URL = "https://gnews.io/api/v4/search"

    # Keywords that may indicate traffic-impacting events
    TRAFFIC_KEYWORDS = [
        "accident", "traffic jam", "roadblock", "fire", "flood", "breakdown",
        "congestion", "pile-up", "crash", "snarl", "road closed"
    ]

    fetch_traffic_news(TRAFFIC_KEYWORDS, API_KEY, GNEWS_BASE_URL)

def fetch_traffic_news(TRAFFIC_KEYWORDS, API_KEY, GNEWS_BASE_URL):
    location = "Bengaluru"
    query = " OR ".join(TRAFFIC_KEYWORDS) + f" {location}"

    params = {
        "q": query,
        "lang": "en",
        "country": "in",
        "token": API_KEY,
        "max": 50,
    }

    response = requests.get(GNEWS_BASE_URL, params=params)
    news_data = response.json()

    incident_articles = []
    for article in news_data.get("articles", []):
        incident_articles.append({
            "title": article.get("title"),
            "description": article.get("description"),
            "url": article.get("url"),
            "publishedAt": article.get("publishedAt"),
        })

    print(f"🚨 Found {len(incident_articles)} traffic-related news articles for {location}:\n")
    return JsonResponse({"location": location, "incidents": incident_articles})

# ________________________________________________________________#


# _______________ GOOGLE RSS API _______________________________________#



def scrape_google_news():
    import feedparser
    from urllib.parse import quote
    query = "Bengaluru traffic OR accident OR roadblock OR fire OR flood"
    url = f"https://news.google.com/rss/search?q={query}"

    feed = feedparser.parse(url)
    results = []

    for entry in feed.entries:
        results.append({
            "title": entry.title,
            "link": entry.link,
            "published": entry.published,
            "summary": entry.summary,
        })
    print(f"🚨 Found {len(results)} Google News articles related to traffic:\n")
    return results
