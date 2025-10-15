import requests

def get_weather(city_name):
    try:
        url = f"https://wttr.in/{city_name}?format=j1"
        response = requests.get(url)
        data = response.json()

        current = data["current_condition"][0]
        temp = current["temp_C"]
        desc = current["weatherDesc"][0]["value"]

        return f"Температура: {temp}°C, {desc}"
    except Exception as e:
        return "Не удалось получить погоду. Проверь
print(response.url)
print(response.text)
