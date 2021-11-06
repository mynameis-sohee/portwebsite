let HarborLatArray = [35.528672, 35.526908, 35.522900, 35.52172551482321, 35.519438, 35.517193,35.516049,35.513676,35.511872,35.507374,35.496572]
let HarborLonArray = [129.375364, 129.373515, 129.373701, 129.37551417157238, 129.374956, 129.376094,129.386027,129.386098,129.386128,129.387898,129.382026]
let HarborName = ['제1부두', '제2부두', '제3부두', '제4부두', '제5부두', '제6부두','제7부두','제8부두','제9부두','일반부두','양곡부두']
let HarborMainCode = ['MB1', 'MB2', 'MB3', 'MB4', 'MB5', 'MB6','MB7','MB8']
//let HarborSubCode=[['01','02'],['01','02','03'],['01','02'],['01','02'],['01'],['01','02','03']]
let HarborSubCode = ['01', '01', '01', '01', '01', '01','01','01','01']


function ShowingHarbor() {
  let marker = new naver.maps.Marker({
    position: new naver.maps.LatLng(35.526908, 129.373515),
    map: map
  });

  for (let i = 0; i < HarborLatArray.length; i++) {
    let marker = new naver.maps.Marker({
      position: new naver.maps.LatLng(HarborLatArray[i], HarborLonArray[i]),
      map: map
    });
    let infowindow = new naver.maps.InfoWindow({
      content: `<div>` + HarborName[i] + `</div>`
    });
    naver.maps.Event.addListener(marker, "click", function (e) {
      if (infowindow.getMap()) {      
        infowindow.close();
      } else {
        infowindow.open(map, marker);
      }
    });
  }
}




