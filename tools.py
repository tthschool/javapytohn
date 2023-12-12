

from pyowm import OWM
import json
import yfinance as yf
owm = OWM("47d996ad143356bd7a443d082e4ae264")
mgr = owm.weather_manager()


tools_list = [{
    "type": "function",
    "function": {

        "name": "get_stock_price",
        "description": "Retrieve the latest closing price of a stock using its ticker symbol",
        "parameters": {
            "type": "object",
            "properties": {
                "symbol": {
                    "type": "string",
                    "description": "The ticker symbol of the stock"
                }
            },
            "required": ["symbol"]
        }
    }
},
{
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the current weather",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The name of , city for example Hanoi",
                    },
                },
                "required": ["location"],
            },
        }
    }
]

def get_stock_price(symbol: str) -> float:
    stock = yf.Ticker(symbol)
    price = stock.history(period="1d")['Close'].iloc[-1]
    return price
def get_weather(city):
    observation = mgr.weather_at_place(city)
    resul = observation.weather
    status = []
    detail_status = resul.detailed_status  
    temperature = resul.temperature('celsius')
    status.append({
        "detailed status":detail_status,
        "tamperatue" :temperature
    })
    return status