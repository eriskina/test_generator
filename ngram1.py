from random import uniform
from pymystem3 import Mystem

model = {
	('маша', 'сидят'): [('на', 1.0)],
	('$', 'леша'): [('и', 1.0)],
	('леша', 'и'): [('леша', 1.0)],
	('$', 'маша'): [('и', 1.0)],
	('лена', 'и'): [('маша', 0.5), ('лера', 0.2)],
	('леша', 'сидят'): [('на', 1.0)],
	('сидят', 'на'): [('стуле', 1.0)],
	('лера', 'и'): [('маша', 0.5), ('лена', 0.5)],
	('и', 'леша'): [('сидят', 1.0)],
	('стуле', '.'): [('$', 1.0)],
	('маша', 'и'): [('леша', 1.0)],
	('и', 'маша'): [('сидят', 1.0)],
	('$', 'лена'): [('и', 1.0)],
	('.', '$'): [('$', 1.0)],
	('и', 'лена'): [('сидят', 1.0)],
	('лена', 'сидят'): [('на', 1.0)],
	('$', '$'): [('лена', 0.2), ('лера', 0.4), ('леша', 0.2), ('маша', 0.2)],
	('$', 'лера'): [('и', 1.0)],
	('на', 'стуле'): [('.', 1.0)],
}

tokens = ['и', 'лена', 'лера', 'леша', 'маша', 'на', 'сидеть', 'стул']

meaning = [1, 2, 7]

ma = Mystem()

def compare(S1,S2):
	ngrams = [S1[i:i+3] for i in range(len(S1))]
	count = 0
	for ngram in ngrams:
		count += S2.count(ngram)

	return count/max(len(S1), len(S2))

def unirand(seq):
	sum_, freq_ = 0, 0
	for item, freq in seq:
		sum_ += freq
	rnd = uniform(0, sum_)
	for token, freq in seq:
		freq_ += freq
		if rnd < freq_:
			return token

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

def find_pair(t0, t1, t2):
	max = ('', 0)
	for t, p_n in [ _ for _ in get_from_model(t0, t1) ]:
		p_w = compare(t, t2)
		if p_w > 0.65:
			p = p_n * p_w
			if p > max[1]:
				max = (t, p)

	print('>>> t0 = %s, t1 = %s , t2 = %s , max = %s' % (t0, t1, t2, max) )
	try:
		assert max != ('', 0)
	except AssertionError:
		raise ValueError('Pair not found for word %s!' % t2)

	return max[0]

def sentence(meaning = meaning):
	t0, t1 = '$', '$'
	phrase = ''
	i = 0
	while 1:
		try:
			t0, t1 = t1, find_pair(t0, t1, tokens[meaning[i]])
			i += 1
		except (ValueError, IndexError):
			_ = get_from_model(t0, t1)
			t0, t1 = t1, unirand(_)
			try:
				if t1 == ma.analyze(t1)[0]['analysis'][0]['lex']:
					i += 1
			except (KeyError, IndexError):
				pass
		if t1 == '$': break
		if t1 in '.!?,;:' or t0 == '$':
			phrase += t1
		else:
			phrase += ' ' + t1
		print(phrase)

	return phrase
		# t0, t1 = '$', '$'
		# while 1:
		# 	t0, t1 = t1, unirand(model[t0, t1])
		# 	if t1 == '$': break
		# 	if t1 in ('.!?,;:') or t0 == '$':
		# 		phrase += t1
		# 	else:
		# 		phrase += ' ' + t1

print(sentence())
