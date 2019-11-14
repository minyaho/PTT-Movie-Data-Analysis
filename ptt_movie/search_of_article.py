from .tendency import make_tendency_score
from ptt_movie.models import Article,Keyword
import datetime,time

def article_search(type,movie_name,arg=None):
	article_for_keyword = set()
					
	#第一階段搜尋: 只比對與電影關鍵字吻合的文章
	articles = article_search_type([type,movie_name,arg])
	for article in articles:
		temp = (article.title,article.author,article.time,article.url,article.push_message_all,article.push_message_good,article.push_message_bad,article.push_message_neutral)
		article_for_keyword.add(temp)
				
	#第二階段搜尋: 比對與電影關鍵字附屬關鍵字吻合的文章
	movie_keywords = Keyword.objects.get(movie=movie_name)
	if(len(movie_keywords.keyword.strip())>0):
		for movie_keyword in movie_keywords.keyword.split(' '):
			articles = article_search_type([type,movie_keyword,arg])
			for article in articles:
				temp = (article.title,article.author,article.time,article.url,article.push_message_all,article.push_message_good,article.push_message_bad,article.push_message_neutral)
				article_for_keyword.add(temp)

	#第三階段剃除: 除去內容相似的電影關鍵字資料
	similar_keywords = Keyword.objects.filter(movie__contains=movie_name)
	if(len(similar_keywords)!=0):
		for similar_keyword in similar_keywords:
			if(similar_keyword.movie!=movie_name):
				articles = article_search_type([type,similar_keyword.movie,arg])
				for article in articles:
					temp = (article.title,article.author,article.time,article.url,article.push_message_all,article.push_message_good,article.push_message_bad,article.push_message_neutral)
					#print(temp)
					article_for_keyword.discard(temp)
				#print(article_for_keyword)

				#第二階段搜尋: 比對與電影關鍵字附屬關鍵字吻合的文章
				if(len(similar_keyword.keyword.strip().split(' '))>0):
					for same_keyword in similar_keyword.keyword.strip().split(' '):
						if(len(same_keyword)>0):
							#print('@'+same_keyword+'@')
							articles = article_search_type([type,same_keyword,arg])
							for article in articles:
								temp = (article.title,article.author,article.time,article.url,article.push_message_all,article.push_message_good,article.push_message_bad,article.push_message_neutral)
								article_for_keyword.discard(temp)
				#print(article_for_keyword)

	#   產生討論數
	number_of_discussion = 0
	for article in article_for_keyword:
		number_of_discussion += article[4] 
					
	#   產生好評、負評、評比
	number_of_good = 0
	number_of_bad = 0
	ration_of_score = 0
	comment_good_bad = ''
	for item in article_for_keyword: 
		tag = item[0].split(']')[0].replace('[','').strip()
		emotion_score = make_tendency_score(tag)
		if(emotion_score == 1):
			#print('Good',item[0])
			number_of_good += item[5]
			number_of_bad += item[6]
		elif(emotion_score == -1):
			#print('Bad',item[0])
			number_of_bad += item[5]
			number_of_good += item[6]
		else:
			#print('Neutral',item[0])
			pass

		if(number_of_good+number_of_bad) < 10 :
			comment_good_bad = '資料不足'
		else:
			try:
				ration_of_score = (number_of_good/(number_of_good+number_of_bad))
				if(ration_of_score<=1) and (ration_of_score>=0.8):
					comment_good_bad = '極好評'
				if(ration_of_score<0.8) and (ration_of_score>=0.6):
					comment_good_bad = '好評'
				if(ration_of_score<0.6) and (ration_of_score>=0.4):
					comment_good_bad = '普評'
				if(ration_of_score<0.4) and (ration_of_score>=0.2):
					comment_good_bad = '壞評'
				if(ration_of_score<0.2) and (ration_of_score>=0):
					comment_good_bad = '極壞評'
			except:
				comment_good_bad = '資料不足'
					
	temp = {
		"a_movie": movie_name,
		"b_article": len(article_for_keyword),
		"c_discussion": number_of_discussion,
		"d_good": number_of_good,
		"e_bad": number_of_bad,
		"f_score": round(ration_of_score*100,1),
		"g_comment": comment_good_bad,
	}
	return temp


def article_search_type(args):	#[type,movie_name,arg]
	if(args[0] == 0): #all
		return Article.objects.filter(time__year=2019,title__icontains=args[1])
	if(args[0] == 1): #year_week
		return Article.objects.filter(time__year=2019,time__week=args[2],title__icontains=args[1])
	if(args[0] == 2): #year_month
		return Article.objects.filter(time__year=2019,time__month=args[2],title__icontains=args[1])
	if(args[0] == 3): #某天
		return Article.objects.filter(time__year=args[2][0],time__month=args[2][1],time__day=args[2][2],title__icontains=args[1]) #2:Start,3:end
	if(args[0] == 4): #時間範圍
		return Article.objects.filter(time__range=(args[2][0],args[2][1]) ,title__icontains=args[1]) #2:Start,3:end