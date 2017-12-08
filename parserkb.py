from json import dump, dumps
from re import findall, match
from random import randint
from pymystem3 import Mystem
from ngramm import ngramm_sentence

ma = Mystem()

def load_kb(filename = "kb.txt"):
	res = {}
	for str in open("kb.txt").readlines():
		try:
			a, b, c = findall(r'.*?"(.*?)".*?"(.*?)".*?"(.*?)".*', str.lower())[0]
			res.update({(a,c,b):1})
		except ValueError:
			pass
		except TypeError:
			pass
		except IndexError:
			pass
	return res

def generate_questions(kb = {}, number = 10):
	def tokenize(phraze = 'программная форма'):
		rez = []
		for a in ma.analyze(phraze):
			try:
				rez += [a['analysis'][0]['lex']]
			except (KeyError, IndexError):
				pass
		return rez

	def what_includes(text, den1, rel, den2):
		def generate_answers(den1, rel, den2, n_incorrect = 3, n_correct = 1):
			var = 'а'
			res = {}
			keys_to_delete = []
			for i in range(n_correct):
				correct = []
				for d1, r, d2 in kb.keys():
					if d1 == den1 and r == rel and kb[(d1, r, d2)]:
						correct += [d2]
						keys_to_delete += [(d1, r, d2)]
				res.update({var:{"is_correct":1, "text": ', '.join(correct)}})
				var = chr(ord(var)+1)

			incorrect = []
			need_to_generate = randint(2,4)
			for d1, r, d2 in kb.keys():
				if d1 != den1 and r == rel and kb[(d1, r, d2)]:
					incorrect += [d2]
					# keys_to_delete += [(d1, r, d2)]
					if need_to_generate:
						res.update({var:{"is_correct":0, "text": ', '.join(incorrect)}})
						var = chr(ord(var)+1)
						incorrect = []
						need_to_generate -= 1

			for key in set(keys_to_delete):
				kb[key] = 0
			return res

		def generate_question(den, template):
			denotats = [den]
			for den1, rel, den2 in kb.keys():
				if den2 == den and rel in ["представлять собой", "cостоять из"] and kb[(den1, rel, den2)]:
					denotats += [den1]
					break

			rez, j = [], 0
			for i in range(len(template)):
				if template[i] == "[D]":
					try:
						rez += tokenize(denotats[j])
						j += 1
					except IndexError:
						pass
				else:
					rez += [template[i]]
			return rez

		q = ngramm_sentence(generate_question(den1, templ_key))
		answers = generate_answers(den1, rel, den2)
		return {"%s) %s" % (i, q):answers}

	question_templates = {
		"%s это:" : (""),
		("что", "включать", "[D]", "[D]") : {
			"function" : what_includes,
			"relations" : (r"представлять собой", "cостоять из"),
			"weight": 1,
		},
		"%s состоит из" : 1,
		"%s определяется как" : 1,
	}
	res = {}
	i = 0
	# templ_key = "Что включает в себя %s, как элемент %s" # question_templates.keys[0]
	templ_key = ("что", "включать", "[D]", "[D]")
	templ_relation_re = question_templates[templ_key]["relations"][0]
	for den1, rel, den2 in kb.keys():
		if match(templ_relation_re, rel) and kb[(den1, rel, den2)]:
			# print(den1, rel, templ_relation_re, den2)
			i += 1
			_ = question_templates[templ_key]["function"](templ_key, den1, rel, den2)
			res.update(_)
			print(_)
			if i > number:
				break
	return res

if __name__ == '__main__':
	kb = load_kb("kb.txt")
	q = generate_questions(kb, 110)
	# print(q)
	dump(q, open('q.json', 'w'), ensure_ascii = 0, indent = 4)
	# print(dumps(q, ensure_ascii = 0, indent = 4))
