# Importing all the necessary libraries and functions.
import streamlit as st
from openai import OpenAI # Since it's a chatbot, we are using openai's api.
import yfinance as yf
from PIL import Image # This is just to laod the Finch logo in the chat bot.


# For this assistant, we are prompt engineering the ticker that the user will enter. 
# We will fetch the ticker's detailed info from yfinance 
# Once we get the detailed info, we can pass it to the LLM ( Open ai model) as an input
# This will provide precise response from the LLM
# here we are using the GPT-4o mini LLM


# Creating a class
class Assistant:
    # Constructor for initializing the api key and the client.
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

    # Function for enhancing the prompt by using the ticker's data that we fetched from yfinance.
    def enhance_prompt(self, prompt, symbol):
        if data := self.get_market_data(symbol):
            return f"""Current {symbol} data:

            
Price: {data['price']} | Change: {data['change']} | Volume: {data['volume']}

# Question prompt.
Question: {prompt}"""
        return prompt

    # Applying the styling, black purple theme.
    @staticmethod
    def apply_styling():
        st.markdown("""
            <style>
            .stApp {
                background-color: #000000;
                color: #E2E8F0;
            }
            
            .stTitle {
                font-size: 2.2rem !important;
                font-weight: 600 !important;
                background: linear-gradient(to right, #E2E8F0, #A855F7);
                -webkit-background-clip: text !important;
                -webkit-text-fill-color: transparent !important;
                margin-bottom: 30px !important;
            }
            
            /* Chat Messages */
            .stChatMessage {
                background: #1F1F1F !important;
                border: 1px solid rgba(168, 85, 247, 0.2) !important;
                border-radius: 12px !important;
                padding: 20px !important;
                margin: 15px 0 !important;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1) !important;
            }
            
            .stChatMessage:hover {
                border-color: rgba(168, 85, 247, 0.4) !important;
                box-shadow: 0 0 15px rgba(168, 85, 247, 0.1) !important;
            }
            
            /* Input Fields */
            [data-testid="stChatInput"] {
                border: 1px solid rgba(168, 85, 247, 0.3) !important;
                background-color: #1F1F1F !important;
                border-radius: 10px !important;
                color: #E2E8F0 !important;
                padding: 12px !important;
            }
            
            [data-testid="stChatInput"]:focus {
                border-color: #A855F7 !important;
                box-shadow: 0 0 10px rgba(168, 85, 247, 0.2) !important;
            }
            
            .stTextInput input {
                background-color: #1F1F1F !important;
                border: 1px solid rgba(168, 85, 247, 0.3) !important;
                color: #E2E8F0 !important;
                border-radius: 8px !important;
                padding: 8px 12px !important;
            }
            
            .stTextInput input:focus {
                border-color: #A855F7 !important;
                box-shadow: 0 0 10px rgba(168, 85, 247, 0.2) !important;
            }
            
            /* Hide Toolbar */
            div[data-testid="stToolbar"] {
                display: none;
            }
            
            /* Animations */
            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(10px); }
                to { opacity: 1; transform: translateY(0); }
            }
            
            .stChatMessage {
                animation: fadeIn 0.3s ease-out;
            }
            </style>
        """, unsafe_allow_html=True)

    # Function for storing the user's chat history
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
                    
        # Firstly we have to apply the styling                    
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
