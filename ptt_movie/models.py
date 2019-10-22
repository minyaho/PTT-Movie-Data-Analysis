from django.db import models

# Create your models here.

class Article(models.Model):
	author = models.CharField(max_length = 40)
	title = models.CharField(max_length = 80)
	time = models.DateTimeField()
	ip = models.CharField(max_length = 60, null=True)
	content = models.TextField()
	url = models.CharField(max_length = 80, unique=True, primary_key=True)
	push_message_all = models.IntegerField()
	push_message_good = models.IntegerField()
	push_message_bad = models.IntegerField()
	push_message_neutral = models.IntegerField()
	
	class Meta:
		ordering = ('-time',)
	
	def __str__(self):
		return self.title
		
class Keyword_Yahoo(models.Model):
	movie = models.CharField(max_length = 60)
	keyword = models.CharField(max_length = 256,null=True)
	
	def __str__(self):
		return self.movie
		
class Keyword_Like(models.Model):
	movie = models.CharField(max_length = 60)
	keyword = models.CharField(max_length = 256,null=True)
	
	def __str__(self):
		return self.movie
		
class Keyword(models.Model):
	movie = models.CharField(max_length = 60)
	keyword = models.CharField(max_length = 256,null=True)
	not_keyword = models.CharField(max_length = 256,null=True)
	
	def __str__(self):
		return self.movie

class Keyword_Analysis(models.Model):
	name = models.CharField(max_length = 60, primary_key=True)
	article = models.IntegerField()
	discussion = models.IntegerField()
	good = models.IntegerField()
	bad = models.IntegerField()
	score = models.FloatField()
	comment = models.CharField(max_length = 10)
	def __str__(self):
		return self.name

class Keyword_Analysis_This_Week(models.Model):
	name = models.CharField(max_length = 60, primary_key=True)
	article = models.IntegerField()
	discussion = models.IntegerField()
	good = models.IntegerField()
	bad = models.IntegerField()
	score = models.FloatField()
	comment = models.CharField(max_length = 10)
	def __str__(self):
		return self.name

class Keyword_Analysis_Last_Week(models.Model):
	name = models.CharField(max_length = 60, primary_key=True)
	article = models.IntegerField()
	discussion = models.IntegerField()
	good = models.IntegerField()
	bad = models.IntegerField()
	score = models.FloatField()
	comment = models.CharField(max_length = 10)
	def __str__(self):
		return self.name
		
class Keyword_Analysis_This_Month(models.Model):
	name = models.CharField(max_length = 60, primary_key=True)
	article = models.IntegerField()
	discussion = models.IntegerField()
	good = models.IntegerField()
	bad = models.IntegerField()
	score = models.FloatField()
	comment = models.CharField(max_length = 10)
	def __str__(self):
		return self.name

class Keyword_Analysis_Last_Month(models.Model):
	name = models.CharField(max_length = 60, primary_key=True)
	article = models.IntegerField()
	discussion = models.IntegerField()
	good = models.IntegerField()
	bad = models.IntegerField()
	score = models.FloatField()
	comment = models.CharField(max_length = 10)
	def __str__(self):
		return self.name
