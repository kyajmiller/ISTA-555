#import statements
from __future__ import print_function
from __future__ import division
import nltk
from nltk import FreqDist
import re

#main
def main():
	
	#Part 1
	#tokenize all items
	tokenize = open('project1_tweets.txt', 'r')
	
	raw = tokenize.read()
	
	pattern = r'''(?x)
		http\://[a-zA-Z|\d]+\.\w+[/[\w|\d]*   #url
		|
		[<>]?                       # optional hat/brow
		[:;=8]                      # eyes
		[\-o\*\']?                  # optional nose
		[\)\]\(\[dDpP/\:\}\{@\|\\]  # mouth      
		|                           #### reverse orientation
		[\)\]\(\[dDpP/\:\}\{@\|\\]  # mouth
		[\-o\*\']?                  # optional nose
		[:;=8]                      # eyes
		[<>]?                       # optional hat/brow
		|
		@[\w_]+                     #twitter username
		|
		\#+[\w_]+[\w\'_\-]*[\w_]+   #hashtags
		|
		([A-Z]\.)+                  #abbreviations
		|
		[a-z][a-z'\-_]+[a-z]        #apostrophes and dash words
		|
		[+\-]?\d+[,/.:-]\d+[+\-]?   #numbers, fractions, decimals
		|
		[\w_]+                      #words without apostrophes and dashes
		|
		\.(?:\s*\.){1,}             #ellipsis
		|
		\S                          #nonwhite space
		'''
		
	tweetout = nltk.regexp_tokenize(raw, pattern)
	print(tweetout)
		
	#Part 2
	#Get hashtags that cooccur with #happy or #sad	
	tweetsin = open('project1_tweets.txt', 'r')
	
	happytweetslist = []
	sadtweetslist = []
	all_hashes = [] #used for Part 6
	#filter lines containing #happy or #sad, append them to respective lists
	for line in tweetsin:
		matchhappy = re.search( r'\#happy\s', line)
		matchsad = re.search( r'\#sad\s', line)
		matchhash_all = re.search( r'\#+[\w_]+[\w\'_\-]*[\w_]+', line)
		if matchhappy:
			happytweetslist.append(line)
		if matchsad:
			sadtweetslist.append(line)
		if matchhash_all:
			all_hashes.append(matchhash_all.group())
	
	#filter #happy hashtags
	hashtags_happy = []
	happy_nohash = []
	for i in happytweetslist:
		matchhash = re.search( r'\#+[\w_]+[\w\'_\-]*[\w_]+', i)
		if matchhash:
			hashtags_happy.append(matchhash.group())
			
	
	#filter #sad hashtags
	hashtags_sad = []
	sad_nohash = []
	for i in sadtweetslist:
		matchhash = re.search( r'\#+[\w_]+[\w\'_\-]*[\w_]+', i)
		if matchhash:
			hashtags_sad.append(matchhash.group())
	
	#filter all the hashtags that are NOT #happy and add them to a new list
	happy_not_happy = []
	for i in hashtags_happy:
		movenothappy = re.search( r'\#happy', i)
		if not movenothappy:
			happy_not_happy.append(i)
			
	#filter all the hashtags that are NOT #sad and add them to a new list
	sad_not_sad = []
	for i in hashtags_sad:
		movenotsad = re.search( r'\#sad', i)
		if not movenotsad:
			sad_not_sad.append(i)
			
	#FreqDist		
	fdist_happy = FreqDist(happy_not_happy)
	fdist_sad = FreqDist(sad_not_sad)
	print("Most common #happy hashtags")
	print(fdist_happy.most_common(20))
	print("\n")
	print("Most common #sad hashtags")
	print(fdist_sad.most_common(20))
	print("\n")
	
	#Part 6
	#put top 20 associated hashtags into list for manipulation
	mc_happy = []
	h_just_hash = []
	for i in fdist_happy.most_common(20):
		mc_happy.append(i)
		h_just_hash.append(i[0])
	mc_sad = []
	s_just_hash = []
	for i in fdist_sad.most_common(20):
		mc_sad.append(i)
		s_just_hash.append(i[0])		
		
	#get frequency distribution for all hashes, add them to new list
	fdist_all_hashes = FreqDist(all_hashes)
	mc_all = []
	for i in fdist_all_hashes.most_common(415): #415 chosen because closest cut off of hashes with at least 2 occurences
		mc_all.append(i)
		
	#pull the top 20 #happy and #sad hashtag distributions out of the total distribution list, make list
	happy_top20hash_totaldist = []
	sad_top20hash_totaldist = []
	for i in mc_all:
		if i[0] in h_just_hash:
			happy_top20hash_totaldist.append(i)
		if i[0] in s_just_hash:
			sad_top20hash_totaldist.append(i)
	
	#sort the lists alphabetically so that the values all line up so you can extract the frequency numbers
	sorted_mchappy = sorted(mc_happy, key=lambda tup: tup[0])
	sorted_mcsad = sorted(mc_sad, key=lambda tup: tup[0])
	sorted_happytop20hash_td = sorted(happy_top20hash_totaldist, key=lambda tup: tup[0])
	sorted_sadtop20hash_td = sorted(sad_top20hash_totaldist, key=lambda tup: tup[0])
	sorted_hjusthash = sorted(h_just_hash)
	sorted_sjusthash = sorted(s_just_hash)

	
	#extract the frequency numbers from the sorted lists, put in list
	happy_s_nums = []
	sad_s_nums = []
	happy_s_t20_nums = []
	sad_s_t20_nums = []
	for i in sorted_mchappy:
		happy_s_nums.append(i[1])
	for i in sorted_mcsad:
		sad_s_nums.append(i[1])
	for i in sorted_happytop20hash_td:
		happy_s_t20_nums.append(i[1])
	for i in sorted_sadtop20hash_td:
		sad_s_t20_nums.append(i[1])
	
	#get conditional proportions for each hash tag
	h1 = happy_s_nums[0] / happy_s_t20_nums[0]
	h2 = happy_s_nums[1] / happy_s_t20_nums[1]
	h3 = happy_s_nums[2] / happy_s_t20_nums[2]
	h4 = happy_s_nums[3] / happy_s_t20_nums[3]
	h5 = happy_s_nums[4] / happy_s_t20_nums[4]
	h6 = happy_s_nums[5] / happy_s_t20_nums[5]
	h7 = happy_s_nums[6] / happy_s_t20_nums[6]
	h8 = happy_s_nums[7] / happy_s_t20_nums[7]
	h9 = happy_s_nums[8] / happy_s_t20_nums[8]
	h10 = happy_s_nums[9] / happy_s_t20_nums[9]
	h11 = happy_s_nums[10] / happy_s_t20_nums[10]
	h12 = happy_s_nums[11] / happy_s_t20_nums[11]
	h13 = happy_s_nums[12] / happy_s_t20_nums[12]
	h14 = happy_s_nums[13] / happy_s_t20_nums[13]
	h15 = happy_s_nums[14] / happy_s_t20_nums[14]
	h16 = happy_s_nums[15] / happy_s_t20_nums[15]
	h17 = happy_s_nums[16] / happy_s_t20_nums[16]
	h18 = happy_s_nums[17] / happy_s_t20_nums[17]
	h19 = happy_s_nums[18] / happy_s_t20_nums[18]
	h20 = happy_s_nums[19] / happy_s_t20_nums[19]
	
	s1 = sad_s_nums[0] / sad_s_t20_nums[0]
	s2 = sad_s_nums[1] / sad_s_t20_nums[1]
	s3 = sad_s_nums[2] / sad_s_t20_nums[2]
	s4 = sad_s_nums[3] / sad_s_t20_nums[3]
	s5 = sad_s_nums[4] / sad_s_t20_nums[4]
	s6 = sad_s_nums[5] / sad_s_t20_nums[5]
	s7 = sad_s_nums[6] / sad_s_t20_nums[6]
	s8 = sad_s_nums[7] / sad_s_t20_nums[7]
	s9 = sad_s_nums[8] / sad_s_t20_nums[8]
	s10 = sad_s_nums[9] / sad_s_t20_nums[9]
	s11 = sad_s_nums[10] / sad_s_t20_nums[10]
	s12 = sad_s_nums[11] / sad_s_t20_nums[11]
	s13 = sad_s_nums[12] / sad_s_t20_nums[12]
	s14 = sad_s_nums[13] / sad_s_t20_nums[13]
	s15 = sad_s_nums[14] / sad_s_t20_nums[14]
	s16 = sad_s_nums[15] / sad_s_t20_nums[15]
	s17 = sad_s_nums[16] / sad_s_t20_nums[16]
	s18 = sad_s_nums[17] / sad_s_t20_nums[17]
	s19 = sad_s_nums[18] / sad_s_t20_nums[18]
	s20 = sad_s_nums[19] / sad_s_t20_nums[19]
	
	#make list of tuples, (#hashtag, conditional proportion)
	happy_ratios = [(sorted_hjusthash[0], h1), (sorted_hjusthash[1], h2), (sorted_hjusthash[2], h3), (sorted_hjusthash[3], h4),
		(sorted_hjusthash[4], h5), (sorted_hjusthash[5], h6), (sorted_hjusthash[6], h7), (sorted_hjusthash[7], h8),
		(sorted_hjusthash[8], h9), (sorted_hjusthash[9], h10), (sorted_hjusthash[10], h11), (sorted_hjusthash[11], h12),
		(sorted_hjusthash[12], h13), (sorted_hjusthash[13], h14), (sorted_hjusthash[14], h15), (sorted_hjusthash[15], h16),
		(sorted_hjusthash[16], h17), (sorted_hjusthash[17], h18), (sorted_hjusthash[18], h19), (sorted_hjusthash[19], h20)]
	
	sad_ratios = [(sorted_sjusthash[0], s1), (sorted_sjusthash[1], s2), (sorted_sjusthash[2], s3), (sorted_sjusthash[3], s4),
		(sorted_sjusthash[4], s5), (sorted_sjusthash[5], s6), (sorted_sjusthash[6], s7), (sorted_sjusthash[7], s8),
		(sorted_sjusthash[8], s9), (sorted_sjusthash[9], s10), (sorted_sjusthash[10], s11), (sorted_sjusthash[11], s12),
		(sorted_sjusthash[12], s13), (sorted_sjusthash[13], s14), (sorted_sjusthash[14], s15), (sorted_sjusthash[15], s16),
		(sorted_sjusthash[16], s17), (sorted_sjusthash[17], s18), (sorted_sjusthash[18], s19), (sorted_sjusthash[19], s20)]
	
	#sort hashtags by conditional propotions in descending order
	sorted_happy_ratios = sorted(happy_ratios, key=lambda tup: tup[1], reverse=True)
	sorted_sad_ratios = sorted(sad_ratios, key=lambda tup: tup[1], reverse=True)
	
	print("Conditional proportions of most common #happy hashtags:")
	print(sorted_happy_ratios)
	print("\n")
	print("Conditional proportions of most common #sad hashtags:")
	print(sorted_sad_ratios)
	print("\n")
	
	
	#Part 3, Part 4
	#Get non-hashtag words that co-occur with #happy or #sad	
	happywords = []
	for i in happytweetslist:
		match = re.search( r"@[\w_]+ | ([A-Z]\.)+ | [a-z][a-z'\-_]+[a-z]' | [\w_]+", i)
		if match:
			happywords.append(match.group())
			
	sadwords = []
	for i in sadtweetslist:
		match = re.search( r"@[\w_]+ | ([A-Z]\.)+ | [a-z][a-z'\-_]+[a-z]' | [\w_]+", i)
		if match:
			sadwords.append(match.group())
			
	#postag
	happy_pos_tag = nltk.pos_tag(happywords)
	sad_pos_tag = nltk.pos_tag(sadwords)
	#this tags basically everything as a noun, which makes the output super strange... possible
	#response to question 5

	#makes all of the elements in the happy_pos_tag list into a string joined by whitespace, because
	#the regex search requires a string to run
	string_hpt_list = []
	for i in happy_pos_tag:
		string_hpt = ' '.join(i)
		string_hpt_list.append(string_hpt)

	#run regex over the elements in string_hpt_list, pulls out elements tagged as nouns or verbs
	#and puts them in their respective lists
	happy_nouns = []	
	happy_verbs = []
	for i in string_hpt_list:
		pos_noun_match = re.search( r'NN', i)
		if pos_noun_match:
			happy_nouns.append(i)
		pos_verb_match = re.search( r'VB', i)
		if pos_verb_match:
			happy_verbs.append(i)
			
	string_spt_list = []
	for i in sad_pos_tag:
		string_spt = ' '.join(i)
		string_spt_list.append(string_spt)

	sad_nouns = []	
	sad_verbs = []
	for i in string_spt_list:
		pos_noun_match = re.search( r'NN', i)
		if pos_noun_match:
			sad_nouns.append(i)
		pos_verb_match = re.search( r'VB', i)
		if pos_verb_match:
			sad_verbs.append(i)
				
	#show #happy and #sad most common nouns
	fdist_happy_nouns = FreqDist(happy_nouns)
	print("Most common #happy nouns")
	print(fdist_happy_nouns.most_common(20))
	print("\n")
	fdist_sad_nouns = FreqDist(sad_nouns)
	print("Most common #sad nouns")
	print(fdist_sad_nouns.most_common(20))	
	print("\n")
	
	#show #happy and #sad most common verbs
	fdist_happy_verbs = FreqDist(happy_verbs)
	print("Most common #happy verbs")
	print(fdist_happy_verbs.most_common(20))
	print("\n")
	fdist_sad_verbs = FreqDist(sad_verbs)
	print("Most common #sad verbs")
	print(fdist_sad_verbs.most_common(20))	
	print("\n")
		
if __name__ == '__main__':
    main()