"""movie_analysis URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from ptt_movie import views as movie_analysis_views

urlpatterns = [
    path('admin/', admin.site.urls),
	path('',movie_analysis_views.index),
	path('b/',movie_analysis_views.analysis),
	path('search/',movie_analysis_views.analysis_type,name = 'search'),
	path('keyword/<str:key>',movie_analysis_views.keyword,name='keyword'),
	path('month/<str:key>',movie_analysis_views.month,name='month'),
	path('week/<str:key>',movie_analysis_views.week,name='week'),
	path('hot/',movie_analysis_views.hot,name='hot'),
	path('rank/',movie_analysis_views.rank,name='rnk'),
]
