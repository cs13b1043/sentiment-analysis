from nltk.corpus import wordnet

synonyms = []
antonyms = []

for syn in wordnet.synsets("commercial"):
    for l in syn.lemmas():
        synonyms.append(l.name())
        if l.antonyms():
            antonyms.append(l.antonyms()[0].name())

print(synonyms)
print(set(antonyms))
