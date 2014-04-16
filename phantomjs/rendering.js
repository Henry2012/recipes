var page = require('webpage').create(),
	system = require('system');
url = system.args[1]	
page.open(url, function (status) {
    if (status !== 'success') {
        console.log('Unable to access network');
    } else {
        var p = page.evaluate(function () {
            return document.getElementsByTagName('html')[0].innerHTML
        });
        console.log(p);
    }
    phantom.exit();
});