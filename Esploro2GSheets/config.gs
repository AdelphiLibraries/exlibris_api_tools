// File to hold API-specific information.
// Make sure this file is listed in "Files" before the code that refers to it.

var keys = {
  esploroProd: "xxxxxxxxxxxxxxxxxxx",
  esploroTest: "xxxxxxxxxxxxxxxxxxx",
};

var urls = {
  esploroUrl: "https://api-na.hosted.exlibrisgroup.com/esploro/v1/",
};

//// Some variables for global use.
var update_date_from = "2020-01-01";
var limit = 100;
var cursor = 0;

var dataFolderID = "xxxxxxxxxxxxxxxxxxxxxxx"; // the ID of folder where JSON data is saved.
var researchersDataFile = "esploro_researchers_data.json"; // name of researcher JSON file
var assetsDataFile = "esploro_assets_data.json"; // name of assets JSON file
