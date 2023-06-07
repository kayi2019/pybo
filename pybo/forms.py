from django import forms
from pybo.models import Question, Answer, Comment, Category


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question  # 사용할 모델
        fields = ['subject', 'content']  # QuestionForm에서 사용할 Question 모델의 속성
        labels = {
            'subject': '제목',
            'content': '내용',
        }


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']
        labels = {'content': '답변내용', }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        # labels = {'content': '댓글내용', }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'type', 'can_answer']
        labels = {'name': '카테고리 이름', 'type': 'type', 'can_answer': '답변가능여부'}
