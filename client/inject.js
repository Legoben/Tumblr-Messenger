//The only purpose of this page is to inject index.js.

var s = document.createElement('script');
s.src = chrome.extension.getURL('index.js');
s.onload = function() {
    this.parentNode.removeChild(this);
};

(document.head||document.documentElement).appendChild(s);
