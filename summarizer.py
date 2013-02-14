#!/usr/bin/env python
# refactored from https://github.com/amsqr/NaiveSumm
# because NLTK module is too heavy to be loaded

import sys
import re

def rangkum(text, jml_kalimat):
	# open the stopwords
	openfile = open("./stopwords.txt")
	exclude = [i.rstrip() for i in openfile]
	openfile.close()

	# text cleaning
	cari = re.compile(r"[^a-zA-Z0-9]+")
	bersih = cari.sub(" ",text)

	# split text
	kalimat = text.replace("\n","").split(".")
	kalimat_lower = [i.lower() for i in kalimat]

	# split words
	kata = bersih.split()
	kata_lower = [i.lower() for i in kata]
	kata_bersih_lower = [i for i in kata_lower if i not in exclude]

	# most frequent words
	sering = {}
	for i in kata_bersih_lower:
		if i not in sering:
			sering[i] = 1
		else:
			sering[i] += 1

	seringfin = sorted(sering, key=sering.__getitem__, reverse=True)
	
	# check main sentences based on most frequent words
	rang_kalimat = []
	for kata in seringfin:
		for i in xrange(len(kalimat_lower)):
			if len(rang_kalimat) < jml_kalimat:
				if (kalimat_lower[i] not in rang_kalimat and kata in kalimat_lower[i]):
					if kalimat[i] not in rang_kalimat:
						rang_kalimat.append(kalimat[i])
					break
	
	# sorting lists
	rang_kalimat.sort(lambda s1, s2: text.find(s1) - text.find(s2))
	return ".".join(rang_kalimat)

if __name__ == "__main__":
	# opening the file
	filenya = open("article.txt","r")
	input = filenya.read()
	filenya.close()

	# number of sentences
	inti_kalimat = int(3)
	hasil = rangkum(input, inti_kalimat)
	print hasil
