import sys
import csv
# import urllib2  # the lib that handles the url stuff
import random
import enchant


f = open('passwords.txt', 'r') 
tenK = [line.split() for line in f]
RY_FILENAME = 'rockyou-withcount.txt' #filename of the Rock You dataset

reverse_dictionary = {   
	'$': ['$', '3', '8', '5', 's'],
	'(': ['(', 'c'],
	'()': ['()', 'o'],
	'(|': ['(|', '4'],
	'(~': ['(~', 'g'],
	'*': ['*', 'x'],
	'-|': ['-|', 't'],
	'/\\|': ['/\\|', 'n'],
	'0': ['0', 'o'],
	'1': ['1', 'i', 'l'],
	'1)': ['1)', 'd'],
	'1_': ['1_', 'l'],
	'1t': ['1t', 'h'],
	'2': ['2', 'z'],
	'3': ['3', 'e'],
	'4': ['4', 'e'],
	'5': ['5', '$', 's'],
	'6': ['6', 'b', 'g', 'h'],
	'7': ['7', 't'],
	'8': ['8', '$', 's'],
	'9': ['9', 'g', 'q'],
	'><': ['><', 'x'],
	'@': ['@', 'a'],
	'A': ['A', '@', 'a'],
	'B': ['B', '6', 'b'],
	'C': ['C', 'c'],
	'D': ['D', 'd'],
	'E': ['E', '3', 'e'],
	'F': ['F', 'f'],
	'G': ['G', 'g'],
	'H': ['H', 'h'],
	'I': ['I', 'i'],
	'J': ['J', 'j'],
	'K': ['K', 'k', 'r'],
	'L': ['L', '1', 'l'],
	'M': ['M', 'm'],
	'N': ['N', 'n'],
	'O': ['O', '0', 'o'],
	'P': ['P', 'p'],
	'Q': ['Q', 'a', 'q'],
	'R': ['R', 'k', 'r'],
	'S': ['S', '5', '$', 's'],
	'T': ['T', '7', 't'],
	'U': ['U', 'u', 'v'],
	'V': ['V', 'v'],
	'VV': ['VV', 'w'],
	'W': ['W', 'w'],
	'X': ['X', 'x'],
	'Y': ['Y', 'y'],
	'Z': ['Z', '2', 'z'],
	'\\/': ['\\/', 'u', 'v'],
	'_1': ['_1', 'j'],
	'_i': ['_i', 'j'],
	'a': ['a', '@'],
	'b': ['b', '6', 'h'],
	'c1': ['c1', 'a'],
	'ci': ['ci', 'a'],
	'cj': ['cj', 'g'],
	'cl': ['cl', 'd'],
	'eight': ['eight', '8'],
	'five': ['five', '5'],
	'four': ['four', '4'],
	'g': ['g', 'q'],
	'h': ['h', 'b'],
	'i': ['i', 'l'],
	'it': ['it', 'h'],
	'l': ['l', '1', 'i'],
	'l_': ['l_', 'l'],
	'n': ['n', 'u'],
	'nine': ['nine', '9'],
	'nn': ['nn', 'm'],
	'o': ['o', '0', 'a'],
	'one': ['one', '1'],
	'oo': ['oo', '8'],
	'q': ['q', '9', 'g'],
	'rn': ['rn', 'm'],
	's': ['s', '5', '$'],
	'seven': ['seven', '7', '7'],
	'six': ['six', '6'],
	'three': ['three', '3'],
	'two': ['two', '2'],
	'u': ['u', 'v', 'y'],
	'v': ['v', 'u', 'y'],
	'vv': ['vv', 'w'],
	'z': ['z', '2'],
	'{': ['{', 'f'],
	'|': ['|', '1', 'l'],
	'|-|': ['|-|', 'h'],
	'|O': ['|O', 'p'],
	'|_': ['|_', 'l'],
	'|o': ['|o', '6'],
	'|v|': ['|v|', 'm'],
	'||': ['||', 'n']
}

def meaningfulword(sweetwords):
	meaningfulword_list = []
	for s in sweetwords:
		if wordBreak(s):
			meaningfulword_list.append(s)
	return meaningfulword_list

def wordBreak(s):
	"""
	:type s: str
	:type wordDict: Set[str]
	:rtype: bool
	"""
	d = enchant.Dict("en_US")
	meaningless = ['b', 'c', 'd', 'e', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x', 'y', 'z']
	ok = [True]
	for i in range(1, len(s)+1):
		ok += any(ok[j] and d.check(s[j:i]) and s[j:i] not in meaningless for j in range(i)),
	return ok[-1]


def readInRockYouTopN(desiredN):
# read in the RockYou Top 10,000 passwords
    top10000_dict = {}
    with open(RY_FILENAME, 'r', encoding='latin-1') as f1: 
        for line_number, line in enumerate(f1):
            if line_number >= desiredN: break
            try:
                (count,pw) = line.strip().split(None,1)
                top10000_dict[pw] = int(count)
            except:
                pass
    return top10000_dict

''' 
	We cannot find a exsting library to figure out if two words are 
	visually simiar, so we decided to use the same dictionary that we used 
	in hw3 to determine if letters are similar. For the purpose of this 
	assignment, we reversed the original dictionary from hw3. The values 
	from the original dictionary become key and the keys points to them become
	values.
'''

def is_similar_char(str1, str2):
	''' 
		This method takes in two substrings and determin if they are 
		visually similar
	'''
	str1 = str1.lower()
	str2 = str2.lower()
	if str1 not in reverse_dictionary and str2 not in reverse_dictionary:
		return str1 == str2
	if str1 not in reverse_dictionary:
		return str1 in reverse_dictionary[str2]
	if str2 not in reverse_dictionary:
		return str2 in reverse_dictionary[str1]
	
	similar_str1 = reverse_dictionary[str1]
	similar_str2 = reverse_dictionary[str2]
	
	# If two list have intersection, means two substrings are similar
	return not set(similar_str1).isdisjoint(similar_str2) or str1 == str2


def is_similar_word(str1, str2):
	'''
		This method takes in two sweetwords and determin if they
		are visually similar
	'''

	pointer_1 = len(str1)
	pointer_2 = len(str2)
	while (pointer_1 > 0 and pointer_2 > 0):
		isSimilar = False
		for i in xrange(pointer_1-1, -1, -1):
			for j in xrange(pointer_2-1, -1, -1):
				if is_similar_char(str1[i:pointer_1], str2[j:pointer_2]):
					isSimilar = True
					pointer_1 = i
					pointer_2 = j
					break
			if isSimilar:
				break

		if not isSimilar:
			return False
			
	return pointer_1 == 0 and pointer_2 == 0
	
'''
An example to use is_similar_word() method
str1 = "|-|e|10"
str2 = "hello"
print(is_similar_word(str1, str2)) => True
'''

def similar_set(sweetwords):
	'''
		Find the group of visually similar words in a list of sweetwords
		As long as there are two words look similar, we will return the two words in a list as a group. 
		Return null if none of them look similar
	'''
	group_similar = []

	for i in xrange(len(sweetwords)):
		for j in xrange(i+1, len(sweetwords)):
			if is_similar_word(sweetwords[i], sweetwords[j]):
				group_similar.append(sweetwords[j])
		if len(group_similar) != 0:
			group_similar.append(sweetwords[i])
			break
	return group_similar


'''
An example to use the similar_set() method

similar_list = similar_set(["password", "pa5$w()r1)", "pass", "pasSVVorcl"])
print(similar_list) => ['pa5$w()r1)', 'pasSVVorcl', 'password']
'''

def readInputFile(fileName):
	# take fileName as input
	# return a list of lists of lowercase sweetwords
	# need to import csv
	output = []

	with open(fileName) as csvfile:
		readCSV = csv.reader(csvfile, delimiter = ',')
		for line in readCSV:
			output.append([x.lower() for x in line])

	csvfile.close()
	return output

def elim_specialChars(inputSet):
	# take a list of sweetwords as input
	# return a list of sweetwords that contain only letters and numbers
	outputSet = []
	for sw in inputSet:
		if sw.isalnum():
			outputSet.append(sw)
	return outputSet

'''
# testing elim_specialChars()
fileName = 'out.txt'
inputSets = readInputFile(fileName)
for inputSet in inputSets:
	print(inputSet)
	print(elim_specialChars(inputSet))
'''


def find_repeat_sweetwords (sweetwords_list):
# find any repeat sweetwords in the inputfile. They should be considered honeywords.
    # get list of sweetwords
    all_sweetwords_list = sweetwords_list
    
    # get list of repeat words
    seen_words = set()
    repeat_words = set()
    for word in all_sweetwords_list:
        if word not in seen_words:
            seen_words.add(word)
        else:
            repeat_words.add(word)
    return repeat_words

def eliminate_repeated_sweetwords (curr_sweetword_set, sweetwords_list):
# eliminate sweetwords from the list that are likely honeywords (because they are repeated in the sweetword input file)
    likely_honeywords = find_repeat_sweetwords(sweetwords_list)
    curr_sweetword_set = [word for word in curr_sweetword_set if word not in likely_honeywords]
    return curr_sweetword_set
	
def find_max_RockYou (curr_sweetword_set, RockYou_dict_with_freqs):
# find the word in the current list that appears most in the Rock You dataset
    # subset of the rock you dict that only contains the current sweetwords set
    sub_dict = {k:RockYou_dict_with_freqs[k] for k in curr_sweetword_set if k in RockYou_dict_with_freqs}
    
    maxFreqWord = max(sub_dict, key=sub_dict.get)
    # choose the word with maximum frequency from the rock you frequencies
    return maxFreqWord
'''
EXAMPLE USAGES:
[In] freq_SW_eliminate (['sw1','sw2','asdlkj'], ['asdlkj','sw1','sw2','sw2','sw1'])
[Out] ['asdlkj']

[In] find_max_RockYou (['first','second','something'], {'first':1,'second':5, 'fourth':2, 'third':2})
[Out] 'second'
'''

def num_words_in_10k(n_set, db):
	count = 0
	for word in n_set:
		if word in db:
			count +=1
	return count

def word_from_db (n_set, db):
	local_set = n_set.copy()
	for i in len(local_set):
		if local_set[i] in db:
			return i

def word_from_db_single (n_set, db):
	local_set = n_set.copy()
	for i in len(local_set):
		if local_set[i] not in db:
			return i

def eliminate_not_in_tenk_subset (miniset, db):
	return_set = []
	for word in miniset:
		if word in db:
			return_set.append (word)
	return return_set

def corner_cases (miniset):
	miniset = elim_specialChars(miniset)
	miniset = meaningfulword(miniset)
	return miniset


def main(m,n,fromFile):


	
	Top_million_dict = readInRockYouTopN(1000000) # we can't possibly look at all the possible passwords...
	return_list = []
	# iterate through the list (which contains m sets of sweetwords)
	for i in range (0,m): 

		n_set = data_as_list[i] # data_as_list is a global var from main()
		words_in_10k = num_words_in_10k(n_set,tenK)
		
		# if only one word in top 10K => return word
		if words_in_10k == 1: 
			return_list.append( word_from_db (n_set,tenK))
		# if only 1 word not in top 10K => return word
		elif words_in_10k == n-1: 
			return_list.append(word_from_db_single (n_set,tenK))
		# if exactly 0 words are in top 10K => corner_cases (set), assuming that corner_cases only returns one word's index
		elif words_in_10k ==0:
			local_set = corner_cases(n_set)
			idx = data_as_list[i].index(random.choice(local_set))
			return_list.append( idx)
		# if 1 < #words_in_10K < n-1 then do work
		else: 
			n_set = eliminate_not_in_tenk_subset(n_set, tenK) #Roy
			n_set = eliminate_repeated_sweetwords (n_set) #Neel

			while len(n_set) > 1:
				if similar_set(n_set): #Yating
					return find_max_rockYou(n_set, Top_million_dict) #Neel
				else:
					n_set = corner_cases(n_set)

			idx = data_as_list[i].index(random.choice(n_set)) #get the index of a random element from the original row
			print(idx)
			return_list.append (idx)

	with open("selected_passwords.txt",'w') as resultFile:
	    wr = csv.writer(resultFile)
	    wr.writerow(return_list)




if  __name__ =='__main__':	
	m = int(sys.argv[1]) # number of sets of sweetwords
	n = int(sys.argv[2]) # number of sweetwords per set
	with open(sys.argv[3], 'r') as f:
		reader = csv.reader(f)
		data_as_list = list(reader)
	main (m,n,data_as_list)