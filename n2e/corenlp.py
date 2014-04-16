# -*- encoding: utf-8 -*-

# Author: Hua Gao
# Created: 5/30/13
# Edited by:
import jpype
import logging

from sentenceLib import removeNewlines, preprocessArticle
from stanfordnlp.sfcorenlp import SFCoreNLP


class StanfordCoreNLP(object):
    def __init__(self, config):
        self.logger = logging.getLogger('pre_processor')

        self.corenlp = SFCoreNLP(
            config.get('pre_processor', 'stanfordnlp-host'),
            config.getint('pre_processor', 'stanfordnlp-port'))

        self.wordLimit = config.getint('pre_processor', 'wordLimit')
        self.sentLimit = config.getint('pre_processor', 'sentLimit')
        self.compDict = {}
        self.numErrors = 0

    def processNewsArticle(self, newsItem):
        # item['title'] and item['content_text'] are the title and article text, respectively
        # performs all preprocessing steps

        if 'content' not in newsItem:
            newsItem['content'] = newsItem.pop('content_text')

        # Remove newlines, depending on context
        title = removeNewlines(newsItem['title'])
        article = removeNewlines(newsItem['content'])

        # Tokenize
        origTitleToksList = self.corenlp.tokenize(title)
        origArticleToksList = self.corenlp.tokenize(article)

        # Preprocessing
        # 80 word sentences requires ~2.1 GB RAM if encountered
        preResults = preprocessArticle(
            origTitleToksList, origArticleToksList, compDict=self.compDict,
            wordLimit=self.wordLimit, sentLimit=self.sentLimit,
            returnRecords=False)

        # Reconstruct articles to pass through entire nlp pipeline
        reconArticle = preResults['article']['recon']
        reconTitle = preResults['title']['recon']

        # Parse
        titleResult = self.processArticle(reconTitle)
        articleResult = self.processArticle(reconArticle)

        errors = 0
        if articleResult['errorFlag']:
            errors += 1
        if titleResult['errorFlag']:
            errors += 1

        parseResults = {
            'titleToksList': titleResult['toksList'],
            'titleLemmasList': titleResult['lemmasList'],
            'titlePOSTagsList': titleResult['posTagsList'],
            'titleNERTagsList': titleResult['nerTagsList'],
            'titleDepsList': titleResult['depsList'],
            'titleParseTreeList': titleResult['parseTreeList'],
            'titleCorefsList': titleResult['corefs'],
            'titleErrorFlag': titleResult['errorFlag'],
            'articleToksList': articleResult['toksList'],
            'articleLemmasList': articleResult['lemmasList'],
            'articlePOSTagsList': articleResult['posTagsList'],
            'articleNERTagsList': articleResult['nerTagsList'],
            'articleDepsList': articleResult['depsList'],
            'articleParseTreeList': articleResult['parseTreeList'],
            'articleCorefsList': articleResult['corefs'],
            'articleErrorFlag': articleResult['errorFlag'],
            'parseErrors': errors,
            'titleRecasedFlagList': preResults['title']['allCapsFlagList'],
            'articleRecasedFlagList': preResults['article']['allCapsFlagList']}

        return parseResults

    def processArticle(self, article):
        try:
            self.result = self.corenlp.process(article)
            self.result['errorFlag'] = False

        except jpype.JavaException:
            # Every once in a while, the parser will get a NullPointerException
            #   or AssertionError in Java, and empty parse results are returned
            self.numErrors += 1
            self.result['errorFlag'] = True

        return self.result
