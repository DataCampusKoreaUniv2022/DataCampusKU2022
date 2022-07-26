chrome.webNavigation.onHistoryStateUpdated.addListener(function(data) {
	chrome.tabs.get(data.tabId, function(tab) {
		chrome.tabs.executeScript(data.tabId, {code: 'if (typeof AddScreenshotButton !== "undefined") { AddScreenshotButton(); }', runAt: 'document_start'});
	});
}, {url: [{hostSuffix: '.youtube.com'}]});

chrome.storage.local.set({labellist: []});

var serverhost = 'http://127.0.0.1:8000/dino_api';
chrome.runtime.onMessage.addListener(
	function(request, sender, sendResponse) {
		if (request.type == 'image'){
			fetch(serverhost, {
				method: 'POST',
				body: request.image
			}).then(response => response.json())
			.then(response => sendResponse({farewell: response}))
			.catch(error => console.log(error))
		}

		return true;
	}
);