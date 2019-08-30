#!/usr/bin/env python
# refactored from https://github.com/amsqr/NaiveSumm

import re
from collections import Counter
from processor import Processor

class Summarize():
    def __init__(self):
        self.stopwords_file = 'stopwords.txt'
        self.abbreviations_file = 'abbreviations.txt'

    def clean_text(self, pars):
        with open(self.stopwords_file, 'r') as f:
            stopwords_read = f.read()
        stopwords = dict.fromkeys(stopwords_read.splitlines(), True)

        alphanumeric = re.compile(r'[^a-zA-Z0-9]+')
        clean_char = alphanumeric.sub(' ', pars)
        words = [word.lower() for word in clean_char.split() if word not in stopwords]
        return words

    def segmentation(self, sentences):
        processor = Processor(self.abbreviations_file)
        return processor.segment(sentences)
    
    def extract(self, article, sentence_num):
        segmented = self.segmentation(article)
        words = self.clean_text(article)

        frequent = Counter(words).keys()

        extracted = []
        for item in frequent:
            for n in range(len(segmented)):
                if len(extracted) < sentence_num:
                    if segmented[n] not in extracted and item in segmented[n]:
                        extracted.append(segmented[n])
                        break
        
        temp_sent = {}
        for e in extracted:
            temp_sent[e] = segmented.index(e)
        
        summ = sorted(temp_sent, key=temp_sent.__getitem__)

        return summ

if __name__ == '__main__':
    with open('article.txt', 'r') as a:
        news = a.read()
    
    s = Summarize()
    sentences = s.extract(news, 4)
    print(sentences)