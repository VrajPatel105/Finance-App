import requests
import streamlit as st
import datetime
import pandas as pd


st.title('News')
# alpha vantage api key -> EQ7QE7SLEI6EDE4K


url = 'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&symbol=IBM&interval=5min&apikey=EQ7QE7SLEI6EDE4K'
r = requests.get(url)
data = r.json()

news = data

# feed->i->title, url, time_published, authors, summary, banner_image, source_domain, topics(i->topic) , 
# overall_sentiment_score, overall_sentiment_label, ticker_sentiment (ticker, relevance_score,  ticker_sentiment_score, ticker_sentiment_label)


if news:
    for item in news:
        with st.container():
            col1, col2 = st.columns([7,3])  # 70% for text, 30% for image
            
            with col1:
                # Clean up the title and remove any special text
                title = item.get('title', '')
                
                # Clean up the summary - safely handle None values
                summary = item.get('summary', '')
                if summary:  # Only process if summary exists
                    summary = summary.replace('In This Article:', '').replace('\n', ' ').strip()
                else:
                    summary = "No summary available."
                
                topics = item.get('topic')
                
                # Use the published time from the news item instead of current time
                published_time = item.get('time_published', datetime.now().strftime('%Y-%m-%d %H:%M'))
                
                st.markdown(f"""
                ### {title}
                <p style="color: #666; font-size: 0.8em;">{published_time}</p>
                
                {summary}
                
                <a href="{item.get('link', '#')}" target="_blank" style="color: #3b82f6; text-decoration: none;">Read Article</a>
                """, unsafe_allow_html=True)
            
            if item.get('banner_image'):
                with col2:
                    st.image(item['banner_image'], use_container_width=True)
            
            st.markdown("<hr style='margin: 2rem 0; opacity: 0.2;'>", unsafe_allow_html=True)
else:
    st.info(f"No recent news available")