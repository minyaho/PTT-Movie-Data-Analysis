from django.contrib import admin
from .models import Article,Keyword_Yahoo,Keyword_Like,Keyword,Keyword_Analysis,Keyword_Analysis_This_Week,Keyword_Analysis_Last_Week,Keyword_Analysis_This_Month,Keyword_Analysis_Last_Month

# Register your models here.

#Article
class Article_Admin(admin.ModelAdmin):
	list_display = ('title','author','time','push_message_all','push_message_good','push_message_bad')
	search_fields = ('title','author',)
	
admin.site.register(Article, Article_Admin)

#Keyword_Yahoo
class Keyword_Yahoo_Admin(admin.ModelAdmin):
	list_display = ('movie','keyword')
	search_fields = ('movie',)

admin.site.register(Keyword_Yahoo, Keyword_Yahoo_Admin)

#Keyword_Like
class Keyword_Like_Admin(admin.ModelAdmin):
	list_display = ('movie','keyword')
	search_fields = ('movie',)
	
admin.site.register(Keyword_Like, Keyword_Like_Admin)

#Keyword
class Keyword_Admin(admin.ModelAdmin):
	list_display = ('movie','keyword','not_keyword')
	search_fields = ('movie',)
	
admin.site.register(Keyword, Keyword_Admin)

#Keyword_Analysis
class Keyword_Analysis_Admin(admin.ModelAdmin):
	list_display = ('name','article','discussion','good','bad','score','comment')
	search_fields = ('name','comment',)
	
admin.site.register(Keyword_Analysis, Keyword_Analysis_Admin)

#Keyword_Analysis_This_Week
class Keyword_Analysis_This_Week_Admin(admin.ModelAdmin):
	list_display = ('name','article','discussion','good','bad','score','comment')
	search_fields = ('name','comment',)
	
admin.site.register(Keyword_Analysis_This_Week, Keyword_Analysis_This_Week_Admin)

#Keyword_Analysis_Last_Week
class Keyword_Analysis_Last_Week_Admin(admin.ModelAdmin):
	list_display = ('name','article','discussion','good','bad','score','comment')
	search_fields = ('name','comment',)
	
admin.site.register(Keyword_Analysis_Last_Week, Keyword_Analysis_Last_Week_Admin)

#Keyword_Analysis_This_Month
class Keyword_Analysis_This_Month_Admin(admin.ModelAdmin):
	list_display = ('name','article','discussion','good','bad','score','comment')
	search_fields = ('name','comment',)
	
admin.site.register(Keyword_Analysis_This_Month, Keyword_Analysis_This_Month_Admin)

#Keyword_Analysis_Last_Month
class Keyword_Analysis_Last_Month_Admin(admin.ModelAdmin):
	list_display = ('name','article','discussion','good','bad','score','comment')
	search_fields = ('name','comment',)
	
admin.site.register(Keyword_Analysis_Last_Month, Keyword_Analysis_Last_Month_Admin)
