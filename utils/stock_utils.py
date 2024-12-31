import plotly.graph_objects as go

# Function for creating a candelstick chart
def create_stock_chart(data, symbol):
    fig = go.Figure(data=[go.Candlestick(x=data.index,
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                close=data['Close'])])  # Here the open, high, low and close are inbuild functiosn offered by plotly. 

    # To update the layout
    fig.update_layout(
        title=f'{symbol} Stock Price',
        yaxis_title='Price',
        template='plotly_dark',
        xaxis_rangeslider_visible=False
    )
    # this will return the plotted figure
    return fig