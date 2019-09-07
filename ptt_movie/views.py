from django.shortcuts import render
from django.http import HttpResponse
from .tendency import make_tendency_score
import json

# Create your views here.
"""
def index(request):
	return render(request, 'index.html')
	
def add(request):
	a = request.GET['a']
	b = request.GET['b']
	a = int(a)
	b = int(b)
	return HttpResponse(str(a+b))
"""

from .forms import AddForm

def index(request):
	if request.method == 'POST':
		form = AddForm(request.POST)
	
		if form.is_valid():
			a = form.cleaned_data['a']
			b = form.cleaned_data['b']
			return HttpResponse(str(int(a)+int(b)))
	else:
		form = AddForm()
	return render(request,'index.html',{'form':form})	

from .forms import MoiveForm
from ptt_movie.models import Article,Keyword
import datetime,time

def analysis(request):
	if request.method == 'POST':
		form = MoiveForm(request.POST)
	
		if form.is_valid():
			movie_name = form.cleaned_data['movie_name']
			result = Article.objects.filter(title__contains=movie_name)
			if len(Keyword.objects.filter(movie=movie_name)) == 0:
				return HttpResponse(str('電影名稱錯誤'))
			else:
				result = list(result)
				
				article_for_keyword = set()
				
				#第一階段搜尋: 只比對與電影關鍵字吻合的文章
				articles = Article.objects.filter(title__contains=movie_name)
				for article in articles:
					temp = (article.title,article.author,article.time,article.url,article.push_message_all,article.push_message_good,article.push_message_bad,article.push_message_neutral)
					article_for_keyword.add(temp)
				
				#第二階段搜尋: 比對與電影關鍵字附屬關鍵字吻合的文章
				movie_keywords = Keyword.objects.get(movie=movie_name)
				if(len(movie_keywords.keyword.strip())>0):
					for movie_keyword in movie_keywords.keyword.split(' '):
						articles = Article.objects.filter(title__contains=movie_keyword)
						for article in articles:
							temp = (article.title,article.author,article.time,article.url,article.push_message_all,article.push_message_good,article.push_message_bad,article.push_message_neutral)
							article_for_keyword.add(temp)
				
				#第三階段剃除: 除去內容相似的電影關鍵字資料
				similar_keywords = Keyword.objects.filter(movie__contains=movie_name)
				if(len(similar_keywords)!=0):
					for similar_keyword in similar_keywords:
						if(similar_keyword.movie!=movie_name):
							#print(similar_keyword.movie)
							#print(movie_name)
							articles = Article.objects.filter(title__contains=similar_keyword.movie)
							for article in articles:
								temp = (article.title,article.author,article.time,article.url,article.push_message_all,article.push_message_good,article.push_message_bad,article.push_message_neutral)
								article_for_keyword.discard(temp)

							#第二階段搜尋: 比對與電影關鍵字附屬關鍵字吻合的文章
							if(len(similar_keyword.keyword.strip().split(' '))>0):
								for same_keyword in similar_keyword.keyword.strip().split(' '):
									#print(same_keyword)
									articles = Article.objects.filter(title__contains=same_keyword)
									for article in articles:
										temp = (article.title,article.author,article.time,article.url,article.push_message_all,article.push_message_good,article.push_message_bad,article.push_message_neutral)
										article_for_keyword.discard(temp)
							
				print(len(article_for_keyword))
				
				return render(request,'result.html',{'article_for_keyword':article_for_keyword,'movie_name':movie_name})
			
	else:
		form = MoiveForm()
	return render(request,'search.html',{'form':form})	


from .forms import MoiveTypeForm
def analysis_type(request):
	if request.method == 'POST':
		form = MoiveTypeForm(request.POST)
	
		if form.is_valid():
			type = form.cleaned_data['type']
			movie_name = form.cleaned_data['movie_name']
			if(type < 0 ) or (type > 1):
				return HttpResponse(str('type error'))
				
			result = Article.objects.filter(title__contains=movie_name)
			
			if len(Keyword.objects.filter(movie=movie_name)) == 0:
				return HttpResponse(str('電影名稱錯誤'))
				
			elif (type == 0):
			
				data = []
				
				for week in range(1,54):
					article_for_keyword = set()
					
					data.append(article_search(0,movie_name,week))
				
				add = 0
				for _data in data:
					add += _data['b_article']
				print(add)
				
				output_label = list()
				for i in range(1,54):
					output_label.append(i)
				
				discussion_data = list()
				for _data in data:
					discussion_data.append(_data['c_discussion'])
					
				good_data = list()
				for _data in data:
					good_data.append(_data['d_good'])
					
				bad_data = list()
				for _data in data:
					bad_data.append(_data['e_bad'])
				
				return render(request,'result2.html',{'data':data,'movie_name':movie_name,'output_label':json.dumps(output_label),'discussion_data':json.dumps(discussion_data),'good_data':json.dumps(good_data),'bad_data':json.dumps(bad_data)})	
				
			elif (type == 1):
			
				data = []
				
				for month in range(1,13):
					article_for_keyword = set()
					
					data.append(article_search(1,movie_name,month))
				
				
				output_label = list()
				for i in range(1,13):
					output_label.append(i)
					
				discussion_data = list()
				for _data in data:
					discussion_data.append(_data['c_discussion'])
					
				good_data = list()
				for _data in data:
					good_data.append(_data['d_good'])
					
				bad_data = list()
				for _data in data:
					bad_data.append(_data['e_bad'])
				
				return render(request,'result2.html',{'data':data,'movie_name':movie_name,'output_label':json.dumps(output_label),'discussion_data':json.dumps(discussion_data),'good_data':json.dumps(good_data),'bad_data':json.dumps(bad_data)})

			else:
			
				return HttpResponse(str(movie_name))
			
			
	else:
		form = MoiveTypeForm()
		
	return render(request,'search.html',{'form':form})

def article_search(type,movie_name,arg):
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
					article_for_keyword.discard(temp)

				#第二階段搜尋: 比對與電影關鍵字附屬關鍵字吻合的文章
				if(len(similar_keyword.keyword.strip().split(' '))>0):
					for same_keyword in similar_keyword.keyword.strip().split(' '):
						#print(same_keyword)
						articles = article_search_type([type,same_keyword,arg])
						for article in articles:
							temp = (article.title,article.author,article.time,article.url,article.push_message_all,article.push_message_good,article.push_message_bad,article.push_message_neutral)
							article_for_keyword.discard(temp)
					
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
		elif(emotion_score == -1):
			#print('Bad',item[0])
			number_of_bad += item[6]
		else:
			#print('Neutral',item[0])
			pass

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
		"f_score": ration_of_score,
		"g_comment": comment_good_bad,
	}
	return temp


def article_search_type(args):	#[type,movie_name,arg]
	if(args[0] == 0): #year_week
		return Article.objects.filter(time__year=2019,time__week=args[2],title__contains=args[1])
	if(args[0] == 1): #year_month
		return Article.objects.filter(time__year=2019,time__month=args[2],title__contains=args[1])