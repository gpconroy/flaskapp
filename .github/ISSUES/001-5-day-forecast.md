# Add 5-Day Weather Forecast view

**Summary**
Add a 5-day weather forecast to the app that displays daily high/low temperatures, weather condition icons, and short descriptions for each day.

**Motivation**
Users can plan ahead if they can see the forecast for the next few days. The current app only shows current conditions.

**Acceptance criteria**
- Fetch and display a 5-day forecast for the searched city using the Open-Meteo API.
- Show date, high/low temperatures, weather icon, and short description for each day.
- Mobile-responsive layout and accessible labels.
- Unit tests or manual test steps documented in the issue.

**Notes**
Open-Meteo supports daily forecast parameters; update `app.py` to request daily highs/lows and render them in `weather.html` or a new partial.

**Labels:** enhancement, api
