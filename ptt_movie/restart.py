from ptt_movie.models import *
def re_analysis():
	try:
		if(len(Keyword_Analysis.objects.all())==0):
			ranking = dict()
			keywords = Keyword.objects.all()
			for _keyword in keywords:
				article_result = article_search(0,_keyword.movie,None)
				ranking[_keyword.movie] = article_result
				
			for _ranking in ranking:
				temp 			= Keyword_Analysis()
				temp.name 		= ranking[_ranking]['a_movie']
				temp.article 	= ranking[_ranking]['b_article']
				temp.discussion = ranking[_ranking]['c_discussion']
				temp.good 		= ranking[_ranking]['d_good']
				temp.bad 		= ranking[_ranking]['e_bad']
				temp.score 		= ranking[_ranking]['f_score']
				temp.comment 	= ranking[_ranking]['g_comment']
				temp.save()
				
			for _ranking in ranking:	#刪除不必要的關鍵字
				if(ranking[_ranking]['b_article']==0):
					temp = Keyword.objects.filter(movie=ranking[_ranking]['a_movie'])
					temp.delete()
		else:
			pass
		print('Re-Analysis is Finish!')
	except:
		print('Re-Analysis is Error!')