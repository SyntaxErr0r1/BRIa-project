# Application for managing EEG data

- This app is a fullstack web-app solution.
- It can display the EEG data
- And apply data transformation
- Filters low frequencies to eliminate linear drift in the data
- Can apply ICA to remove airtifacts such as muscle, eye blinks, or eye movements
- Calculates EEG Connectivity analysis

# Frontend
- For frontend it Uses Vue.js framework
- It displays the time series of EEG electrodes with/without transformations and filters
- Displays the EEG connectivity analysis

# Backend
- Backend uses Python Flask framework
- Pulls the EEG data from MySQL DB
- Applies the data transformation
