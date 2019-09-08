from django.shortcuts import render
from django.http import HttpResponse
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
	return render(request,'ptt_movie/index.html',{'form':form})	
"""
from ptt_movie.models import Keyword
def index(request):
	keywords = Keyword.objects.all()
	return render(request,'ptt_movie/index.html', locals())
	

from .forms import MoiveForm
from ptt_movie.models import Article,Keyword
from .tendency import make_tendency_score
from dateutil.relativedelta import relativedelta
import datetime,time

def keyword(request,key):
	keyword_result = Keyword.objects.filter(movie = key)
	if len(keyword_result) != 0:
		movie_name = key
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
						
		data = {
			"a_movie": movie_name,
			"b_article": len(article_for_keyword),
			"c_discussion": number_of_discussion,
			"d_good": number_of_good,
			"e_bad": number_of_bad,
			"f_score": ration_of_score,
			"g_comment": comment_good_bad,
		}
		
		#近7天
		end_date = datetime.datetime.today().date()
		start_date = end_date - relativedelta(days=7)
		
		label_of_7_days = list()
		for i in range(1,8):
			label_of_7_days.append((start_date + relativedelta(days=i)).strftime('%m-%d'))
		label_of_7_days = json.dumps(label_of_7_days)
		
		data_of_7_days = []
			
		for day in range(1,8):
			data_of_7_days.append(article_search(3,movie_name,[int((start_date + relativedelta(days=i)).strftime('%m')),int((start_date + relativedelta(days=day)).strftime('%d'))]))

		article_of_7_days = list()
		for _data in data_of_7_days:
			article_of_7_days.append(_data['b_article'])
		article_of_7_days = json.dumps(article_of_7_days)

		discussion_of_7_days = list()
		for _data in data_of_7_days:
			discussion_of_7_days.append(_data['c_discussion'])
		discussion_of_7_days = json.dumps(discussion_of_7_days)
		
		good_of_7_days = list()
		for _data in data_of_7_days:
			good_of_7_days.append(_data['d_good'])
		good_of_7_days = json.dumps(good_of_7_days)		
				
		bad_of_7_days = list()
		for _data in data_of_7_days:
			bad_of_7_days.append(_data['e_bad'])
		bad_of_7_days = json.dumps(bad_of_7_days)	
		
		
		#近5周
		end_date = datetime.datetime.today().date()
		start_date = end_date - relativedelta(days=7*5)
		
		label_of_5_weeks = list()
		for i in range(1,6):
			label_of_5_weeks.append(start_date.strftime('%m-%d') + ' ~ ' +(start_date + relativedelta(days=7)).strftime('%m-%d'))
			start_date = start_date + relativedelta(days=7)
		label_of_5_weeks = json.dumps(label_of_5_weeks)
		
		data_of_5_weeks = []
		start_date = end_date - relativedelta(days=7*5)
		for week in range(1,6):
			data_of_5_weeks.append(article_search(4,movie_name,[start_date, start_date + relativedelta(days=7)]))
			start_date = start_date + relativedelta(days=7)

		article_of_5_weeks = list()
		for _data in data_of_5_weeks:
			article_of_5_weeks.append(_data['b_article'])
		article_of_5_weeks = json.dumps(article_of_5_weeks)

		discussion_of_5_weeks = list()
		for _data in data_of_5_weeks:
			discussion_of_5_weeks.append(_data['c_discussion'])
		discussion_of_5_weeks = json.dumps(discussion_of_5_weeks)
		
		good_of_5_weeks = list()
		for _data in data_of_5_weeks:
			good_of_5_weeks.append(_data['d_good'])
		good_of_5_weeks = json.dumps(good_of_5_weeks)		
				
		bad_of_5_weeks = list()
		for _data in data_of_5_weeks:
			bad_of_5_weeks.append(_data['e_bad'])
		bad_of_5_weeks = json.dumps(bad_of_5_weeks)	

				
		return render(request,'ptt_movie/keyword.html',locals())
	else:
		return HttpResponse(str('電影名稱錯誤'))

def week(request,key):

	keyword_result = Keyword.objects.filter(movie = key)
	
	if len(keyword_result) != 0:
	
		movie_name = key
		data = []
				
		for week in range(1,54):
					
			data.append(article_search(1,movie_name,week))
				
		output_label = list()
		for i in range(1,54):
			output_label.append(i)
		output_label = json.dumps(output_label)
		
		article_data = list()
		for _data in data:
			article_data.append(_data['b_article'])
		article_data = json.dumps(article_data)
				
		discussion_data = list()
		for _data in data:
			discussion_data.append(_data['c_discussion'])
		discussion_data = json.dumps(discussion_data)		
		
		good_data = list()
		for _data in data:
			good_data.append(_data['d_good'])
		good_data = json.dumps(good_data)
					
		bad_data = list()
		for _data in data:
			bad_data.append(_data['e_bad'])
		bad_data = json.dumps(bad_data)
		
		return render(request,'ptt_movie/result2.html',locals())
	else:
		return HttpResponse(str('電影名稱錯誤'))
		
		
def month(request,key):

	keyword_result = Keyword.objects.filter(movie = key)
	
	if len(keyword_result) != 0:
	
		movie_name = key
		data = []
				
		for month in range(1,13):
					
			data.append(article_search(2,movie_name,month))
				
		output_label = list()
		for i in range(1,13):
			output_label.append(i)
		output_label = json.dumps(output_label)
		
		article_data = list()
		for _data in data:
			article_data.append(_data['b_article'])
		article_data = json.dumps(article_data)
				
		discussion_data = list()
		for _data in data:
			discussion_data.append(_data['c_discussion'])
		discussion_data = json.dumps(discussion_data)		
		
		good_data = list()
		for _data in data:
			good_data.append(_data['d_good'])
		good_data = json.dumps(good_data)
					
		bad_data = list()
		for _data in data:
			bad_data.append(_data['e_bad'])
		bad_data = json.dumps(bad_data)
		
		return render(request,'ptt_movie/result2.html',locals())
	else:
		return HttpResponse(str('電影名稱錯誤'))

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
				
				return render(request,'ptt_movie/result.html',{'article_for_keyword':article_for_keyword,'movie_name':movie_name})
			
	else:
		form = MoiveForm()
	return render(request,'ptt_movie/search.html',{'form':form})	


from .forms import MoiveTypeForm
from .search_of_article import article_search
def analysis_type(request):
	if request.method == 'POST':
		form = MoiveTypeForm(request.POST)
	
		if form.is_valid():
			type = form.cleaned_data['type']
			movie_name = form.cleaned_data['movie_name']
			if(type < 1 ) or (type > 2):
				return HttpResponse(str('type error'))
				
			result = Article.objects.filter(title__contains=movie_name)
			
			if len(Keyword.objects.filter(movie=movie_name)) == 0:
				return HttpResponse(str('電影名稱錯誤'))
				
			elif (type == 1):
			
				data = []
				
				for week in range(1,54):
					
					data.append(article_search(type,movie_name,week))
				
				add = 0
				for _data in data:
					add += _data['b_article']
				print(add)
				
				output_label = list()
				for i in range(1,54):
					output_label.append(i)
				
				article_data = list()
				for _data in data:
					article_data.append(_data['b_article'])
				article_data = json.dumps(article_data)
						
				discussion_data = list()
				for _data in data:
					discussion_data.append(_data['c_discussion'])
				discussion_data = json.dumps(discussion_data)		
				
				good_data = list()
				for _data in data:
					good_data.append(_data['d_good'])
				good_data = json.dumps(good_data)
							
				bad_data = list()
				for _data in data:
					bad_data.append(_data['e_bad'])
				bad_data = json.dumps(bad_data)
				
				return render(request,'ptt_movie/result2.html',locals())	
				
			elif (type == 2):
			
				data = []
				
				for month in range(1,13):
					
					data.append(article_search(type,movie_name,month))
				
				
				output_label = list()
				for i in range(1,13):
					output_label.append(i)
					
				article_data = list()
				for _data in data:
					article_data.append(_data['b_article'])
				article_data = json.dumps(article_data)
						
				discussion_data = list()
				for _data in data:
					discussion_data.append(_data['c_discussion'])
				discussion_data = json.dumps(discussion_data)		
				
				good_data = list()
				for _data in data:
					good_data.append(_data['d_good'])
				good_data = json.dumps(good_data)
							
				bad_data = list()
				for _data in data:
					bad_data.append(_data['e_bad'])
				bad_data = json.dumps(bad_data)
				
				return render(request,'ptt_movie/result2.html',locals())	
			else:
			
				return HttpResponse(str(movie_name))
			
			
	else:
		form = MoiveTypeForm()
		
	return render(request,'ptt_movie/search.html',{'form':form})