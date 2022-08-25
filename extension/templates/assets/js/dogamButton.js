document.getElementById("dogam").addEventListener("click", addDogamImageToStorage);

function addDogamImageToStorage(){
    chrome.storage.local.get(['labellist'], function(result) {
        var labelList = result.labellist;

        var newLabel = document.querySelector("title").id;
        var hanName = document.querySelector("h1").innerText;

        var isDup = false;
        for (var i = 0; i < labelList.length; i++) {
            if (newLabel == labelList[i]) {
                isDup = true;
            }
        }
        if (isDup) {
            alert(hanName + ' 은(는) 이미 도감에 있습니다.');
        }
        else {
            labelList.push(newLabel);
            chrome.storage.local.set({labellist: labelList});
            alert(hanName + ' 이(가) 도감에 추가되었습니다!');
        }
    });
}