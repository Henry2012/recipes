var page = require('webpage').create(),
system = require('system');
url = system.args[1]
photo_name = system.args[2]

page.open(url, function () {
    page.render(photo_name);
    phantom.exit();
});