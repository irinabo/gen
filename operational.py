#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""A collection of functions used regularly """

import itertools, tarfile
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

def merge_dics(d1, d2, d3):
	keys = set(d1).union(d2)
	no = []
	return list((k, d1.get(k, no), d2.get(k, no), d3.get(k, no)) for k in keys)
	
def generate_paraphrase(source, rules):
	source = open(source).read()
	source = source.lower()
	source = source.decode('utf-8').split('\n')
	rules = open(rules).read()
	rules = rules.decode('utf-8').split('\n')
	rules = [x.split('\t') for x in rules]
	out_lists = {}
	for orig_str in source:
		out_lists[orig_str] = {orig_str}
		for rule in rules:
			old_x = rule[0]
			new_strs = set()
			for s in out_lists[orig_str]:
				s1 = s.split()
				if old_x in s1:
					for new_x in rule[1:]:
						new_strs.add(re.sub(old_x,new_x,s))
			out_lists[orig_str] = out_lists[orig_str]|new_strs
	return out_lists
	
def read_file(file):
        f1 = open(file).read()
        f2 = f1.decode('utf-8').lower().split('\n')
        f3 = [x.split() for x in f2]
        return f3

def calc_ngrams(file):
        f = read_file(file)
        out_bi = []
        out_tri = []
        for title in file:
                cand_bi = [(title[x], title[x+1]) for x in range(0, (len(title)-1))]
                cabd_tri = [(title[x], title[x+1], title[x+2]) for x in range(0, (len(title)-2))]
                out_bi += cand_bi
                out_tri += cabd_tri
        return out_bi, out_tri

def n_gram_overlap(cand_file, ref_file):
        cand_bi, cand_tri = calc_ngrams(cand_file)
        ref_bi, ref_tri = calc_ngrams(ref_file)
        bigram_overlap = len(set(cand_bi) & set(ref_bi))
        trigram_overlap = len(set(cand_tri) & set(ref_tri))
        print "total bigrams in the candidate set", len(cand_bi)
        print "total of those occuring in the reference set", bigram_overlap
        print "total trigrams in th candidate set", len(cand_tri)
        print "total of those occuring in the reference set", trigram_overlap
        print bigram_overlap, trigram_overlap

def get_brands_in_missed_untr_words(file, br_data1 = single_word_brands, br_data2 = two_and_more_word_brands):
	res = []
	source = get_missed_untr_words1(file)
	br_data2_sorted = sorted(br_data2,key=lambda t:len(t),reverse=True)
	max_len_br_data2 = max([len(t) for t in br_data2])
	br_data2_dict = {x:[] for x in range(2,max_len_br_data2+1)}
	br_data2_dict[1] = br_data1
	for t in br_data2:
		br_data2_dict[len(t)].append(t)
	for common_words in source:
		jcw = ' '.join(common_words)
		lcw = len(common_words)
		if lcw == 0:
			res += [] # == common_words
		else:
			keep_searching = True
			for x in range(min(lcw,max_len_br_data2),0,-1):
				if keep_searching == False:
					break
				for brand_wordlist in br_data2_dict[x]:
					if keep_searching == False: # should be unnecessary
						break
					if brand_wordlist[0] not in common_words:
						continue
					else:
						jbwl = ' '.join(brand_wordlist)
						if jbwl not in jcw:
							continue
						else:
							############# append jbwl to the list of brands that we did find a match for #####
							res.append(jbwl)
							keep_searching = False
							break
	return res	

def create_targz(archive_name, *args):
	archive_name1 = '_'.join(archive_name.split())
	archive_name2 = archive_name1+'.tar.gz'
	tar = tarfile.open(archive_name2, "w:gz")
	for a in args:
		tar.add(a)
	tar.close()
	
def shuffle_files(file1, output_name):
	f1 = open(file1).read()
	#format: bing, emt
	f1 = f1.decode('utf-8').split('\n')
	f2 = [x.split('\t') for x in f1]
	outfile = open(output_name, 'w')
	for x in range(0, len(f2)):
		if len(f2[x]) == 2:
			if int(x) % 2 == 0:
				print >> outfile, '%s\t%s\t%s' %(f2[x][0].encode('utf-8'), f2[x][1].encode('utf-8'), 'bing_first')
			else:
				print >> outfile, '%s\t%s\t%s' %(f2[x][1].encode('utf-8'), f2[x][0].encode('utf-8'), 'emt_first')
	outfile.close()
