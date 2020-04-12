from django.urls import path
from . import views
urlpatterns = [
	path('',views.index,name="home"),
	path('search_result/',views.SearchResultView.as_view(),name="search_result"),
	path('search/',views.search,name="search"),
	path('book/<str:isbn>/',views.BookDetail.as_view(),name="book_detail"),
	# path('book/<str:isbn>/',views.BookDetail,name="book_detail"),
	path('api/<str:isbn>/',views.bookReviewApi,name="book_review_api"),

]