chrome.storage.local.get(['image', 'labels', 'width', 'height'], function(result) {
    let image = document.createElement('img');
    image.src = result.image;
    image.style.width = result.width;
    image.style.height = result.height;

    let imageURL = "url('" + result.image + "')";

    let bg = document.getElementById("wrapper");
    // bg.prepend(image);
    bg.style.backgroundImage = imageURL;
    bg.style.backgroundSize = "cover";
    // bg.style.width = result.width;
    // bg.style.height = result.height;
    // alert(bg.style)

    let whereBtnAppend = document.getElementById("header");
    for (var i = 0; i < result.labels.length; i++) {
        let labelBtn = document.createElement('a');
        let labelName = document.createTextNode(result.labels[i]);
        labelBtn.appendChild(labelName);
        labelBtn.setAttribute('href', "../templates/" + result.labels[i] +".html");
        labelBtn.className = "button";
        whereBtnAppend.append(labelBtn);
    }
});

document.getElementById("exit").addEventListener("click", exitFunction);

function exitFunction(){
    chrome.tabs.executeScript({file: "/xray/assets/js/exit.js"});;
}