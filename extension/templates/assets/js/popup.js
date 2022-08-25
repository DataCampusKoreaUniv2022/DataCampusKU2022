chrome.storage.local.get(['dogamimage', 'dogamlabel'], function(result) {
    var dogamColumn = document.getElementById("columns");
    var newLabel = result.dogamlabel;
    var newImage = document.createElement('img');
    newImage.src = result.dogamimage;

    var newFigure = document.createElement('figure');
    var newCaption = document.createElement('figcaption');
    newCaption.innerText = newLabel;
    newFigure.append(newImage);
    newFigure.append(newCaption);

    dogamColumn.append(newFigure);
    dogamColumn.append(newFigure);
    }
);