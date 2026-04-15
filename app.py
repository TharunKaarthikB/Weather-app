from flask import Flask, render_template, request
import requests
from datetime import datetime

app = Flask(__name__)

API_KEY = "7f7879f0ac8acc3cbc67978dcec61532"

@app.route("/", methods=["GET", "POST"])
def home():
    weather = None
    bg_class = "default"

    if request.method == "POST":
        city = request.form.get("city")

        if city:
            city = city.strip()

            url = "http://api.openweathermap.org/data/2.5/weather"
            params = {
                "q": city + ",IN",
                "appid": API_KEY,
                "units": "metric"
            }

            response = requests.get(url, params=params)
            data = response.json()

            print(data)  # debug

            if response.status_code == 200:
                weather = {
                    "city": data["name"],
                    "temp": data["main"]["temp"],
                    "feels": data["main"]["feels_like"],
                    "desc": data["weather"][0]["description"],
                    "icon": data["weather"][0]["icon"],
                    "humidity": data["main"]["humidity"],
                    "wind": data["wind"]["speed"],
                    "pressure": data["main"]["pressure"],
                    "visibility": round(data.get("visibility", 0) / 1000, 1),
                    "sunrise": datetime.fromtimestamp(data["sys"]["sunrise"]).strftime("%I:%M %p"),
                    "sunset": datetime.fromtimestamp(data["sys"]["sunset"]).strftime("%I:%M %p")
                }

                # 🎨 Dynamic background
                condition = data["weather"][0]["main"].lower()

                if "clear" in condition:
                    bg_class = "sunny"
                elif "cloud" in condition:
                    bg_class = "cloudy"
                elif "rain" in condition:
                    bg_class = "rainy"

            else:
                weather = {"error": data.get("message", "City not found")}

    return render_template("index.html", weather=weather, bg_class=bg_class)


if __name__ == "__main__":
    app.run(debug=True)