#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""A collection of functions used regularly """

import itertools
import re, math
from collections import Counter

def group_records(iterable, n, fillvalue=None):
	""" A length of each record is n fields """
	args = [iter(iterable)] * n
	grouped_obj = itertools.izip_longest(fillvalue=fillvalue, *args)
	return list(grouped_obj)

def line_overlap(a, b):
	output = []
	for line in a:
		a = line.lower().split()
		for line in b:
			b = line.lower().split()
			ov = set(a) & set(b)
			if len(ov)/len(b) > 0.8:
				output.append(line)
	return output
	
WORD = re.compile(r'\w+')

def get_cosine(vec1, vec2):
  intersection = set(vec1.keys()) & set(vec2.keys())
  numerator = sum([vec1[x] * vec2[x] for x in intersection])
  sum1 = sum([vec1[x]**2 for x in vec1.keys()])
  sum2 = sum([vec2[x]**2 for x in vec2.keys()])
  denominator = math.sqrt(sum1) * math.sqrt(sum2)
  if not denominator:
    return 0.0
  else:
    return float(numerator) / denominator

def text_to_vector(text):
  words = WORD.findall(text)
  return Counter(words)
  
def print1000(inlist, outfile):
	for x in inlist:
		if len(x) != 0:
			for i in range(1000):
				print >> outfile, x.decode('utf-8')
	outfile.close()
	
def filter_file_by_brands(titles, brands, filename):
	input = open(titles).read()
	input = input.decode('utf-8').split('\n')
	input = [x.split('\a') for x in input]
	use_brands = open(brands).read()
	br = use_brands.decode('utf-8').lower().split('\n')
	outfile = open(filename, 'w')
	for x in input:
		if len(x) >5:
			title = {w.lower() for w in x[2].split()}
			if title & set(br) != set([]):
				print >> outfile, "%s\t%s\t%s\t%s\t%s\n" %(x[0].encode('utf-8'), x[1].encode('utf-8'), x[2].encode('utf-8'), x[3].encode('utf-8'), x[4].encode('utf-8'))
	outfile.close()
	
def filter_file_by_brands(titles, brands, filename):
	input = open(titles).read()
	input = input.decode('utf-8').split('\n')
	input = [x.split('\a') for x in input]
	use_brands = open(brands).read()
	br = use_brands.decode('utf-8').lower().split('\n')
	outfile = open(filename, 'w')
	for x in input:
		if len(x) >5:
			title = {w.lower() for w in x[2].split()}
			if title & set(br) != set([]):
				print >> outfile, "%s\t%s\t%s\t%s\t%s\n" %(x[0].encode('utf-8'), x[1].encode('utf-8'), x[2].encode('utf-8'), x[3].encode('utf-8'), x[4].encode('utf-8'))
	outfile.close()
	
def document_features(document, bigram_list): 
  features = {}
  for bigram in bigram_list:
    features['contains(%s)' % bigram] = (bigram in document)
  return features
