#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import re
import json

class Processor:
    def __init__(self, abbreviations_file):
        # set abbreviation file
        try:
            with open(abbreviations_file) as f:
                self.abbreviations = dict.fromkeys(f.read().splitlines(), True)
        except Exception as err:
            print(err)
            sys.exit()
        
        # end punctuation
        self.end_punct = ['.', '!', '?']

        # punctuation
        self.punct = ['.', '!', '?', ',', '"', '\'', '(', ')']

        # set array quote
        self.quotes = ['"', '\'']
        self.start_end_char = ['"', '\'', '(', ')']

        # mark for start and end quote
        self.open_quote = False
        self.quote_count = 0

        self.digit_pattern = [
            '\d*\.\d{1,2}', 
            '\d*\,\d{1,2}', 
            '(\d+)$', 
            '(\d+\.?)$'
        ]

        # penanda akhir abbreviation
        self.abb_punct = [',', '.']

    def is_digit(self, word):
        # return true if find any digit
        if re.search('|'.join(self.digit_pattern), word):
            return True
        return False
    
    def is_abbreviation(self, word):
        # return true if find any abbreviation
        word = word.lower()

        if len(word) == 0:
            return False
            
        if word[-1] in self.abb_punct:
            word = word[:-1]
        
        if word in self.abbreviations:
            return True
            
        return False
    
    def get_symbol(self, word):
        return re.findall(r'(\W+)', word)

    def segment(self, sentences):
        # split words in sentences
        temp_segmented = []
        # split sentences in paragraphs
        segmented = []

        words = sentences.split()

        for word in words:
            # get end word
            end_word = word[-1]

            # when find starting quote, set True to open_quote
            if re.search("|".join(self.quotes), word):
                self.quote_count += 1
                if self.get_symbol(word).count('"') == 2 \
                    or self.get_symbol(word).count('\'') == 2:
                    self.quote_count += 1
                if self.quote_count == 1:
                    self.open_quote = True
        
            # when find any punctuation at the end of sentences, set True to found_punct
            found_punct = False
            if end_word in self.end_punct:
                found_punct = True
            
            if found_punct:
                if self.is_digit(word) or self.is_abbreviation(word):
                    if end_word in self.end_punct:
                        if self.quote_count == 1:
                            # ignore punctuation when end quote not found yet
                            temp_segmented.append(word)
                        else:
                            # end of sentence when there is no quote
                            temp_segmented.append(word)
                            segmented.append(' '.join(temp_segmented))
                            temp_segmented = []
                    else:
                        temp_segmented.append(word)
                else:
                    if not self.open_quote:
                        temp_segmented.append(word)
                        segmented.append(' '.join(temp_segmented))
                        temp_segmented = []
                    else:
                        if self.quote_count == 1:
                            temp_segmented.append(word)
                        else:
                            temp_segmented.append(word)
                            # when we didn't find any open quote, reset state
                            self.open_quote = False
                            self.quote_count = 0
            else:
                # when we find end quote, reset quote state
                if self.quote_count == 2:
                    self.open_quote = False
                    self.quote_count = 0
                temp_segmented.append(word)

        
        return segmented
