/*window.onload = function(){
    let marker = new naver.maps.Marker({
        position: new naver.maps.LatLng(35.44043374181368,129.3934977814075),
        map: map
      });
}*/
window.onload=function ShowingData() {
  ShowingHarbor()
}

function ShowingHarbor(){
  /*let marker = new naver.maps.Marker({
    position: new naver.maps.LatLng(35.526908,129.373515),
    map: map
  });*/

  for(let i=0;i<HarborLatArray.length;i++){
    let marker = new naver.maps.Marker({
      position: new naver.maps.LatLng(HarborLatArray[i],HarborLonArray[i]),
      map: map
    });
    let infowindow = new naver.maps.InfoWindow({
      content: `<div>`+HarborName[i]+`</div>`
    });
    naver.maps.Event.addListener(marker, "click", function (e) {
      if (infowindow.getMap()) {
        infowindow.close();
      } else {
        infowindow.open(map, marker);
        /*for(let j=0;j<HarborSubCode[i].length;j++)
        {
          $.ajax({
            type: 'GET',
            url: "{% url 'GetHarborData' %}",
            dataType: "json",
            data: {
              'harbor_maincode': HarborMainCode[i],
              'harbor_subcode' : HarborSubCode[j]
            },
            error: function() {
              alert("오류!")
            },
            success: function(data) {
              console.log(data)
            }
          })
        }*/

      }
    });    
  }
}

let HarborLatArray=[35.528672,35.526908,35.522900,35.52172551482321,35.519438,35.517193]
let HarborLonArray=[129.375364,129.373515,129.373701,129.37551417157238,129.374956,129.376094]
let HarborName=['제1부두','제2부두','제3부두','제4부두','제5부두','제6부두']
let HarborMainCode=['MB1','MB2','MB3','MB4','MB5','MB6']
let HarborSubCode=[['01','02'],['01','02','03'],['01','02'],['01','02'],['01'],['01','02','03']]