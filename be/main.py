from fastapi import FastAPI,Query
from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langchain.tools import tool
import requests
from dotenv import  load_dotenv
import os

load_dotenv()
app=FastAPI()

OPENWEATHER_API_KEY=os.getenv("OPENWEATHER_API_KEY")

llm=ChatGroq(
    model="llama-3.3-70b-versatile",
    
    api_key=os.getenv("GROQ_API_KEY")
)



@tool
def get_temp_details(city:str):
    """
    this is to get city details
    """
    #print(type(city))

    res=requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}")
    
    data=res.json()
    return data

agent=create_agent(
    model=llm,
    tools=[get_temp_details]#return
)

@app.get("/")
def home():
    return {"status": "running"}


# @app.post("/get_weather")
# def incoming_weather_parameters(
#     city:str=Query(...),
#     question:str=Query(...)):
#     result=agent.invoke({
#         "messages":[{"role":"user","content":f"city:{city} question:{question}" }]

#     })
#     return result

@app.post("/get_weather")
def incoming_weather_parameters(
    city: str = Query(...),
    question: str = Query(...)
):
    try:
        result = agent.invoke({
            "messages": [
                {
                    "role": "user",
                    "content": f"city:{city} question:{question}"
                }
            ]
        })

        return result

    except Exception as e:
        return {"error": str(e)}