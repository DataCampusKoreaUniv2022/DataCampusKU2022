chrome.storage.local.get(['image', 'width', 'height'], function(result) {
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
});