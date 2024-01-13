# Analytics-2-Gsheet

Functions in [Google Apps Script](https://developers.google.com/apps-script) to enable the automated extraction of analytics data from Alma or Esploro for reporting or analysis.

Note: This code is appreciatively forked from the GWU's [alma-analytics-sheets](https://github.com/gwu-libraries/alma-analytics-sheets) project. The most notable change is switching the data write to use Google Advanced Services for better performance and to avoid timeouts for large tables.

## Requirements

- Exlibris Developer API Key(s) with read permissions for analytics (either Alma or Esploro)
- Google Sheets with Apps Script editor enabled
- Google Sheets API service enabled from within the Apps Script project. In the code editor select Services, and then Sheets API. This will make the API avaible via the Sheets class.

## How to use

- Set up a sheet document with tabs named for the reports to generate.
- Create a tab called "reports" (or another name as defined in config.gs, see below)
  - In the "reports" tab use columns "reportPath" and "spreadsheetTab"
  - For each analytics report, put its path (as discoverable in Analytics) in the first column and the destination tab name in the second.
- In the Files sidebar of Apps Script editor add a new script file called "analytics.gs", with the contents from the file in this repo (note, the editor adds ".gs" automatically, so just name it "analytics").
- Add another file called "config.gs", with the contents modified with your institution's API credentials information. You can also customize other aspects of the sheet here such as column labels.
  - Make sure the config.gs file is listed in "Files" _before_ (above) the code that refers to it. This ensures that the needed variables are defined ahead of the main script execution.
- When things are set up as needed, select the "main" function and run it. The first time you execute you will need to authorize script access to the sheet.
- Note that the order of analytics columns may differ from what you see in Alma or Esploro Analytics. This seems to be unavoidable as the XML output from the API does not always reflect the display order of columns.

## Automation

Report harvesting can be automated by setting up a timed trigger in your Apps Script project. Find "Triggers" in the Apps Script sidebar.
