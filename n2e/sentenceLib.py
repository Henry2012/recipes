# -*- encoding: utf-8 -*-
#
# Original Author: Hua Gao
# Date: 1/27/2013
# Additional edits by:  
#

import re
#import nltk
import cPickle

#stemmer = nltk.PorterStemmer()

monthSet = set(['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December', \
                 'mid-January', 'mid-February', 'mid-March', 'mid-April', 'mid-May', 'mid-June', 'mid-July', 'mid-August', 'mid-September', 'mid-October', 'mid-November', 'mid-December', \
                 'Jan.', 'Feb.', 'Mar.', 'Apr.', 'Jun.', 'Jul.', 'Aug.', 'Sep.', 'Sept.', 'Oct.', 'Nov.,', 'Dec.', \
                 'Jan', 'Feb', 'Mar,', 'Apr', 'Jun', 'Jul', 'Aug', 'Sep', 'Sept', 'Oct', 'Nov', 'Dec'])

dateSet = set(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday', \
                 'Mon.', 'Tues.', 'Tue', 'Wed.', 'Thurs.', 'Fri.', 'Sat.', 'Sun.', \
                 'Mon', 'Tues', 'Tue.', 'Wed', 'Thurs', 'Fri', \
                 'Now', 'Today', 'Yesterday', 'Tomorrow'])  # Sat Sun removed
dateSet |= monthSet

usaSet = set(['AK', 'Alaska', 'AL', 'Alabama', 'AR', 'Arkansas', 'AS', 'American Samoa', 'AZ', 'Arizona', 'CA', 'California', 'CO', 'Colorado', 'CT', 'Connecticut', \
                'DC', 'District of Columbia', 'DE', 'Delaware', 'FL', 'Florida', 'GA', 'Georgia', 'GU', 'Guam', 'HI', 'Hawaii', 'IA', 'Iowa', \
                'ID', 'Idaho', 'IL', 'Illinois', 'IN', 'Indiana', 'KS', 'Kansas', 'KY', 'Kentucky', 'LA', 'Louisiana', 'MA', 'Massachusetts', 'MD', 'Maryland', 'ME', 'Maine', \
                'MI', 'Michigan', 'MN', 'Minnesota', 'MO', 'Missouri', 'MP', 'Northern Mariana Islands', 'MS', 'Mississippi', 'MT', 'Montana', 'NC', 'North Carolina', \
                'ND', 'North Dakota', 'NE', 'Nebraska', 'NH', 'New Hampshire', 'NJ', 'New Jersey', 'NM', 'New Mexico', 'NV', 'Nevada', 'NY', 'New York', 'OH', 'Ohio', \
                'OK', 'Oklahoma', 'OR', 'Oregon', 'PA', 'Pennsylvania', 'PR', 'Puerto Rico', 'RI', 'Rhode Island', 'SC', 'South Carolina', 'SD', 'South Dakota', \
                'TN', 'Tennessee', 'TX', 'Texas', 'UT', 'Utah', 'VA', 'Virginia', 'VI', 'Virgin Islands', 'VT', 'Vermont', 'WA', 'Washington', 'WI', 'Wisconsin', \
                'WV', 'West Virginia', 'WY', 'Wyoming'])

countriesSet = set(['France', 'USA', 'U.S.A.', 'United States', 'United States of America', 'China', 'Japan', 'Canada', 'Germany', 'Mexico', 'Australia', 'UK', 'U.K.', 'United Kingdom', \
                    'Spain', 'Argentina', 'Italy', 'India', 'Portugal', 'Ireland', 'South Georgia', 'Austria', 'South Korea', 'North Korea', 'Korea', 'Venezuela', 'Europe', \
                    'Taiwan', 'Chile', 'South Africa', 'Africa', 'Brazil', 'Indonesia', 'Hong Kong', 'Georgia', 'Israel', 'Vietnam', 'Singapore', 'Jersey', 'Peru', 'Colombia', \
                    'Thailand', 'Netherlands', 'Poland', 'Ecuador', 'Sweden', 'Russia', 'Uruguay', 'Romania', 'Iraq', 'Malaysia', 'Ukraine', 'Iran', 'Turkey', 'Panama', 'Greece', \
                    'Czech Republic', 'Belgium', 'Switzerland', 'Bulgaria', 'Finland', 'Costa Rica', 'Cuba', 'Egypt', 'Philippines', 'Malta', 'Hungary', 'Denmark', 'Pakistan', \
                    'New Zealand', 'Saudi Arabia', 'Luxembourg', 'Guatemala', 'Paraguay', 'Estonia', 'Kuwait', 'Mali', 'Norway', 'Puerto Rico', 'Bolivia', 'Honduras', 'Nicaragua', \
                    'Guadeloupe', 'Liechtenstein', 'Afghanistan', 'Kenya', 'Nepal', 'Senegal', 'Latvia', 'Andorra', 'Nigeria', 'Slovakia', 'Lithuania', 'Bangladesh', 'El Salvador', \
                    'BJamaica', 'Ghana', 'Croatia', 'Sri Lanka', 'Slovenia', 'Gibraltar', 'Belize', 'Guam', 'Zimbabwe', 'Laos', 'Guyana', 'Lebanon', 'Burundi', 'Niger', 'Bosnia', \
                    'Botswana', 'Tanzania', 'Syria', 'Lesotho', 'Kazakhstan', 'Uganda', 'Namibia', 'Macedonia', 'Haiti', 'Albania', 'Mongolia', 'Rwanda', 'Uzbekistan', 'Mozambique', \
                    'Zambia', 'Somalia', 'Cambodia', 'Tunisia', 'Herzegovina', 'Azerbaijan', 'Macau', 'Kyrgyzstan', 'Mauritania', 'Ethiopia', 'Libya', 'Cayman Islands', 'Yugoslavia', \
                    'Antartica', 'French Polynesia', 'USSR', 'EEUU'])

citiesSet = set(['Tokyo', 'New York', 'New York City', 'NYC', 'Sao Paulo', 'Seoul', 'Mexico City', 'Osaka', 'Mumbai', 'Jakarta', 'Kolkata', 'Delhi', 'Cairo', 'Los Angeles', \
                 'Buenos Aires', 'Rio de Janeiro', 'Moscow', 'Shanghai', 'Paris', 'Istanbul', 'Beijing', 'Chicago', 'London', 'Shenzhen', 'Houston', 'San Diego', 'San Jose', \
                 'Austin', 'Fort Worth', 'El Paso', 'Las Vegas', 'Oklahoma City', 'Long Beach', 'Colorado Springs', 'St. Louis', 'Honolulu', 'Bangkok', 'Atlantic City', \
                 'Dubai', 'San Francisco', 'Mountain View', 'Sunnyvale'])

abbrevSet = set(['MD', 'M.D.', 'PC', 'PCs', 'Ph.D.', 'PhD', 'TV', 'TVs', 'GPS', 'R&D', 'Jr.', 'Sr.', 'OS', 'IPO', 'IPTV', 'IP', 'IPs', 'ISP', 'ISPs', 'OEMs', 'OEM', 'UI', 'API', 'APIs', '3D', 'RF', 'HDCP', \
                 'HDMI', 'DVD', 'DVDs', 'DVR', 'DVRs', 'DNA', 'CAD', 'VOD', 'SMS', 'SDK', 'SDKs', 'RFID', 'RFIDs', 'RPG', 'RPGs', 'FPS', 'FPSs', 'QoS', 'LAN', 'LANs', ''])
 
locationKW = set(['Europe', 'Germany', 'North America', 'China', 'Canada', 'Brazil', 'Israel', 'Australia', 'Asia', 'California', 'CA', 'New York', 'New Jersey', 'New York City', 'London', \
                  'Miami', ''])
descBigramStopwords = set(['in particular', 'of course', 'as expected', 'for example', 'not least', 'he said', 'she said', 'they said', 'this one', ])

acqKW = set(['acquire', 'acquires', 'acquired', 'acquiring', 'acquisition', 'acquisitions', 'buy', 'buys', 'bought', 'buying',
              'procure', 'procures', 'procured', 'procuring', 'procurement', 'procurements',
              'purchase', 'purchases', 'purchased', 'purchasing'])
#stemAcqKW = set([stemmer.stem_word(word) for word in acqKW])  # get unique elements, might be slow for huge lists

subjRel = set(['nsubj', 'agent', 'poss'])  # removed dep
subjAugRel = subjRel | set(['dep'])
subjAug2Rel = subjRel | set(['dep', 'nsubjpass'])

objRel = set(['dobj', 'nsubjpass', 'prep_of', 'appos', 'partmod', 'prep_over'])  # removed 'xcomp', added 'dep'
objAugRel = objRel | set(['xcomp'])
objAug2Rel = objRel | set(['xcomp', 'nsubjpass'])
rumorRel = set(['aux', 'amod'])
rumorKW = set(['might', 'may', 'contemplates', 'contemplate', 'possible', 'possibly'])
reverseRel = set(['prep_by'])
amountRel = set(['num', 'number'])
amountKW = set(['dollars', 'dollar', 'usd', 'euro', 'euros', 'eur', 'gbp', 'cad', 'aud', 'inr', 'dkk', 'czk', 'hkd', 'sgd', 'yen', 'jpy'])
amountSym = set(['$', 'US$'])  # might add unicode currency symbols later
amountKW |= amountSym
numKW = set(['billion', 'million', 'thousand', 'billions', 'millions', 'thousands', 'trillion', 'trillions'])
numKW2 = set(['b', 'm', 'k']) | numKW
replaceNumAbbrevDict2 = {'m':'million', 'k':'thousand', 'b':'billion', 't':'trillion'}
verbModRel = set(['xcomp', 'infmod', 'prepc_in', 'dobj', 'prep_to'])
ccompRel = set(['ccomp', 'dobj', 'infmod', 'xcomp', 'prep_of'])
ccompAugRel = ccompRel | verbModRel
pronounKW = set(['it', 'It', 'its', 'Its', 'theirs', 'Theirs', 'their', 'Their', 'they', 'They', 'them', 'Them', 'he', 'He', 'she', 'She', 'I'])

stakeKW = set(['stake', 'ownership'])
assetsKW = set(['assets', 'most'])
verbModKW = set(['agrees', 'agreed', 'commits', 'committed', 'decides', 'decided', 'prepares', 'prepared'])

andRel = set(['conj_and'])  # removed nn
orRel = set(['conj_or'])
unsureRel = set(['nn'])

removeKW = pronounKW  # things to remove from the company dictionary just in case

numPostfixSet = set(['st', 'nd', 'rd', 'th', 'ST', 'ND', 'RD', 'TH'])

# # Fundraise variables
FRKW1 = set(['raise', 'raises', 'raised', 'raising', 'secure', 'secures', 'secured', 'securing', 'land', 'lands', 'landed', 'landing', 'receive', 'receives', 'received', 'receiving', \
       'got', 'gotten', 'get', 'gets', 'getting', 'snag', 'snags', 'snagged', 'snaggin'])
FRKW2 = set(['close', 'closes', 'closed', 'leads', 'led', 'lead', 'complete', 'completes', 'completed', 'joined', 'co-led'])
FRKW3 = set(['invest', 'invests', 'invested', 'investment'])

roundNumKW = set(['first', 'second', 'third', 'fourth', 'fifth', 'sixth', 'a', 'b', 'c', 'd', 'f', 'g', 'h'])

# # Company description variables
descPhrasePOS = set(['NN', 'NNP', 'NNS', 'NNPS', 'JJ', 'JJR', 'JJS', 'VBG', 'DT'])  # added DT
descPhraseAugPOS = descPhrasePOS | set(['CC', ',', 'POS'])  # added ','
nounPOS = set(['NN', 'NNP', 'NNS', 'NNPS'])
verbPOS = set(['VB', 'VBD', 'VBG', 'VBN', 'VBN', 'VBP', 'VBZ'])
jobPositionKW = set(['CEO', 'CTO', 'VP', 'Vice', 'President', 'CFO', 'CIO', 'Chief', 'COO', 'Sr.', 'Sr', 'Senior', 'Director', 'Chief', 'Chairman'])
bracketSym = set(['-RRB-', '-LRB-', '-RSB-', '-LSB-', '-RCB-', '-LCB-'])
openCloseBracketSym = {'-LRB-':'-RRB-', '-LSB-':'-RSB-', '-LCB-':'-RCB-'}

capStopwords = set(['I', 'It', 'Its', 'He', 'She', 'They', 'We', 'There', 'Internet', 'Well', 'First', 'Second', 'Third', 'Fourth', 'Fifth', 'Corporation', 'Calif.', \
                 'Further', 'TVs', 'Plus', 'Jr.', 'Directors', 'Data', 'D', 'Customers', 'Below', 'iPhone', 'Technology', 'News', 'Global', 'Platform', \
                 'This', 'Technologies', 'Networks', 'HTML5', 'HTML', 'Management', 'M&A', 'H1', 'Dr.', 'Yep', 'Wifi', 'Wi-fi', 'Wi-LAN', 'URL', 'Research', \
                 'Advertisers', 'The Company', 'Historically', 'Risks', 'Pricing', 'NFC', 'Mobile', 'However', 'But', 'And', 'Otherwise', 'Instead', 'Nevertheless', 'Also', \
                 'Yet', 'Therefore', 'Thus', 'So', 'Finally', 'Meanwhile', 'Actually', 'Anyway', 'Although', 'Alternatively', 'Alternately', 'Specifically', 'Moreover', 'Luckily', 'Ads', \
                 '2G', '3G', '4G', 'L.L.C.', 'Software', 'Series A', 'Series B', 'Series C', 'Series D', 'Series E', 'One', 'Top News', 'Such', 'That', 'The', \
                 'e-Commerce', 'Stockholders', 'Q1', 'Q2', 'Q3', 'Q4', 'USD', 'US', 'U.S.', 'Euro', 'IT', 'I.T.', 'Indeed']) | dateSet | usaSet | countriesSet | citiesSet | jobPositionKW | abbrevSet

descUnigramStopwords = set(['and'])
descBigramStopwords = set(['as well', 'along with', 'combined with', 'coupled with'])
whichWhoStopwords = set(['which', 'who'])
leadingTrigramStopwords = set(['Related articles :', 'Related Articles :', 'For more :', 'For More :'])
andOrSet = set(['and', '&', 'or'])
NPDescEndStopwords = andOrSet | set(['the', ','])
startCNameStopwords = set(['The', 'About'])
nounVerbPOS = nounPOS | verbPOS

# direct desc kw
providesKW = set(['provides', 'offers', 'develops', 'delivers', 'engages', 'empowers'])
isWasKW = set(['is', 'was', 'are'])
aTheKW = set(['a', 'an', 'the'])
inForKW = set(['in', 'for', 'of', 'to', 'through', 'throughout'])
thatWhichKW = set(['that', 'which', 'where'])
companyPronounKW = set(['it', 'company', 'firm', 'organization', 'business', 'they', 'They', 'It', 'corporation'])
compKW = set(['company', 'firm', 'organization', 'group', 'conglomerate', 'corporation', 'outfit', 'enterprise', 'partnership', 'gang', \
              'house', 'association', 'bunch', 'megacorp', 'crew', 'crowd', 'agency', 'business', 'department', 'office', 'bureau', 'leader'])
# #

replaceNumAbbrevDict = {'mln':'million', 'bln':'billion', 'tln':'trillion'}

nnRel = set(['nn', 'amod', 'num', 'number'])  # for finding noun phrases

puncKW = set(['.', ',', ':', ';', '?', '/', '\\', ']', '}', '!', '*', '^', '%', '-', '--', '---', '-RRB-', ' ', '..', '...'])
sentEndSet = set(['.', '?', '!'])
interrobangSet = set(['?', '!'])

# For sentence begin/end detection
closeQuotesSet = set(['"', '”', '’', "'", u'\u2019', u'\u201d', u'\u201a', u'\u201e', u'\u301e', u'\u301f'])  # note the use of unicode quote symbols so utf-8 encoding must be set at the top of this file
openQuotesSet = set(['"', '“', '‘', "'", '`', u'\u2018', u'\u201b', u'\u201c', u'\u201f', u'\u301d'])
spaceSet = set([' ', u'\u00a0', u'\u2000', u'\u2001', u'\u2002', u'\u2003', u'\u2004', u'\u2005', u'\u2006', u'\u2007', u'\u2008', u'\u2009', u'\u200a', u'\u202f', u'\u205f'])
snlpCloseBracketSet = set([')', '}', ']', '-RRB-', '-RCB-', '-RSB-'])
snlpOpenQuotesSet = set([u'`', u'``']) | openQuotesSet  # Stanford tokenizer maps common single char quotes to multi-char ascii versions, but determines whether they should be opening or closing quotes
snlpCloseQuotesSet = set([u"'", u"''"]) | closeQuotesSet
sentEndContinueSet = snlpCloseQuotesSet | spaceSet | snlpCloseBracketSet  # Potential ending characters of a complete sentence, but must continue checking to the left for actual ending punctuation
sentBeginContinueSet = snlpOpenQuotesSet | spaceSet | set([u'|'])

# For capitalization at beginning of sentences
sentBeginContinueRelaxedSet = sentBeginContinueSet | bracketSym

# allUnicode = sentEndSet | closeQuotesSet | openQuotesSet | spaceSet | set(["He said, 'Hello World.'", 'He said, "Hello World."'])

incSet = ["inc", "co", "dba", "llc", "ltd", "lc", "lllp", "llp", "lp", "pllc", "rllp", "rlllp", "corp", "pvt", "pty", "ultd", "unltd"]
incSet += [word + '.' for word in incSet]
incProperList = [word[0].upper() + word[1:] for word in incSet]
incSet += ['l.l.c.', 'l.c.', 'l.l.l.p.', 'l.l.p.', 'l.p.', 'p.c.', 'p.l.l.c.', 'r.l.l.p.', 'r.l.l.l.p.', 'd.b.a.', ]
incSet = set(incSet)
incUpperCaseSet = set(incProperList) | set([item.upper() for item in incSet]) # Inc., INC., INC, LLC, etc...

nerRemoveKW = set(['LOCATION', 'DATE'])

addKW = []

maxDepth = 6
defaultWordLimit = 64 # 80 words requires up to ~2.1GB of memory
defaultSentLimit = 200 

# # NLP tools variables
incStopwords = set(["inc", "co", "dba", "llc", "ltd", "lc", "lllp", "llp", "pllc", "corp", "pvt", "pty"])
incStopwords |= set([word[0].upper() + word[1:] for word in incStopwords])
incStopwords |= set(['INC', 'CO', 'DBA', 'LLC', 'LTD', 'LC', 'LLLP', 'LLP', 'PLLC', 'CORP', 'PVT', 'PTY'])
incStopwords |= set([word + '.' for word in incStopwords])

POSMaster = ['CC', 'CD', 'DT', 'EX', 'FW', 'IN', 'JJ', 'JJR', 'JJS', 'LS', 'MD', 'NN', 'NNS', 'NNP', 'NNPS', 'PDT', 'POS', 'PRP', 'PRP$', 'PP$', 'RB', 'RBR', 'RBS', 'RP', 'SYM', \
             'TO', 'UH', 'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ', 'WDT', 'WP', 'WP$', 'WRB', '#', '$', '.', ',', ':', '(', ')', '"', '`', '``', '\'', '\'\'', '-LRB-', '-RRB-']
#POSMasterDict = {POSMaster[idx]:idx for idx in xrange(len(POSMaster))} # not Python 2.6 friendly
POSMasterDict = {}
for idx in xrange(len(POSMaster)):
    POSMasterDict[POSMaster[idx]] = idx

NERMaster = ['O', 'TIME', 'LOCATION', 'ORGANIZATION', 'PERSON', 'MONEY', 'PERCENT', 'DATE', 'ORDINAL', 'NUMBER', 'MISC', 'SET', 'DURATION']
#NERMasterDict = {NERMaster[idx]:idx for idx in xrange(len(NERMaster))} # not Python 2.6 friendly
NERMasterDict = {}
for idx in xrange(len(NERMaster)):
    NERMasterDict[NERMaster[idx]] = idx
    
DEPMaster = [u'root',u'aux',u'auxpass',u'cop',u'arg',u'agent',u'comp',u'acomp',u'attr',u'ccomp',u'xcomp',u'complm',u'obj',u'dobj',u'iobj',u'pobj',u'mark',u'rel',u'subj',u'nsubj',u'nsubjpass',u'csubj',
             'csubjpass',u'cc',u'conj',u'expl',u'mod',u'abbrev',u'amod',u'appos',u'advcl',u'purpcl',u'det',u'predet',u'preconj',u'infmod',u'mwe',u'partmod',u'advmod',u'neg',u'rcmod',
             'quantmod',u'nn',u'npadvmod',u'tmod',u'num',u'number',u'prep',u'poss',u'possessive',u'prt',u'parataxis',u'punct',u'ref',u'sdep',u'xsubj',u'prep_of',u'prep_with',u'prep_in',\
             u'prep_on',u'prep_for',u'prep_at',u'prep_over',u'prep_about',u'prep_by',u'prep_to',u'prep_during']
DEPMasterDict = {}
for idx in xrange(len(DEPMaster)):
    DEPMasterDict[DEPMaster[idx]] = idx

titleLowerCaseKW = set(['of', 'the', 'a', 'an', 'for', 'in', 'on', 'at', 'to', 'by', 'and'])

compLowerCaseKW = set(['of', '&', 'for', 'de', 'the', 'in', 'at', 'on', 'to', 'by', '\'s'])

excludeFirstWordDict = {'PRESS':set(['RELEASE']), \
                        'UPDATE':set([':']), \
                        'REVIEW':set([':']), \
                        'SOURCE':set([':']), \
                        'Press':set(['Release', 'release'])}

webExtSet = set(['ac', 'ad', 'ae', 'af', 'ag', 'ai', 'al', 'ao', 'aq', 'ar', 'as', 'au', 'ax', 'az', 'ba', 'bb', 'bd', 'bf', 'bg', 'bh', 'bi', \
                 'bj', 'bm', 'bn', 'bo', 'br', 'bs', 'bt', 'bv', 'bw', 'bz', 'ca', 'cc', 'cd', 'cf', 'cg', 'ch', 'ci', 'ck', 'cl', 'cm', 'cn', 'co', 'cr', \
                 'cs', 'cu', 'cv', 'cx', 'cy', 'cz', 'dd', 'de', 'dj', 'dk', 'dm', 'dz', 'ec', 'ee', 'eg', 'er', 'es', 'et', 'eu', 'fi', 'fj', \
                 'fk', 'fm', 'fo', 'fr', 'ga', 'gb', 'gd', 'ge', 'gf', 'gg', 'gh', 'gi', 'gl', 'gm', 'gn', 'gp', 'gq', 'gr', 'gs', 'gt', 'gu', 'gw', 'gy', \
                 'hk', 'gm', 'gn', 'hr', 'ht', 'hu', 'id', 'il', 'im', 'io', 'iq', 'ir', 'je', 'jm', 'jo', 'jp', 'ke', 'kh', 'ki', 'kn', 'kp', 'kr', 'kw', 'ky', 'kz', \
                 'la', 'lb', 'lc', 'li', 'lk', 'lr', 'ls', 'lt', 'lu', 'lv', 'ly', 'ma', 'mc', 'md', 'me', 'mh', 'mk', 'ml', 'mm', 'mn', 'mo', 'mp', 'mq', \
                 'mv', 'mw', 'mx', 'mz', 'na', 'nf', 'ni', 'nl', 'np', 'nr', 'nu', 'nz', 'om', 'pa', 'pe', 'pf', 'pg', 'ph', 'pk', 'pl', 'pm', 'pn', 'pr', \
                 'ps', 'pt', 'pw', 'py', 'qa', 're', 'ro', 'rs', 'ru', 'rw', 'sa', 'sb', 'sc', 'se', 'sg', 'sh', 'si', 'sj', 'sk', 'sl', 'sm', 'sn', \
                 'sr', 'ss', 'su', 'sv', 'sx', 'sy', 'sz', 'tc', 'td', 'tf', 'tg', 'th', 'tj', 'tk', 'tl', 'tm', 'tn', 'tp', 'tr', 'tt', 'tv', 'tw', 'tz', 'ua', \
                 'ug', 'uk', 'us', 'uy', 'uz', 'va', 'vc', 've', 'vg', 'vi', 'vn', 'vu', 'wf', 'ws', 'ye', 'yt', 'yu', 'za', 'zm', 'zw', 'com', 'net', 'org', 'biz'])

# General stopwords, used in relevance
nltkStopwordsLower = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', \
                 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'these', \
                 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', \
                 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', \
                 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', \
                 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', \
                 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now']

nltkStopwords = set(nltkStopwordsLower + [word[0].upper()+word[1:] for word in nltkStopwordsLower] + ['EST','UPDATED','PUBLISHED','Instead','However','Although',]) | jobPositionKW

# Generate sequential stopwords for company name replacement
excludeCompNameDict = {}
excludeCompNameFirstDict = {}
for item in jobPositionKW:
    excludeCompNameDict[item] = set(['of', 'at', '&'])  # CEO of, CTO at, etc.
excludeCompNameDict['in'] = dateSet
excludeCompNameDict['on'] = dateSet
excludeCompNameFirstDict = {'According':set(['to']), \
                            'Headquartered':set(['in']), \
                            'Based':set(['in', 'on', 'at']), \
                            'About':set(['the']), \
                            'Prior':set(['to']), \
                            'As':set(['of', 'for', 'the', 'in', 'to']), \
                            'In':set(['the']), \
                            'With':set(['the']), \
                            'While':set(['the', 'at', 'in', 'for', 'on']), \
                            'On':set(['the']), \
                            'At':set(['the']), \
                            'But':set(['the', 'in', 'for', 'on', 'by']), \
                            'Both':set(['the', 'of']), \
                            'Founded':set(['by', 'in', 'on', 'at']), \
                            'And':set(['the', 'in', 'for', 'on', 'at']), \
                            'Using':set(['the']), \
                            'Like':set(['the', 'on', 'in']), \
                            'All':set(['of', 'the', 'in']), \
                            'If':set(['the']), \
                            'One':set(['of']), \
                            'Although':set(['the']), \
                            'From':set(['the']), \
                            'Some':set(['of', 'in']), \
                            'Similar':set(['to']), \
                            'Through':set(['the']), \
                            'Thanks':set(['to']), \
                            'News':set(['of']), \
                            'For':set(['the']), \
                            'When':set(['the']), \
                            'Speaking':set(['at', 'of', 'to', 'in', 'on', 'for']), \
                            'Pricing':set(['for', 'on', 'in', 'of']), \
                            'Visit':set(['the']), \
                            'Shares':set(['of', 'in']), \
                            'Because':set(['the', 'of']), \
                            'Users':set(['of', 'in', 'on', 'at']), \
                            'Powered':set(['by']), \
                            'Members':set(['of', 'in']), \
                            'New':set(['to', 'in']), \
                            'Led':set(['by']), \
                            'Available':set(['in', 'for', 'on', 'to', 'at']), \
                            'Located':set(['in', 'on', 'at']), \
                            'Back':set(['to', 'at', 'in', 'on']), \
                            'Unlike':set(['the', 'in', 'on']), \
                            'Today':set(['at', 'the', 'in', 'on']), \
                            'Since':set(['the']), \
                            'Posted':set(['by', 'in', 'for']), \
                            'Download':set(['the']), \
                            'Backed':set(['by']), \
                            'More':set(['on']), \
                            'Called':set(['the']), \
                            'Support':set(['for']), \
                            'Most':set(['of']), \
                            'Under':set(['the']), \
                            'After':set(['the']), \
                            'Developed':set(['by', 'on', 'at', 'in']), \
                            'Built':set(['by', 'on', 'at']), \
                            'Part':set(['of']), \
                            'Also':set(['on', 'at', 'in', 'the', 'for', 'by']), \
                            'Note':set(['to', 'the']), \
                            'Contact':set(['the']), \
                            'Hosted':set(['by', 'at', 'in', 'on']), \
                            'Many':set(['of']), \
                            'Read':set(['the', 'on']), \
                            'During':set(['the']), \
                            'Visitors':set(['to', 'of']), \
                            'Now':set(['the', 'on', 'in', 'at']), \
                            'Here':set(['at']), \
                            'Features':set(['of']), \
                            'Following':set(['the', 'on', 'in']), \
                            'Subscribe':set(['to']), \
                            'Though':set(['the']), \
                            'Via':set(['the']), \
                            'See':set(['the']), \
                            'Join':set(['the']), \
                            'Investors':set(['in', 'of']), \
                            'Written':set(['by', 'in']), \
                            'Customers':set(['of', 'in']), \
                            'Once':set(['the', 'on', 'in']), \
                            'How':set(['to', 'the']), \
                            'Details':set(['of', 'on', 'at']), \
                            'Sales':set(['of']), \
                            'Created':set(['by', 'for', 'in']), \
                            'Where':set(['the', 'to']), \
                            'Launched':set(['by', 'in', 'at']), \
                            'So':set(['the', 'in', 'for', 'at']), \
                            'Best':set(['of', 'in']), \
                            'Compared':set(['to']), \
                            'Over':set(['in', 'at']), \
                            'Look':set(['for', 'at']), \
                            'Information':set(['on']), \
                            'Even':set(['the', 'in', 'at', 'for', 'on']), \
                            'Building':set(['on']), \
                            'What':set(['the']), \
                            'Research':set(['by']), \
                            'Add':set(['to']), \
                            'Access':set(['to']), \
                            'Within':set(['the']), \
                            'We':set(['at']), \
                            'Running':set(['on', 'the']), \
                            'Presented':set(['by', 'at']), \
                            'Unfortunately':set(['for', 'the']), \
                            'By':set(['the']), \
                            'Announced':set(['at', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']), \
                            'Agencies':set(['of']), \
                            'Registration':set(['for']), \
                            'Outside':set(['of', 'the']), \
                            'Notes':set(['to']), \
                            'Neither':set(['the', 'of']), \
                            'Held':set(['at', 'in', 'on']), \
                            'Dubbed':set(['the']), \
                            'Winners':set(['of']), \
                            'Inclusion':set(['in', 'of']), \
                            'Go':set(['to']), \
                            'Designed':set(['by']), \
                            'Use':set(['of', 'the']), \
                            'Published':set(['by', 'in', 'on']), \
                            'Commenting':set(['on']), \
                            'Officials':set(['at', 'in', 'of', 'for']), \
                            'Named':set(['to', 'the', 'Best']), \
                            'Fans':set(['of']), \
                            'Before':set(['the']), \
                            'Register':set(['for']), \
                            'Ranked':set(['by']), \
                            'Much':set(['of']), \
                            'Submitted':set(['by']), \
                            'Sponsors':set(['of', 'for']), \
                            'Representatives':set(['of', 'for']), \
                            'Reporting':set(['to']), \
                            'Membership':set(['in']), \
                            'Each':set(['of']), \
                            'Attendees':set(['of', 'at']), \
                            'Among':set(['the']), \
                            'Adding':set(['to', 'the']), \
                            'Prices':set(['for', 'in', 'of']), \
                            'Highlights':set(['of', 'in']), \
                            'Whether':set(['the', 'in', 'on', 'for']), \
                            'Think':set(['of']), \
                            'Moderated':set(['by']), \
                            'Funded':set(['by']), \
                            'Click':set(['the', 'on', 'to']), \
                            'Several':set(['of']), \
                            'Owners':set(['of']), \
                            'Leading':set(['the']), \
                            'Currently':set(['the', 'in', 'at']), \
                            'Joining':set(['the']), \
                            'Investing':set(['in']), \
                            'First':set(['the', 'to']), \
                            'Company':set(['to']), \
                            'Co-founded':set(['by']), \
                            'Writing':set(['on', 'for', 'to', 'in']), \
                            'Take':set(['the']), \
                            'Shop':set(['for']), \
                            'Optimized':set(['for', 'by']), \
                            'Filed':set(['in', 'by']), \
                            'Despite':set(['the']), \
                            'Congratulations':set(['to']), \
                            'Central':set(['to']), \
                            'Expenditures':set(['by', 'for']), \
                            'Two':set(['of']), \
                            'Three':set(['of']), \
                            'Terms':set(['of']), \
                            'Subscribers':set(['to', 'of']), \
                            'Participants':set(['in', 'of', 'at']), \
                            'Organized':set(['by']), \
                            'Looking':set(['at', 'to', 'for']), \
                            'Installation':set(['of', 'on']), \
                            'Does':set(['the']), \
                            'Beyond':set(['the']), \
                            'Benefits':set(['of', 'to', 'for']), \
                            'Utilizing':set(['the']), \
                            'Listed':set(['on', 'by', 'in']), \
                            'Everyone':set(['in', 'at', 'on']), \
                            'Dial':set(['in']), \
                            'Whereas':set(['the', 'in']), \
                            'Unique':set(['to']), \
                            'Similarly':set(['to', 'in', 'on']), \
                            'Produced':set(['by']), \
                            'People':set(['in', 'on', 'at']), \
                            'Only':set(['the', 'for']), \
                            'Integration':set(['of', 'to']), \
                            'Enter':set(['the']), \
                            'Due':set(['to']), \
                            'Why':set(['the']), \
                            'Welcome':set(['to']), \
                            'Rumors':set(['of', 'on']), \
                            'Recognized':set(['by', 'for', 'on']), \
                            'Photo':set(['of', 'by']), \
                            'Growth':set(['in', 'of']), \
                            'Given':set(['the', 'by']), \
                            'Come':set(['to', 'on']), \
                            'Additionally':set(['the']), \
                            'Watch':set(['the']), \
                            'View':set(['the']), \
                            'Previous':set(['to']), \
                            'Live':set(['from', 'at']), \
                            'Launching':set(['in', 'on', 'at']), \
                            'Inside':set(['the', 'of']), \
                            'Get':set(['the']), \
                            'Turning':set(['to']), \
                            'Tickets':set(['for', 'to']), \
                            'Taking':set(['on', 'the']), \
                            'Half':set(['of', 'the']), \
                            'Find':set(['the']), \
                            'Established':set(['in', 'by']), \
                            'Demonstrations':set(['of']), \
                            'Working':set(['on', 'in', 'for', 'at']), \
                            'Up':set(['to']), \
                            'Scheduled':set(['for']), \
                            'Owned':set(['by']), \
                            'Meanwhile':set(['the', 'on', 'in', 'for', 'at']), \
                            'Fortunately':set(['for', 'the']), \
                            'Demand':set(['for']), \
                            'Availability':set(['for', 'of']), \
                            'Thousands':set(['of']), \
                            'Then':set(['the', 'in', 'on', 'for']), \
                            'Supported':set(['by']), \
                            'Return':set(['to', 'of']), \
                            'Resources':set(['for']), \
                            'Next':set(['to', 'the']), \
                            'Featured':set(['in']), \
                            'Editing':set(['by']), \
                            'Copies':set(['of']), \
                            'Connecting':set(['to', 'the']), \
                            'Comments':set(['on', 'for']), \
                            'Changes':set(['to', 'in']), \
                            'Born':set(['in']), \
                            'Applications':set(['for', 'on', 'of', 'to']), \
                            'Another':set(['of']), \
                            'Acquisition':set(['of']), \
                            'Acquired':set(['by']), \
                            'Specializing':set(['in']), \
                            'Moving':set(['to', 'on']), \
                            'Launches':set(['the']), \
                            'Is':set(['the']), \
                            'Interest':set(['in', 'by']), \
                            'Installing':set(['the']), \
                            'Being':set(['in', 'on', 'the']), \
                            'Apparently':set(['the', 'in']), \
                            'Whilst':set(['the']), \
                            'Speakers':set(['for', 'at', 'on', 'in']), \
                            'Reports':set(['of', 'the', 'on', 'in', 'for']), \
                            'Previously':set(['the', 'at']), \
                            'Millions':set(['of']), \
                            'Measurements':set(['of']), \
                            'Manufactured':set(['by', 'in']), \
                            'Introducing':set(['the']), \
                            'Featuring':set(['the']), \
                            'Everything':set(['in']), \
                            'Developers':set(['of']), \
                            'Data':set(['on']), \
                            'Congrats':set(['to']), \
                            'Clicking':set(['the']), \
                            'None':set(['of']), \
                            'Luckily':set(['for']), \
                            'Inspired':set(['by']), \
                            'Focusing':set(['on']), \
                            'Finally':set(['the']), \
                            'Expect':set(['the']), \
                            'Could':set(['the']), \
                            'Components':set(['of']), \
                            'Co-sponsored':set(['by']), \
                            'Background':set(['on']), \
                            'Alongside':set(['the']), \
                            'Updates':set(['to']), \
                            'Revenue':set(['for']), \
                            'Management':set(['of']), \
                            'Initially':set(['the']), \
                            'Development':set(['of']), \
                            'Debt':set(['to']), \
                            'Complementing':set(['the']), \
                            'Attend':set(['the']), \
                            'Applied':set(['to']), \
                            'Without':set(['the']), \
                            'Starting':set(['in', 'at']), \
                            'Started':set(['in', 'by']), \
                            'Registrations':set(['for']), \
                            'Perfect':set(['for']), \
                            'Overview':set(['of']), \
                            'Of':set(['the']), \
                            'Making':set(['the']), \
                            'Link':set(['to']), \
                            'Inventor':set(['of']), \
                            'Including':set(['the']), \
                            'Images':set(['of', 'on']), \
                            'Extending':set(['the']), \
                            'Except':set(['for', 'the']), \
                            'Driven':set(['by']), \
                            'Drawing':set(['on']), \
                            'Comprised':set(['of']), \
                            'Competitors':set(['to']), \
                            'Co-headquartered':set(['in']), \
                            'Capitalizing':set(['on']), \
                            'Calls':set(['to']), \
                            'Attendance':set(['at', 'on', 'in']), \
                            'Are':set(['the']), \
                            'Announcing':set(['the']), \
                            'True':set(['to']), \
                            'Timing':set(['of']), \
                            'Until':set(['the']), \
                            'Targeted':set(['at']), \
                            'Supply':set(['of']), \
                            'Study':set(['of']), \
                            'Summary':set(['of']), \
                            'Presentation':set(['at', 'by']), \
                            'Photos':set(['of', 'by', 'on']), \
                            'Links':set(['to']), \
                            'Introduced':set(['in', 'by', 'for', 'at']), \
                            'Interested':set(['in']), \
                            'Expanding':set(['to']), \
                            'Excluding':set(['the']), \
                            'Examples':set(['of']), \
                            'Employees':set(['of', 'in', 'at']), \
                            'Delivery':set(['of']), \
                            'Cost':set(['of']), \
                            'Co-founder':set(['of']), \
                            'Founder':set(['of']), \
                            'Exclusive':set(['to']), \
                            'Deployment':set(['of']), \
                            'Can':set(['the']), \
                            'Aimed':set(['at']), \
                            'Used':set(['by']), \
                            'Having':set(['the']), \
                            }

excludeFirstKW = {}
excludeFirstTwoKW = {'PRESS':set(['RELEASE']), \
                  'Update':set([':']), \
                  'Press':set(['Release']), \
                  }

# #
def createValidCapSet(articleToksList, allCapsFlagList):
    # Generate a set of capital words that appear in the article, not including first words of sentences, and not using all cap sentences
    validCapSet = set([])
    
    # Create dictionary of words:idx
    articleToksDictList = createDictList(articleToksList)
    
    # Find first valid index to take capital words
    minValidIdxList = []  # stores index of 2nd token that is not a quote or bracket from the beginning of the sentence
    for sentIdx in xrange(len(articleToksList)):
        sentToks = articleToksList[sentIdx]
        # Create list of valid first indices, counting past initial quotes, spaces, or brackets
        if not allCapsFlagList[sentIdx]:
            for i in xrange(len(sentToks)):
                # Check that the sentence in the article isn't all caps either.
                if sentToks[i] not in sentBeginContinueRelaxedSet:  # i is index of first token that is not bracket or quote
                    break
            minValidIdxList.append(i + 1)
        else:
            minValidIdxList.append(1000)  # arbitrary number, won't get exercised later
    # Extract only valid words from sentence dictionaries and compile into one
    for i in xrange(len(articleToksDictList)):
        if not allCapsFlagList[i]:
            toksDict = articleToksDictList[i]
            for word in toksDict.keys():
                # Add valid words that have capitals
                if toksDict[word][-1] >= minValidIdxList[i] and containsCap(word, allowNumPostfix=False):
                    validCapSet.add(word)   
    return validCapSet

def recaseNewsTokens(titleToksList, articleToksList):
    # This checks the words in all cap sentences against lower case sentences in the article.
    # Keep capitalization if it finds the same word in a sentence (2nd word or later) that isn't all caps. Also takes into account leading quotes, brackets, etc.
    
    # Tokenizer will incorrectly split titles with Inc. or Corp. followed by capital word, rejoin these extra sentences first
    # Only do this for title because it should almost always be one sentence.  
    # If we don't rejoin, the next word will stay capitalized because it thinks its the first word of a new sentence.
    newTitleToksList = []
    if len(titleToksList)>0:
        newTitleToksList.append(titleToksList[0])
        for i in xrange(1,len(titleToksList)):
            if len(titleToksList[i-1])>1 and titleToksList[i-1][-1] == '.' and titleToksList[i-1][-2][-1] == '.':
                newTitleToksList[-1].pop() # remove period
                newTitleToksList[-1] += titleToksList[i] # merge token lists
    titleToksList = newTitleToksList
    
    # Form list of flags for sentences that are all caps
    titleAllCapsFlagList = [isAllCaps(titleToks) for titleToks in titleToksList]
    allCapsFlagList = [isAllCaps(toks) for toks in articleToksList]
    
    shouldRecaseTitle = any(titleAllCapsFlagList)
    shouldRecaseArticle = any(allCapsFlagList)
    if shouldRecaseTitle or shouldRecaseArticle:
        validCapSet = createValidCapSet(articleToksList, allCapsFlagList) | incUpperCaseSet
        
    if shouldRecaseTitle:
        recasedTitleToksList = []
        for i in xrange(len(titleToksList)):
            if titleAllCapsFlagList[i]:
                recasedTitleToksList.append(recaseSentence(titleToksList[i], validCapSet))
            else:
                recasedTitleToksList.append(titleToksList[i])
    else:
        recasedTitleToksList = titleToksList
    
    if shouldRecaseArticle:
        recasedArticleToksList = []
        for i in xrange(len(articleToksList)):
            if allCapsFlagList[i]:
                recasedArticleToksList.append(recaseSentence(articleToksList[i], validCapSet))
            else:
                recasedArticleToksList.append(articleToksList[i])
    else:
        recasedArticleToksList = articleToksList
    
    return recasedTitleToksList, recasedArticleToksList, titleAllCapsFlagList, allCapsFlagList
        
def recaseSentence(toks, validCapSet):
    # Returns toks in lowercase form unless they appear in validCapSet or is first word
    
    # Find location of first actual word
    firstValidIdx = 0
    for firstValidIdx in xrange(len(toks)):
        if toks[firstValidIdx] not in sentBeginContinueRelaxedSet:  # ignore brackets / quotes
            break 
    # Recase each token
    newToks = []
    for i in xrange(len(toks)):
        if i > firstValidIdx and toks[i] not in validCapSet:  # keep capitalization of first valid word
            newToks.append(toks[i].lower())
        else:
            newToks.append(toks[i])
    return newToks

def validSentEnd(segment):
    # Checks whether segment is likely to be a properly ended sentence (ends on punctuation, but skip past spaces and closing quotes)
    if len(segment) > 0:
        for i in xrange(-1, -len(segment) - 1, -1):
            if segment[i] in sentEndSet:
                return True
            elif segment[i] not in sentEndContinueSet:
                return False
    return False

def validSentBeginning(segment):
    # Checks whether segment is likely to be a properly started sentence (first word contains cap, but skip past spaces and opening quotes)
    if len(segment) > 0:
        started = False  # found a lowercase
        for i in xrange(len(segment)):
            if segment[i].isupper():
                return True
            elif not started and segment[i] not in sentBeginContinueSet:  # encountered a lower case
                started = True
            elif started and segment[i] in spaceSet:  # end search if we encounter a space after the first lower case
                return False
    return False

def getFirstValidCapIdx(toks):
    # skips to first word that should be capitalized (i.e. ignores opening quotes and brackets)
    for i in xrange(len(toks)):
        if toks[i] not in sentBeginContinueRelaxedSet:
            return i
    return len(toks)

def removeNewlines(article):
    # Remove newlines, but infer whether they were used to delineate the end of a sentence or not. 
    # Count the swing number of times sentences don't end with punctuation and start with capital letter vs. ending with a period or not starting with capital
    # If count > 0 then that means majority of newlines are at the ends of sentences, so we need to add periods. If count<0, then we probably don't.
    
    article = article.decode('utf-8',errors='replace')  # make sure strings are represented in Unicode so 1 literal character is 1 slot
    
    # Replace pathological words
    article = article.replace('.NET', '-DOT-NET')
    
    # First split using carriage return newlines \r\n (supposed to be the web standard, but not usually followed)
    crSegments = article.split('\r\n')
    
    # Then segment further using \r and \n separately
    crnSegments = []
    segments = []
    for crSeg in crSegments:
        segs = crSeg.split('\n')
        crnSegments += [item for item in segs if len(item) > 0]  # only include non empty segments
    for crnSeg in crnSegments:
        segs = crnSeg.split('\r')
        segments += [item for item in segs if len(item) > 0]
    
    if len(segments) > 1:
        goodEnd = []
        goodBegin = []
        for i in xrange(len(segments)):
            if i > 0:
                goodEnd.append(validSentEnd(segments[i - 1]))
            if i < len(segments) - 1:
                goodBegin.append(validSentBeginning(segments[i + 1]))

        count = 0.0  # swing number of times newlines are at the end of completed sentences.
        addPunc = []                
        for i in xrange(len(goodEnd)):
            if goodEnd[i]:  # previous segment is complete sentence
                count += 1  # newline used at end of complete sentence
                addPunc.append(False)
            elif goodBegin[i]:  # previous sentence not complete, but next segment starts with cap, suggests newlines might delineate end of sentences (but not sure)
                count += 0.7
                addPunc.append(True)
            else:  # both segments should be contiguous, suggests newlines not used at end of complete 
                count -= 1
                addPunc.append(False)
                # print segments[i][-50:], '<No .>', segments[i+1][:50]
                
        reconSegments = [segments[0]]
        for i in xrange(len(goodEnd)):
            if addPunc[i] and count >= 0:
                reconSegments.append('.')
                # print segments[i][-50:], '<C .>', segments[i+1][:50]
            # elif addPunc[i] and count < 0:
                # print segments[i][-50:], '<NoC .>', segments[i+1][:50]
            reconSegments.append(segments[i + 1])
        return ' '.join(reconSegments)  # it is much faster to create a list and then use ' '.join() than to use string1 += string2
    else:
        return article 

def sentenceRemap(toksList1, toksList2):
    # Not used, breaks because sometimes malformed unicode characters are ignored in the pipeline vs tokenizer, making tokens slightly different
    # Assumes toksList1 has more sentences than toksList2
    # Returns mapping of sentence indices in toksList2 to toksList1
    # Useful for copying all capital flags
    # This is a band-aid function for the <1% of articles where the sentences get extra splits when re-passed through the pipeline after the tokenizer itself 
    # Does not cover the case if several toksList2 sentences get extra splits in a row in toksList1 (will skip the mapping to the next COMPLETE sentence match)
    # This should be <0.1% of the cases, probably
    j = 0
    jLast = 0
    mapping = []
    for i in xrange(max(len(toksList1), len(toksList2))):
        try:
            print '1>', toksList1[i]
        except:
            pass
        try:
            print '2>', toksList2[i]
        except:
            pass
    for i in xrange(len(toksList1)):
        foundMatch = False
        for k in xrange(j, len(toksList2)):
            if tokensMatch(toksList1[i], toksList2[k]):
                mapping.append(k)
                if k - jLast > 1:
                    print 'WARNING: Skipped toksList2 sentence:', k - jLast
                jLast = k
                j = k + 1
                foundMatch = True
                break
        if not foundMatch:
            mapping.append(j)
    return mapping
        
def tokensMatch(toks1, toks2):
    if len(toks1) == len(toks2):
        for i in xrange(len(toks1)):
            if toks1[i] != toks2[i]:
                return False
    return True

def isAllCaps(tokens):
    # Works on one sentence (a single list of tokens)
    # Returns False if at least one word has a capital letter and is more than 3 characters long
    for tok in tokens:     
        if len(tok) > 3 and not containsCap(tok, allowNumPostfix=False, countBracketAsCap=True) and not isNumber(tok):
            return False
    return True

def removeLeadingParenthetical(origToks, origDict):
    # Operates on one sentence
    # If sentence starts with opening bracket, will return first index after closing bracket
    if origToks[0] in openCloseBracketSym:
        if openCloseBracketSym[origToks[0]] in origDict:
            return origDict[openCloseBracketSym[origToks[0]]][0] + 1
    return 0

def removeLeadingParenthetical_old2(origToksList, origDictList):
    # Operates on all sentences list
    # Will split sentences with leading parenthetical expressions into two, and returns new sentences list.
    # Assumes that if parenthetical expression ends in .!? (inside or outside closing parens), it will already be its own sentence and won't split further (property of Stanford Tokenizer)
    newToksList = []
    for sentIdx in xrange(len(origToksList)):
        toks = origToksList[sentIdx]
        if toks[0] in openCloseBracketSym:
            if openCloseBracketSym[toks[0]] in origDictList[sentIdx]:
                startIdx = origDictList[openCloseBracketSym[toks[0]]][0] + 1
                # make sure at least 2 tokens after end of leading parenthetical expression, meaning the parenthetical isn't the whole sentence
                if startIdx < len(origToksList[sentIdx] - 1):  
                    newToksList.append(origToksList[sentIdx][:startIdx])
                    newToksList[-1].append('.')  # add period so that next tokenization makes sure to make this parenthetical a separate sentence
                    newToksList.append(origToksList[sentIdx][startIdx:]) 
    return newToksList
    
def removeLeadingParenthetical_old(toks, toksDict):
    # old
    # Takes as input the list of tokens, and a hashtable of tokens which point to an ascending list of indices of the words in the sentence.
    # Acts on the beginning of the sentence only, and removes up to the first ')' or ']'
    excludeIdx = set([])
    firstIdx = 0
    if len(toks) > 0:
        if toks[0] == '-LRB-' and '-RRB-' in toksDict:
            excludeIdx |= set(range(toksDict['-RRB-'][0] + 1))
            firstIdx = toksDict['-RRB-'][0] + 1
        elif toks[0] == '-LSB-' and '-RSB-' in toksDict:
            excludeIdx |= set(range(toksDict['-RSB-'][0] + 1))
            firstIdx = toksDict['-RSB-'][0] + 1
        elif toks[0] == '-LCB-' and '-RCB-' in toksDict:
            excludeIdx |= set(range(toksDict['-RCB-'][0] + 1))
            firstIdx = toksDict['-RCB-'][0] + 1
    return firstIdx, excludeIdx

def removeLeadingDates(toks):
    # Returns first index that is valid (not a date), if following word is not a lowercase word (i.e. use this for beginning of sentences only)
    # Case 1: June ##, #### or ## June, ####
    if len(toks) > 4 and len(toks[3]) == 4 and toks[2] == ',' and not containsOnlyLowerLetters(toks[4]) and isInteger(toks[3]):
        if toks[0] in monthSet and isNumberRelaxed(toks[1]):
            return 4
        if toks[1] in monthSet and isNumberRelaxed(toks[0]):
            return 4
    # Case 2: June ## #### or ## June #### or #### June ##
    elif len(toks) > 3 and not containsOnlyLowerLetters(toks[3]):
        if len(toks[2]) == 4 and isInteger(toks[2]):
            if toks[0] in monthSet and isNumberRelaxed(toks[1]):
                return 3
            if toks[1] in monthSet and isNumberRelaxed(toks[0]):
                return 3
        elif toks[0] in monthSet and len(toks[0]) == 4 and isInteger(toks[2]) and isNumberRelaxed(toks[0]):
            return 3
    # Case 3: June ## or ## June
    elif len(toks) > 2 and not containsOnlyLowerLetters(toks[2]):
        if toks[0] in monthSet and isNumberRelaxed(toks[1]):
            return 2
        if toks[1] in monthSet and isNumberRelaxed(toks[0]):
            return 2
    return 0

def removeLeadingDatesRelaxed(toks):
    # Returns first index that is valid (not a date), with relaxed variants (... of ...)
    # June ##, #### or ## June, ####
    if len(toks) >= 4 and len(toks[3]) == 4 and toks[2] == ',' and isInteger(toks[3]):
        if toks[0] in monthSet and isNumberRelaxed(toks[1]):
            return 4
        if toks[1] in monthSet and isNumberRelaxed(toks[0]):
            return 4
    # Case 2: June ## #### or ## June #### or June of #### or #### June ##
    elif len(toks) >= 3:
        if len(toks[2]) == 4 and isInteger(toks[2]):
            if toks[0] in monthSet:
                if isNumberRelaxed(toks[1]):
                    return 3
                if toks[1] == 'of':
                    return 3
            if toks[1] in monthSet and isNumberRelaxed(toks[0]):
                return 3
        elif len(toks[0]) == 4 and toks[1] in monthSet and isInteger(toks[0]) and isNumberRelaxed(toks[2]):
            return 3
    # Case 3: June ## or ## June
    elif len(toks) >= 2:
        if toks[0] in monthSet and isNumberRelaxed(toks[1]):
            return 2
        if toks[1] in monthSet and isNumberRelaxed(toks[0]):
            return 2
    return 0 

def removeLeadingPathologicalPhrases(origToks):
    # Returns first valid index after leading pathological expressions like PRESS RELEASE, Update:
    # Currently only works on first two tokens 
    if len(origToks) > 2:
        if origToks[0] in excludeFirstTwoKW and origToks[1] in excludeFirstTwoKW[origToks[0]]:
            return 2
    return 0

def fixSentenceSplits(origToksList, compDict, checkBangs=True):
    # Rejoin sentences that were split incorrectly due to two letter domain extensions, then replace periods with -DOT- so it doesn't happen again
    # If desired, also check for sentences split due to ! in company names, and check against AUGMENTED gazetteer
    newToksList = []
    numReplacements = 0
    # numEmpty = 0
    for sentIdx in xrange(len(origToksList)):
        if len(origToksList[sentIdx]) > 0:
            if sentIdx > 0:
                newIdx = sentIdx - 1 - numReplacements
                firstTok = origToksList[sentIdx][0]
                segments = firstTok.split('.')  # for cases like .co.uk so that on the next tokenize, it won't make the same mistake on the second period
                if segments[0] in webExtSet and len(newToksList[newIdx]) > 1 and newToksList[newIdx][-1] == '.' and containsOnlyLowerLetters(segments[0]):
                    newToksList[newIdx].pop()
                    newToksList[newIdx][-1] = newToksList[newIdx][-1] + '-DOT-' + '-DOT-'.join(segments)
                    if len(origToksList[sentIdx]) > 1:  # push rest of tokens into previous sentence
                        newToksList[newIdx] += origToksList[sentIdx][1:]
                    numReplacements += 1
                # Check incorrectly split sentences due to exclamation marks in company names
                elif checkBangs and len(newToksList[newIdx]) > 1 and newToksList[newIdx][-1] == '!':
                    prevToks = []
                    nextToks = []
                    # Check cap words at end of previous sentence before !
                    for i in xrange(len(newToksList[newIdx]) - 1, -1, -1):
                        tok = newToksList[newIdx][i]
                        tokIsCapped, _ = validCompName(tok)  # don't consider if number, since its rare for company name to have both numbers and !
                        if tokIsCapped or tok == '!':
                            prevToks.append(tok)
                        else:
                            break
                    if len(prevToks) > 1:
                        prevToks.reverse()
                        prevToks.pop()  # remove ! and then append -BANG- to previous token
                        prevToks[-1] += '-BANG-'
                        # Check cap words at beginning of sentence after !
                        for i in xrange(len(origToksList[sentIdx])):
                            tok = origToksList[sentIdx][i]
                            tokIsCapped, _ = validCompName(tok)  # again, don't consider if number
                            if tokIsCapped:
                                nextToks.append(tok)
                            else:
                                break
                        # First check longest capitalized phrase possible (e.g. for E! Entertainment Television)
                        foundMatch = False
                        if len(nextToks) > 0:
                            comp = '_'.join(prevToks + nextToks)
                            if comp in compDict:
                                foundMatch = True
                                newToksList[newIdx].pop()  # remove !
                                newToksList[newIdx][-1] += '-BANG-'
                                newToksList[newIdx] += origToksList[sentIdx]
                                numReplacements += 1
                        # Next, if longest phrase didn't match, just check previous sentence tokens (e.g. for Yahoo!)
                        if not foundMatch:
                            comp = '_'.join(prevToks)
                            if comp in compDict:
                                foundMatch = True
                                newToksList[newIdx].pop()  # remove !
                                newToksList[newIdx][-1] += '-BANG-'
                                # Rejoin sentence only if next sentence doesn't contain capital
                                if len(nextToks) == 0:
                                    newToksList[newIdx] += origToksList[sentIdx]
                                    numReplacements += 1
                                else:
                                    newToksList[newIdx].append('.')  # add period otherwise to symbolize end of sentence
                                    newToksList.append(origToksList[sentIdx])
                        if not foundMatch:
                            newToksList.append(origToksList[sentIdx])
                    else:
                        newToksList.append(origToksList[sentIdx])   
                else:
                    newToksList.append(origToksList[sentIdx])
            else:
                newToksList.append(origToksList[0])
        # Empty sentence, ignore
        else:
            # numEmpty += 1 # if empty sentence, we don't append an item to newToksList, so must keep track of additional count
            numReplacements += 1
    return newToksList

def createDictList(origToksList):
    # Works at the sentence level (tokenized)
    # Creates a dictionary where {word:[ascending indices of appearances of the word]}
    origDictList = []
    for sentIdx in xrange(len(origToksList)):
        origToks = origToksList[sentIdx]
        origDictList.append({})
        for idx in range(len(origToks)):
            if origToks[idx] not in origDictList[-1]:
                origDictList[-1][origToks[idx]] = []
            origDictList[-1][origToks[idx]].append(idx)
    return origDictList

def batchRemoveNewlines(newsItem):
    # This function can be pooled
    title = removeNewlines(newsItem['title'])
    article = removeNewlines(newsItem['content'])
    return (title, article)

def batchPreprocessArticles(inputs):
    # This function can be pooled
    # inputs is a tuple of a tokens tuple and parameter tuple: ((titleToksList, articleToksList),(compDict, wordLImit, sentLimit))
    titleToksList, articleToksList, sentLimit = inputs[0]
    compDict, wordLimit = inputs[1]
    preResults = preprocessArticle(titleToksList, articleToksList, compDict=compDict, wordLimit=wordLimit, sentLimit=sentLimit)  # 80 word sentences requires ~2.1 GB RAM if encountered

    return preResults

def batchPreprocessArticles_old(inputs):
    # Didn't work because jpype can't attach the jvm to multiple python threads, I think
    newsItem, params = inputs
    compDict, wordLimit = params
    
    import jpype
    
    jpype.attachThreadToJVM()
    package = jpype.JPackage('edu.stanford.nlp')
    javaIOPackage = jpype.JPackage('java.io')
    
    # Remove newlines, depending on context
    title = removeNewlines(newsItem['title'])
    article = removeNewlines(newsItem['content'])
    
    # Tokenize title
    stringReader = javaIOPackage.StringReader(title)  # processor needs a Reader stream
    docProcessor = package.process.DocumentPreprocessor(stringReader)
    sentIterator = docProcessor.iterator()
    titleToksList = []
    while sentIterator.hasNext():
        sentToks = sentIterator.next().toArray()
        words = [item.word() for item in sentToks]
        if len(words) > 0:
            titleToksList.append(words)
        else:
            titleToksList.append(['-blank-line-', '.'])
            
    # Tokenize article
    stringReader = javaIOPackage.StringReader(article)  # processor needs a Reader stream
    docProcessor = package.process.DocumentPreprocessor(stringReader)
    sentIterator = docProcessor.iterator()
    articleToksList = []
    while sentIterator.hasNext():
        sentToks = sentIterator.next().toArray()
        words = [item.word() for item in sentToks]
        if len(words) > 0:
            articleToksList.append(words)
        else:
            articleToksList.append(['-blank-line-', '.'])
            
    preResults = preprocessArticle(titleToksList, articleToksList, compDict=compDict, wordLimit=wordLimit)  # 80 word sentences requires ~2.1 GB RAM if encountered

    return preResults

def preprocessArticle(titleToksList, articleToksList, compDict, wordLimit=defaultWordLimit, sentLimit=defaultSentLimit, returnRecords=True):
    # First preprocessing step, works on both articles and titles at the same time (for recasing before second step of preprocessing)
    # Rejoins incorrectly split sentences
    # Recases all cap sentences and titles
    # Assumes newlines already removed
    
    # 1. Reform sentences that have been incorrectly tokenized due to 2-letter domain extensions (e.g. .fm, .co.uk, ...) or exclamation marks
    articleToksList = fixSentenceSplits(articleToksList, compDict=compDict)
    titleToksList = fixSentenceSplits(titleToksList, compDict=compDict)
    
    # 2. Perform recasing on all-capitalized sentences
    titleToksList, articleToksList, titleAllCapsFlagList, articleAllCapsFlagList = recaseNewsTokens(titleToksList, articleToksList)
    
    # Perform next steps of preprocessing (additional sentence splitting, company name replacement, removing tokens, etc.) on title and article separately
    reconArticleToksList, articleAllCapsFlagList, articleRecords = preprocessToksStepTwo(articleToksList, articleAllCapsFlagList, compDict=compDict, wordLimit=wordLimit, sentLimit=sentLimit, returnRecords=True)
    reconTitleToksList, titleAllCapsFlagList, titleRecords = preprocessToksStepTwo(titleToksList, titleAllCapsFlagList, compDict=compDict, wordLimit=wordLimit, sentLimit=sentLimit, returnRecords=True)
    
    return {'title':{'toksList':reconTitleToksList, 'allCapsFlagList':titleAllCapsFlagList, 'records':titleRecords, 'recon':' '.join([' '.join(toks) for toks in reconTitleToksList])}, \
            'article':{'toksList':reconArticleToksList, 'allCapsFlagList':articleAllCapsFlagList, 'records':articleRecords, 'recon':' '.join([' '.join(toks) for toks in reconArticleToksList])}}
    
def preprocessToksStepTwo(origToksList, allCapsFlagList, compDict, wordLimit=defaultWordLimit, sentLimit=defaultSentLimit, returnRecords=True):
    reconToksList = []
    
    if returnRecords:
        records = {}
        records['suggestions'] = {}
        records['replacements'] = {}
    
    # Create dictionary of words:idx, has redundant computation for now...can edit createValidCaps to return dictionary, but would need to modify capitalization of keys
    origDictList = createDictList(origToksList)
    
    # First iterate over all sentences, and split sentences when they lead with parentheticals or dates not followed by capitalized word
    newToksList = []
    newAllCapsFlagList = []
    for sentIdx in xrange(len(origToksList)):
        origToks = origToksList[sentIdx]
        origDict = origDictList[sentIdx]
        allCapsFlag = allCapsFlagList[sentIdx]
        
        startIdxParens = removeLeadingParenthetical(origToks, origDict)
        startIdxDate = removeLeadingDates(origToks)
        startIdxPathology = removeLeadingPathologicalPhrases(origToks)
        
        # 3. Check for parenthetical phrases at beginning of sentence, and split into another one
        if 0 < startIdxParens < len(origToks) - 1:  
            newToksList.append(origToks[:startIdxParens])
            if newToksList[-1][-2] not in sentEndSet:
                newToksList[-1].append('.')  # add period so that next tokenization makes sure to make this parenthetical a separate sentence
            newToksList.append(origToks[startIdxParens:])
            newAllCapsFlagList.append(allCapsFlag)
            newAllCapsFlagList.append(allCapsFlag)
        # 4. Check for leading dates and split into another sentence
        elif 0 < startIdxDate < len(origToks) - 1:
            tokIsCapped, tokIsNum = validCompName(origToks[startIdxDate])
            if tokIsCapped and tokIsNum:
                newToksList.append(origToks[:startIdxDate])
                newToksList[-1].append('.')  # Make sure date becomes its own sentence
                newToksList.append(origToks[startIdxDate:])
                newAllCapsFlagList.append(allCapsFlag)
                newAllCapsFlagList.append(allCapsFlag)
            else:
                newToksList.append(origToks)
                newAllCapsFlagList.append(allCapsFlag)
        # 5. Check for leading pathological phrases like PRESS RELEASE
        elif 0 < startIdxPathology < len(origToks) - 1:
            newToksList.append(origToks[:startIdxPathology])
            newToksList[-1].append('.')  # Make sure date becomes its own sentence
            newToksList.append(origToks[startIdxPathology:])
            newAllCapsFlagList.append(allCapsFlag)
            newAllCapsFlagList.append(allCapsFlag)
        else:
            newToksList.append(origToks)
            newAllCapsFlagList.append(allCapsFlag)
    
    # if considering very few sentences, make sure they are not trivially short sentences like "Press Release"
    shortSents = 0
    if sentLimit < 10: 
        for i in xrange(len(newToksList)):
            if len(newToksList[i]) <= 6:
                shortSents += 1
            if i >= shortSents+sentLimit:
                break
    
    origToksList = newToksList[:sentLimit+shortSents]  # use new sentences from now on, and cut off long articles
    allCapsFlagList = newAllCapsFlagList
    
    # Iterate over all sentences again, this time replace company names with underscore versions
    # Assumes that all sentences have valid beginnings (since last part split out the pathologies)
    for sentIdx in xrange(len(origToksList)):
        origToks = origToksList[sentIdx]
        
        # 6. Replace multiword company names with common phrases with single token variants
        excludeIdx = set([])  # not used for now...was set(range(startValidIdx))
        augmentedExcludeIdx = set([])  # create copy of excluded indices
        chainIndices = []  # stores sublists of runs of potential company names
        
        # Generate new set of reconstructed tokens
        if  len(origToks) >= 2:  # assumes sentences are not all capitalized and only runs if remaining length is at least 2 words
            inChain = False
            chainIdx = []
            lastCapIdx = 0
            firstLowerIdx = wordLimit  # set initial value to unachievable index
            reconToks = []
            for i in xrange(len(origToks)):
                tok = origToks[i]
                # Augment exclusion indices
                if i < len(origToks) - 1:
                    # Exclude things like "CEO of..." or "in March..."
                    if tok in excludeCompNameDict and origToks[i + 1] in excludeCompNameDict[tok]:
                        augmentedExcludeIdx |= set([i, i + 1])
                    # Now exclude dates (because we are including numbers to form potential company names), right before we 
                    offset = removeLeadingDatesRelaxed(origToks[i + 1:])
                    if offset > 0:
                        augmentedExcludeIdx |= set(range(i + 1, i + 1 + offset))
                    if origToks[i + 1].lower() in incSet:
                        augmentedExcludeIdx.add(i + 1)
                else:
                    offset = 0
                
                if i not in augmentedExcludeIdx:
                    (tokIsCapped, tokIsNumber) = validCompName(tok)
                    # Begin chain or continue chain if cap words / numbers are encountered (exclude years)
                    if tokIsCapped or (tok.isdigit() and len(tok) == 4 and (int(tok) < 1500 or int(tok) > 2050)):  # year cutoffs
                        inChain = True
                        chainIdx.append(i) 
                        lastCapIdx = i  # track last word that was capitalized / number, check later to only end on cap/numbers
                    elif inChain:
                        # Continue chain on special lower case terms (cannot begin on lower case)
                        if tok in compLowerCaseKW:
                            chainIdx.append(i)
                            if firstLowerIdx == wordLimit:  # track the location of the first lower case word
                                firstLowerIdx = i
                        # NOT including inc. anymore
                        # Continue chain if find comma followed by 'inc.' and similar words
                        # elif tok == ',' and i+1 < len(origToks) and origToks[i+1].lower() in incSet:
                        #    chainIdx.append(i)
                        #    if firstLowerIdx == wordLimit:
                        #        firstLowerIdx = i
                        #    incIdx.add(i)
                        # Continue chain if 'inc.' or similar, and count as capital word (so that it can end on it)
                        # elif tok.lower() in incSet:
                        #    chainIdx.append(i)
                        #    lastCapIdx = i
                        #    incIdx.add(i)
                        # End the chain if no valid terms are found
                        else:
                            # If lowercase word was in chain, make sure to end on the last capital word 
                            while chainIdx[-1] != lastCapIdx:
                                chainIdx.pop()
                            chainIndices.append(chainIdx)
                            inChain = False  # reset chain variables
                            chainIdx = []
                            firstLowerIdx = wordLimit
                        
                    # Also end the chain if it is the last word in the sentence
                    if inChain and i == len(origToks) - 1:
                        while chainIdx[-1] != lastCapIdx:  # make sure to end on capital word
                            chainIdx.pop()
                        chainIndices.append(chainIdx)
                        inChain = False  # reset chain variables
                        chainIdx = []
                        firstLowerIdx = wordLimit        
                elif inChain:
                    # If we encounter an excluded index in the middle of the chain, end the chain
                    while chainIdx[-1] != lastCapIdx:  # make sure to end on capital word
                        chainIdx.pop()
                    chainIndices.append(chainIdx)
                    inChain = False
                    chainIdx = []
                    firstLowerIdx = wordLimit
                        
            # Once all chains in the sentence are found, post-process them
            # Join chain tokens and compare to company gazette
            # Deal with capitalization due to first word of sentence or numbers leading cap phrases (due to diffbot mistakes)
            validChainIdx = []  # stores bools for determining whether to delete or keep chains for single token replacement
            replaceToks = []
            multiWord = []  # tracks whether original chains has multiple words or not
            newChainIndices = []
            for i in xrange(len(chainIndices)):
                chainIdx = chainIndices[i]
                newChainIndices.append(chainIdx)
                if len(chainIdx) > 1:
                    multiWord.append(True)
                else:
                    multiWord.append(False)
                comp = replacePunctuation('_'.join(origToks[idx] for idx in chainIdx))
                if comp in compDict:
                    validChainIdx.append(True)
                # remove , Inc. and check again
                # elif len(chainIdx)>2 and origToks[chainIdx[-1]].lower() in incSet and origToks[chainIdx[-2]]==',' and '_'.join([origToks[idx] for idx in chainIdx[:-2]]) in compDict:
                #    validChainIdx.append(True)
                # remove Inc. and check again
                # elif len(chainIdx)>1 and origToks[chainIdx[-1]].lower() in incSet and '_'.join([origToks[idx] for idx in chainIdx[:-1]]) in compDict:
                #    validChainIdx.append(True)
                else:
                    validChainIdx.append(False)
                replaceToks.append(comp)  # can contain invalid companies as well
            
                # If chain isn't in gazette, try some relaxations if starting with a number or if it contains first valid word of sentence
                if not validChainIdx[-1]:
                    nextValidIdx = 0  # second valid index into chainIdx such that origToks[chainIdx[nextValidIdx]] is capped 
                    # if chain starts with a number and isn't in gazette, try removing all leading numbers
                    numOrFirstFlag = False
                    if isNumber(origToks[chainIdx[0]]):
                        numOrFirstFlag = True
                        for j in xrange(1, len(chainIdx)):
                            tokIsCapped, tokIsNumber = validCompName(origToks[chainIdx[j]])
                            if tokIsCapped and len(chainIdx) - j > 1:  # only consider if more than 1 tokens remain
                                comp = replacePunctuation('_'.join(origToks[idx] for idx in chainIdx[j:]))
                                nextValidIdx = j
                                if comp in compDict:
                                    validChainIdx[-1] = True
                                    newChainIndices[i] = chainIdx[j:]  # update master chainIndices list to new valid indices
                                # UPDATE: not joining , Inc. with underscores, since it causes a lot of problems -> sentence splitting, commas causes tokenization split
                                # remove , Inc. and check again
                                # elif len(chainIdx)-j>2 and origToks[chainIdx[-1]].lower() in incSet and origToks[chainIdx[-2]]==',' and '_'.join([origToks[idx] for idx in chainIdx[j:-2]]) in compDict:
                                #    validChainIdx[-1] = True
                                #    newChainIndices[i] = chainIdx[j:]
                                # remove Inc. and check again
                                # elif len(chainIdx)-j>1 and origToks[chainIdx[-1]].lower() in incSet and '_'.join([origToks[idx] for idx in chainIdx[j:-1]]) in compDict:
                                #    validChainIdx[-1] = True
                                #    newChainIndices[i] = chainIdx[j:]
                                break
                        replaceToks[-1] = comp
                    # if chain involves first word and wasn't found in gazette, try starting from next capitalized word
                    elif chainIdx[0] == 0:
                        numOrFirstFlag = True
                        for j in xrange(1, len(chainIdx)):
                            tokIsCapped, tokIsNumber = validCompName(origToks[chainIdx[j]])
                            if (tokIsCapped or tokIsNumber) and len(chainIdx) - j > 1:  # only consider if more than one tokens remain
                                comp = replacePunctuation('_'.join(origToks[idx] for idx in chainIdx[j:]))
                                nextValidIdx = j
                                if comp in compDict:
                                    validChainIdx[-1] = True
                                    newChainIndices[i] = chainIdx[j:]  # update master chainIndices list to new valid indices
                                # remove , Inc. and check again
                                # elif len(chainIdx)-j>2 and origToks[chainIdx[-1]].lower() in incSet and origToks[chainIdx[-2]]==',' and '_'.join([origToks[idx] for idx in chainIdx[j:-2]]) in compDict:
                                #    validChainIdx[-1] = True
                                #    newChainIndices[i] = chainIdx[j:]
                                # remove Inc. and check again
                                # elif len(chainIdx)-j>1 and origToks[chainIdx[-1]].lower() in incSet and '_'.join([origToks[idx] for idx in chainIdx[j:-1]]) in compDict:
                                #    validChainIdx[-1] = True
                                #    newChainIndices[i] = chainIdx[j:]
                                break
                        replaceToks[-1] = comp
                    
                    # if chain has a 's, and it wasn't found in gazetteer, then check only up to the first 's
                    if not validChainIdx[-1] and len(chainIdx) > 3:  # make sure at least 2 tokens prior to 's (and must implicitly have 1 after)
                        if '\'s' in set([origToks[k] for k in chainIdx[2:]]):
                            for j in xrange(2, len(chainIdx)):
                                if origToks[chainIdx[j]] == '\'s':
                                    break
                            comp = replacePunctuation('_'.join(origToks[idx] for idx in chainIdx[:j]))
                            if comp in compDict:
                                validChainIdx[-1] = True
                                newChainIndices[i] = chainIdx[:j]
                                replaceToks[-1] = comp
                    # if chain started with a number or includes first word of sentence, and has 's, check for phrase between 2nd cap and first 's
                    if not validChainIdx[-1] and len(chainIdx[nextValidIdx:]) > 3 and numOrFirstFlag:  # make sure at least 2 tokens prior to 's (and must implicitly have 1 after)
                        if '\'s' in set([origToks[k] for k in chainIdx[nextValidIdx + 2:]]):
                            for j in xrange(nextValidIdx + 2, len(chainIdx)):
                                if origToks[chainIdx[j]] == '\'s':
                                    break
                            comp = replacePunctuation('_'.join(origToks[idx] for idx in chainIdx[nextValidIdx:j]))
                            # print 'poss ->',comp
                            if comp in compDict:
                                validChainIdx[-1] = True
                                newChainIndices[i] = chainIdx[nextValidIdx:j]
                                replaceToks[-1] = comp 
                        
                # If want to keep track of company name replacement, store results and count to recResults
                if returnRecords and multiWord[-1]:
                    if validChainIdx[-1]:
                        if replaceToks[-1] not in records['replacements']:
                            records['replacements'][replaceToks[-1]] = 1
                        else:
                            records['replacements'][replaceToks[-1]] += 1
                    else:
                        if replaceToks[-1] not in records['suggestions']:
                            records['suggestions'][replaceToks[-1]] = 1
                        else:
                            records['suggestions'][replaceToks[-1]] += 1
            
            # Reconstruct sentence tokens with valid replacements if company is found in dictionary
            reconToks = []
            j = 0  # index into chainIdx
            i = 0  # index into tokens
            while i < len(origToks):
                if i not in excludeIdx:
                    # If we reach the start of a valid chain, append replacement word, then increment j and skip ahead with i
                    if j < len(chainIndices):
                        if validChainIdx[j] and chainIndices[j][0] == i:
                            reconToks.append(replaceToks[j])
                            i = chainIndices[j][-1]
                            j += 1
                        # If we reach the start of an invalid chain, append original word, then increment j only
                        elif not validChainIdx[j] and chainIndices[j][0] == i:
                            reconToks.append(origToks[i])
                            j += 1
                        else:
                            reconToks.append(origToks[i])
                    else:
                        reconToks.append(origToks[i])
                i += 1
            
            # Append sentence to master reconstructed token list            
            reconToksList.append(reconToks)     
            
        else:  # if title, just append back to article
            reconToksList.append(origToks)
        
        # Limit number of tokens
        if len(reconToksList[-1]) >= wordLimit:
            reconToksList[-1] = reconToksList[-1][:wordLimit] + ['.']
        
        # 7. Final cleanup of punctuation and the end of the sentence
        # First crush all multi-punctuation tokens into one character (e.g. !!! -> !, ?? -> ?, !? -> !, ?! -> ?)
        for i in xrange(len(reconToksList[-1])):
            if len(reconToksList[-1][i]) > 1 and isAllPunctuation(reconToksList[-1][i]):
                reconToksList[-1][i] = reconToksList[-1][i][0]  # replace with first punctuation character
        
        # Remove long runs of punctuation (can occur if there is an untokenizable word, leaving only punctuation)
        while len(reconToksList[-1]) > 1:
            if reconToksList[-1][-1] in sentEndSet and reconToksList[-1][-2] in sentEndSet:
                reconToksList[-1].pop()
            else:
                break
        
        # Remove redundant ending punctuation e.g. ... ?). or ...?"). or ?".
        if len(reconToksList[-1]) > 1 and reconToksList[-1][-1] in sentEndSet:
            # First get last valid index that is not a closing quote or bracket
            for i in xrange(len(reconToksList[-1]) - 2, -1, -1):
                if reconToksList[-1][i] not in sentEndContinueSet:
                    break
            if reconToksList[-1][i] in sentEndSet and i < len(reconToksList[-1]) - 2:  # found another punctuation mark
                # case 1: .). -> remove punctuation inside parenthesis
                if reconToksList[-1][i + 1] in snlpCloseBracketSet:
                    reconToksList[-1] = [reconToksList[-1][j] for j in xrange(len(reconToksList[-1])) if j != i]
                # case 2: .". -> remove punctuation outside quotes
                if reconToksList[-1][i + 1] in snlpCloseQuotesSet:
                    reconToksList[-1].pop()  # remove outer punctuation
        
        # Remove singleton punctuation or empty lists
        if (len(reconToksList[-1]) == 1 and reconToksList[-1][0] in sentEndSet) or len(reconToksList[-1]) == 0:
            reconToksList.pop()
    
    # print origToksList        
    if returnRecords:
        return reconToksList, allCapsFlagList, records
    else:
        return reconToksList, allCapsFlagList   

def replacePunctuation(token):
    newTok = token.replace('.', '-DOT-')
    newTok = newTok.replace('!', '-BANG-')
    newTok = newTok.replace('?', '-QRY-')
    return newTok

def isAllPunctuation(token):
    for i in xrange(len(token)):
        if token[i] not in interrobangSet:
            return False
    return True

def chainWords(triTuple, origWord, currWord, contRelDict, contRelAugDict, stopRelDict, stopRelAugDict, disregardKW, pronounKWDict={}, depth=0):
    # old
    # Only use pronounKWDict when chaining across pronouns
    depth += 1
    nextWords = []
    returns = []
    # print 'currword=',currWord
    for rel, gov, dep in triTuple:
        if gov.i == currWord.i and rel in stopRelDict and dep.t not in disregardKW and not dep.t.lower() in pronounKWDict:  # Found a desired relation
            return dep            
        if dep.i == currWord.i and rel in contRelDict:  # Continue the chaining
            nextWords.append(gov)
            # verbModDict[gov] += 1 # for statistics
    
    if len(nextWords) > 0 and depth < maxDepth:
        for nextWord in nextWords:
            if currWord.i == origWord.i:
                returns.append(chainWords(triTuple, origWord, nextWord, contRelAugDict, contRelAugDict, stopRelAugDict, stopRelAugDict, disregardKW, pronounKWDict, depth))
            else:
                returns.append(chainWords(triTuple, origWord, nextWord, contRelDict, contRelAugDict, stopRelDict, stopRelAugDict, disregardKW, pronounKWDict, depth))
        for item in returns:
            if item != None:
                return item
    else:
        return None

def getDateToks(toks):
    returnToks = []
    state = 0
    startIdx = 1000
    for i in xrange(len(toks)):
        tok = toks[i]
        if state == 0:  # check for month
            if tok in monthSet:
                state = 1
                returnToks.append(tok)
                startIdx = i
        elif state == 1:  # check for comma or number
            if len(tok) <= 2 and isNumber(tok):
                returnToks.append(tok)
                state = 2
            elif tok == ',' or isNumberRelaxed(tok):
                try:  # check for number before month for cases like 19 Oct 2012
                    if isNumberRelaxed(toks[i - 2]):
                        temp = returnToks[-1]
                        returnToks.pop()
                        returnToks.append(toks[i - 2])
                        returnToks.append(temp)
                        startIdx -= 1
                except IndexError:
                    pass
                if tok == ',':
                    returnToks.append(tok)
                    state = 3
                else:  # case where year comes after month
                    # returnToks.append(',')
                    returnToks.append(tok)
                    return returnToks, startIdx
            else:
                return returnToks, startIdx
        elif state == 2:  # check for comma
            if tok == ',':
                returnToks.append(tok)
                state = 3
            else:
                return returnToks, startIdx
        elif state == 3:  # check for year
            if isNumber(tok):
                returnToks.append(tok)
            return returnToks, startIdx
    return returnToks, startIdx

def getMoney(tokens):
    moneyList = []
    length = len(tokens)
    for i in range(len(tokens)):
        word = tokens[i].lower()
        if i + 1 < length and word in amountSym:  # Case of $
            moneyList.append(tokens[i] + ' ' + tokens[i + 1])
            i += 2
            if i < length and (tokens[i].lower() in numKW or tokens[i].lower() in amountKW):  # Case of $ 3 billion or $ 3B dollars
                moneyList[-1] += ' ' + tokens[i]
                i += 1
                if i < length and (tokens[i].lower() in numKW or tokens[i].lower() in amountKW):  # Case of $ 3 billion dollars (I know, this is grammatically wrong)
                    moneyList[-1] += ' ' + tokens[i]
                    i += 1
        elif i > 1 and word in amountKW:
            moneyList.append(tokens[i - 1] + ' ' + tokens[i])  # Case of 3B hkd
            if i > 2 and tokens[i - 1].lower() in numKW:
                moneyList[-1] = tokens[i - 2] + ' ' + moneyList[-1]  # Case of 3 billion hkd
    return moneyList

def getNgrams(tokens, n):
    # Returns a list of n grams from tokens
    ngrams = []   
    if n > 0:
        for i in range(len(tokens) - n + 1):
            item = tokens[i]
            for j in range(1, n):
                item += ' ' + tokens[i + j]
            ngrams.append(item)
    return ngrams

def getAllNgrams(tokens, maxN=1000):
    # Returns a list of all ngrams up to length maxN
    NgramList = []
    for i in range(1, min([len(tokens), maxN]) + 1):
        NgramList += getNgrams(tokens, i)
    return NgramList
    
def cleanNames(companyList, companyDict):
    # Currently this doesn't handle the case where the company name has an & or 'and' joining them
    # Later, maybe we can preprocess all articles such that '&' becomes '__' and then postprocess accordingly
    filteredCompanyList = []
    for company in companyList:  
        found = 0     
        iterVec = range(min([4, len(company.split())]), 0, -1)  # only consider up to quadgrams    
        for i in iterVec:  # take largest ngrams first
            if found == 0:
                for item in getNgrams(company.split(), i):
                    if item in companyDict:
                        filteredCompanyList.append(item)
                        company.replace(item, '')  # remove company that's been found 
                        found = 1  # only allow one company per list item
        if found == 0:
            filteredCompanyList.append(None)
    return filteredCompanyList
    
def getMask(idxList):
    mask = []
    for idx in idxList:
        if idx != None:
            mask.append(1)
        else:
            mask.append(0)
    return mask

def removeParens(toks):
    # Assumes PTB tokenizer was used, which converts parentheses into -LRB- and -RRB-
    # Only removes innermost brackets
    # Old, deprecated
    newToks = []
    tempToks = []
    insideParens = False
    # for word, i in zip(toks, range(len(toks))):
    for word in toks:
        if not insideParens:
            if word == '-LRB-':
                insideParens = True
                tempToks.append(word)
            else:
                newToks.append(word)
        else:
            if word == '-RRB-':
                insideParens = False
                tempToks = []
            elif word == '-LRB-':  # encounter left parens again, negate last parens
                newToks += tempToks
                tempToks = ['-LRB-']
            else:
                tempToks.append(word)                
    return newToks

def isInteger(token):
    # Note: Only works for nonnegative
    return token.isdigit()
    #return re.search('[0-9]', token)

def isNumber(token):
    # allow at most 1 decimal point, but any number of commas (but not both at the same time)
    if token[0] == '-':
        try:
            return (token[1:].replace('.', '', 1).isdigit() or token[1:].replace(',', '').isdigit())
        except IndexError:
            return False
    else:
        return (token.replace('.', '', 1).isdigit() or token.replace(',', '').isdigit())
        
def isNumberPostfix(token):
    # Checks whether token is of the form 42nd, 1st, etc...
    if len(word) > 2 and word[-2:-1] in numPostfixSet:
        return isNumber(word[:-2])
    else:
        return False

def isNumberRelaxed(token):
    # Will return True for things like 24th or 3rd, etc...
    if isNumber(token):
        return True
    else:
        return isNumberPostfix(token)   

def containsCap(word, allowNumPostfix=True, countBracketAsCap=False):
    # old
    # Returns true for words containing a capital letter or numbers with postfixes
    if word not in bracketSym:
        if re.search('[A-Z]', word):
            return True
        elif allowNumPostfix and len(word) > 2 and word[-2:-1] in numPostfixSet:  # consider numbers to be valid (e.g. 42nd)
            return isNumber(word[:-2])
        else:
            return False
    else:
        return countBracketAsCap

def validCompName(word):
    # Returns tuple (<contains capital>, <isNumberRelaxed>), relaxed numbers are pure numbers or with postfixes e.g. 34th
    if word not in bracketSym:
        if re.search('[A-Z]', word):
            return True, False
        else:
            return False, isNumberRelaxed(word)
    return False, False

def containsLetterOrNum(word):
    return re.search('[A-Z,a-z,0-9]', word)

def containsOnlyCapLetters(word):
    for i in xrange(len(word)):
        if not word[i].isupper():
            return False
    return True  

def containsOnlyLowerLetters(word):
    for i in xrange(len(word)):
        if not word[i].islower():
            return False
    return True

def getCapitalizedWords(toks, idxOffset=0):
    # Input is a list of tokens
    # Returns indices of capitalized words, plus offset
    # Considers tokens with underscores automatic companies and ends the chain (preprocessing join known multi-word company names with underscores)
    capWords = []  # capital word sequences
    capIndices = []  # list of tuples containing the start and end of the capital words
    startIdx = None
    inChain = False
    for i in xrange(len(toks)):
        tok = toks[i]
        tokIsCapped, tokIsNum = validCompName(tok)
        segs = tok.split('_')
        
        if not inChain:
            if tokIsCapped:
                # If encounter a definite company name (with underscores), then only add this token as a standalone company
                if len(segs) > 1:
                    capWords.append(tok)
                    capIndices.append((i, i + 1))
                # Start a new chain
                else:
                    inChain = True
                    startIdx = i
                    # If starting chain word is at the end of sentence, must end immediately
                    if i == len(toks) - 1:
                        inChain = False
                        capWords.append(tok)
                        capIndices.append(i, i + 1)
        else:
            # End chain if in chain and encountered a non-capped word
            if not tokIsCapped:
                inChain = False
                capWords.append(' '.join([toks[j] for j in xrange(startIdx, i)]))
            
            
    ####
    #### Check statistics on noun phrases to company name correlation (in order to simplify 
    #### Also go back and add parse tree saving
            

def getCapWords(toks, idxOffset=0):
    # Offset should be verbIdx+1 if taking sentences to the right
    capWords = []  # capital word sequences
    capIdx = []  # idx to first capital word
    numWords = []  # number of words in the cap words sequence
    currWord = None
    cont = False
    lcom = []
    rcom = []
    numWord = 0
    for word, i in zip(toks, range(len(toks))):
        isNum = isNumber(word)
        if containsCap(word) or word == '&' or isNum:
            if currWord == None and not isNum:  # number cannot be first word
                currWord = word
                numWord += 1
                capIdx.append(i)
                if i > 1 and toks[i - 1] == ',':  # first word of a cap sequence
                    lcom.append(i - 1)
                else:
                    lcom.append(None)
                cont = True
            elif cont:
                currWord += ' ' + word
                numWord += 1
                cont = True
            if i == (len(toks) - 1) and currWord != None:  # last word
                capWords.append(currWord)
                numWords.append(numWord)
                numWord = 0
                rcom.append(None)
        elif currWord != None:
            capWords.append(currWord)
            numWords.append(numWord)
            numWord = 0
            cont = False
            currWord = None
            if toks[i] == ',':  # last word of a cap sequence
                rcom.append(i)
            else:
                rcom.append(None)
    if idxOffset != None:
        for idx, i in zip(lcom, range(len(lcom))):
            if idx != None:
                lcom[i] = lcom[i]
        for idx, i in zip(rcom, range(len(rcom))):
            if idx != None:
                rcom[i] = rcom[i]
                
    return capWords, capIdx, numWords, lcom, rcom

def substituteCNames(sentToks, cNameDict, labelOffset=0):
    # Old
    # Only replace complete matches, except if it includes first word, or if a day / month name is included
    capWordsList, capIdxList, numWordsList = getCapWords(sentToks)[0:3]
   
    # Determine indices where words need to be replaced or removed
    replaceList = []
    replaceIdxList = []
    removeIdxList = []
    replaceDict = {}
    numEnt = labelOffset
    for capWord, capIdx, numWord in zip(capWordsList, capIdxList, numWordsList):
        if capWord in cNameDict:
            replacement = 'CompanyEnt' + '%d' % numEnt
            replaceList.append(replacement)
            replaceIdxList.append(capIdx)
            removeIdxList += range(capIdx + 1, capIdx + numWord)  # indices where the word will be removed
            replaceDict[replacement] = capWord  # to revert back to 
            numEnt += 1
        else:
            if capIdx == 0:  # first word may be capitalized, try checking company names using subsequent words only
                tempToks = capWord.split()[1:]
                if len(tempToks) > 0:
                    tempCapWord = ' '.join(tempToks)
                    if tempCapWord in cNameDict:
                        replacement = 'CompanyEnt' + '%d' % numEnt
                        replaceList.append(replacement)
                        replaceIdxList.append(capIdx + 1)
                        removeIdxList += range(capIdx + 2, capIdx + numWord)
                        replaceDict[replacement] = tempCapWord
                        numEnt += 1
                    else:  # check for additional date words which may be capitalized, company still not found
                        pass  # implement later, can be recursive
                        # newCapToks = []
                        # for tok in tempToks:
                            # if tok in dateStopWords:
                                             
    # Go through tokens and replace / remove where necessary
    for replacement, i in zip(replaceList, replaceIdxList):
        sentToks[i] = replacement    
    newToks = []
    for tok, i in zip(sentToks, range(len(sentToks))):
        if i not in removeIdxList:
            newToks.append(tok)
            
    return newToks, replaceDict
        
def cleanLabel(label):
    # Remove words that don't contain a capital letter, and remove stopwords like llc
    toks = label.split()
    reconToks = []
    for tok in toks:
        if containsCap(tok) and not tok.lower() in incSet:
            if tok[-1] == ',':
                reconToks.append(tok[:len(tok) - 1])
            else:
                reconToks.append(tok)
    return ' '.join(tok for tok in reconToks)
        
def preProcSentence(sent):
    # Remove any uncleaned newlines and return longest string segment
    segments = sent.split('\n')
    lens = [len(segment) for segment in segments]
    maxlen = max(lens)
    for i in xrange(len(lens)):
        if lens[i] == maxlen:
            return segments[i]         

def getLongestList(inputList):
    lens = [len(item) for item in inputList]
    maxlen = max(lens)
    for i in xrange(len(lens)):
        if lens[i] == maxlen:
            return inputList[i], i
        
def removeCertainWords(sentToks, removeBasedToks=True, separateBasedToks=False):
    # DEPRECATED: In current pipeline, please use preprocessToks(...)
    # Remove PRESS RELEASE or PRESS UPDATE
    if len(sentToks) > 2:
        if sentToks[0].lower() == 'press' and sentToks[1].lower() == 'release':
            sentToks = sentToks[2:]
        elif sentToks[0].lower() == 'update':
            sentToks = sentToks[1:]
    if len(sentToks) > defaultWordLimit:
        sentToks = sentToks[:defaultWordLimit]  # limit sentence length
    
    # Remove leading symbols
    while len(sentToks) > 1 and sentToks[0] in puncKW:
        sentToks = sentToks[1:]
    
    # Then remove leading 'Today,'
    if len(sentToks) > 2:
        if sentToks[0] in ['Today'] and sentToks[1] == ',':
            sentToks = sentToks[2:]
            
    # Remove 'today announced'
    removeIdx = []
    # tempTok = []
    sentLen = len(sentToks)
    for i in xrange(sentLen):
        if sentToks[i].lower() == 'today':
            if i < sentLen - 1:
                if sentToks[i + 1] == 'announced':
                    removeIdx.append(i)
                    removeIdx.append(i + 1)
        # Old code:
        # if i < sentLen-1 and not (sentToks[i].lower()=='today' and sentToks[i+1].lower=='announced'):
        #    tempTok.append(sentToks[i])
        # elif i == sentLen-1:
        #    tempTok.append(sentToks[i])
    # sentToks = tempTok
    
    # Remove -based words and replace 'mln', 'bln', 'tln' with million, billion and trillion
    tempToks = []
    for word, i in zip(sentToks, range(len(sentToks))):
        wordlen = len(word)
        if removeBasedToks:
            # completely remove -based word phrases, since it messes up dependency parser sometimes
            if wordlen > 6:
                if word[wordlen - 6:].lower() == '-based' and word[0].isupper():
                    removeIdx.append(i)
                    if i > 0 and (sentToks[i - 1] == ',' or sentToks[i - 1].isupper()):
                        removeIdx.append(i - 1)
                    # Now go backwards, checking for contiguous capitalized words and remove them
                    if removeIdx[-1] > 0:
                        for j in range(removeIdx[-1] - 1, -1, -1):
                            if sentToks[j][0].isupper():
                                removeIdx.append(j)
                            else:
                                break
        elif separateBasedToks:
            # split -based words at the hyphen
            if wordlen > 6:
                if word[wordlen - 6:] == '-based' and word[0].isupper():
                    try:
                        if word[wordlen - 7] == '.':
                            tempToks += [word[:wordlen - 7], 'based']
                        else:
                            tempToks += [word[:wordlen - 6], 'based']
                    except:
                        pass                
                elif i not in removeIdx:
                    tempToks.append(replaceNumAbbrevDict.get(word, word))
            elif i not in removeIdx:
                tempToks.append(replaceNumAbbrevDict.get(word, word))
        elif i not in removeIdx:
            tempToks.append(replaceNumAbbrevDict.get(word, word))
    
    if removeBasedToks:                                  
        return [replaceNumAbbrevDict.get(word, word) for word, idx in zip(sentToks, range(len(sentToks))) if idx not in removeIdx]
    else:
        return tempToks

def removeLeadingDatesLocs(sentToks, nerList):
    # old
        removeIdx = []
        if len(nerList) != len(sentToks):
            print 'Warning: NERList not same length as tokens.'
            print
        for word, i in zip(sentToks, range(len(sentToks))):
            if nerList[i] in nerRemoveKW or word in puncKW:
                removeIdx.append(i)
            elif len(removeIdx) > 0 and len(sentToks) > 2 and removeIdx[-1] == 0 and sentToks[1] == ',' and len(sentToks[2]) == 2 and sentToks[2][0].isupper() and sentToks[2][1].isupper():
                # in case the NER doesn't pick up the two letter state abbreviations
                removeIdx += [1, 2]
            else:
                break
        return [word for word, i in zip(sentToks, range(len(sentToks))) if i not in removeIdx]
    
def getMoneyIndices(ners, sentToks):
    # stopIdx is 1 higher than actual index, to account for Python slicing conventions
    startIdxList = []
    stopIdxList = []
    inChain = False
    lenNers = len(ners)
    for i in range(lenNers):
        ner = ners[i]
        if ner == 'MONEY':
            # Correct for NER tagger mistakes
            try:
                if sentToks[i + 1].lower() in numKW2:
                    ners[i + 1] = 'MONEY'
            except:
                pass
            if not inChain:
                startIdxList.append(i)
                inChain = True
            if i == lenNers - 1:
                stopIdxList.append(lenNers)
        else:
            if inChain:
                stopIdxList.append(i)
                inChain = False
    return zip(startIdxList, stopIdxList)

def getDescPhraseIndices(pos, sentToks):
    # stopIdx is 1 higher than actual index, to account for Python slicing conventions
    startIdxList = []
    stopIdxList = []
    inChain = False
    lenPos = len(pos)
    lastNounIdx = None
    for i in range(lenPos):
        if pos[i] in nounPOS:
            lastNounIdx = i
        if not inChain:
            if pos[i] in descPhrasePOS:
                startIdxList.append(i)
                inChain = True
                if i == lenPos - 1:
                    # if startIdxList[-1] == lenPos-1 or lastNounIdx is None:
                    if lastNounIdx is None:
                        startIdxList.pop()  # don't keep if no nouns are in run
                    elif pos[i] not in nounPOS and lastNounIdx != None:  # don't end on non-Noun
                        stopIdxList.append(lastNounIdx + 1)
                    else:
                        stopIdxList.append(lenPos)                    
        else:
            if pos[i] not in descPhraseAugPOS:
                # if startIdxList[-1] == i-1 or lastNounIdx is None:
                if lastNounIdx is None:
                    startIdxList.pop()
                elif pos[i] not in nounPOS and lastNounIdx != None:
                    stopIdxList.append(lastNounIdx + 1)
                else:
                    stopIdxList.append(i)
                inChain = False
                lastNounIdx = None
    return zip(startIdxList, stopIdxList)            
            
def getNounPhrase(wordObjList, triTuple, replaceNameDict={}):
    # Checks for entity noun phrase
    companyDesc = []
    # for companyName, i in zip(wordObjList, range(len(wordObjList))):
    for companyName in wordObjList:
        addCo = []  # text only
        started = 0
        tempWord = WordObj()
        for rel, gov, dep in triTuple:
            if gov.i == companyName.i:
                if rel in nnRel:
                    addCo.append(dep.t)
                    started = 1
                    tempWord = dep  # covers the case of conjunction in description
            elif rel in ['conj_and', 'conj_or'] and gov.i == tempWord.i:
                if rel == 'conj_and':
                    conjunction = 'and '
                else:
                    conjunction = 'or '
                addCo.append(conjunction + dep.t)
                tempWord = dep
            elif started == 1:
                break  # end search after finding one contiguous phrase
        companyDesc.append(addCo)
    return companyDesc

def getPronounDict():
    return pronounKW

def getCompanyName(sentToks, replaceDict, seedIdx):
    if sentToks[seedIdx] in replaceDict:
        return replaceDict[sentToks[seedIdx]]  # return just this name if it was found in company DB
    else:
        name = sentToks[seedIdx]
        # check to the left
        if seedIdx > 0:
            for i in xrange(seedIdx - 1, -1, -1):
                if sentToks[i] not in pronounKW and containsCap(sentToks[i]):
                    if i == 0 and sentToks[i] in startCNameStopwords:
                        break
                    else:
                        lenTok = len(sentToks[i])
                        if lenTok > 6 and sentToks[i][lenTok - 6:] == '-based':
                            break
                        else:
                            name = replaceDict.get(sentToks[i], sentToks[i]) + ' ' + name
                else:
                    break 
        # check to the right
        # if seedIdx < len(sentToks):
        #    for i in xrange(seedIdx,len(sentToks)):
        #        if sentToks[i] not in pronounKW and containsCap(sentToks[i]):
        #            name = name + ' ' + replaceDict.get(sentToks[i],sentToks[i])
        #        else:
        #            break
        return name
    
def standardizeMoney(amountStr):
    tempStr = amountStr.split(',')
    if len(tempStr) == 2 and tempStr[1] == '000':
        amountStr = tempStr[0] + ' k'
    
    lenAmt = len(amountStr)
    if amountStr[-1].lower() in replaceNumAbbrevDict2:
        if amountStr[-2] == ' ':
            amountStr = amountStr[:lenAmt - 1] + replaceNumAbbrevDict2[amountStr[-1].lower()]
        else:
            amountStr = amountStr[:lenAmt - 1] + ' ' + replaceNumAbbrevDict2[amountStr[-1].lower()]
    if amountStr[0] == '$':        
        try:
            if amountStr[1] != ' ':
                amountStr = amountStr[0] + ' ' + amountStr[1:]
        except:
            pass
    return amountStr
    
def isEq(x, y):
    # Check for equality
    return x.t == y.t and x.i == y.i

class WordObj(object):
    # Essentially a struct for storing a word string and position
    def __init__(self, text='', idx=None):
        self.t = text
        self.i = idx

def formMentionString(toksList,coref):
    headMention = '<'+' '.join(toksList[coref[0][0]][coref[0][1]:coref[0][2]]) + '> in Sent. %i' % coref[0][0]
    mentions = ['<'+' '.join(toksList[ment[0]][ment[1]:ment[2]])+'> in Sent. %i' % ment[0] for ment in coref[1] if ment != coref[0]]
    return headMention + ' --- ' + ', '.join(mentions) 

def formMentionString_old(results,coref):
    # ((head sentNum, beginIdx, endIdx), [(mention0),(mention1),...])
    headMention = '<'+' '.join(results['sentences'][coref[0][0]]['tokens'][coref[0][1]:coref[0][2]]) + '> in Sent. %i' % coref[0][0]
    mentions = []
    
    for i in xrange(len(coref[1])):
        if not (coref[1][i][0] == coref[0][0] and coref[1][i][1] == coref[0][1] and coref[1][i][2] == coref[0][2]):
            mention = '<'+' '.join(results['sentences'][coref[1][i][0]]['tokens'][coref[1][i][1]:coref[1][i][2]]) + '> in Sent. %i' % coref[1][i][0]
            mentions.append(mention)
    return headMention + ' --- ' + ', '.join(mentions)

def printArticleResults(toksList,lemmasList,posTagsList,nerTagsList,depsList,parseTreeList,corefsList,recasedFlagList,errorFlag,label,printLemmas,printParseTree):
    print '+%s' % label, 'Sentence Results+'
    if len(recasedFlagList) != len(toksList):
        prefix = '[Mis]'
    else:
        prefix = ''
    for i, toks in enumerate(toksList):
        sent = ' '.join([tok + '/' + POSMaster[posTagsList[i][j]] for j, tok in enumerate(toks)])
        if i < len(recasedFlagList) and recasedFlagList[i]:
            print '%2i >>' % i, prefix, '[Recased]', sent
        else:
            print '%2i >>' % i, prefix, sent

    if printLemmas:
        print '+%s' % label, 'Lemma Results+'
        for i, lemmas in enumerate(lemmasList):
            print '%2i >>' % i, ' '.join(lemmas)
    
    print '+%s' % label, 'Dependencies+'
    for i, deps in enumerate(depsList):
        print '%2i >>' % i, ' '.join([dep[0] + '(' + toksList[i][dep[1]] + ', ' + toksList[i][dep[2]] + ')' for dep in deps])

    print '+%s' % label, 'NER Tags+'
    for i, ners in enumerate(nerTagsList):
        validNER = [str(j) + '/' + NERMaster[ner] for j, ner in enumerate(ners) if ner != 0]
        if len(validNER)>0:
            print '%2i >>' % i, ' '.join(validNER)
    
    if printParseTree:
        print '+%s' % label, 'Parse Trees+'
        for i, parseTree in enumerate(parseTreeList):
            print '%2i >>' % i 
            print parseTree
    
    print '+%s' % label, 'Coreferences+'
    for coref in corefsList:
        print formMentionString(toksList,coref)
        
    print '+%s' % label, 'Error Flag+'
    print errorFlag 
        
def printParseResults(results, printParseTree=False, printLemmas=False):
    titleToksList = results['titleToksList']
    titleLemmasList = results['titleLemmasList']
    titlePOSTagsList = results['titlePOSTagsList']
    titleNERTagsList = results['titleNERTagsList']
    titleDepsList = results['titleDepsList']
    titleParseTreeList = results['titleParseTreeList']
    titleCorefsList = results['titleCorefsList']
    titleErrorFlag = results['titleErrorFlag']
    titleRecasedFlagList = results['titleRecasedFlagList']
    
    articleToksList = results['articleToksList']
    articleLemmasList = results['articleLemmasList']
    articlePOSTagsList = results['articlePOSTagsList']
    articleNERTagsList = results['articleNERTagsList']
    articleDepsList = results['articleDepsList']
    articleParseTreeList = results['articleParseTreeList']
    articleCorefsList = results['articleCorefsList']
    articleErrorFlag = results['articleErrorFlag']
    articleRecasedFlagList = results['articleRecasedFlagList']
    parseErrors = results['parseErrors']
    
    printArticleResults(titleToksList,titleLemmasList,titlePOSTagsList,titleNERTagsList,titleDepsList,titleParseTreeList,
                        titleCorefsList,titleRecasedFlagList,titleErrorFlag,label='Title',printLemmas=printLemmas,printParseTree=printParseTree)
    printArticleResults(articleToksList,articleLemmasList,articlePOSTagsList,articleNERTagsList,articleDepsList,articleParseTreeList,
                        articleCorefsList,articleRecasedFlagList,articleErrorFlag,label='Article',printLemmas=printLemmas,printParseTree=printParseTree)
    
    print '+Parse Errors+ :', parseErrors

"""
def printParseResults_old(result, nTop = 10, printParseTree=False, printLemmas=False):
    titleResults = result['titleResults']
    print '+Title Sentence Results+'
    if len(titleResults['recasedFlagList'])!=len(titleResults['sentences']):
        # If extra sentence appeared after pipeling processing, will be unsure about the recase flags (generated during preprocesing)
        for idx in xrange(len(titleResults['sentences'])):
            item = titleResults['sentences'][idx]
            sent = ' '.join([item['tokens'][i] + '/' + POSMaster[item['posTags'][i]] for i in xrange(len(item['tokens']))])
            if idx < len(titleResults['recasedFlagList']):
                if titleResults['recasedFlagList'][idx]:
                    print '%2i >>' % idx,'[?Recased?]', sent
                else:
                    print '%2i >>' % idx,'[??]', sent
            else:
                print '%2i >>' % idx,'[?Missing?]', sent
    else:
        for idx in xrange(len(titleResults['sentences'])):
            item = titleResults['sentences'][idx]
            sent = ' '.join([item['tokens'][i] + '/' + POSMaster[item['posTags'][i]] for i in xrange(len(item['tokens']))])
            if titleResults['recasedFlagList'][idx]:
                print '%2i >>' % idx,'[Recased]', sent
            else:
                print '%2i >>' % idx,sent
    
    if printLemmas:
        print '+Title Lemmas+'
        for idx in xrange(len(titleResults['sentences'])):
            item = titleResults['sentences'][idx]
            print '%2i >>' % idx, ' '.join(item['lemmas'])
    
    print '+Title Dependencies+'
    for idx in xrange(len(titleResults['sentences'])):
        deps = titleResults['sentences'][idx]['dependencies']
        toks = titleResults['sentences'][idx]['tokens']
        depStr = ', '.join([dep[0]+'('+toks[dep[1]]+', '+toks[dep[2]]+')' for dep in deps])
        print '%2i >>' % idx, depStr
    
    print '+Title NER Tags+'
    for idx in xrange(len(titleResults['sentences'])):
        item = titleResults['sentences'][idx]
        validNER = [str(j)+'/'+NERMaster[i] for i,j in zip(item['nerTags'],xrange(len(item['tokens']))) if i!= 0]
        if len(validNER)>0:
            print '%2i >>' % idx, validNER
    
    if printParseTree:
        print '+Title Parse Trees+'
        for idx in xrange(len(titleResults['sentences'])):
            print '%2i >>' %idx
            print titleResults['sentences'][idx]['parseTree']
    
    print '+Title Coreferences+'
    for idx in xrange(len(titleResults['corefs'])):
        coref = titleResults['corefs'][idx]
        print formMentionString(titleResults,coref)
    
    print '+Top %i+' % nTop
    titleRecords = result['titleRecords']
    print 'Replacements:', sortDictToList(titleRecords['replacements'])[:nTop]
    print 'Suggestions: ', sortDictToList(titleRecords['suggestions'])[:nTop]
    
    print '+Errors+ :', titleResults['errorFlag']

    print '----------'
    
    articleResults = result['articleResults']
    print '+Article Sentence Results+'
    if len(articleResults['recasedFlagList'])!=len(articleResults['sentences']):
        # If extra sentence appeared after pipeling processing, will be unsure about the recase flags (generated during preprocesing)
        for idx in xrange(len(articleResults['sentences'])):
            item = articleResults['sentences'][idx]
            sent = ' '.join([item['tokens'][i] + '/' + POSMaster[item['posTags'][i]] for i in xrange(len(item['tokens']))])
            if idx < len(articleResults['recasedFlagList']):
                if articleResults['recasedFlagList'][idx]:
                    print '%2i >>' % idx,'[?Recased?]', sent
                else:
                    print '%2i >>' % idx,'[??]', sent
            else:
                print '%2i >>' % idx,'[?Missing?]', sent
    else:
        for idx in xrange(len(articleResults['sentences'])):
            item = articleResults['sentences'][idx]
            sent = ' '.join([item['tokens'][i] + '/' + POSMaster[item['posTags'][i]] for i in xrange(len(item['tokens']))])
            if articleResults['recasedFlagList'][idx]:
                print '%2i >>' % idx,'[Recased]', sent
            else:
                print '%2i >>' % idx,sent

    if printLemmas:
        print '+Article Lemmas+'
        for idx in xrange(len(articleResults['sentences'])):
            item = articleResults['sentences'][idx]
            print '%2i >>' % idx, ' '.join(item['lemmas'])

    print '+Article Dependencies+'
    for idx in xrange(len(articleResults['sentences'])):
        deps = articleResults['sentences'][idx]['dependencies']
        toks = articleResults['sentences'][idx]['tokens']
        depStr = ', '.join([dep[0]+'('+toks[dep[1]]+', '+toks[dep[2]]+')' for dep in deps])
        print '%2i >>' % idx, depStr

    print '+Article NER Tags+'
    for idx in xrange(len(articleResults['sentences'])):
        item = articleResults['sentences'][idx]
        validNER = [str(j)+'/'+NERMaster[i] for i,j in zip(item['nerTags'],xrange(len(item['tokens']))) if i!= 0] 
        if len(validNER)>0:
            print '%2i >>' % idx, validNER

    if printParseTree:
        print '+Article Parse Trees+'
        for idx in xrange(len(articleResults['sentences'])):
            print '%2i >>' %idx
            print articleResults['sentences'][idx]['parseTree']

    print '+Article Coreferences+'
    for idx in xrange(len(articleResults['corefs'])):
        coref = articleResults['corefs'][idx]
        print formMentionString(articleResults,coref)

    print '+Top %i+' % nTop
    articleRecords = result['articleRecords']
    print 'Replacements:', sortDictToList(articleRecords['replacements'])[:nTop]
    print 'Suggestions: ', sortDictToList(articleRecords['suggestions'])[:nTop]
    
    print '+Errors+ :', articleResults['errorFlag']
"""

def sortDictToList(myDict, ascending=False):
    # converts dictionary of {key:counts} to sorted list of [(key, counts)]
    sortedList = sorted(myDict.items(), key=lambda (k, v):(v, k))
    if not ascending:
        sortedList.reverse()
    return sortedList

def elementwiseOr(boolList1, boolList2):
    return [any(tup) for tup in zip(boolList1,boolList2)]

def elementwiseAnd(boolList1, boolList2):
    return [all(tup) for tup in zip(boolList1,boolList2)]
    

def getCompanyNameChains(toksList):
    # This generates a list of (startIdx, endIdx) which are the potential company names
    # Different than in parser preprocessing, because we must include single capital tokens, and Inc. in the chain
    
    wordLimit = 1000
    chainList = []
    capNumFlagsList = []
    
    for sentIdx, origToks in enumerate(toksList):
        excludeIdx = set([])  # not used for now...was set(range(startValidIdx))
        augmentedExcludeIdx = set([])  # create copy of excluded indices
        chainIndices = []  # stores sublists of runs of potential company names
        capNumFlags = []
        
        # Generate new set of reconstructed tokens
        inChain = False
        chainIdx = []
        lastCapIdx = 0
        firstLowerIdx = wordLimit  # set initial value to unachievable index
        
        for i, tok in enumerate(origToks):
            tokIsCapped, tokIsNumber = validCompName(tok)
            capNumFlags.append((tokIsCapped,tokIsNumber))
            
            # Augment exclusion indices
            if i < len(origToks) - 1:
                # Exclude things like "CEO of..." or "in March..."
                if tok in excludeCompNameDict and origToks[i + 1] in excludeCompNameDict[tok]:
                    augmentedExcludeIdx |= set([i, i + 1])
                # Now exclude dates (because we are including numbers to form potential company names), right before we 
                offset = removeLeadingDatesRelaxed(origToks[i + 1:])
                if offset > 0:
                    augmentedExcludeIdx |= set(range(i + 1, i + 1 + offset))
            else:
                offset = 0
            
            if i not in augmentedExcludeIdx:
                
                # Begin chain or continue chain if cap words / numbers are encountered (exclude years)
                if (tokIsCapped or tokIsNumber) and not (tok.isdigit() and len(tok) == 4 and 1500 < int(tok) < 2050):  # year cutoffs (tokIsNumber gives relaxed variants, but we want strictly numbers)
                    inChain = True
                    chainIdx.append(i) 
                    lastCapIdx = i  # track last word that was capitalized / number, check later to only end on cap/numbers
                elif inChain:
                    # Continue chain on special lower case terms (cannot begin on lower case)
                    if tok in compLowerCaseKW:
                        chainIdx.append(i)
                        if firstLowerIdx == wordLimit:  # track the location of the first lower case word
                            firstLowerIdx = i
                    # Continue chain if find comma followed by 'inc.' and similar words
                    elif tok == ',' and i+1 < len(origToks) and origToks[i+1].lower() in incSet:
                        chainIdx.append(i)
                        if firstLowerIdx == wordLimit:
                            firstLowerIdx = i
                    #    incIdx.add(i)
                    # Continue chain if 'inc.' or similar, and count as capital word (so that it can end on it)
                    elif tok.lower() in incSet:
                        chainIdx.append(i)
                        lastCapIdx = i
                    #   incIdx.add(i)
                    # End the chain if no valid terms are found
                    else:
                        # If lowercase word was in chain, make sure to end on the last capital word 
                        while chainIdx[-1] != lastCapIdx:
                            chainIdx.pop()
                        # If only one word, remove stopword cases and numbers
                        if len(chainIdx) == 1 and (capNumFlags[chainIdx[0]][1] or origToks[chainIdx[0]] in nltkStopwords):
                            chainIdx.pop() 
                        if len(chainIdx) > 0:
                            chainIndices.append(chainIdx)
                        inChain = False  # reset chain variables
                        chainIdx = []
                        firstLowerIdx = wordLimit
                    
                # Also end the chain if it is the last word in the sentence
                if inChain and i == len(origToks) - 1:
                    while chainIdx[-1] != lastCapIdx:  # make sure to end on capital word
                        chainIdx.pop()
                    # If only one word, remove stopword cases and numbers
                    if len(chainIdx) == 1 and (capNumFlags[chainIdx[0]][1] or origToks[chainIdx[0]] in nltkStopwords):
                        chainIdx.pop() 
                    if len(chainIdx) > 0:
                        chainIndices.append(chainIdx)
                    inChain = False  # reset chain variables
                    chainIdx = []
                    firstLowerIdx = wordLimit        
            elif inChain:
                # If we encounter an excluded index in the middle of the chain, end the chain
                while chainIdx[-1] != lastCapIdx:  # make sure to end on capital word
                    chainIdx.pop()
                # If only one word, remove stopword cases and numbers
                if len(chainIdx) == 1 and (capNumFlags[chainIdx[0]][1] or origToks[chainIdx[0]] in nltkStopwords):
                    chainIdx.pop() 
                if len(chainIdx) > 0:
                    chainIndices.append(chainIdx)
                inChain = False
                chainIdx = []
                firstLowerIdx = wordLimit
        
        capNumFlagsList.append(capNumFlags)
        chainList.append(chainIndices)
    return chainList, capNumFlagsList
    