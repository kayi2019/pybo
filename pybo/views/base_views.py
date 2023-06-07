from django.shortcuts import render, get_object_or_404
from ..models import Question, Answer, Comment, Category
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
import datetime

def index(request):
    page = request.GET.get('page', '1')
    kw = request.GET.get('kw','')
    question_list = Question.objects.order_by('-create_date')

    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) |  # 제목 검색
            Q(content__icontains=kw) |  # 내용 검색
            Q(answer__content__icontains=kw) |  # 답변 내용 검색
            Q(author__username__icontains=kw) |  # 질문 글쓴이 검색
            Q(answer__author__username__icontains=kw)  # 답변 글쓴이 검색
        ).distinct()

    category_list = Category.objects.all()

    paginator = Paginator(question_list, 10)
    page_obj = paginator.get_page(page)
    context = {'question_list':page_obj, 'page':page, 'kw':kw,'category_list':category_list, 'cur_category':0}
    return render(request,'pybo/question_list.html',context)



def index_category(request, category_id):
    page = request.GET.get('page', '1')
    kw = request.GET.get('kw','')
    question_list = Question.objects.order_by('-create_date')
    # if kw:
    #     question_list = question_list.filter(
    #         Q(subject__icontains=kw) |  # 제목 검색
    #         Q(content__icontains=kw) |  # 내용 검색
    #         Q(answer__content__icontains=kw) |  # 답변 내용 검색
    #         Q(author__username__icontains=kw) |  # 질문 글쓴이 검색
    #         Q(answer__author__username__icontains=kw)  # 답변 글쓴이 검색
    #
    #     ).distinct()
    category_list = Category.objects.all()
    category=get_object_or_404(Category,pk=category_id)
    question_list = question_list.filter(category=category)

    paginator = Paginator(question_list, 10)
    page_obj = paginator.get_page(page)
    context = {'question_list':page_obj, 'page':page, 'kw':kw,'category_list':category_list, 'cur_category':category}
    return render(request,'pybo/question_list.html',context)







def detail(request, question_id, sort):
    question =get_object_or_404(Question,pk=question_id)
    page = request.GET.get('page',1)
    answer_list_cr = Answer.objects.filter(question=question).order_by('-create_date')
    answer_list_vo = Answer.objects.filter(question=question).order_by('-voter')
    question_comment = Comment.objects.filter(question=question).order_by('create_date')



    answer_list = answer_list_cr
    if sort==2:
        answer_list=answer_list_vo

    for answer in answer_list_cr:
        answer_comments = Comment.objects.filter(answer=answer).order_by('-create_date')
    paginator = Paginator(answer_list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)

    context = {'question' : question, 'answer_list':page_obj, 'q_comment_list':question_comment,
                'page':page}
    # return render(request,'pybo/question_detail.html',context)
    return view(request, question_id, context)

def detail_comment(request, question_id, check):
    question = get_object_or_404(Question, pk=question_id)
    page = request.GET.get('page',1)

    answer_list = Answer.objects.filter(question=question).order_by('-create_date')
    question_comment = Comment.objects.filter(question=question).order_by('create_date')



    paginator = Paginator(answer_list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)

    context = {'question' : question, 'answer_list':page_obj, 'q_comment_list':question_comment,
               'a_comment_list':question_comment, 'page':page, 'check':check}
    # return render(request,'pybo/question_detail.html',context)
    return view(request, question_id, context)


def view(request,question_id, context):
    question = get_object_or_404(Question, pk = question_id)
    tomorrow = datetime.datetime.replace(datetime.datetime.now(), hour=23, minute=59, second=0)
    expires = datetime.datetime.strftime(tomorrow, "%a, %d-%b-%Y %H:%M:%S GMT")
    response = render(request, 'pybo/question_detail.html', context)

    if request.session.get('authUser') is None:
        cookie_name = 'view'
    else:
        cookie_name = f'view:{request.session["authUser"]["id"]}'
    if request.COOKIES.get(cookie_name) is not None:
        cookies = request.COOKIES.get(cookie_name)
        cookies_list = cookies.split('|')
        if str(question_id) not in cookies_list:
            response.set_cookie(cookie_name, cookies + f'|{question_id}', expires=expires)
            # board.update(hit=F('hit') + 1)
            question.views += 1
            question.save()
            return response
        # [4] hit를 check하는 쿠키가 없는 경우
    else:
        response.set_cookie(cookie_name, question_id, expires=expires)
        question.views += 1
        question.save()
        return response
    return render(request, 'pybo/question_detail.html', context)


