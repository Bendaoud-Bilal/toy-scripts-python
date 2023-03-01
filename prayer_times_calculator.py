# Problem: Daily prayer times from the Aladhan API
# Request the prayer timetable of a city (Ouargla, Algeria; calculation method
# 3) from the public Aladhan API and print the timings of the first day of the
# month.
# Context: Personal practice / experiment


city = "Ouargla"
country = "Algeria"
method = 3  # Calculation method (3 for Algeria)
url = f"https://api.aladhan.com/v1/calendarByCity?city={city}&country={country}&method={method}"

response =get(url)
data = response.json()

# Extracting prayer times from the response
prayer_times = data["data"][0]["timings"]

for prayer, time in prayer_times.items():
    print(f"{prayer}: {time}")
