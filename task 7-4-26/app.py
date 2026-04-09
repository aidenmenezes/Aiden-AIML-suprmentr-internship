import streamlit as st
from openai import OpenAI
import requests
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

def get_weather(city):

    geocoding_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=en&format=json"
    
    try:
        geo_response = requests.get(geocoding_url).json()
        
        if not geo_response.get("results"):
            return f"City '{city}' not found"
        
        location = geo_response["results"][0]
        latitude = location["latitude"]
        longitude = location["longitude"]
        country = location.get("country", "")

        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,weather_code,wind_speed_10m&temperature_unit=celsius"
        weather_response = requests.get(weather_url).json()
        
        current = weather_response.get("current", {})
        temp = current.get("temperature_2m", "N/A")
        wind_speed = current.get("wind_speed_10m", "N/A")
        
        return f"Weather in {city}, {country}: {temp}°C, Wind: {wind_speed} km/h"
    except Exception as e:
        return f"Error fetching weather: {str(e)}"

def read_file(file_path):
    try:
        with open(file_path, "r") as f:
            return f.read()
    except:
        return "Error reading file"


def smart_agent(user_input):
    
    if "weather" in user_input.lower():
        city = user_input.split("in")[-1].strip()
        return get_weather(city)
  
    elif "read file" in user_input.lower():
        file_path = user_input.split("read file")[-1].strip()
        return read_file(file_path)
    
 
    else:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are a smart assistant."},
                {"role": "user", "content": user_input}
            ]
        )
        return response.choices[0].message.content


st.title("Smart Agent with Tools")

query = st.text_input("Enter your query:")

if query:
    result = smart_agent(query)
    st.write("Response:")
    st.write(result)