# Day Trade Logging App
A lightweight Python GUI app for tracking daily trades and trade performance.

## Features
- easy to log your trades through out or during the day
- can be exported to json, csv and text
- simple GUI

## Usage
after downloading the latest final_version.
by going to,
```bash
project\final_version\
```
```bash
python app.py
```
or create a .exe of app.py
```bash
pyinstaller --onefile --add-data "icons;icons" --add-data "config.json;." app.py
```


## Built with
Python

## Demo
<img width="1366" height="768" alt="Screenshot (14)" src="https://github.com/user-attachments/assets/099eed12-e459-4e10-af95-ee855b6d807f" />

##Important Note
- the api feature is available after the Flask is online.

## Files
- app.py  -main file
- util.py  -GUI file
- config.json


## Roadmap
- [x] Basic Trade logging
- [x] export for '.txt', '.json' and '.csv'
- [x] Add `.exe` build
- [x] API integration
- [ ] excel export
- [ ] obsidian export
