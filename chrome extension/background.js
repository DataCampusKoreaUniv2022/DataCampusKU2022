let color = '#ff4081'

chrome.runtime.onInstalled.addListener(() => {
    chrome.storage.sync.set({ color });
    console.log('Default background color set to %cpink', `color: ${color}`);
});