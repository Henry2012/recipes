import string
import nltk
import cPickle
import time
import numpy as np
from multiprocessing import Pool
from math import floor
import gensim
import logging
from sklearn import svm, linear_model, ensemble
import os
import errno
from functools import partial
import itertools

stemmer = nltk.PorterStemmer()

def getTitleDict(startIdx):
    titleKeywords = getTitleKeywords()
    return dict(zip(titleKeywords,range(startIdx,startIdx+len(titleKeywords))))

def getTitleKeywords():
    # if any of these change, must retrain SVM
    fundraiseUnigram = ['finance','fund','raise','fundraise','$$$','round','invest','investor','secure','valuation','million',
                        'billion','stake','infuse','cash','equity','angel','seed']
    fundraiseBigram = ['seri a','seri b','seri c','seri d','ventur capit']
    maUnigram = ['buy','bought','acquire','acquisition','merger','merge']
    maBigram = []
    personUnigram = ['joins','recruit','hire','terminate','employee','appoint','president','director','executive','elect'
                        'resign','chief','ceo','coo','cfo','cto','departure','depart','fire','officer','quit','vp']
    personBigram = ['step down','step up']
    productUnigram = ['unveil','release','launch','announce','introduce','introduction'] 
    productBigram = ['roll out']
    partnerUnigram = ['partner','partnership','collaborate',]
    partnerBigram = ['joint ventur','team up','partner with','partnership with']
    prodRevUnigram = ['review','vs','preview']
    prodRevBigram = ['hand on','first look','top 10','top 25','top 5','top 3','shoot out','10 best','10 great']
    awardUnigram = ['award','wins','excellence','winner','finalist','honored','recipient','receive']
    awardBigram = ['year award']
    confUnigram = ['conference']
    confBigram = ['press conference','to present']
    marketResUnigram = ['forecast','market','analysis','growth']
    marketResBigram = ['market forecast', 'market research','industri studi']
    prodDemoUnigram = ['showcase']
    prodDemoBigram = ['present at']
    earningUnigram = ['profit','gross','revenue','cost','fiscal','quarter','net','q1','q2','q3','q4','cut','loss']
    earningBigram = []
    customerUnigram = ['customer','subscriber']
    customerBigram = ['subscrib growth', 'custom base']
    downsizeUnigram = ['downsize']
    downsizeBigram = ['lay off','laid off']
    lawsuitUnigram = ['litigation','arbitration','mediation','lawsuit','settlement','sue','suing','antitrust']
    lawsuitBigram = ['patent infring','law suit']
    interviewUnigram = ['interview']
    interviewBigram = ['interview with']
    topListUnigram = []
    topListBigram = ['top 100','top 50','top 20']
    product_launch_ver1Unigram = ['newest', 'often', 'launch', 'leak', 'refresh', 'unveil', 'coming', 'release', 'post', 'preview', 'come', 'latest']
    product_launch_ver1Bigram = []
    buyback_ver1Unigram = ['repurchase', 'buyout', 'return', 'back', 'buyback']
    buyback_ver1Bigram = ['buy back', 'to sell', 'sell back']
    key_hire_ver1Unigram = ['named', 'vp', 'hiring', 'manager', 'staff', 'chairman', 'department', 'engineer', 'seeks', 'hires', 'director', 'hired', 'advisor', 'appointed', 'successor', 'hire', 'join', 'name', 'vice', 'joined', 'leaving', 'leave', 'chief', 'senior', 'joining']
    key_hire_ver1Bigram = ['chairman of', 'have appoint', 'as chairman']
    sales_record_ver1Unigram = ['lowest', 'all-time', 'slumps', 'record', 'growth', 'quarter']
    sales_record_ver1Bigram = ['investor relat', 'expect earn', 'earn to', 'continu to']
    product_price_cut_ver1Unigram = ['lowers', 'reduces', 'slashed', 'dropping', 'slashing', 'cuts', 'prices', 'reduced', 'dropped']
    product_price_cut_ver1Bigram = ['compani restructur']
    acquisition_ver1Unigram = ['acquiring', 'acquired', 'acquire', 'purchased', 'buys', 'buying', 'acquires']
    acquisition_ver1Bigram = []
    earning_ver1Unigram = ['drop', 'revenue', 'reduce', 'pop', 'growth', 'slip', 'hit', 'miss', 'earning', 'market', 'q1', 'decline', 'q3', 'q2', 'q4', 'profit', 'increase', 'dominate', 'boost', 'shrink', 'soar', 'explosion', 'rise', 'slow', 'sink', 'fall', 'report', 'annual', 'contract', 'quarter', 'dip']
    earning_ver1Bigram = ['great opportun', 'opportun in', 'thi level']
    layoff_ver1Unigram = ['trim', 'stores', 'restructure', 'retire', 'out', 'cut', 'workers', 'reduction', 'eliminate', 'slash', 'destroy', 'layoffs', 'resignation', 'jobs', 'resign', 'job', 'cutting', 'lay', 'off', 'employees', 'restructuring', 'leave', 'costs', 'clean', 'axe']
    layoff_ver1Bigram = []
    dividend_ver1Unigram = ['payout', 'profitable', 'stocks', 'revenue', 'dividends', 'quarterly', 'portfolio', 'quarter', 'bond']
    dividend_ver1Bigram = []
    beat_expectation_ver1Unigram = ['delivered', 'outlook', 'strong', 'improved', 'beat', 'surge', 'tops', 'expectations', 'topped', 'surpassed', 'beats', 'exceeding', 'surging', 'forecast', 'soaring', 'smashes', 'climb', 'posted']
    beat_expectation_ver1Bigram = ['revenu fall', 'despit revenu', 'beat expect', 'result beat', 'expect despit']

    
    unigrams = fundraiseUnigram+maUnigram+personUnigram+productUnigram+partnerUnigram+prodRevUnigram+awardUnigram+confUnigram + \
                marketResUnigram+prodDemoUnigram+earningUnigram+customerUnigram+downsizeUnigram+lawsuitUnigram+interviewUnigram+topListUnigram \
                +product_launch_ver1Unigram+buyback_ver1Unigram+key_hire_ver1Unigram+sales_record_ver1Unigram+product_price_cut_ver1Unigram+acquisition_ver1Unigram+earning_ver1Unigram+layoff_ver1Unigram+dividend_ver1Unigram+beat_expectation_ver1Unigram
    bigrams = fundraiseBigram+maBigram+personBigram+productBigram+partnerBigram+prodRevBigram+awardBigram+confBigram + \
                marketResBigram+prodDemoBigram+earningBigram+customerBigram+downsizeBigram+lawsuitBigram+interviewBigram+topListBigram \
                +product_launch_ver1Bigram+buyback_ver1Bigram+key_hire_ver1Bigram+sales_record_ver1Bigram+product_price_cut_ver1Bigram+acquisition_ver1Bigram+earning_ver1Bigram+layoff_ver1Bigram+dividend_ver1Bigram+beat_expectation_ver1Bigram
                   
    return list(set([stemmer.stem_word(word) for word in unigrams]+bigrams))

def titleProc(article):
    # includes bigrams
    #stemmer = nltk.PorterStemmer()
    temp = article.decode("ascii","ignore").encode("utf-8").lower().split("\n")[0]
    tokens = [stemmer.stem_word(word) for word in stripPunct(temp.split(".")[0]).split() if len(word) <= 15]
    for item in nltk.bigrams(tokens):
        tokens.append(item[0] + " " + item[1])    
    return tokens

def ensurePathExists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

def tokProc(article):
    # Strip encoding, lower case, tokenize, and stem
    #stemmer = nltk.PorterStemmer()
    return [stemmer.stem_word(word) for word in stripPunct(article.decode("ascii", "ignore").encode("utf-8").lower()).split() \
            if word not in nltk.corpus.stopwords.words("english") and 2 <= len(word) <= 15]    

def bigramTokProc(article):
    # Return unigrams plus bigrams in same list
    tokens = tokProc(article)
    for item in nltk.bigrams(tokens):
        tokens.append(item[0] + " " + item[1])    
    return tokens
    
def stripPunct(sent):
    # Replace all punctuation with spaces
    # Not sure if we should keep apostrophes for contractions
    #table = string.maketrans('-.!"#$%&\'()*+,/:;<=>?@[\\]^_`{|}~','                                ')
    #return sent.translate(table)
    
    table = string.maketrans('-.!"#&()*+,/:;<=>?@[\\]^_`{|}~','                             ')
    return sent.translate(table).replace("$", " $$$ ").replace("%", " %%% ").replace("' ", " ").replace(" '", " ")

def getChunk(itemList, chunkNo, chunkSize):
    # chunkNo starts at 0
    # Returns a tuple (chunk, done)
    if chunkSize * (chunkNo+1) < len(itemList):
        return (itemList[chunkNo*chunkSize:(chunkNo+1)*chunkSize], 0)
    else:
        return (itemList[chunkNo*chunkSize:], 1)

def clfData(SVMPath, outPath, features, myClf = None):
    if myClf == None:
        fname = SVMPath + "svm.svm"
        logging.info("Loading SVM from " + fname)
        myClf = cPickle.load(open(fname,"rb"))
    else:
        logging.info("Using passed-in SVM.")
        
    return myClf.decision_function(features) # returns matrix of confidence scores

def procTok(args):
    # This one uses a passed-in stemmer, for multithreaded use
    # arg0 = article
    # arg1 = stemmer object
    return [args[1].stem_word(word) for word in stripPunct(args[0].decode("ascii", "ignore").encode("utf-8").lower()).split() \
            if word not in nltk.corpus.stopwords.words("english") and 2 <= len(word) <= 15]    

class NewsClf:
    def __init__(self, trainedPath, numProc=1, classifier="svm"):
        """
        classifier = "svm" or "lr" for logistic regression
        """
        # Load dictionary
        self.dictfname = trainedPath + "dictionary.dict"
        logging.info("Loading dictionary from (" + self.dictfname + ")...",)
        self.start = time.time()
        self.dict = gensim.corpora.Dictionary.load(self.dictfname)
        logging.info("Done [%f sec]" % (time.time()-self.start))
        logging.info(self.dict)
        
        # Load LDA model and generate topic probabilities for each article
        self.ldafname = trainedPath + "lda.lda"
        logging.info("Loading LDA model from (" + self.ldafname + ")...",)
        self.start = time.time()
        self.lda = gensim.models.LdaModel.load(self.ldafname)
        logging.info("Done [%f sec]" % (time.time()-self.start))
        logging.info(self.lda)
        
        
        # Load trained SVM
        self.start = time.time()
        if classifier == "svm":
            self.clffname = trainedPath + "svm.svm"
            logging.info("Loading SVM from (" + self.clffname + ")...",)
        else:
            self.clffname = trainedPath + "logiReg.lr"
            logging.info("Loading logistic regression classifier from (" + self.clffname + ")...")
        
        self.clf = cPickle.load(open(self.clffname, "rb"))
        logging.info("Done [%f sec]" % (time.time()-self.start))
        logging.info(self.clf)
        
        # Initialize other variables and objects
        self.stemmer = nltk.PorterStemmer()
        self.labelNames = cPickle.load(open(trainedPath + "labelNames.bin", "rb"))
        self.labelCounts = cPickle.load(open(trainedPath + "labelCounts.bin","rb"))
        self.classifier = classifier
        self.topicVec = []
        self.titleDict = getTitleDict(startIdx = self.lda.num_topics)
        self.numFeatures = self.lda.num_topics + len(self.titleDict)
        
        self.numProc = numProc
        self.pool = Pool(processes = self.numProc)    

    def clfConfArticle(self, article):
        # For a single article only!
        # This returns a vector of confidence scores for the categories.
        # The largest positive value corresponds to the most likely class.
        self.features = [0]*self.numFeatures
        for topic in self.lda[self.dict.doc2bow(self.procTok(article))]:
            self.features[topic[0]] = topic[1]
        for tok in titleProc(article):
            idx = self.titleDict.get(tok,-1)
            if idx != -1:
                self.features[idx] = 1
            
        if self.classifier == "svm":
            return self.clf.decision_function(np.array(self.features))[0]
                
        else:
            return self.clf.predict_proba(np.array(self.features))[0]
    
    def clfArticle(self, article):
        # For a single article only!
        # This returns a class prediction (rather than confidence scores).
        self.features = [0]*(self.numFeatures)
        for topic in self.lda[self.dict.doc2bow(self.procTok(article))]:
            self.features[topic[0]] = topic[1]
        for tok in titleProc(article):
            idx = self.titleDict.get(tok,-1)
            if idx != -1:
                self.features[idx] = 1
        
        return self.clf.predict(np.array(self.features))[0]
    
    def getFeatures(self, articles):
        self.features = []
        self.bowVec = []
        self.titleToks = []
        for i in xrange(len(articles)):
            self.features.append([0]*self.numFeatures)
        if self.numProc > 1:
            self.bowVec =[self.dict.doc2bow(tok) for tok in self.pool.map(procTok, itertools.izip(articles, itertools.repeat(self.stemmer)), int(floor(len(articles)/self.numProc)))]
            self.titleToks = self.pool.map(titleProc, articles, int(floor(len(articles)/self.numProc)))
            self.pool.close()
            self.pool.join()
        else:
            # Don't use pool if only single thread (has overhead)
            for article in articles:
                self.bowVec.append(self.dict.doc2bow(self.procTok(article)))
                self.titleToks.append(titleProc(article))
        for bow in self.bowVec:
            self.topicVec.append(self.lda[bow])
        i = 0
        for item in self.topicVec:
            for topic in item:
                self.features[i][topic[0]] = topic[1]
            i += 1
        
        # add hand-crafted features
        i = 0
        for toks in self.titleToks:
            for tok in toks:
                idx = self.titleDict.get(tok,-1)
                if idx != -1:
                    print i
                    print idx
                    print "==============="
                    self.features[i][idx] = 1
            i += 1
        
        return self.features
    
    def clfConfArticles(self, articles):        
        if self.classifier == "svm":
            try:
                return self.clf.decision_function(np.array(self.getFeatures(articles)))
            except:
                return self.clf.predict_proba(np.array(self.getFeatures(articles)))[0]
        else:
            return self.clf.predict_proba(np.array(self.getFeatures(articles))) # for logistic regression
        
        
    def clfArticles(self, articles):        
        #return self.clf.predict(np.array(self.pool.map(articleToFeatures, itertools.izip(articles,itertools.repeat((self.dict, self.lda, self.stemmer))), int(floor(len(articles)/self.numProc)))))
        return self.clf.predict(np.array(self.getFeatures(articles)))
        
    def procTok(self, article):
        return [self.stemmer.stem_word(word) for word in stripPunct(article.decode("ascii", "ignore").encode("utf-8").lower()).split() \
            if word not in nltk.corpus.stopwords.words("english") and 2 <= len(word) <= 15]   

def genSVM(outPath, features, labels, kernel = "linear", cacheSize = 200, oneVsAll = 1, C = 10):
    """
    
    """
    ensurePathExists(outPath)
    logging.info("="*20+"Generate SVM Classifier" + "="*20,)
    
    if oneVsAll == 1:
        # this is a one-vs-all classifier
        myClf = svm.LinearSVC(C = C)
        #myClf = ensemble.RandomForestClassifier(n_estimators=100)
    else:
        # this creates a one-vs-one classifer
        myClf = svm.SVC(C = C, kernel = kernel, cache_size = cacheSize)
    
    n = len(features[0])
    m = len(labels)
    
    logging.info("Training SVM [%d features, %d vectors]..." % (n, m),)
    start = time.time()
    myClf.fit(np.array(features), np.array(labels))
    logging.info("Done [%f sec]" % (time.time()-start))
    fname = outPath + "svm.svm"
    cPickle.dump(myClf, open(fname,"wb"))
    logging.info("Saved to " + fname)
    return myClf

def genLR(outPath, features, labels, C=10):
    ensurePathExists(outPath)
    logging.info("="*20+"Generate Logistic Regression Classifier" + "="*20,)
    
    myClf = linear_model.LogisticRegression(C=C)
    
    n = len(features[0])
    m = len(labels)
    
    logging.info("Training LR [%d features, %d vectors]..." % (n, m),)
    start = time.time()
    myClf.fit(np.array(features), np.array(labels))
    logging.info("Done [%f sec]" % (time.time()-start))
    fname = outPath + "logiReg.lr"
    cPickle.dump(myClf, open(fname,"wb"))
    logging.info("Saved to " + fname)
    return myClf    
    
def genLDA(outPath, numTopics, numPass, updateEvery, corpusPath, dictPath, corpus = None, myDict = None):
    """
    This trains the LDA
    """
    ensurePathExists(outPath)
    logging.info("="*20+"Generate LDA Model" + "="*20,)
    
    if myDict == None:
        fname = dictPath + "dictionary.dict"
        logging.info("Loading dictionary from " + fname)
        myDict = gensim.corpora.Dictionary.load(fname)
    else:
        logging.info("Using passed-in dictionary.")
    
    if corpus == None:
        fname = corpusPath + "corpus.mm"
        logging.info("Loading corpus from " + fname)
        corpus = gensim.corpora.MmCorpus(fname)
    else:
        logging.info("Using passed-in corpus.")
        
    logging.info(corpus)
    
    logging.info("Training LDA [updateEvery = %d, numTopic = %d, numPass = %d]..." % (updateEvery, numTopics, numPass),)
    start = time.time()
    lda = gensim.models.ldamodel.LdaModel(corpus=corpus, id2word=myDict, num_topics=numTopics, update_every=updateEvery, passes=numPass)    

    fname = outPath+"lda.lda"
    lda.save(fname)
    logging.info("Done [%f sec]" % (time.time()-start))
    logging.info("Saved to " + fname)
    return lda

def genCorpus(inFileName, inPath, outPath, numProc, dictPath, chunkSize = 10000, myDict = None):
    """
    dictPath = Path to dictionary to use
    myDict = Dictionary object, if available already
    chunkSize = Split articles into chunks of this size for sequential processing (e.g. 10000)
    
    """    
    logging.info("="*20+"Generate Corpus" + "="*20,)
    ensurePathExists(outPath+"temp/")
    
    # Generate corpus from articles file
    inName = inPath + inFileName
    logging.info("Loading articles from " + inName)
    start = time.time()
    allArticles = cPickle.load(open(inName,"rb"))
    #allArticles = allArticles[0:10] # limit articles for debug
    logging.info("Done [%f sec]" % (time.time()-start))
    
    if myDict == None:
        fname = dictPath + "dictionary.dict"
        logging.info("Loading dictionary from " + fname)
        myDict = gensim.corpora.Dictionary.load(fname)
    else:
        logging.info("Using passed-in dictionary.")
           
    # Tokenize
    logging.info("Tokenizing and processing the articles [%d threads]." % numProc)
    start0 = time.time()
    
    done = 0
    chunkNo = 0
    corpus = []
    while done == 0:        
        pool = Pool(processes = numProc)
        logging.info("Processing chunk %d..." % chunkNo,)
        start = time.time()
        articleChunk, done = getChunk(allArticles, chunkNo, chunkSize)
        tokens = pool.map(tokProc, articleChunk, int(floor(chunkSize/numProc)))
        corpus += [myDict.doc2bow(item) for item in tokens]
        
        pool.close()
        pool.join()
        
        # Save to files just in case something goes wrong
        #fname = outPath+"temp/"+"tokChunk%d.dat" % chunkNo
        #fio = open(fname,"wb")
        #cPickle.dump(tokens, fio)
        #fio.close()
        
        del articleChunk, tokens
        chunkNo += 1        
        logging.info("Done [%f sec]" % (time.time()-start))     
        
    fname = outPath + "corpus.mm"
    gensim.corpora.MmCorpus.serialize(fname, corpus)
    logging.info("Corpus generated [Total: %f sec]." % (time.time()-start0))
    logging.info("Saved to " + fname)
    del corpus
    return gensim.corpora.MmCorpus(fname)
    

def genDict(inPath, outPath, numProc, chunkSize = 10000, filtMinArticle = 5, filtMaxArticle = 0.5, maxDictWords = 50000, genCorp = 1):
    """
    numProc = Number of threads to use
    chunkSize = Split articles into chunks of this size for sequential processing (e.g. 10000)
    filtMinArticle = Min # articles a word must appear in to be saved in dictionary (e.g. 5)
    filtMaxArticle = Max fraction of articles a word can appear in to be saved in dictionary (e.g. 0.5)
    maxDictWords = Maximum words to keep in dictionary (e.g. 50000)
    genCorp = Generate corpus using same input file? (1 or 0)
    
    Returns (Dictionary_object, chunkNo), where (chunkNo-1) is the # of temporary token chunks saved to disk
    """
    logging.info("="*20+"Generate Dictionary" + "="*20,)
    ensurePathExists(outPath+"temp/")

    # Load the combined file
    logging.info("Loading articles...",)
    start = time.time()
    allArticles = cPickle.load(open(inPath + "allArticles.bin","rb"))
    #allArticles = allArticles[0:10] # limit articles for debug
    logging.info("Done [%f sec]" % (time.time()-start))
    
    myDict = gensim.corpora.dictionary.Dictionary()
           
    # Tokenize and load into dictionary
    logging.info("Tokenizing and processing the articles [%d threads]." % numProc)
    start0 = time.time()
    
    done = 0
    chunkNo = 0
    while done == 0:        
        pool = Pool(processes = numProc)
        logging.info("Processing chunk %d..." % chunkNo,)
        start = time.time()
        articleChunk, done = getChunk(allArticles, chunkNo, chunkSize)
        tokens = pool.map(tokProc, articleChunk, int(floor(chunkSize/numProc)))
        #myDict.add_documents(pool.map(hgaoHelper.bigramTokProc, articleChunk, int(floor(chunkSize/numProc))))
        myDict.add_documents(tokens)
        
        pool.close()
        pool.join()
        
        fname = outPath+"temp/"+"tokChunk%d.dat" % chunkNo
        fio = open(fname,"wb")
        cPickle.dump(tokens, fio)
        fio.close()
        
        del articleChunk, tokens
        chunkNo += 1        
        logging.info("Done [%f sec]" % (time.time()-start))
        
    logging.info("Pruning the dictionary.")
    myDict.filter_extremes(no_below=filtMinArticle, no_above=filtMaxArticle, keep_n=maxDictWords)
    dictName = outPath+"dictionary.dict"   
    myDict.save(dictName)
    myDict.save_as_text(outPath+"dictText.txt")
    logging.info(myDict)
    logging.info("Dictionary generated [Total: %f sec]." % (time.time()-start0))
    logging.info("Saved to "+ dictName + "\n")
    
    if genCorp==1:
        # Generate corpus, after dictionary has been built
        logging.info("Generating corpus.")
        start0 = time.time()
        
        corpus = []
        for i in xrange(chunkNo):
            logging.info("Processing chunk %d..." % i,)
            start = time.time()
            fname = outPath+"temp/"+"tokChunk%d.dat" % i
            fio = open(fname,"rb")
            corpus += [myDict.doc2bow(item) for item in cPickle.load(fio)]
            fio.close()
            logging.info("Done [%f sec]" % (time.time()-start))
    
        corpName = outPath+"corpus.mm"
        gensim.corpora.MmCorpus.serialize(corpName, corpus)
        
        logging.info("Corpus generated [Total: %f sec]." % (time.time()-start0))
        logging.info("Saved to " + corpName + "\n")
        del corpus
        return myDict, gensim.corpora.MmCorpus(corpName)
    else:
        return myDict
            
def corpusToSVMInput(mm, lda):
    # inputs are the corpus and lda objects
    # returns a list of feature vectors, corresponding to each article in corpus mm
    topicDat = []
    logging.info("Generating topic probabilities [%d] for each article [%d]..." % (lda.num_topics, mm.num_docs),)
    start = time.time()
    
    for doc_bow in mm:
        topicDat.append(lda[doc_bow])
    logging.info("Done [%f sec]" % (time.time()-start))
    
    labDat = []
    for i in xrange(mm.num_docs):
        labDat.append([0]*lda.num_topics)
    logging.info( "Converting to feature vectors for SVM...",)
    start = time.time()
    i = 0
    for articleVec in topicDat:
        for topic in articleVec:
            labDat[i][topic[0]] = topic[1]
        i += 1   
    logging.info("Done [%f sec]" % (time.time()-start))
    return labDat

def getCombinedFeatures(corpus, lda, inFileName, inPath, outPath, numProc=1, chunkSize=10000):
    features = corpusToSVMInput(corpus, lda) # create features from LDA model
    
    # Load the combined articles file
    ensurePathExists(outPath+"temp/")
    logging.info("Loading articles...",)
    start = time.time()
    allArticles = cPickle.load(open(inPath + "allArticles.bin","rb"))
    #allArticles = allArticles[0:10] # limit articles for debug
    logging.info("Done [%f sec]" % (time.time()-start))
    
    # Add hand crafted features
    titleDict = getTitleDict(startIdx=lda.num_topics)
    for i in xrange(len(features)):
        features[i] += [0]*len(titleDict) # augment number of features
    
    logging.info("Adding [%d] hand crafted features from titles..." % len(titleDict))   
    start0 = time.time()
    done = 0
    chunkNo = 0
    i = 0
    while done == 0:        
        pool = Pool(processes = numProc)
        logging.info("Processing chunk %d..." % chunkNo,)
        start = time.time()
        articleChunk, done = getChunk(allArticles, chunkNo, chunkSize)
        tokens = pool.map(titleProc, articleChunk, int(floor(chunkSize/numProc)))        
        pool.close()
        pool.join()
        
        for toks in tokens:
            for tok in toks:
                idx = titleDict.get(tok,-1)
                if idx != -1:
                    features[i][idx] = 1
            i += 1
        
        fname = outPath+"temp/"+"tokChunk%d.dat" % chunkNo
        fio = open(fname,"wb")
        cPickle.dump(tokens, fio)
        fio.close()
        
        del articleChunk, tokens
        chunkNo += 1        
        logging.info("Done [%f sec]" % (time.time()-start))
        
    logging.info("Combined features generated [%f sec]" % (time.time()-start0))
    return features

def combineArticles(inPath, fnames, outPath, maxArticles = -1):
    ensurePathExists(outPath)
    logging.info("="*20+"Combining Articles" + "="*20,)
    logging.info("Loading files from (" + inPath + ")...")
    start = time.time()
    
    catArticles = []
    numArtVec = []
    for fname in fnames:
        catArticles.append(cPickle.load(open(inPath+fname,"rb")))
        numArtVec.append(len(catArticles[-1]))
        logging.info(fname + " [%d articles]" % numArtVec[-1])
    
    logging.info("Done [%f sec]\n" % (time.time()-start))
    
    logging.info("Reorganizing and aggregating articles...",)
    start = time.time()
    
    allArticles = []
    catVec = []
    count = 0
    for i in xrange(max(numArtVec)):
        for j in xrange(len(fnames)):
            if i < len(catArticles[j]) and (maxArticles < 0 or count < maxArticles):
                allArticles.append(catArticles[j][i])
                catVec.append(j)
                count += 1
    logging.info("Done [%f sec]\n" % (time.time()-start))
    
    logging.info("Total number of articles: %d" % len(allArticles))
        
    # Save 
    fo = [open(outPath+"allArticles.bin","wb"), open(outPath+"labels.bin", "wb"), \
          open(outPath+"labelNames.bin","wb"), open(outPath+"labelCounts.bin","wb") ]
    
    cPickle.dump(allArticles, fo[0])
    cPickle.dump(np.array(catVec), fo[1])
    cPickle.dump(fnames, fo[2])
    cPickle.dump(numArtVec, fo[3])
    for fio in fo:
        fio.close()
    
    logging.info("Data saved to " + outPath + "allArticles.bin")
    
def configLogger():
    # set up logging to file
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt='%m-%d %H:%M',
                        filename='topicLog.log',
                        filemode='a')
    # define a Handler which writes INFO messages or higher to the sys.stderr
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    # set a format which is simpler for console use
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    # tell the handler to use this format
    console.setFormatter(formatter)
    # add the handler to the root logger
    logging.getLogger('').addHandler(console)

if __name__ == '__main__':
    pass