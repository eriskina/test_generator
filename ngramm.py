from random import uniform

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

def get_from_model(model, t0, t1):
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

def find_pair(model, t0, t1, t2, used):
	max = ('', 0)
	for t, p_n in [ _ for _ in get_from_model(model, t0, t1) ]:
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

def ngramm_sentence(tokens, model, mystem):
	t0, t1 = '$', '$'
	used = []
	phrase = ''
	i = 0
	while 1:
		# print(i, tokens[meaning[i]])
		try:
			t0, t1 = t1, find_pair(model, t0, t1, tokens[i], used)
			i += 1
		except (ValueError, IndexError):
			_ = get_from_model(model, t0, t1)
			_t1 = t1
			try:
				__t1 = unirand(_, used)
				# print(__t1)
			except ValueError:
				__t1 = '$'
			t0, t1 = t1, __t1
			try:
				if t1 == mystem.analyze(_t1)[0]['analysis'][0]['lex']:
					i += 1
			except (KeyError, IndexError):
				pass
		if t1 == '$' or not t1: break
		if t1 in '.!?,;:' or t0 == '$':
			phrase += t1
		else:
			phrase += ' ' + t1
		used += [t1]

	return phrase


if __name__ == '__main__':
	from pymystem3 import Mystem
	from model_a import model
	ma = Mystem()

	tests = [['что', 'включать', 'двоичный', 'код'],
			 ['что', 'включать', 'блок-схема'],
			 ['что', 'такое', 'пролог'],
			 ['что', 'блок-схема', "программа"],
			 ["как", "сигнал", "величина"],
			 ['что', 'включать', 'непрерывный', 'физический', 'величина']]
	for test in tests:
		print(test, ngramm_sentence(test,model,ma))
