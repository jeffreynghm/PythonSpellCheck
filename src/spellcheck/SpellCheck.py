"""
Requires re, collections, os.path

_edits1 code credit goes to Peter Norvig
http://norvig.com/spell-correct.html
"""
import re, collections, string, pickle

def unserialize(pathToFile):
	f = open(pathToFile, 'rb');
	_temp = pickle.load(f); 	
	f.close();
	return _temp;


class SpellCheck:
	#Can't serialize a lambda function
	def _fn(self):
		return 1;

	def __init__(self):
		self._model = collections.defaultdict(self._fn);
		self.wordCount = 0; #counts the number of words in dictionary
		self.size = 0; #counts the total weights of words recorded
		self.ALPHABET = 'abcdefghijklmnopqrstuvwxyz';
		self._name = "";

	def __str__(self):
		return "SpellCheck{0}, wordCount: {1}, size: {2}".format(self._name, self.wordCount, self.size);

	#Sets an identifier/descriptor
	def setName(self, name):
		self._name = " "+name;

	#takes a string, identifies valid words
	def trainText(self, text):
		individualWords = text.lower().split();
		for word in individualWords:
			self._train(word, 1);

	#Imports a dictionary K-V file
	def importWeights(self, filepath):
		pathToDict = filepath;
		f = open(pathToDict, "r");
		for line in f:
			x = line.split();
			self._train(x[1].lower(), int(float(x[0])));
		f.close();

	def exportWeights(self, filepath):
		f = open(filepath, 'w');
		for k in self._model.keys():
			f.write("{0} {1}\n".format(self._model[k],k));
		f.close();


	#Returns the weights of word occuring in model
	def getWeight(self, word):
		weight = self._model[word.lower()];

		return weight-1;

	def _known(self, words): 
		return set(w for w in words if w in self._model);

	#Trains the model by introducing the string
	#in the text to collection
	def _train(self, word, count):
		validWord = True;
		for char in word:
			if(not(char in string.ascii_lowercase)):
				validWord = False;
				break;
		if(validWord):		
			if(self._model[word] == 1):
				self.wordCount += 1;
			self._model[word] += count;
			self.size += int(count);

	#Finds all words that are 1 edit distance away
	def _edits1(self, word):
		splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
		deletes    = [a + b[1:] for a, b in splits if b]
		transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
		replaces   = [a + c + b[1:] for a, b in splits for c in self.ALPHABET if b]
		inserts    = [a + c + b     for a, b in splits for c in self.ALPHABET]
		return set(deletes + transposes + replaces + inserts)

	#Override this method to change how to determine correct words.
	#Options: Change order of word so it accounts sentence structure
	# via some NLP software
	#Options: Give more value to words that have been encountered more
	# frequently
	def correct(self, word):
	    candidates = self._known([word]) or self._known(self._edits1(word)) or [word]
	    return list(reversed(sorted(candidates, key=self._model.get)))

	def serialize(self, filePath):
		try:
			f = open(filePath, 'wb');
			pickle.dump(self, f);
		except Exception as e:
			print("Error trying to pickle. Check args")
			raise e;
		finally:
			f.close();
		



