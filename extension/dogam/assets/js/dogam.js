chrome.storage.local.get(['labellist'], function(result) {
    var labelList = result.labellist;
    // labelList = ['orange_jasmine', 'alocasia', 'moneytree', 'monstera']

    var whereDogamAdded = document.getElementById("main");
    for (var i = 0; i < labelList.length; i++) {
        var dogamToAdd = document.createElement("article");
        dogamToAdd.className = "thumb";

        var dogamSquare = document.createElement("a");
        dogamSquare.id = labelList[i];
        dogamSquare.href = "../templates/" + labelList[i] + ".html";
        dogamSquare.target = '_blank';
        dogamSquare.className = "image";
        dogamSquare.style.backgroundImage = "url('" + "../templates/images/" + labelList[i] + ".jpg" + "')";
        dogamToAdd.append(dogamSquare);

        var dogamLabel = document.createElement("h2");
        dogamLabel.innerText = labelList[i];
        dogamToAdd.append(dogamLabel);

        whereDogamAdded.prepend(dogamToAdd);
    }
});


document.getElementById("reset").addEventListener("click", resetDogam);
function resetDogam(){
    chrome.storage.local.set({labellist: []});
}