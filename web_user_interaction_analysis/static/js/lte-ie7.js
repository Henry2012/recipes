/* Load this script using conditional IE comments if you need to support IE 7 and IE 6. */

window.onload = function() {
	function addIcon(el, entity) {
		var html = el.innerHTML;
		el.innerHTML = '<span style="font-family: \'icomoon\'">' + entity + '</span>' + html;
	}
	var icons = {
			'icon-google-plus' : '&#xe000;',
			'icon-facebook' : '&#xe001;',
			'icon-facebook-2' : '&#xe002;',
			'icon-twitter' : '&#xe003;',
			'icon-twitter-2' : '&#xe004;',
			'icon-twitter-3' : '&#xe005;',
			'icon-google-plus-2' : '&#xe006;',
			'icon-mail' : '&#xe007;',
			'icon-mail-2' : '&#xe008;',
			'icon-mail-3' : '&#xe009;',
			'icon-github' : '&#xe00a;',
			'icon-github-2' : '&#xe00b;',
			'icon-screen' : '&#xe00c;',
			'icon-home' : '&#xe00d;',
			'icon-camera' : '&#xe00e;',
			'icon-images' : '&#xe00f;',
			'icon-location' : '&#xe010;',
			'icon-location-2' : '&#xe011;',
			'icon-compass' : '&#xe012;',
			'icon-user' : '&#xe013;',
			'icon-arrow-down' : '&#xe018;',
			'icon-arrow-up' : '&#xe019;',
			'icon-arrow-right' : '&#xe01a;',
			'icon-checkmark' : '&#xe01b;',
			'icon-cancel' : '&#xe01c;',
			'icon-arrow-left' : '&#xe01f;',
			'icon-paragraph-left' : '&#xe020;',
			'icon-download' : '&#xe021;',
			'icon-user-2' : '&#xe022;',
			'icon-location-3' : '&#xe023;',
			'icon-angle-down' : '&#xf107;',
			'icon-chevron-left' : '&#xf053;',
			'icon-chevron-right' : '&#xf054;',
			'icon-chevron-up' : '&#xf077;',
			'icon-chevron-down' : '&#xf078;',
			'icon-angle-up' : '&#xf106;',
			'icon-angle-left' : '&#xf104;',
			'icon-angle-right' : '&#xf105;'
		},
		els = document.getElementsByTagName('*'),
		i, attr, html, c, el;
	for (i = 0; ; i += 1) {
		el = els[i];
		if(!el) {
			break;
		}
		attr = el.getAttribute('data-icon');
		if (attr) {
			addIcon(el, attr);
		}
		c = el.className;
		c = c.match(/icon-[^\s'"]+/);
		if (c && icons[c[0]]) {
			addIcon(el, icons[c[0]]);
		}
	}
};