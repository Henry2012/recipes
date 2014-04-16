var page = require('webpage').create();
page.open('http://www.baidu.com/', function () {
    page.render('baidu_v2.jpg');
    phantom.exit();
});