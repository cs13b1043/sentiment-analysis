from nltk.corpus import wordnet

def syns(E):
	synonyms = []
	synonyms.append(E)
	for syn in wordnet.synsets(E):
    		for l in syn.lemmas():
        		synonyms.append(l.name())
	return set(synonyms)

def ants(E):
	antonyms = []
	for syn in wordnet.synsets(E):
    		for l in syn.lemmas():
        		if l.antonyms():
            			antonyms.append(l.antonyms()[0].name())
	return set(antonyms)


def count(E, filenames):
	count =0
	for filename in filenames:
		f  = open(filename, 'r').read().lower().decode('utf-8')
		for syn in syns(E):
			count = count+f.count(syn)

	return count

def count_both(F,C, filenames):
	count =0
	for filename in filenames:
		lst  = open(filename, 'r').readlines()
		for syn_F in syns(F):
			for syn_C in syns(C):
				for line in lst:
					line = line.decode('utf-8')
					line_lst = line.split('.')
					for sentence in line_lst:
						if syn_F in sentence.lower() and syn_C in sentence.lower():
							count=count+1
	return count
	

def OSA(C, F, filenames):
	
	Pr_FC = count_both(F,C, filenames)
	Pr_F = count(F, filenames)
	Pr_C = count(C, filenames)
	
		
	if Pr_F==0 or Pr_C==0:
		return 0	
	return (Pr_FC * Pr_FC) /float(Pr_F * Pr_F * Pr_C) 
