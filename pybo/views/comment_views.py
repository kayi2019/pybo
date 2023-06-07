from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.utils import timezone
from ..forms import CommentForm
from ..models import Question, Answer, Comment
from django.db.models import Q


@login_required(login_url='common:login')
def comment_create_q(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user  # author 속성에 로그인 계정 저장
            comment.create_date = timezone.now()
            comment.question = question
            comment.answer = None
            comment.save()
            return redirect('{}#comment_{}'.format(
                resolve_url('pybo:detail_comment_q', question_id=question.id, check=0), comment.id))


@login_required(login_url='common:login')
def comment_create_answer(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    question = answer.question
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user  # author 속성에 로그인 계정 저장
            comment.create_date = timezone.now()
            comment.question = question
            comment.answer = answer
            comment.save()
            return redirect('{}#comment_{}'.format(
                resolve_url('pybo:detail_comment_q', question_id=question.id, check=1), comment.id))


@login_required(login_url='common:login')
def comment_modify(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('pybo:detail', question_id=comment.question.id, sort=1)

    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.modify_date = timezone.now()
            comment.save()
            return redirect('{}#answer_{}'.format(
                resolve_url('pybo:detail', question_id=comment.question.id, sort=1), comment.question.id))
    else:
        form = CommentForm(instance=comment)
        context = {'comment': comment, 'form': form}
        return render(request, 'pybo/answer_form.html', context)


@login_required(login_url='common:login')
def comment_delete(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    # if request.user != comment.author:
    #     messages.error(request, '삭제권한이 없습니다')
    # else:
    #     comment.delete()
    question_id = comment.question.id
    if request.user != comment.author:
        messages.error(request, '삭제권한이 없습니다')
    else:
        comment.delete()
    return redirect('pybo:detail', question_id=question_id, sort=1)



@login_required(login_url='common:login')
def comment_vote(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user == comment.author:
        messages.error(request, '본인이 작성한 글은 추천할수 없습니다')
    elif Comment.objects.filter(Q(voter=request.user) & Q(id=comment.id)):
        messages.error(request, '이미 추천한 댓글입니다.')

    else:
        comment.voter.add(request.user)

    if comment.question == None:
        question = comment.answer.question
    elif comment.answer == None:
        question = comment.question
        comment.voter

    return redirect('{}#comment_{}'.format(
        resolve_url('pybo:detail_comment_q', id=question.id, check=0, comment_id=comment.id), comment.id))
