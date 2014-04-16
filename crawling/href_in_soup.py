#! /usr/bin/python
#-*- coding:utf-8 -*-

"""
Author(s): Qiqun Han, Chao Peng
Company: EverString Technology Ltd.
File: crawling.href_in_soup.py
Description: this program
Creation: 2013-11-25
Revision: 2013-11-25
Copyright (c) All Right Reserved, EverString Technology Ltd.
"""

import os
import sys
basepath = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(basepath, "..")))

import json
import pdb
import pickle
import re
import timeit
from bs4 import BeautifulSoup
from lxml import html
from lxml.html import fromstring
from lxml import etree
from timer import Timer

html_text = """{"domain": "3dbresearch.com", "html": "<html>\n<head>\n<title>3dB Research</title>\n<meta http-equiv=\"Content-Type\" content=\"text/html; charset=iso-8859-1\">\n<META HTTP-EQUIV=\"Content-Language\" content=\"EN\">\n<META name=\"Copyright\" content=\"3dB Research\">\n<META name=\"Distribution\" content=\"Global\">\n<META name=\"Revisit-After\" content=\"21 Days\">\n<META name=\"Robots\" content=\"index,follow\">\n<META name=\"keywords\" content=\"3, 3dB, 3 Decibel, audio, audio research, voice, human voice, voice research, voice processing, technology, audio technology, Peter Lupini, Glen Rutledge, Norm Campbell\">\n<META name=\"description\" content=\"3dB Research is a technology company specializing in human voice processing.\">\n<meta http-equiv=\"Content-Type\" content=\"text/html;\">\n<script language=\"JavaScript\" type=\"text/JavaScript\">\n<!--\nfunction MM_swapImgRestore() { //v3.0\n  var i,x,a=document.MM_sr; for(i=0;a&&i<a.length&&(x=a[i])&&x.oSrc;i++) x.src=x.oSrc;\n}\n\nfunction MM_preloadImages() { //v3.0\n  var d=document; if(d.images){ if(!d.MM_p) d.MM_p=new Array();\n    var i,j=d.MM_p.length,a=MM_preloadImages.arguments; for(i=0; i<a.length; i++)\n    if (a[i].indexOf(\"#\")!=0){ d.MM_p[j]=new Image; d.MM_p[j++].src=a[i];}}\n}\n\nfunction MM_findObj(n, d) { //v4.01\n  var p,i,x;  if(!d) d=document; if((p=n.indexOf(\"?\"))>0&&parent.frames.length) {\n    d=parent.frames[n.substring(p+1)].document; n=n.substring(0,p);}\n  if(!(x=d[n])&&d.all) x=d.all[n]; for (i=0;!x&&i<d.forms.length;i++) x=d.forms[i][n];\n  for(i=0;!x&&d.layers&&i<d.layers.length;i++) x=MM_findObj(n,d.layers[i].document);\n  if(!x && d.getElementById) x=d.getElementById(n); return x;\n}\n\nfunction MM_swapImage() { //v3.0\n  var i,j=0,x,a=MM_swapImage.arguments; document.MM_sr=new Array; for(i=0;i<(a.length-2);i+=3)\n   if ((x=MM_findObj(a[i]))!=null){document.MM_sr[j++]=x; if(!x.oSrc) x.oSrc=x.src; x.src=a[i+2];}\n}\n//-->\n</script>\n</head>\n<script type=\"text/javascript\">\nvar gaJsHost = ((\"https:\" == document.location.protocol) ? \"https://ssl.\" : \"http://www.\");\ndocument.write(unescape(\"%3Cscript src='\" + gaJsHost + \"google-analytics.com/ga.js' type='text/javascript'%3E%3C/script%3E\"));\n</script>\n<script type=\"text/javascript\">\ntry {\nvar pageTracker = _gat._getTracker(\"UA-8719222-2\");\npageTracker._trackPageview();\n} catch(err) {}</script>\n<body background=\"Images/Bg.jpg\" topmargin=\"25\" onLoad=\"MM_preloadImages('Images/ImagesHome/OverTabHome.gif','Images/ImagesHome/OverTabTechnology.gif','Images/ImagesHome/OverTabAboutUs.gif','Images/ImagesHome/OverTabContact.gif')\">\n<table border=\"0\" cellpadding=\"0\" cellspacing=\"0\" width=\"745\" align=\"center\" valign=\"top\">\n  <tr>\n   <td><img src=\"spacer.gif\" width=\"6\" height=\"1\" border=\"0\" alt=\"\"></td>\n   <td><img src=\"spacer.gif\" width=\"228\" height=\"1\" border=\"0\" alt=\"\"></td>\n   <td><img src=\"spacer.gif\" width=\"127\" height=\"1\" border=\"0\" alt=\"\"></td>\n   <td><img src=\"spacer.gif\" width=\"125\" height=\"1\" border=\"0\" alt=\"\"></td>\n   <td><img src=\"spacer.gif\" width=\"59\" height=\"1\" border=\"0\" alt=\"\"></td>\n   <td><img src=\"spacer.gif\" width=\"67\" height=\"1\" border=\"0\" alt=\"\"></td>\n   <td><img src=\"spacer.gif\" width=\"127\" height=\"1\" border=\"0\" alt=\"\"></td>\n   <td><img src=\"spacer.gif\" width=\"6\" height=\"1\" border=\"0\" alt=\"\"></td>\n   <td><img src=\"spacer.gif\" width=\"1\" height=\"1\" border=\"0\" alt=\"\"></td>\n  </tr>\n\n  <tr>\n    <td rowspan=\"4\">&nbsp;</td>\n    <td rowspan=\"2\"><a href=\"index.htm\"><img src=\"Images/3dBLogo.gif\" alt=\"3dB Logo\" width=\"228\" height=\"146\" border=\"0\"></a></td>\n    <td colspan=\"5\"><img src=\"Images/Specrogram.gif\" alt=\"Spectrogram\" width=\"505\" height=\"90\"></td>\n    <td rowspan=\"4\">&nbsp;</td>\n   <td><img src=\"spacer.gif\" width=\"1\" height=\"90\" border=\"0\" alt=\"\"></td>\n  </tr>\n  <tr>\n    <td><a href=\"index.htm\" onMouseOut=\"MM_swapImgRestore()\" onMouseOver=\"MM_swapImage('Image19','','Images/ImagesHome/OverTabHome.gif',1)\"><img src=\"Images/ImagesHome/TabHome.gif\" alt=\"Home\" name=\"Image19\" width=\"127\" height=\"56\" border=\"0\"></a></td> \n    <td><a href=\"Technology.htm\" onMouseOut=\"MM_swapImgRestore()\" onMouseOver=\"MM_swapImage('Image20','','Images/ImagesHome/OverTabTechnology.gif',1)\"><img src=\"Images/ImagesHome/TabTechnology.gif\" alt=\"Technology\" name=\"Image20\" width=\"125\" height=\"56\" border=\"0\"></a></td> \n    <td colspan=\"2\"><a href=\"AboutUs.htm\" onMouseOut=\"MM_swapImgRestore()\" onMouseOver=\"MM_swapImage('Image21','','Images/ImagesHome/OverTabAboutUs.gif',1)\"><img src=\"Images/ImagesHome/TabAboutUs.gif\" alt=\"About Us\" name=\"Image21\" width=\"126\" height=\"56\" border=\"0\"></a></td> \n    <td><a href=\"Contact.htm\" onMouseOut=\"MM_swapImgRestore()\" onMouseOver=\"MM_swapImage('Image22','','Images/ImagesHome/OverTabContact.gif',1)\"><img src=\"Images/ImagesHome/TabContact.gif\" alt=\"Contact\" name=\"Image22\" width=\"127\" height=\"56\" border=\"0\"></a></td>\n   <td><img src=\"spacer.gif\" width=\"1\" height=\"56\" border=\"0\" alt=\"\"></td>\n  </tr>\n  <tr>\n    <td valign=\"top\" bgcolor=\"#FFFFFF\"><img src=\"Images/3.gif\" width=\"228\" height=\"315\"></td>\n    <td width=\"505\" colspan=\"5\" valign=\"top\" bgcolor=\"#FFFFFF\">\n<table width=\"505\" border=\"0\" cellpadding=\"10\">\n        <tr> \n          <td valign=\"top\"> <div align=\"justify\"> \n              <p><font color=\"4A4C4D\" size=\"4\" face=\"Verdana, Arial, Helvetica, sans-serif\"><strong>3dB \n                Research Ltd. </strong></font></p>\n            </div></td>\n        </tr>\n        <tr>\n<td height=\"19\" valign=\"top\"><p><font color=\"4A4C4D\" size=\"2\" face=\"Verdana, \nArial, Helvetica, sans-serif\"> \n                         \n    <table width=\"100%\" align=\"center\" cellspacing=\"2\" cellpadding=\"0\" border=\"0\" bgcolor=\"#000000\">\n    <tr>\n        <td bgcolor=\"#FFFFFF\">\n<table width=\"100%\" align=\"center\" cellspacing=\"20\" cellpadding=\"0\" border=\"0\" bgcolor=\"#FFFFFF\">\n    <tr>\n        <td align=\"center\"><font face=\"Arial\" size=\"3\"><b>Exciting News!</b></font></td>\n    </tr>\n    <tr>\n        <td><font face=\"Arial\" size=\"2\"><b>Harman Acquires Canadian Based 3dB Research for Music and Voice Processing Technology</b></font></td>\n        \n    </tr>\n    <tr>\n <td><font face=\"Arial\" size=\"2\"><a href=\"http://www.harman.com/EN-US/Newscenter/Pages/Harmanacquires3dbresearch.aspx?name=Press Release\">Harman Press Release</a></font></td>   \n    </tr>\n</table>\n</td></tr></table>\n  <br><br>\nMusic is our passion. Technology is our \nexpertise. Combining these is our business. <br><br> \n\nAt 3dB Research, we \ncombine creativity with strong technical skills and extensive music industry \nexperience to develop innovative and exciting products. Music brings joy to \npeople who play it. Our dream is to invent and build technologies that enhance \nthis joy, not detract from it. <br><br> \n\nIn fact, this dream has already become a reality for the tens of thousands of musicians \naround the world who have discovered the musIQ<sup>&#0174;</sup> \nadvantage in the following DigiTech<sup>&#0174;</sup> products:\n<ul>\n<li><a href=\"http://www.vocalistpro.com/product.php?name=Live2\">Live 2</a></li>\n<li><a href=\"http://www.vocalistpro.com/product.php?name=Live4\">Live 4</a></li>\n<li><a href=\"http://www.vocalistpro.com/product.php?name=LivePro\">LivePro</a></li>\n<li><a href=\"http://www.vocalistpro.com/product.php?name=VL3D\">VL3D</a></li>\n<li><a href=\"http://www.vocalistpro.com/product.php?name=Live3\">Live 3</a></li>\n<li><a href=\"http://www.digitech.com/products/Pedals/HarmonyMan.php\">HarmonyMan</a></li>\n<li><a href=\"http://www.digitech.com/products/Pedals/TimeBender.php\">TimeBender</a> \n    (lots of great info at: <a href=\"http://www.timebenderdelay.com\"> timebenderdelay.com</a> ) </li>\n<li><a href=\"http://www.hardwirepedals.com/ht6-polyphonic-tuner-overview.php\">HardWire HT-6 Polyphonic Tuner</a> ) </li>\n\n</ul>\n\nCheck out our technology section to learn more about how our innovative musIQ<sup>&#0174;</sup> \ntechnology applies musical intelligence in order to improve the quality and usability of vocal and \ninstrumental musical effects, or jump straight to our popular <a href=\"FAQ_musIQ_Harmony.htm\">\nmusIQ Harmony FAQ</a> page.<br></font><br>\n\n <img \nsrc=\"Images/musIQMedLineSmallReg.gif\" width=\"126\" height=\"31\" align=\"right\"></p>\n\n<p><span style='font-size:7.0pt;font-family:Verdana;color:#4A4C4D'>musIQ is a\n    registered trademark of 3dB Research Ltd.<br>\n\tDigiTech,Vocalist,HarmonyMan and TimeBender are trademarks of Harman International Industries Inc.</span><span style='font-size:8.0pt;font-family:Verdana;color:#4A4C4D'></span></p>\n\n          </td>\n        </tr>\n      </table></td>\n   <td><img src=\"spacer.gif\" width=\"1\" height=\"315\" border=\"0\" alt=\"\"></td>\n  </tr>\n  <tr>\n    <td colspan=\"4\"><img src=\"Images/BottomLeft.gif\" alt=\"Copyright\" width=\"539\" height=\"22\"></td> \n    <td colspan=\"2\"><a href=\"mailto:byronthompson@shaw.ca\"><img src=\"Images/BottomRight.gif\" alt=\"Design Credit\" width=\"194\" height=\"22\" border=\"0\"></a></td>\n   <td><img src=\"spacer.gif\" width=\"1\" height=\"22\" border=\"0\" alt=\"\"></td>\n  </tr>\n</table>\n</body>\n</html>"}"""

def href_of_html_v1():
    if html_text is None:
        return []
    
    urls = []
    soup = BeautifulSoup(html_text, 'lxml')
    #soup = BeautifulSoup(html_text)
    links = soup.find_all('a')
    #pdb.set_trace()
    for link in links:
        url = link.get('href', None)
        if url and len(url) > 1:
            urls.append(url)

    return urls

def href_of_html_v2(html_text):
    if html_text is None:
        return []
    
    urls = []
    #soup = BeautifulSoup(html_text, 'lxml')
    soup = BeautifulSoup(html_text)
    links = soup.find_all('a')
    #pdb.set_trace()
    for link in links:
        url = link.get('href', None)
        if url and len(url) > 1:
            urls.append(url)

    return urls

def href_of_html_v3(html_text):
    if html_text is None:
        return []
    
    urls = []
    
    pattern = r"""<a href=\\?['"](.*?)\\?['"]"""
    for m in re.findall(pattern, html_text):
        urls.append(m)

    return urls

def href_of_html_v4():
    if html_text is None:
        return []
    
    urls = []
    
    pattern = r"""<a href=\\?['"](.*?)\\?['"]"""
    for m in re.finditer(pattern, html_text):
        urls.append(m.groups(1)[0])

    return urls

def href_of_html_v5(html_text):
    if html_text is None:
        return []
    
    doc = fromstring(html_text)
    urls = doc.xpath('//a/@href')
    
    return urls

def href_of_html_v6():
    if html_text is None:
        return []
    doc = html.document_fromstring(html_text)
    urls = doc.xpath('//script')
    #urls = doc.xpath('.stumble-upon.com/js/widgets.js')
    
    return urls

def href_of_html_v7(html_text):
    if html_text is None:
        return []
    
    doc = fromstring(html_text)
    scripts = [each.text for each in doc.xpath('//script')]
    
    return scripts

# def contains_v1():
#     
#     for href in href_of_html(html):
#         if "index.htm" in href:
#             return True
#     else:
#         return False
# 
# def contains_v2():
#     html = """<html xmlns=\"http://www.w3.org/1999/xhtml\">\r\n<head><title></title>\r\n<script src=\"http://ak2.imgaft.com/script/jquery-1.3.1.min.js\" type=\"text/javascript\"></script>\r\n<script type=\"text/javascript\" language=\"javascript\">\r\n$(document).ready(function () {\r\n\tjQuery.ajax({ url: 'http://mcc.godaddy.com/parked/park.aspx/?q=pFHmpJcdnv4mYKS6ozI4pzqzYaOvrvHlAzM2pFHmpGR0ZQp3ZGpkWGV2L3MkWGAkZwD0AwtmZGNkAmR2ZwZ5ZGH1ZvHlAzIaWGAkZwNkZmRkZGRkAQRmAQZyZwMwrFHmpGR=-1', dataType: 'jsonp', type: 'GET', jsonpCallback: 'parkcallback',\r\n\t    success: function (data) { if (data[\"returnval\"] != null) { window.location.href = 'http://3-dmarkets.com?nr=' + data[\"returnval\"]; } else { window.location.href = 'http://3-dmarkets.com?hg=0' } }\r\n\t});\r\n    var t = setTimeout(function () { window.location.href = 'http://3-dmarkets.com?nr=0'; }, 3000);\r\n});\r\n</script></head><body></body></html>"""
#     return "index.htm" in html


if __name__ == '__main__':
#     with open('../io/test_10.json') as of:
#         for line in of:
#             record = json.loads(line.strip())
#             html = record['html']
#             urls = href_of_html_v1(html)
#             print urls

#     t1 = timeit.Timer('contains_v1', 'from __main__ import contains_v1')
#     t2 = timeit.Timer('contains_v2', 'from __main__ import contains_v2')
#     
#     print t1.repeat(3, 1000000)
#     print t2.repeat(3, 1000000)

    #===============================================================================
    # Open patterns
    #===============================================================================
#     with open('../io/signal_pattern.pkl', 'rb') as f:
#         d = pickle.load(f)
#         for k, v in d.iteritems():
#             print k, v
#             raw_input()

    #===============================================================================
    # Compare default beautifulsoup parser with bs parser using lxml
    #===============================================================================
#     assert (href_of_html_v1() == href_of_html_v2()
#             == href_of_html_v3() == href_of_html_v4()
#             == href_of_html_v5() == href_of_html_v6())

#     t1 = timeit.Timer('href_of_html_v1', 'from __main__ import href_of_html_v1')
#     t2 = timeit.Timer('href_of_html_v2', 'from __main__ import href_of_html_v2')
#     t3 = timeit.Timer('href_of_html_v3', 'from __main__ import href_of_html_v3')
#     t4 = timeit.Timer('href_of_html_v4', 'from __main__ import href_of_html_v4')
#     t5 = timeit.Timer('href_of_html_v5', 'from __main__ import href_of_html_v5')
#     t6 = timeit.Timer('href_of_html_v6', 'from __main__ import href_of_html_v6')
#     print t1.timeit()
    
#     min_t1 = min(t1.repeat(3, 10000000))
#     min_t2 = min(t2.repeat(3, 10000000))
#     min_t3 = min(t3.repeat(3, 10000000))
#     min_t4 = min(t4.repeat(3, 10000000))
#     min_t5 = min(t5.repeat(3, 10000000))
#     min_t6 = min(t6.repeat(3, 10000000))
    
#     print min_t1, min_t2, min_t3, min_t4, min_t5, min_t6

    with Timer() as t:
        scripts = href_of_html_v6()
        from pprint import pprint
        pprint(scripts)
#         print dir(scripts[0])
#         print "values: ", scripts[0].values
#         print "text_content: ", scripts[0].text_content
        print "text: ", scripts[0].text
#         pdb.set_trace()
    print t.interval
