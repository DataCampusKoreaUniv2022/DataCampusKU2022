'use strict';

var screenshotKey = false;
var screenshotFunctionality = 0;
var screenshotFormat = "png";
var extension = 'png';

function CaptureScreenshot() {

	var appendixTitle = "screenshot." + extension;

	var title;

	var headerEls = document.querySelectorAll("h1.title.ytd-video-primary-info-renderer");

	function SetTitle() {
		if (headerEls.length > 0) {
			title = headerEls[0].innerText.trim();
			return true;
		} else {
			return false;
		}
	}
	
	if (SetTitle() == false) {
		headerEls = document.querySelectorAll("h1.watch-title-container");

		if (SetTitle() == false)
			title = '';
	}

	var player = document.getElementsByClassName("video-stream")[0];

	var time = player.currentTime;

	title += " ";

	let minutes = Math.floor(time / 60)

	time = Math.floor(time - (minutes * 60));

	if (minutes > 60) {
		let hours = Math.floor(minutes / 60)
		minutes -= hours * 60;
		title += hours + "-";
	}

	title += minutes + "-" + time;

	title += " " + appendixTitle;

	var canvas = document.createElement("canvas");
	canvas.width = player.videoWidth;
	canvas.height = player.videoHeight;
	canvas.getContext('2d').drawImage(player, 0, 0, canvas.width, canvas.height);

	// var downloadLink = document.createElement("a");
	// downloadLink.download = title;

	// function DownloadBlob(blob) {
	// 	downloadLink.href = URL.createObjectURL(blob);
	// 	downloadLink.click();
	// }

	// async function ClipboardBlob(blob) {
	// 	const clipboardItemInput = new ClipboardItem({ "image/png": blob });
	// 	await navigator.clipboard.write([clipboardItemInput]);
	// }

	// // If clipboard copy is needed generate png (clipboard only supports png)
	// if (screenshotFunctionality == 1 || screenshotFunctionality == 2) {
	// 	canvas.toBlob(async function (blob) {
	// 		await ClipboardBlob(blob);
	// 		// Also download it if it's needed and it's in the correct format
	// 		if (screenshotFunctionality == 2 && screenshotFormat === 'png') {
	// 			DownloadBlob(blob);
	// 		}
	// 	}, 'image/png');
	// }

	// // Create and download image in the selected format if needed
	// if (screenshotFunctionality == 0 || (screenshotFunctionality == 2 && screenshotFormat !== 'png')) {
	// 	canvas.toBlob(async function (blob) {
	// 		DownloadBlob(blob);
	// 	}, 'image/' + screenshotFormat);
	// }

	player.pause()

	var imgURL = canvas.toDataURL("image/jpeg", 1.0);
	chrome.runtime.sendMessage(
		{type: 'image', image: imgURL},
		function(response){
			chrome.storage.local.set({image: response.farewell.image, labels: response.farewell.labels});

			// alert(response.farewell.scores)
			let newDiv = document.createElement('div');
			newDiv.id = 'xraydiv';

			let iframeToAdd = document.createElement('iframe');
			let xrayHtmlUrl = chrome.runtime.getURL('xray/index.html');
			iframeToAdd.src = xrayHtmlUrl;
			// let imgToAdd = document.createElement('img');
			// imgToAdd.src = response.farewell.image;

			let whereToAdd = document.getElementById('primary-inner');
			let ytpPlayer = document.getElementById('player-container-inner');
			let htmlPlayer = document.getElementsByClassName("video-stream html5-main-video")[0]

			let getWidth = htmlPlayer.style.width;
			let getHeight = htmlPlayer.style.height;
			iframeToAdd.style.width = getWidth;
			iframeToAdd.style.height = getHeight;
			// iframeToAdd.frameBorder = '0';
			iframeToAdd.marginWidth = '0';
			iframeToAdd.marginHeight = '0';
			// iframeToAdd.scrolling = 'no';

			chrome.storage.local.set({width: getWidth, height: getHeight});

			newDiv.append(iframeToAdd);
			
			ytpPlayer.style.display = 'none';
			whereToAdd.prepend(newDiv);

			// setTimeout(() => {
			// 	alert('짜잔');
			// 	newDiv.style.display = 'none';
			// 	ytpPlayer.style.display = '';
			// }, 3000000);

		}
	);
}

function exitFunction(){
    let xrayDiv = document.getElementById("xraydiv");
    alert(parent.document.title);
    let ytpPlayer = document.getElementById('player-container-inner');

    xrayDiv.style.display = 'none';
    ytpPlayer.style.display = '';
}

function AddScreenshotButton() {
	var ytpRightControls = document.getElementsByClassName("ytp-right-controls")[0];
	if (ytpRightControls) {
		ytpRightControls.prepend(screenshotButton);
	};
}

var screenshotButton = document.createElement("button");
screenshotButton.className = "screenshotButton ytp-button";
screenshotButton.style.width = "auto";
screenshotButton.innerHTML = "☘️ 식물 X-RAY";
screenshotButton.style.cssFloat = "left";
screenshotButton.onclick = CaptureScreenshot;

chrome.storage.sync.get(['screenshotKey', 'screenshotFunctionality', 'screenshotFileFormat'], function(result) {
	screenshotKey = result.screenshotKey;
	if (result.screenshotFileFormat === undefined) {
		screenshotFormat = 'png'
	} else {
		screenshotFormat = result.screenshotFileFormat
	}

	if (result.screenshotFunctionality === undefined) {
		screenshotFunctionality = 0;
	} else {
    	screenshotFunctionality = result.screenshotFunctionality;
	}

	if (screenshotFormat === 'jpeg') {
		extension = 'jpg';
	} else {
		extension = screenshotFormat;
	}
});

AddScreenshotButton();
