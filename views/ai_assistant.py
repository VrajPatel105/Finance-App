import streamlit as st
from openai import OpenAI
import yfinance as yf
from PIL import Image

class Assistant:
    def __init__(self):
        self.api_key = st.secrets["OPENAI_API_KEY"]
        # Initializing the client..
        self.openai_client = OpenAI(api_key=self.api_key)

# getting data from yfinance
    def get_market_data(self, symbol):
        try:
            stock = yf.Ticker(symbol)
            info = stock.info
            price = info.get('currentPrice', 0)
            change = info.get('regularMarketChangePercent', 0)
            volume = info.get('volume', 0)
            
            price_str = f"${price:.2f}" if isinstance(price, (int, float)) else "N/A"
            change_str = f"{change:.2f}%" if isinstance(change, (int, float)) else "N/A"
            volume_str = f"{volume:,}" if isinstance(volume, (int, float)) else "N/A"
            
            return {
                "price": price_str,
                "change": change_str,
                "volume": volume_str
            }
        except Exception as e:
            print(f"Error fetching data: {e}")
            return None

    def enhance_prompt(self, prompt, symbol):
        if data := self.get_market_data(symbol):
            return f"""Current {symbol} data:
Price: {data['price']} | Change: {data['change']} | Volume: {data['volume']}

Question: {prompt}"""
        return prompt

    @staticmethod
    def apply_styling():
        st.markdown("""
            <style>
            .stApp {
                background-color: #1E1E1E;
                color: #FFFFFF;
            }
            
            .stTitle {
                font-size: 2rem !important;
                font-weight: 500 !important;
                padding-bottom: 20px !important;
                color: #FFFFFF !important;
            }
            
            .block-container {
                background-color: transparent !important;
            }
            
            div[data-testid="stToolbar"] {
                display: none;
            }
            
            .stChatMessage {
                background-color: #2D2D2D !important;
                border-radius: 15px !important;
                padding: 15px !important;
                border: 1px solid #3D3D3D !important;
                margin: 10px 0 !important;
            }
            
            [data-testid="stChatInput"] {
                border-color: #4D4D4D !important;
                background-color: #2D2D2D !important;
                color: #FFFFFF !important;
                border-radius: 10px !important;
            }
            
            .stTextInput input {
                background-color: #2D2D2D !important;
                border: 1px solid #3D3D3D !important;
                color: #FFFFFF !important;
            }
            
            </style>
        """, unsafe_allow_html=True)

    @staticmethod
    def init_chat_history():
        return [{
            "role": "system",
            "content": """You are an experienced trading assistant. Provide concise market analysis with clear rationales. 
            Include brief disclaimers for any market-related advice. Focus on technical analysis, market trends, 
            and risk assessment. Be direct but professional."""
        }, {
            "role": "assistant",
            "content": f"""Welcome {st.session_state.user['name']}. I can assist you in several ways:

1. Market Analysis: I'll analyze current market conditions and trends

2. Stock Research: Enter any stock symbol, and I'll provide:
• Current price and volume data
• Technical analysis
• Market sentiment insights

3. Risk Assessment: I'll help identify potential risks and market factors

Remember to enter a stock symbol in the input field above to get specific analysis."""
        }]

    def run(self):
            
        col1, col2 = st.columns([0.05, 0.92])
        with col1:
            # This is just to alight the symblo and the text in one line.
            st.write("  ")
            image = Image.open('resources/finch.ico')
            st.image(image, width=50)
        with col2:
            st.title("Finch Assistant")
                    
        # Firstly we have to applyt the styling                    
        self.apply_styling()
        
        # checking the messages in the session state
        if "messages" not in st.session_state:
            st.session_state.messages = self.init_chat_history()
        
        col1, col2 = st.columns([2, 3])
        with col1:
            symbol = st.text_input("Stock Symbol:", key="symbol_input")
            
        # THis will display all the messages in the session state.
        for message in st.session_state.messages:
            if message["role"] != "system":
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])
        
        # := this is walrus operator. used for assignment withing the if statement
        if prompt := st.chat_input("Ask about market analysis..."):
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # enhancing the prompt more to get better response from model (gpt4)
            enhanced_prompt = self.enhance_prompt(prompt, symbol.upper()) if symbol else prompt
            st.session_state.messages.append({"role": "user", "content": enhanced_prompt})
            
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                try:
                    # calling the api
                    stream = self.openai_client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=st.session_state.messages,
                        stream=True
                    )
                    
                    full_response = ""
                    for chunk in stream:
                        if chunk.choices[0].delta.content is not None:
                            full_response += chunk.choices[0].delta.content
                            message_placeholder.markdown(full_response + "▌")
                    message_placeholder.markdown(full_response)
                    
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": full_response
                    })
                    
                except Exception as e:
                    st.error(f"Error: {str(e)}")