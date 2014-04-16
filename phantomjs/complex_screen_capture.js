var page = require('webpage').create(),
system = require('system');
url = system.args[1]
photo_name = system.args[2]

page.open(url, function (status) {
	if (status !== 'success') {
		console.log('Unable to load the address!');
		phantom.exit();
	} else {
		window.setTimeout(function () {
			page.render(photo_name);
			phantom.exit();
		}, 200);
	}
});
