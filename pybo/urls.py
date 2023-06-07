from django.urls import path
from . import views
from .views import base_views, question_views, answer_views, comment_views, category_views

app_name = 'pybo'

urlpatterns= [
    # base_views.py
    path('',
         base_views.index, name='index'),
    path('<int:category_id>/', base_views.index_category, name='index_category'),
    path('<int:question_id>/<int:sort>/',
         base_views.detail, name='detail'),
    path('<int:question_id>/<int:check>/',
         base_views.detail_comment, name='detail_comment_q'),



    # question_views.py
    path('question/create/<int:category_id>/',
         question_views.question_create, name='question_create'),
    path('question/modify/<int:question_id>/',
         question_views.question_modify, name='question_modify'),
    path('question/delete/<int:question_id>/',
         question_views.question_delete, name='question_delete'),

    # answer_views.py
    path('answer/create/<int:question_id>/',
         answer_views.answer_create, name='answer_create'),
    path('answer/modify/<int:answer_id>/',
         answer_views.answer_modify, name='answer_modify'),
    path('answer/delete/<int:answer_id>/',
         answer_views.answer_delete, name='answer_delete'),
    path('question/vote/<int:question_id>/', question_views.question_vote, name='question_vote'),
    path('answer/vote/<int:answer_id>/', answer_views.answer_vote, name='answer_vote'),

    # comment_views.py
    path('comment/create/<int:question_id>/',
         comment_views.comment_create_q , name='comment_create_q'),

    path('comment/create_answer/<int:answer_id>/',
         comment_views.comment_create_answer , name='comment_create_answer'),

    path('comment/modify/<int:comment_id>/',
         comment_views.comment_modify, name='comment_modify'),
    path('comment/delete/<int:comment_id>/',
         comment_views.comment_delete, name='comment_delete'),
    path('comment/vote/<int:comment_id>/',
         comment_views.comment_vote, name='comment_vote'),

    #category_views.py
    path('category/create/',
         category_views.category_create, name='category_create'),
    path('category/modify/<int:category_id>/',
         category_views.category_modify, name='category_modify'),
    path('category/delete/<int:category_id>/',
         category_views.category_delete, name='category_delete'),


]

