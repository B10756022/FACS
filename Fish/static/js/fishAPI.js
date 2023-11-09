//https://data.coa.gov.tw/Service/OpenData/FromM/AquaticTransData.aspx

const url =
  'https://data.coa.gov.tw/Service/OpenData/FromM/AquaticTransData.aspx?$top=1000&$skip=0'

const tableAPI = document.querySelector('.tableAPI')
const serchBTN = document.querySelector('.serchBTN')
const allBTN = document.querySelector('.allBTN')
const serchName = document.querySelector('.serchName')
tableAPI.innerHTML = `
<tr>
<td></td>
<td></td>
<td></td>
<td>資料載入中 請稍等</td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
<tr >
<td></td>
<td></td>
<td></td>
<td><img
src="http://b.blog.xuite.net/b/3/a/c/11893557/blog_10351/txt/11293067/7.gif"
alt=""
/></td>
<td></td>
<td></td>
<td></td>
<td></td>

  </tr>`

axios.get(url).then(function (response) {
  console.log(response.data)
  let str = ''
  let serch = ''

  response.data.forEach(function (item, index) {
    str += `<tr >
    <td>${item.交易日期}</td>
    <td class="stress">${item.魚貨名稱}</td>
    <td>${item.市場名稱}</td>
    <td>${item.上價}</td>
    <td>${item.中價}</td>
    <td>${item.下價}</td>
    <td>${item.交易量}</td>
    <td>${item.平均價}</td>
  </tr>`
  })

  serchBTN.addEventListener('click', function (e) {
    e.preventDefault() //取消預設觸發行為
    //   console.log(serchName.value.trim())
    let noserch = true
    response.data.forEach(function (item, index) {
      if (
        serchName.value.trim() == item.魚貨名稱 ||
        serchName.value.trim() == item.市場名稱
      ) {
        serch += `<tr >
      <td>${item.交易日期}</td>
      <td class="stress">${item.魚貨名稱}</td>
      <td>${item.市場名稱}</td>
      <td>${item.上價}</td>
      <td>${item.中價}</td>
      <td>${item.下價}</td>
      <td>${item.交易量}</td>
      <td>${item.平均價}</td>
        </tr>`
        noserch = false
      }
    })

    tableAPI.innerHTML = serch
    serch = '' //清空serch

    if (noserch === true) {
      alert('找不到符合您搜尋條件的內容')
      tableAPI.innerHTML = str
    }
  })

  allBTN.addEventListener('click', function (e) {
    tableAPI.innerHTML = str
    serchName.value = ''
    console.log('展開全部')
  })

  tableAPI.innerHTML = str
})
