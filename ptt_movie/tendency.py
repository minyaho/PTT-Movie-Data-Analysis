#tendency(傾向)判定演算法

#好壞普評判斷字典
emotional_words = {"good":["好","神","淚","感動","哭","有趣","爽","不錯","OK"],"bad":["壞","糞","爛","負","圾","-","噁"],"neutral":["平"]}

#好壞普評判斷(輸入句子，輸出分數)
def make_tendency_score(sentiences):
	score = 0	#1:good, 0:bad, -1:neutral
	for keyword in emotional_words['good']:
		if keyword in sentiences:
			score = 1
	for keyword in emotional_words['bad']:
		if keyword in sentiences:
			score = -1
	return score