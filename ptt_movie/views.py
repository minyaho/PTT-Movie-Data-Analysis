from django.shortcuts import render
from django.http import HttpResponse
from dateutil.relativedelta import relativedelta
from ptt_movie.models import Keyword_Analysis_This_Month, Keyword_Analysis_Last_Month, Keyword_Analysis_Last_Week, Keyword_Analysis_This_Week
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
from .search_of_article import article_search
from ptt_movie.models import Keyword_Analysis,Keyword
from django.db.models import Sum
def index(request):
	
	#今日
	today = datetime.datetime.today().date()
	
	#今日討論電影關鍵字
	todays_keywords = set()
	
	#所有關鍵字
	keywords = Keyword.objects.all()
	keyword_len = len(keywords)
	discussion_len = Article.objects.aggregate(Sum('push_message_all'))['push_message_all__sum']
	article_len = Article.objects.count()
	
	#近一周整體討論量
	#Article.objects.filter(time__year=today.strftime('%Y'),time__month=today.strftime('%m'),time__day=today.strftime('%d'))
	start_date = today - relativedelta(days=7)
	label_of_7_days = list()
	for i in range(1,8):
		label_of_7_days.append((start_date + relativedelta(days=i)).strftime('%m-%d'))
	label_of_7_days = json.dumps(label_of_7_days)
	
	discussion_tihs_week_datas = list()
	for i in range(1,8):
		discussion_tihs_week_datas.append(Article.objects.filter(time__year=start_date.strftime('%Y'),time__month=start_date.strftime('%m'),time__day=(start_date+relativedelta(days=i)).strftime('%d')).aggregate(Sum('push_message_all'))['push_message_all__sum'])
	discussion_tihs_week_datas = json.dumps(discussion_tihs_week_datas)
	
	#近一周討論比例(最多六筆)	
	datas = Keyword_Analysis_This_Week.objects.all().order_by("-discussion")[:6]
	if(len(datas)>0):
		keyword_analysis_of_this_week = []
		for data in datas:
			temp = {
				"a_movie": data.name,
				"b_article": data.article,
				"c_discussion": data.discussion,
				"d_good": data.good,
				"e_bad": data.bad,
				"f_score": data.score,
				"g_comment": data.comment,
			}
			keyword_analysis_of_this_week.append(temp)
		
		keyword_discussion_of_this_week = list()
		keyword_label_of_this_week = list()
		for i in range(len(keyword_analysis_of_this_week)):
			if(i%6==0):
				keyword_analysis_of_this_week[i].update({'h_color':'text-primary'})
			elif(i%6==1):
				keyword_analysis_of_this_week[i].update({'h_color':'text-danger'})
			elif(i%6==2):
				keyword_analysis_of_this_week[i].update({'h_color':'text-info'})
			elif(i%6==3):
				keyword_analysis_of_this_week[i].update({'h_color':'text-warning'})
			elif(i%6==4):
				keyword_analysis_of_this_week[i].update({'h_color':'text-muted'})
			elif(i%6==5):
				keyword_analysis_of_this_week[i].update({'h_color':'text-success'})
			keyword_discussion_of_this_week.append(keyword_analysis_of_this_week[i]['c_discussion'])
			keyword_label_of_this_week.append(keyword_analysis_of_this_week[i]['a_movie'])
			#print(keyword_analysis_of_this_week[i])
		#print(keyword_discussion_of_this_week)
		keyword_discussion_of_this_week = json.dumps(keyword_discussion_of_this_week)
		keyword_label_of_this_week = json.dumps(keyword_label_of_this_week,ensure_ascii=False)
	
	#今日文章
	article_today = Article.objects.filter(time__year=today.strftime('%Y'),time__month=today.strftime('%m'),time__day=today.strftime('%d'))
	
	"""
	尋找今日電影關鍵字的快速做法
	
	"""
	article_str = ''
	
	for _article_today in article_today:
		article_str += _article_today.title + ' '
	article_str = article_str.strip()
	
	for _keyword in keywords:
		
		if(_keyword.movie in article_str):
			todays_keywords.add(_keyword.movie)
			
		for same_keyword in _keyword.keyword.strip().split(' '):
			if(same_keyword.strip()!='') and (same_keyword.strip() in article_str):
				todays_keywords.add(_keyword.movie)

	#今日熱門關鍵字
	data_of_today_keyword = list()
	if(len(todays_keywords)>0):
		for todays_keyword in todays_keywords:
			data_of_today_keyword.append(article_search(3,todays_keyword,[2019,int(today.strftime('%m')),int(today.strftime('%d'))]))
		data_of_today_keyword.sort(key=lambda k: k['c_discussion'],reverse=True)

		keyword_today_hot = data_of_today_keyword[0]
		keyword_today_hot_all_data = article_search(0,data_of_today_keyword[0]['a_movie'])
		
		start_date = today - relativedelta(days=7)
		label_of_7_days = list()
		for i in range(1,8):
			label_of_7_days.append((start_date + relativedelta(days=i)).strftime('%m-%d'))
		label_of_7_days = json.dumps(label_of_7_days)

		data_of_7_days = []
		for day in range(1,8):
			data_of_7_days.append(article_search(3,keyword_today_hot['a_movie'],[2019,int((start_date + relativedelta(days=i)).strftime('%m')),int((start_date + relativedelta(days=day)).strftime('%d'))]))

		discussion_of_7_days = list()
		for _data in data_of_7_days:
			discussion_of_7_days.append(_data['c_discussion'])
		discussion_of_7_days = json.dumps(discussion_of_7_days)
		
	#昨日
	yesterday = datetime.datetime.today().date() - relativedelta(days=1)
	
	#昨日討論電影關鍵字
	yesterday_keywords = set()
	
	#昨日文章
	article_yesterday = Article.objects.filter(time__year=yesterday.strftime('%Y'),time__month=yesterday.strftime('%m'),time__day=yesterday.strftime('%d'))
	
	"""
	尋找今日電影關鍵字的快速做法
	
	"""
	article_str = ''
	
	for _article_today in article_yesterday:
		article_str += _article_today.title + ' '
	article_str = article_str.strip()
	
	for _keyword in keywords:
		
		if(_keyword.movie in article_str):
			yesterday_keywords.add(_keyword.movie)
			
		for same_keyword in _keyword.keyword.strip().split(' '):
			if(same_keyword.strip()!='') and (same_keyword.strip() in article_str):
				yesterday_keywords.add(_keyword.movie)

	return render(request,'ptt_movie/index.html', locals())
	

from .forms import MoiveForm
from ptt_movie.models import Article,Keyword
from .tendency import make_tendency_score
import datetime,time

def keyword(request,key):
	keyword_result = Keyword.objects.filter(movie = key)
	if len(keyword_result) != 0:
		movie_name = key
		article_for_keyword = set()
				
		#第一階段搜尋: 只比對與電影關鍵字吻合的文章
		articles = Article.objects.filter(title__icontains=movie_name)
		for article in articles:
			temp = (article.title,article.author,article.time,article.url,article.push_message_all,article.push_message_good,article.push_message_bad,article.push_message_neutral)
			article_for_keyword.add(temp)
			
		#第二階段搜尋: 比對與電影關鍵字附屬關鍵字吻合的文章
		movie_keywords = Keyword.objects.get(movie=movie_name)
		if(len(movie_keywords.keyword.strip())>0):
			for movie_keyword in movie_keywords.keyword.split(' '):
				articles = Article.objects.filter(title__icontains=movie_keyword)
				for article in articles:
					temp = (article.title,article.author,article.time,article.url,article.push_message_all,article.push_message_good,article.push_message_bad,article.push_message_neutral)
					article_for_keyword.add(temp)
			
		#第三階段剃除: 除去內容相似的電影關鍵字資料
		similar_keywords = Keyword.objects.filter(movie__icontains=movie_name)
		if(len(similar_keywords)!=0):
			for similar_keyword in similar_keywords:
				if(similar_keyword.movie!=movie_name):
					articles = Article.objects.filter(title__icontains=similar_keyword.movie)
					for article in articles:
						temp = (article.title,article.author,article.time,article.url,article.push_message_all,article.push_message_good,article.push_message_bad,article.push_message_neutral)
						article_for_keyword.discard(temp)

					#第二階段搜尋: 比對與電影關鍵字附屬關鍵字吻合的文章
					if(len(similar_keyword.keyword.strip().split(' '))>0) and (similar_keyword.keyword.strip()!=''):
						#error_ = similar_keyword.keyword.strip().split(' ')
						#error_len = len(error_)
						#if(movie_name=='生日'):
						#	a = 1/0
						if(len(similar_keyword.keyword.strip().split(' '))>0):
							for same_keyword in similar_keyword.keyword.strip().split(' '):
								if(len(same_keyword)>0):
									articles = Article.objects.filter(title__icontains=same_keyword)
									for article in articles:
										temp = (article.title,article.author,article.time,article.url,article.push_message_all,article.push_message_good,article.push_message_bad,article.push_message_neutral)
										article_for_keyword.discard(temp)

		article_for_keyword = list(article_for_keyword)
		article_for_keyword.sort(key=lambda k:k[2], reverse=True)
		
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
							
		data = {
			"a_movie": movie_name,
			"b_article": len(article_for_keyword),
			"c_discussion": number_of_discussion,
			"d_good": number_of_good,
			"e_bad": number_of_bad,
			"f_score": round(ration_of_score,3),
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
			data_of_7_days.append(article_search(3,movie_name,[2019,int((start_date + relativedelta(days=i)).strftime('%m')),int((start_date + relativedelta(days=day)).strftime('%d'))]))

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
		end_date = datetime.datetime.today().date()+ relativedelta(days=1)
		start_date = end_date - relativedelta(days=7*5)
		
		label_of_5_weeks = list()
		for i in range(1,6):
			label_of_5_weeks.append(start_date.strftime('%m-%d') + ' ~ ' +(start_date + relativedelta(days=6)).strftime('%m-%d'))
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
		return_message = '錯誤關鍵字搜尋'
		return render(request,'ptt_movie/404.html',locals())

def week(request,key):

	keyword_result = Keyword.objects.filter(movie = key)
	
	if len(keyword_result) != 0:
	
		type_name = '周'
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
	
		type_name = '月'
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

from .search_of_article import article_search
from ptt_movie.models import Keyword_Analysis
def rank(request):

	# 極好評 好評 普評 壞評 極壞評
	# better good ordinary bad worse

	#---這一周---------------------------------------------------------------

	#極好評電影
	better_keywords_this_week_datas = Keyword_Analysis_This_Week.objects.filter(comment='極好評')
	better_keywords_this_week_len = len(better_keywords_this_week_datas)
	
	#好評電影
	good_keywords_this_week_datas = Keyword_Analysis_This_Week.objects.filter(comment='好評')
	good_keywords_this_week_len = len(good_keywords_this_week_datas)

	#普評電影
	ordinary_keywords_this_week_datas = Keyword_Analysis_This_Week.objects.filter(comment='普評')
	ordinary_keywords_this_week_len = len(ordinary_keywords_this_week_datas)

	#壞評電影
	bad_keywords_this_week_datas = Keyword_Analysis_This_Week.objects.filter(comment='壞評')
	bad_keywords_this_week_len = len(bad_keywords_this_week_datas)
	
	#極壞評電影
	worse_keywords_this_week_datas = Keyword_Analysis_This_Week.objects.filter(comment='極壞評')
	worse_keywords_this_week_len = len(worse_keywords_this_week_datas)
	
	#資料量不足
	insufficient_keywords_this_week_datas = Keyword_Analysis_This_Week.objects.filter(comment='資料不足')
	insufficient_keywords_this_week_len = len(insufficient_keywords_this_week_datas)
	

	#---上一周---------------------------------------------------------------

	#極好評電影
	better_keywords_last_week_datas = Keyword_Analysis_Last_Week.objects.filter(comment='極好評')
	better_keywords_last_week_len = len(better_keywords_last_week_datas)

	#好評電影
	good_keywords_last_week_datas = Keyword_Analysis_Last_Week.objects.filter(comment='好評')
	good_keywords_last_week_len = len(good_keywords_last_week_datas)

	#普評電影
	ordinary_keywords_last_week_datas = Keyword_Analysis_Last_Week.objects.filter(comment='普評')
	ordinary_keywords_last_week_len = len(ordinary_keywords_last_week_datas)

	#壞評電影
	bad_keywords_last_week_datas = Keyword_Analysis_Last_Week.objects.filter(comment='壞評')
	bad_keywords_last_week_len = len(bad_keywords_last_week_datas)
	
	#極壞評電影
	worse_keywords_last_week_datas = Keyword_Analysis_Last_Week.objects.filter(comment='極壞評')
	worse_keywords_last_week_len = len(worse_keywords_last_week_datas)
	
	#資料量不足
	insufficient_keywords_last_week_datas = Keyword_Analysis_Last_Week.objects.filter(comment='資料不足')
	insufficient_keywords_last_week_len = len(insufficient_keywords_last_week_datas)
	
	#---這一月---------------------------------------------------------------

	#極好評電影
	better_keywords_this_month_datas = Keyword_Analysis_This_Month.objects.filter(comment='極好評')
	better_keywords_this_month_len = len(better_keywords_this_month_datas)

	#好評電影
	good_keywords_this_month_datas = Keyword_Analysis_This_Month.objects.filter(comment='好評')
	good_keywords_this_month_len = len(good_keywords_this_month_datas)

	#普評電影
	ordinary_keywords_this_month_datas = Keyword_Analysis_This_Month.objects.filter(comment='普評')
	ordinary_keywords_this_month_len = len(ordinary_keywords_this_month_datas)

	#壞評電影
	bad_keywords_this_month_datas = Keyword_Analysis_This_Month.objects.filter(comment='壞評')
	bad_keywords_this_month_len = len(bad_keywords_this_month_datas)
	
	#極壞評電影
	worse_keywords_this_month_datas = Keyword_Analysis_This_Month.objects.filter(comment='極壞評')
	worse_keywords_this_month_len = len(worse_keywords_this_month_datas)
	
	#資料量不足
	insufficient_keywords_this_month_datas = Keyword_Analysis_This_Month.objects.filter(comment='資料不足')
	insufficient_keywords_this_month_len = len(insufficient_keywords_this_month_datas)
	
	#---上一月---------------------------------------------------------------

	#極好評電影
	better_keywords_last_month_datas = Keyword_Analysis_Last_Month.objects.filter(comment='極好評')
	better_keywords_last_month_len = len(better_keywords_last_month_datas)

	#好評電影
	good_keywords_last_month_datas = Keyword_Analysis_Last_Month.objects.filter(comment='好評')
	good_keywords_last_month_len = len(good_keywords_last_month_datas)

	#普評電影
	ordinary_keywords_last_month_datas = Keyword_Analysis_Last_Month.objects.filter(comment='普評')
	ordinary_keywords_last_month_len = len(ordinary_keywords_last_month_datas)

	#壞評電影
	bad_keywords_last_month_datas = Keyword_Analysis_Last_Month.objects.filter(comment='壞評')
	bad_keywords_last_month_len = len(bad_keywords_last_month_datas)
	
	#極壞評電影
	worse_keywords_last_month_datas = Keyword_Analysis_Last_Month.objects.filter(comment='極壞評')
	worse_keywords_last_month_len = len(worse_keywords_last_month_datas)
	
	#資料量不足
	insufficient_keywords_last_month_datas = Keyword_Analysis_Last_Month.objects.filter(comment='資料不足')
	insufficient_keywords_last_month_len = len(insufficient_keywords_last_month_datas)

	#---總體-----------------------------------------------------------------------

	#極好評電影
	better_keywords_all_datas = Keyword_Analysis.objects.filter(comment='極好評')
	better_keywords_all_len = len(better_keywords_all_datas)
	#better_keywords_datas = list()
	#for better_keyword in better_keywords:
	#	better_keywords_datas.append(better_keyword.name)
	
	#好評電影
	good_keywords_all_datas = Keyword_Analysis.objects.filter(comment='好評')
	good_keywords_all_len = len(good_keywords_all_datas)
	#good_keywords_datas = list()
	#for good_keyword in good_keywords:
	#	good_keywords_datas.append(good_keyword.name)

	#普評電影
	ordinary_keywords_all_datas = Keyword_Analysis.objects.filter(comment='普評')
	ordinary_keywords_all_len = len(ordinary_keywords_all_datas)
	#ordinary_keywords_datas = list()
	#for ordinary_keyword in ordinary_keywords:
	#	ordinary_keywords_datas.append(ordinary_keyword.name)

	#壞評電影
	bad_keywords_all_datas = Keyword_Analysis.objects.filter(comment='壞評')
	bad_keywords_all_len = len(bad_keywords_all_datas)
	#bad_keywords_datas = list()
	#for bad_keyword in bad_keywords:
	#	bad_keywords_datas.append(bad_keyword.name)
	
	#極壞評電影
	worse_keywords_all_datas = Keyword_Analysis.objects.filter(comment='極壞評')
	worse_keywords_all_len = len(worse_keywords_all_datas)
	#worse_keywords_datas = list()
	#for worse_keyword in worse_keywords:
	#	worse_keywords_datas.append(worse_keyword.name)
		
	#資料量不足
	insufficient_keywords_all_datas = Keyword_Analysis.objects.filter(comment='資料不足')
	insufficient_keywords_all_len = len(insufficient_keywords_all_datas)
	#insufficient_keywords_datas = list()
	#for insufficient_keyword in insufficient_keywords:
	#	insufficient_keywords_datas.append(insufficient_keyword.name)
		
	return render(request,'ptt_movie/rank.html',locals())

def hot(request):
				
	movie_keywords = Keyword.objects.all()
	num_movie_keyword = 8					#輸出電影的數量
		
	#這一周
	timenow = datetime.datetime.now()		#現在時間
	this_week = timenow.isocalendar()[1]	#找出目前第幾周
	
	"""
	this_week_keywords = set()				#這周的電影關鍵字

	article_this_week = Article.objects.filter(time__year=2019,time__week=this_week)	#這周的文章
	
	article_str = ''	#從文章標題去找電影關鍵字
	for _article_this_week in article_this_week:
		article_str += _article_this_week.title + ' '
	article_str = article_str.strip()

	for _keyword in movie_keywords:
		
		if(_keyword.movie in article_str):
			this_week_keywords.add(_keyword.movie)
			
		for same_keyword in _keyword.keyword.strip().split(' '):
			if(same_keyword.strip()!='') and (same_keyword.strip() in article_str):
				this_week_keywords.add(_keyword.movie)
				
				
	data_this_week = []	#裝這周電影關鍵字的資料
		
	for _keyword in this_week_keywords:			#抓取這周的電影資料
		movie_name = _keyword
		data_this_week.append(article_search(1,movie_name,this_week))
	"""
	
	data_this_week = []
	for data in Keyword_Analysis_This_Week.objects.all():
		temp = {
			"a_movie": data.name,
			"b_article": data.article,
			"c_discussion": data.discussion,
			"d_good": data.good,
			"e_bad": data.bad,
			"f_score": data.score,
			"g_comment": data.comment,
		}
		data_this_week.append(temp)
	
	#依照文章數進行逆排序(大->小)，只擷取8筆
	data_this_week.sort(key=lambda k: k['b_article'],reverse=True)
	a_data_this_week = data_this_week[:num_movie_keyword]
	#依照討論度進行逆排序(大->小)，只擷取8筆
	data_this_week.sort(key=lambda k: k['c_discussion'],reverse=True)
	d_data_this_week = data_this_week[:num_movie_keyword]
			
	#匯出電影名稱
	article_label_this_week = list()			#文
	for _keyword in a_data_this_week:
		article_label_this_week.append(_keyword['a_movie'])
	article_label_this_week = json.dumps(article_label_this_week)
	
	discussion_label_this_week = list()			#討
	for _keyword in d_data_this_week:
		discussion_label_this_week.append(_keyword['a_movie'])
	discussion_label_this_week = json.dumps(discussion_label_this_week)
	
	#匯出電影討論度
	article_data_this_week = list()			#文
	for _data in a_data_this_week:
		article_data_this_week.append(_data['b_article'])
	article_data_this_week = json.dumps(article_data_this_week)

	discussiond_data_this_week = list()			#討
	for _data in d_data_this_week:
		discussiond_data_this_week.append(_data['c_discussion'])
	discussiond_data_this_week = json.dumps(discussiond_data_this_week)
	
	
	#上一周
	
	timenow = datetime.datetime.now()		#現在時間
	last_week = timenow.isocalendar()[1]-1	#找出目前第幾周
	"""
	last_week_keywords = set()				#這周的電影關鍵字

	article_last_week = Article.objects.filter(time__year=2019,time__week=last_week)	#這周的文章
	
	article_str = ''	#從文章標題去找電影關鍵字
	for _article_last_week in article_last_week:
		article_str += _article_last_week.title + ' '
	article_str = article_str.strip()

	for _keyword in movie_keywords:
		
		if(_keyword.movie in article_str):
			last_week_keywords.add(_keyword.movie)
			
		for same_keyword in _keyword.keyword.strip().split(' '):
			if(same_keyword.strip()!='') and (same_keyword.strip() in article_str):
				last_week_keywords.add(_keyword.movie)
				
				
	data_last_week = []	#裝這周電影關鍵字的資料
		
	for _keyword in last_week_keywords:			#抓取這周的電影資料
		movie_name = _keyword
		data_last_week.append(article_search(1,movie_name,last_week))
	"""

	data_last_week = []
	for data in Keyword_Analysis_Last_Week.objects.all():
		temp = {
			"a_movie": data.name,
			"b_article": data.article,
			"c_discussion": data.discussion,
			"d_good": data.good,
			"e_bad": data.bad,
			"f_score": data.score,
			"g_comment": data.comment,
		}
		data_last_week.append(temp)
			
	#依照文章數進行逆排序(大->小)，只擷取8筆
	data_last_week.sort(key=lambda k: k['b_article'],reverse=True)
	a_data_last_week = data_last_week[:num_movie_keyword]
	#依照討論度進行逆排序(大->小)，只擷取8筆
	data_last_week.sort(key=lambda k: k['c_discussion'],reverse=True)
	d_data_last_week = data_last_week[:num_movie_keyword]

	#匯出電影名稱
	article_label_last_week = list()				#文
	for _keyword in a_data_last_week:
		article_label_last_week.append(_keyword['a_movie'])
	article_label_last_week = json.dumps(article_label_last_week)
	
	discussion_label_last_week = list()				#討
	for _keyword in d_data_last_week:
		discussion_label_last_week.append(_keyword['a_movie'])
	discussion_label_last_week = json.dumps(discussion_label_last_week)
	
	#匯出電影討論度
	article_data_last_week = list()				#文
	for _data in a_data_last_week:
		article_data_last_week.append(_data['b_article'])
	article_data_last_week = json.dumps(article_data_last_week)

	discussiond_data_last_week = list()				#討
	for _data in d_data_last_week:
		discussiond_data_last_week.append(_data['c_discussion'])
	discussiond_data_last_week = json.dumps(discussiond_data_last_week)
	
	
	#這一月
	
	timenow = datetime.datetime.now().date()		#現在時間
	
	this_month = int(timenow.strftime('%m'))
	"""
	this_month_keywords = set()				#這周的電影關鍵字

	article_this_month =  Article.objects.filter(time__year=timenow.strftime('%Y'),time__month=timenow.strftime('%m'))	#這周的文章
	
	article_str = ''	#從文章標題去找電影關鍵字
	for _article_this_month in article_this_month:
		article_str += _article_this_month.title + ' '
	article_str = article_str.strip()

	for _keyword in movie_keywords:
		
		if(_keyword.movie in article_str):
			this_month_keywords.add(_keyword.movie)
			
		for same_keyword in _keyword.keyword.strip().split(' '):
			if(same_keyword.strip()!='') and (same_keyword.strip() in article_str):
				this_month_keywords.add(_keyword.movie)
				
				
	data_this_month = []	#裝這周電影關鍵字的資料
		
	for _keyword in last_week_keywords:			#抓取這周的電影資料
		movie_name = _keyword
		data_this_month.append(article_search(2,movie_name,timenow.strftime('%m')))
	"""
	data_this_month = []
	for data in Keyword_Analysis_This_Month.objects.all():
		temp = {
			"a_movie": data.name,
			"b_article": data.article,
			"c_discussion": data.discussion,
			"d_good": data.good,
			"e_bad": data.bad,
			"f_score": data.score,
			"g_comment": data.comment,
		}
		data_this_month.append(temp)

	#依照文章數進行逆排序(大->小)，只擷取8筆
	data_this_month.sort(key=lambda k: k['b_article'],reverse=True)
	a_data_this_month = data_this_month[:num_movie_keyword]
	#依照討論度進行逆排序(大->小)，只擷取8筆
	data_this_month.sort(key=lambda k: k['c_discussion'],reverse=True)
	d_data_this_month = data_this_month[:num_movie_keyword]
			
	#匯出電影名稱
	article_label_this_month = list()		#文
	for _keyword in a_data_this_month:
		article_label_this_month.append(_keyword['a_movie'])
	article_label_this_month = json.dumps(article_label_this_month)
	
	discussion_label_this_month = list()		#討
	for _keyword in d_data_this_month:
		discussion_label_this_month.append(_keyword['a_movie'])
	discussion_label_this_month = json.dumps(discussion_label_this_month)
	
	#匯出電影討論度
	article_data_this_month = list()		#文
	for _data in a_data_this_month:
		article_data_this_month.append(_data['b_article'])
	article_data_this_month = json.dumps(article_data_this_month)
	
	discussiond_data_this_month = list()		#討
	for _data in d_data_this_month:
		discussiond_data_this_month.append(_data['c_discussion'])
	discussiond_data_this_month = json.dumps(discussiond_data_this_month)

	#上一月
	
	timenow = datetime.datetime.now().date() - relativedelta(months=1)		#現在時間
	
	last_month = int(timenow.strftime('%m'))
	"""
	last_month_keywords = set()				#這周的電影關鍵字

	article_last_month =  Article.objects.filter(time__year=timenow.strftime('%Y'),time__month=timenow.strftime('%m'))	#這周的文章
	
	article_str = ''	#從文章標題去找電影關鍵字
	for _article_last_month in article_last_month:
		article_str += _article_last_month.title + ' '
	article_str = article_str.strip()

	for _keyword in movie_keywords:
		
		if(_keyword.movie in article_str):
			last_month_keywords.add(_keyword.movie)
			
		for same_keyword in _keyword.keyword.strip().split(' '):
			if(same_keyword.strip()!='') and (same_keyword.strip() in article_str):
				last_month_keywords.add(_keyword.movie)
				
				
	data_last_month = []	#裝這周電影關鍵字的資料
	
	for _keyword in last_month_keywords:			#抓取這周的電影資料
		movie_name = _keyword
		data_last_month.append(article_search(2,movie_name,timenow.strftime('%m')))
	"""
	data_last_month = []
	for data in Keyword_Analysis_Last_Month.objects.all():
		temp = {
			"a_movie": data.name,
			"b_article": data.article,
			"c_discussion": data.discussion,
			"d_good": data.good,
			"e_bad": data.bad,
			"f_score": data.score,
			"g_comment": data.comment,
		}
		data_last_month.append(temp)
	
	#依照文章數進行逆排序(大->小)，只擷取8筆
	data_last_month.sort(key=lambda k: k['b_article'],reverse=True)
	a_data_last_month = data_last_month[:num_movie_keyword]
	#依照討論度進行逆排序(大->小)，只擷取8筆
	data_last_month.sort(key=lambda k: k['c_discussion'],reverse=True)
	d_data_last_month = data_last_month[:num_movie_keyword]
			
	#匯出電影名稱
	article_label_last_month = list()		#文
	for _keyword in a_data_last_month:
		article_label_last_month.append(_keyword['a_movie'])
	article_label_last_month = json.dumps(article_label_last_month)

	discussion_label_last_month = list()	#討
	for _keyword in d_data_last_month:
		discussion_label_last_month.append(_keyword['a_movie'])
	discussion_label_last_month = json.dumps(discussion_label_last_month)
	
	#匯出電影討論度
	article_data_last_month = list()		#文
	for _data in a_data_last_month:
		article_data_last_month.append(_data['b_article'])
	article_data_last_month = json.dumps(article_data_last_month)
	
	discussiond_data_last_month = list()	#討
	for _data in d_data_last_month:
		discussiond_data_last_month.append(_data['c_discussion'])
	discussiond_data_last_month = json.dumps(discussiond_data_last_month)
	
	return render(request,'ptt_movie/hot.html',locals())

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


from .forms import MoiveForm
from .search_of_article import article_search
def analysis_type(request):
	"""
	if request.method == 'POST':
		form = MoiveTypeForm(request.POST)
	
		if form.is_valid():
			type = form.cleaned_data['type']
			movie_name = form.cleaned_data['movie_name']
			if(type < 0 ) or (type > 2):
				return HttpResponse(str('type error'))
				
			result = Article.objects.filter(title__contains=movie_name)
			
			if len(Keyword.objects.filter(movie=movie_name)) == 0:
				return HttpResponse(str('電影名稱錯誤'))
				
			elif (type == 0):
				
				return keyword(request,movie_name)
				
			elif (type == 1):
			
				type_name = '周'
				
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
			
				type_name = '月'
			
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
	"""
	return_message = '無資料...'
	if request.method == 'POST':
		form = MoiveForm(request.POST)
	
		if form.is_valid():
			keyword = form.cleaned_data['movie_keyword_name']
			results = Keyword_Analysis.objects.filter(name__contains=keyword)
			input_value = 'value='+ keyword 
			if len(results) == 0:
				return_message = '未搜尋到任何結果'
				return render(request,'ptt_movie/search.html',locals())
			else:
				return_datas = []
				for data in results:
					temp = {
						"a_movie": data.name,
						"b_article": data.article,
						"c_discussion": data.discussion,
						"d_good": data.good,
						"e_bad": data.bad,
						"f_score": data.score,
						"g_comment": data.comment,
					}
					return_datas.append(temp)
				print(input_value)
				return render(request,'ptt_movie/search.html',locals())
	else:
		form = MoiveForm()
		return_message = '請輸入關鍵字搜索'
	return render(request,'ptt_movie/search.html',{'form':form,'return_message':return_message})