from django.shortcuts import render,get_object_or_404
from django.views.generic import ListView,DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist

import requests
import json
import os

from .models import Books

def index(request):
	templates = 'books/index.html'
	return render(request,templates)



class SearchResultView(ListView):
	model = Books
	template_name = "books/search_result.html"
	def get_context_data(self,*args,**kwargs):
		context = super().get_context_data(*args,**kwargs)
		context['query'] = self.request.GET.get('q')
		return context

	def get_queryset(self):
		query = self.request.GET.get('q')
		object_list = Books.objects.filter(
			Q(title__icontains=query) | Q(author__icontains = query) 
			| Q(isbn__exact=query)

		)
		return object_list


def search(request):
	template_name = "books/search.html"
	return render(request,template_name)

#DETAILVIEW

class BookDetail(LoginRequiredMixin,DetailView):
	#CLASS BASED VIEW
	login_url = '/login/'
	model = Books
	template_name = "books/book_detail.html"
	def get_object(self, queryset=None):
		isbn = self.kwargs.get("isbn")
		return get_object_or_404(Books,isbn=isbn)
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		isbn = self.kwargs.get("isbn")
		res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": api_key, "isbns": isbn})
		print(res.json())
		average_rating = res.json()['books'][0]['average_rating']
		average_rating = float(average_rating)
		work_ratings_count=res.json()['books'][0]['work_ratings_count']
		context.update({
			'average_rating':average_rating,
			'work_ratings_count':work_ratings_count,
		})
		
		return context


# def BookDetail(request,isbn):
	# FUNCTION BASED VIEW
# 	book = get_object_or_404(Books,isbn=isbn)
# 	#API
# 	res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": api_key, "isbns": isbn})
# 	average_rating = res.json()['books'][0]['average_rating']
# 	work_ratings_count=res.json()['books'][0]['work_ratings_count']

# 	context = {'object':book,'average_rating':average_rating,'work_ratings_count':work_ratings_count}
# 	return render(request,"books/book_detail.html",context) 






#API
api_key  = os.getenv('goodreads_api')
def bookReviewApi(request,isbn):
	book = get_object_or_404(Books,isbn=isbn)
	res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": api_key, "isbns": isbn})
	average_rating = res.json()['books'][0]['average_rating']
	work_ratings_count=res.json()['books'][0]['work_ratings_count']
	context = {
		"title":book.title,
		"author":book.author,
		"year":book.year,
		"isbn":isbn,
		"work_ratings_count":work_ratings_count,
		"average_rating":average_rating
	}
	return JsonResponse(context)



