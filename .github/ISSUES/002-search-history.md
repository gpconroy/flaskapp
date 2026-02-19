# Add Search History for recent cities

**Summary**
Save recently searched cities and surface them as quick-access buttons on the main page.

**Motivation**
Improve UX by letting users quickly re-open recent searches without typing.

**Acceptance criteria**
- Store the last 5 (configurable) searched city names in `localStorage` or server-side session.
- Display them as buttons on the index page; clicking a button performs the search.
- Provide a "Clear history" option.
- Persist across page reloads and respect privacy (no additional telemetry).

**Notes**
Prefer client-side `localStorage` for simplicity; add small UI in `index.html` and update `script.js`.

**Labels:** enhancement, ux
