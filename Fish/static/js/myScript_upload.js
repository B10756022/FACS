  const spinnerbox = document.getElementById('spinner-box');
  const upload = document.getElementById('upload_field');
  console.log(spinnerbox);
  console.log(upload);
  const realFileBtn = document.getElementById("real-file");
  const customBtn = document.getElementById("custom-button");
  const customTxt = document.getElementById("custom-text");
  const textArea = document.getElementById('textarea');

  customBtn.addEventListener("click", function () {
      realFileBtn.click();
  });

  realFileBtn.addEventListener("change", function () {
      if (realFileBtn.files[0]) {
          customTxt.innerHTML = realFileBtn.files[0].name;
      } else {
          customTxt.innerHTML = "未選擇任何檔案";
      }
  });
  function myFunction1() {
    if(textArea.value.length > 2 && customTxt.innerHTML != "未選擇任何檔案"){
        spinnerbox.style.display="block";
        upload.style.display="none";
        alert("上傳成功，請稍等！");
    }
    else if(customTxt.innerHTML == "未選擇任何檔案")
    {
        alert("請選擇檔案！");
    }
    else
    {
        alert("請輸入文字！");
    }

}

function charCount() {
    var element = textArea.value.length;
    document.getElementById('textarea_count').innerHTML = element + "/50 (Max Character 50).";
}
