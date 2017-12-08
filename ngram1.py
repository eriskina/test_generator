from random import uniform
from pymystem3 import Mystem

# import pickle
# pickle.dump(model, open('model-a','wb'))
# model = pickle.load(open('model-a','rb'))

from model_a import model

ma = Mystem()

def compare(S1,S2):
	ngrams = [S1[i:i+3] for i in range(len(S1))]
	count = 0
	for ngram in ngrams:
		count += S2.count(ngram)

	return count/max(len(S1), len(S2))

def unirand(seq, used):
	rez, sum_, freq_ = None, 0, 0
	for item, freq in seq:
		sum_ += freq
	rnd = uniform(0, sum_)
	for token, freq in seq:
		if token not in used: freq_ += freq
		else: freq_ += freq / 2
		if rnd < freq_:
			rez = token

	try:
		assert rez != None
		return rez
	except AssertionError:
		raise ValueError("Nothing found for %s" % seq)

def get_from_model(t0, t1):
	try:
		rez = model[(t0, t1)]
	except KeyError:
		rez = []
		max = 0
		for _t0, _t1 in model.keys():
			p0, p1 = compare(_t0, t0), compare(_t1, t1)
			p = p0 * p1
			if p > max:
				rez += model[(_t0, _t1)]

	# print(rez)
	return rez

def find_pair(t0, t1, t2, used):
	max = ('', 0)
	for t, p_n in [ _ for _ in get_from_model(t0, t1) ]:
		p_w = compare(t, t2)
		if t in used: p_w /= 2
		if p_w > 0.62:
			p = p_n * p_w
			if p > max[1]:
				max = (t, p)

	# print('>>> t0 = %s, t1 = %s , t2 = %s , max = %s' % (t0, t1, t2, max) )
	try:
		assert max != ('', 0)
	except AssertionError:
		# print(compare("включает", "включать"))
		raise ValueError('Pair not found for word %s!' % t2)

	return max[0]

def sentence(meaning):
	t0, t1 = '$', '$'
	used = []
	phrase = ''
	i = 0
	while 1:
		# print(i, tokens[meaning[i]])
		try:
			t0, t1 = t1, find_pair(t0, t1, tokens[meaning[i]], used)
			i += 1
		except (ValueError, IndexError):
			_ = get_from_model(t0, t1)
			_t1 = t1
			try:
				__t1 = unirand(_, used)
				# print(__t1)
			except ValueError:
				__t1 = '$'
			t0, t1 = t1, __t1
			try:
				if t1 == ma.analyze(_t1)[0]['analysis'][0]['lex']:
					i += 1
			except (KeyError, IndexError):
				pass
		if t1 == '$' or not t1 or len(used) > len(meaning): break
		if t1 in '.!?,;:' or t0 == '$':
			phrase += t1
		else:
			phrase += ' ' + t1
		used += [t1]

	return phrase

tokens = ["что",
		  "сигнал",
		  "двоичный",
		  "код",
		  "блок-схема",
		  "псевдокод",
		  "программный",
		  "форма",
		  "информационный",
		  "ресурс",
		  "текстуальный",
		  "пролог",
		  "включать",
		  "в",
		  "себя",
		  "язык",
		  "как"]

# meaning = [0,12,13,14,1,2]
# print([tokens[i] for i in meaning], sentence(meaning))
# meaning = [0,12,13,14,4,5]
# print([tokens[i] for i in meaning], sentence(meaning))
# meaning = [0,12,13,14,10,11]
# print([tokens[i] for i in meaning], sentence(meaning))
# meaning = [0,12,13,14,8,9]
# print([tokens[i] for i in meaning], sentence(meaning))
meaning = [0,12,13,14,6,7]
print([tokens[i] for i in meaning], sentence(meaning))
meaning = [0,12,13,14,11,16,15]
print([tokens[i] for i in meaning], sentence(meaning))
meaning = [0,12,11,16,15]
print([tokens[i] for i in meaning], sentence(meaning))
