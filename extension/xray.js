chrome.storage.local.get(['image', 'width', 'height'], function(result) {
    let image = document.createElement('img');
    image.src = result.image;
    image.style.width = result.width;
    image.style.height = result.height;

    let body = document.querySelector('body');
    body.append(image);
});