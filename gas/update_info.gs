// ツイートを収集したスプレッドシートから完売した店舗名を取得
function getSoldOutStoreName() {
  // スプレッドシートのIDをもとにシートを読み込む
  let tweetSpreadsheet = SpreadsheetApp.openById("StoaredTweetSpreadSheetID");
  let tweetSheet = tweetSpreadsheet.getSheetByName("シート1");

  // ツイートを収集したスプレッドシートの最終行を取得
  let tweetSheetLastRow = tweetSheet.getLastRow();

  // C列に格納されているツイート文字列を取得
  let tweetArray = tweetSheet.getRange(1, 3, tweetSheetLastRow).getValues()

  // 店舗名を格納する配列を定義
  let storeNameArray = new Array();
  for (let i = 0; i < tweetArray.length ; i++){
    if(tweetSheet.getRange(i + 1, 6).getValue() == ""){
      let tweetText = tweetArray[i][0]
      // 改行でツイート文字列を分割し、店舗名にあたる行を取得
      let splitTweetTextArray =tweetText.split(/\r\n|\n/);
      for (let j = 3; j < splitTweetTextArray.length ; j++){
        if (splitTweetTextArray[j].includes("◯")){
          let storeName = splitTweetTextArray[j].split(" ")[1];
          console.log(storeName + "のカスタムステンレスボトルセット完売情報ツイートを取得")
          // 店舗名の配列に格納
          storeNameArray.push(storeName)
          // E列にUpdatedと書き込む
          tweetSheet.getRange(i + 1, 6).setValue("Updated")
        }
      }
    }
  }
 return storeNameArray;
}


// 販売状況を更新
function updateSalesSituation(sheet, storeNameArray) {
  // 格納されているデータすべてをデータとして保持
  let data = sheet.getDataRange().getValues();
  for (let i = 0; i < storeNameArray.length ; i++){
    for (let j = 2; j < data.length ; j++){
      // A列j行目(店舗名)のデータを取得
      let storeName = data[j][0];
      // ツイートから取得した店舗名がA列j行目の中に含まれている場合
      if(storeName.includes(storeNameArray[i])){
        // F列j行目のセルが「販売中」の場合は、「完売」に書き換え
        if(data[j][7] == "販売中"){
          sheet.getRange(j+1, 8).setValue("完売")
          SpreadsheetApp.flush();
          console.log(storeNameArray[i] + "のカスタムステンレスボトルセットを「販売中」から「完売」に更新")
        }
      }
    }
  }
}


// folium版のスプレッドシートを読み込み、getStoreName関数の返り値をもとに編集
function updateMyMapSpreadSheet(storeNameArray) {
  // folium版の店舗情報スプレッドシートを読み込む
  let StoreInfoSpreadsheet = SpreadsheetApp.openById("StoreInomationSpreadSheetID");
  let StoreInfoSheet = StoreInfoSpreadsheet.getSheetByName("シート1");

  console.log("グッズ販売状況を確認中...")
  updateSalesSituation(StoreInfoSheet, storeNameArray)

}

// 実行部
function main() {
  let storeNameArray = getSoldOutStoreName()
  if(storeNameArray.length > 0) {
    updateMyMapSpreadSheet(storeNameArray)
  }
  else {
    console.log("この時間の更新はありませんでした。")
  }
}
