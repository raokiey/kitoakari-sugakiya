function geocoder() {
  let START_ROW = 2;
  let FACILITY_COL = 1;
  let LAT_COL = 10;
  let LNG_COL = 11;
 
  let StoreSpreadsheet = SpreadsheetApp.openById("StoreInomationSpreadSheetID");
  let StoreSheet = StoreSpreadsheet.getSheetByName("シート1");
  let lastrow = StoreSheet.getLastRow();
  
  for(let i=START_ROW; i<=lastrow; i++){
    var facility = StoreSheet.getRange(i,FACILITY_COL).getValue();

    var geocoder = Maps.newGeocoder();
    geocoder.setLanguage('ja');

    var response = geocoder.geocode(facility);

    if(response['results'][0] != null){
      StoreSheet.getRange(i,LAT_COL).setValue(response['results'][0]['geometry']['location']['lat']);
      StoreSheet.getRange(i,LNG_COL).setValue(response['results'][0]['geometry']['location']['lng']);
    }
    else {
      console.log(facility + "のジオコーディングに失敗しました。")
    }
  }
}
