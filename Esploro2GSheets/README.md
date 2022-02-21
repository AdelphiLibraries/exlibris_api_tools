# Esploro2GSheets

Functions in [Google Apps Script](https://developers.google.com/apps-script) to enable the automated extraction of Esploro data to sheets for reporting or analysis.

## Requirements

- Exlibris Developer API Key(s)
- Google Sheets with App Script editor enabled

## How to use

- Set up a sheet document with tabs named for the reports to generate (assets, researchers, agents, files, links).
- Create or use the default App script (Code.gs) with the contents of esploroFunctions.gs.
- In the Files sidebar create another file called config.gs, with the contents containing your institution's API credentials information.
- Make sure the config.gs file is listed in "Files" _before_ (above) the code that refers to it.

### Data storage

The JSON output from the API can be large and slow to harvest at the 100/page max. The function saveAsJSON() is used to save the data at rest within Google Drive. You will need to enable Google Drive in your project for this to work. Currently it saves files 'esploro_assets_data.json' and 'esploro_researchers_data.json' at the root of Drive. They are then read by the "output" functions.

Note: If the harvesting of assets or researchers exceeds the time limit of Google App Scripts (supposedly 5 minutes but seems to allow much longer times in practice), you will need to save partial JSON files and adjust the scripts to concatenate the data.
