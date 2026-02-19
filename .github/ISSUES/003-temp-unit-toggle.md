# Add Celsius/Fahrenheit toggle with persistence

**Summary**
Add a UI toggle to switch temperature units between Celsius and Fahrenheit. Persist the user's choice across sessions.

**Motivation**
Some users prefer Fahrenheit; providing a toggle makes the app more usable internationally.

**Acceptance criteria**
- Add a toggle in the UI to switch between `°C` and `°F`.
- Convert all displayed temperatures (current and forecast) when the unit is changed.
- Persist the preference using `localStorage` or cookies.
- Ensure the default stays metric if no preference is set.

**Notes**
Implement unit conversion in `app.py` (server-side) or in `script.js` (client-side). If server-side, send unit preference with the form; if client-side, fetch metric and convert in JS.

**Labels:** enhancement, ux
