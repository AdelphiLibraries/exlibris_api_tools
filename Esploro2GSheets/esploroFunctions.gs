// Esploro API docs: https://developers.exlibrisgroup.com/esploro/apis/

var update_date_from = "2020-01-01";
var limit = 100;
var cursor = 0;

// set API info from adjacent config.gs file
var apiKey = keys.esploroProd;
var baseUrl = urls.esploroUrl;

var researchersDataFile = "esploro_researchers_data.json";
var assetsDataFile = "esploro_assets_data.json";

function harvestEsploroResearchers() {
  // harvest all researcher data from API as a single list of records and save to JSON in Drive.
  var researchers = getEsploroResearchers();
  saveAsJSON(researchers, researchersDataFile);
}

function harvestEsploroAssets() {
  // harvest all assets data from API as a single list of records and save to JSON in Drive.
  var assets = getEsploroAssets();
  saveAsJSON(assets, assetsDataFile);
}

function populateTables() {
  // Populate tables with data from saved JSON files for researchers and assets.
  outputEsploroResearchers();
  outputEsploroAssets();
  outputEsploroAgents();
  outputEsploroFiles();
  outputEsploroLinks();
}

function getEsploroResearchers() {
  // get all researcher data from API as a single list of records.
  var apiUrl = baseUrl + "researchers" + "?apikey=" + apiKey + "&format=json";

  recordCount = getRecordCount("researchers");
  Logger.log(recordCount);

  var records = [];
  Logger.log("Getting records " + (cursor + 1) + " - " + (cursor + limit));
  var newRecords = getRecords(apiUrl, cursor, "user");
  Logger.log("Found " + newRecords.length);
  records.push(...newRecords);

  while (newRecords.length !== 0 && cursor + limit <= recordCount) {
    cursor += limit;
    Logger.log("Getting records " + (cursor + 1) + " - " + (cursor + limit));
    newRecords = getRecords(apiUrl, cursor, "user");
    Logger.log("Found " + newRecords.length);
    Logger.log("Offset: " + cursor);
    records.push(...newRecords);
  }
  return records;
}

function outputEsploroResearchers() {
  // Read researchers from JSON file in Drive and output tabular data to sheet.
  records = loadJSON(researchersDataFile);

  researcherSheet = mySheet("researchers");
  researcherSheet.clear();

  // Headers for researchers table
  appendRows(researcherSheet, [
    [
      "index",
      "primary_id",
      "first_name",
      "last_name",
      "status",
      "is_researcher",
      "link",
    ],
  ]);
  var theData = [];
  records.forEach(function (row, index) {
    // Loop through records and parse out data into tabular form
    rowData = parseResearcher(row, index);
    Logger.log(rowData);
    theData.push(rowData);
  });
  appendRows(researcherSheet, theData);
}

function getEsploroAssets() {
  // harvest all asset data from API as a single list of records.
  var apiUrl =
    baseUrl +
    "assets" +
    "?update_date_from=" +
    update_date_from +
    "&apikey=" +
    apiKey +
    "&format=json";

  var records = [];
  Logger.log("Getting records " + (cursor + 1) + " - " + (cursor + limit));
  var newRecords = getRecords(apiUrl, cursor, "records");
  records.push(...newRecords);

  Logger.log("Found " + newRecords.length);

  while (newRecords.length !== 0) {
    cursor += limit;
    Logger.log("Getting records " + (cursor + 1) + " - " + (cursor + limit));
    newRecords = getRecords(apiUrl, cursor, "records");
    Logger.log("Found " + newRecords.length);
    Logger.log("Offset: " + cursor);
    records.push(...newRecords);
  }

  return records;
}

function outputEsploroAssets() {
  // Read assets from JSON file in Drive and output tabular data to sheet.
  records = loadJSON(assetsDataFile);

  assetSheet = mySheet("assets");
  assetSheet.clear();

  // Headers for assets table
  appendRows(assetSheet, [
    [
      "index",
      "mms_id",
      "title",
      "publisher",
      "identifier.doi",
      "identifier.pmid",
      "date.published",
      "resourcetype.esploro",
      "openaccess",
      "peerreview",
      "portalVisibilty",
      "profileVisibility",
      "has_link",
      "has_file",
      "asset.views",
      "depositStatus",
      "creator1",
      "asset.affiliation",
      "discipline.summon",
      "local.note1",
      "local.note2",
      "local.note3",
    ],
  ]);

  var theData = [];
  records.forEach(function (row, index) {
    // Loop through records and parse out data into tabular form
    rowData = parseAsset(row, index);
    Logger.log(rowData);
    theData.push(rowData);
  });
  appendRows(assetSheet, theData);
}

function outputEsploroAgents() {
  records = loadJSON(assetsDataFile);

  agentSheet = mySheet("agents");

  agentSheet.clear();

  // Headers for agents table
  appendRows(agentSheet, [
    [
      "mms_id",
      "title",
      "type",
      "order",
      "isDisplayInPublicProfile",
      "name",
      "user.primaryId",
      "almaUserId",
      "affiliationWithDesc",
    ],
  ]);
  var theData = [];

  records.forEach(function (row, index) {
    if (row.hasOwnProperty("creators")) {
      var creators = parseAgents(row, "creators");
      Logger.log(creators);
      theData.push(...creators);
    }
    if (row.hasOwnProperty("contributors")) {
      var contributors = parseAgents(row, "contributors");
      Logger.log(contributors);
      theData.push(...contributors);
    }
  });
  appendRows(agentSheet, theData);
}

function outputEsploroLinks() {
  records = loadJSON(assetsDataFile);

  linksSheet = mySheet("links");

  linksSheet.clear();

  // Headers for agents table
  appendRows(linksSheet, [
    ["mms_id", "link.url", "linkTypeWithDesc", "link.type", "link.rights"],
  ]);
  var theData = [];

  records.forEach(function (row, index) {
    if (row.hasOwnProperty("links")) {
      var links = parseLinks(row, "links");
      Logger.log(links);
      theData.push(...links);
    }
  });
  appendRows(linksSheet, theData);
}

function outputEsploroFiles() {
  records = loadJSON(assetsDataFile);
  filesSheet = mySheet("files");
  filesSheet.clear();

  // Headers for files table
  appendRows(filesSheet, [
    ["mms_id", "fileDownloadUrl", "file.name", "file.creationDate", "mimeType"],
  ]);
  var theData = [];

  records.forEach(function (row, index) {
    if (row.hasOwnProperty("files")) {
      var files = parseFiles(row, index);
      // Logger.log(files);
      theData.push(...files);
    }
  });
  Logger.log(theData);
  appendRows(filesSheet, theData);
}

function getRecords(url, offset, key) {
  // general function to fetch a set of records.
  var apiUrl = url + "&offset=" + offset + "&limit=" + limit;
  Logger.log(apiUrl);
  var response = UrlFetchApp.fetch(apiUrl);
  var json = response.getContentText();
  var data = JSON.parse(json);

  return data[key];
}

function parseResearcher(record, index) {
  try {
    rowData = [
      index,
      prop(record, "primary_id"),
      prop(record, "first_name"),
      prop(record, "last_name"),
      prop(prop(record, "status"), "value"),
      prop(record, "is_researcher"),
      prop(record, "link"),
    ];
  } catch (err) {
    rowData = [index];
  }
  return rowData;
}

function parseAsset(record, index) {
  // Put the parsing logic to turn a record into a table row here

  try {
    rowData = [
      index,
      prop(prop(record, "originalRepository"), "assetId"),
      prop(record, "title"),
      prop(record, "publisher"),
      prop(record, "identifier.doi"),
      prop(record, "identifier.pmid"),
      prop(record, "date.published"),
      prop(record, "resourcetype.esploro"),
      prop(record, "openaccess"),
      prop(record, "peerreview"),
      prop(record, "portalVisibility"),
      prop(record, "profileVisibility"),
      prop(record, "links") !== null ? "Y" : "N",
      prop(record, "files") !== null ? "Y" : "N",
      prop(record, "asset.views"),
      prop(prop(record, "depositStatusWithDesc"), "value"),
      prop(prop(prop(record, "creators"), 0), "creatorname"),
      concat(prop(record, "asset.affiliation")),
      concat(prop(record, "discipline.summon")),
      prop(prop(record, "local.fields"), "local.note1"),
      prop(prop(record, "local.fields"), "local.note2"),
      prop(prop(record, "local.fields"), "local.note3"),
    ];
  } catch (err) {
    rowData = [index];
  }
  return rowData;
}

function parseAgents(data, type) {
  //
  var result = [];
  var mmsid = prop(prop(data, "originalRepository"), "assetId");
  var title = prop(data, "title");
  if (data.hasOwnProperty(type)) {
    data[type].forEach(function (row) {
      row_data = [
        mmsid,
        title,
        type,
        prop(row, "order"),
        prop(row, "isDisplayInPublicProfile"),
        // get either creator or contributor name, not both
        prop(row, "creatorname")
          ? prop(row, "creatorname")
          : prop(row, "contributorname"),
        prop(row, "user.primaryId"),
        prop(row, "almaUserId"),
        sanitize(prop(prop(prop(row, "affiliationWithDesc"), 0), "value")),
      ];

      result.push(row_data);
    });
  }
  return result;
}

function parseLinks(data, index) {
  //
  var result = [];
  var mmsid = prop(prop(data, "originalRepository"), "assetId");
  if (data.hasOwnProperty("links")) {
    data["links"].forEach(function (row) {
      row_data = [
        mmsid,
        prop(row, "link.url"),
        prop(prop(row, "linkTypeWithDesc"), "desc"),
        prop(row, "link.type"),
        prop(row, "link.rights"),
      ];
      result.push(row_data);
    });
  }
  Logger.log(result);
  return result;
}
function parseFiles(data, index) {
  //
  var result = [];
  var mmsid = prop(prop(data, "originalRepository"), "assetId");
  if (data.hasOwnProperty("files")) {
    data["files"].forEach(function (row) {
      row_data = [
        mmsid,
        prop(row, "fileDownloadUrl"),
        prop(row, "file.name"),
        prop(row, "file.creationDate"),
        prop(row, "file.mimeType"),
      ];
      result.push(row_data);
    });
  }
  Logger.log(result);
  return result;
}

function concat(stuff) {
  if (Array.isArray(stuff)) {
    return stuff.join("; ");
  }
}

function mySheet(name) {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  return ss.getSheetByName(name);
}

function appendRows(sheet, data) {
  var row_range = sheet.getRange(
    sheet.getLastRow() + 1,
    1,
    data.length,
    data[0].length
  );
  row_range.setValues(data);
}

function prop(record, key) {
  // extract property if it exists, without throwing errors if doesn't exist
  if (record !== null) {
    if (record.hasOwnProperty(key)) {
      return record[key];
    } else {
      return null;
    }
  } else {
    return null;
  }
}

function sanitize(str) {
  // strip out carriage returns from strings
  if (str !== null) {
    return str.replace(/\r?\n|\r/g, "");
  } else {
    return null;
  }
}

function getRecordCount(endpoint) {
  // get the total record count of set
  if (endpoint == "researchers") {
    var apiUrl =
      baseUrl +
      endpoint +
      "?apikey=" +
      apiKey +
      "&offset=0&limit=1&format=json";
    var countKey = "total_record_count";
  } else if (endpoint == "assets") {
    var apiUrl =
      baseUrl +
      endpoint +
      "?apikey=" +
      apiKey +
      "&offset=0&limit=1&format=json" +
      "&update_date_from=" +
      update_date_from;
    var countKey = "totalRecordCount";
  } else {
    return null;
  }
  var response = UrlFetchApp.fetch(apiUrl);
  var json = response.getContentText();
  var data = JSON.parse(json);

  return parseInt(data[countKey]);
}

function saveAsJSON(obj, fileName) {
  // borrowed from https://stackoverflow.com/questions/52777524/how-to-save-a-json-file-to-google-drive-using-google-apps-script
  // TODO: find way to save to a folder.
  var blob, file, fileSets, obj;

  var parentFolder = DriveApp.getFolderById(
    "1wRt9fLwx7DKgv_gNkKQBm_WJPJJ3Iz-Y"
  );

  fileSets = {
    title: fileName,
    mimeType: "application/json",
  };

  blob = Utilities.newBlob(
    JSON.stringify(obj),
    "application/vnd.google-apps.script+json"
  );
  file = Drive.Files.insert(fileSets, blob);
  Logger.log(
    "ID: %s, File size (bytes): %s, type: %s",
    file.id,
    file.fileSize,
    file.mimeType
  );
  return file.id;
}

function loadJSON(fileName) {
  // Load file from Drive by name.
  // TODO: find way to get from within a folder
  var files = DriveApp.getFilesByName(fileName);
  if (files.hasNext()) {
    var file = files.next();
    var content = file.getBlob().getDataAsString();
    var json = JSON.parse(content);
    return json;
  }
}

function test() {
  //   x = getEsploroResearchers();

  Logger.log(x);
}
