import aheui
import random

TRIALS = 10000
# TRIALS = 100000000
MAX_STEPS = 50

if __name__ == '__main__':

	start, stop = ord(u'가'), ord(u'힣') + 1
	hangul = [chr(i) for i in range(start, stop)]

	start, stop = ord(u'하'), ord(u'힣') + 1
	halt_jamo = [chr(i) for i in range(start, stop)]

	count = 0

	for _ in range(TRIALS):
		w = [random.choice(hangul) for _ in range(3)] + [random.choice(halt_jamo)]
		random.shuffle(w)
		idiom = ''.join(w)

		res = aheui.eval(idiom, max_steps = MAX_STEPS)

		count += 1 if res else 0

	print(count*1.0/TRIALS)

	