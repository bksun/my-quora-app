from django.contrib.auth.hashers import PBKDF2PasswordHasher
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from myquora.models import Answer, Author, Comment, Question


class UpdateAnswer(LoginRequiredMixin, UpdateView):
    model = Answer
    fields = ['answer_text']
    template_name = 'myquora/answer_update_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        answer_id = self.kwargs['pk']
        answer = Answer.objects.get(id=answer_id)
        self.pk = answer.question.id
        context['answer_text'] = answer.answer_text
        return context

    def get_success_url(self):
        return (reverse('question-detail', kwargs={'pk': self.object.question.id}))


class UpdateQuestion(LoginRequiredMixin, UpdateView):
    model = Question
    fields = ['question_text']
    success_url = reverse_lazy('questions')
    template_name = 'myquora/question_update_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        question_id = self.kwargs['pk']
        question = Question.objects.get(id=question_id)
        context['question_text'] = question.question_text
        return context


class CommentCreate(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['author', 'answer', 'comment_text']

    def get(self, request, *args, **kwargs):
        a_id = self.kwargs['pk']
        return render(request, 'myquora/comment_form.html', {"a_id": a_id})

    def post(self, request, *args, **kwargs):
        comment_text = request.POST.get('comment_text')
        params = self.kwargs['pk']
        author = Author.objects.get(user=self.request.user)
        answer = Answer.objects.get(id=params)
        Comment.objects.create(
            author=author, answer=answer, comment_text=comment_text)
        response = redirect(
            reverse('question-detail', kwargs={'pk': answer.question.id}))
        return response


class UpvoteCreate(LoginRequiredMixin, CreateView):
    model = Answer
    fields = ['answer_text', 'id', 'upvote']

    def post(self, request, *args, **kwargs):
        answer_id = self.kwargs['pk']
        answer = Answer.objects.get(id=answer_id)
        answer.upvote += 1
        answer.save()
        response = redirect(
            reverse('question-detail', kwargs={'pk': answer.question.id}))
        return response


class DownvoteCreate(LoginRequiredMixin, CreateView):
    model = Answer
    fields = ['answer_text', 'id', 'downvote']

    def post(self, request, *args, **kwargs):
        answer_id = self.kwargs['pk']
        answer = Answer.objects.get(id=answer_id)
        answer.downvote += 1
        answer.save()
        response = redirect(
            reverse('question-detail', kwargs={'pk': answer.question.id}))
        return response


class QuestionCreate(LoginRequiredMixin, CreateView):
    model = Question
    fields = ['question_text', 'credits']

    def get(self, request, *args, **kwargs):
        return render(request, 'myquora/question_form.html')

    def post(self, request, *args, **kwargs):
        response = redirect('/myquora/questions')
        return response


class AnswerCreate(LoginRequiredMixin, CreateView):
    model = Answer
    fields = ['answer_text']

    def get(self, request, *args, **kwargs):
        q_id = self.kwargs['pk']
        return render(request, 'myquora/answer_form.html', {"q_id": q_id})

    def post(self, request, *args, **kwargs):
        answer_text = request.POST.get('answer_text')
        answer = Answer.objects.create(author=Author.objects.get(
            user=self.request.user), question=Question.objects.get(
                id=self.kwargs['pk']), answer_text=answer_text)
        response = redirect(reverse('question-detail', kwargs={'pk': answer.question.id}))
        return response


class AuthorCreate(CreateView):
    model = Author
    fields = ['email', 'credits']

    def get(self, request, *args, **kwargs):
        return render(request, 'myquora/author_form.html')

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        email = request.POST.get('email')

        if password1 == password2:
            hasher = PBKDF2PasswordHasher()
            password = hasher.encode(
                password=password1, salt='salt', iterations=150000)

            user = User.objects.create(username=username, password=password)
            Author.objects.create(user=user, email=email, )
            response = redirect('/accounts/login/')
            return response
        else:
            return render(request, 'myquora/author_form.html')


class AuthorUpdate(UpdateView):
    model = Author
    fields = ['email']


class AuthorDelete(DeleteView):
    model = Author
    fields = ['user']
    fields = ['email']
    fields = ['credits']
    success_url = reverse_lazy('questions')


class AuthorDetailView(generic.DetailView):
    """Generic class-based detail view for an Author."""
    model = Author


class QuestionDetailView(generic.DetailView):
    """Generic class-based detail view for a Question."""
    model = Question

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        question_id = self.kwargs['pk']
        question = Question.objects.get(id=question_id)
        answer_list = Answer.objects.filter(question=question)
        comment_dictionary = {
                ans.id: Comment.objects.filter(answer=ans) for ans in answer_list
            }
        context['answer_list'] = answer_list
        context['answer_url'] = '/myquora/question/'+str(question_id)+'/answer/'
        context['upvote_url'] = '/myquora/answer/upvote/'
        context['downvote_url'] = '/myquora/answer/downvote/'
        context['comment_dictionary'] = comment_dictionary
        return context


class AnswerListView(generic.ListView):
    model = Answer
    paginate_by = 3


class QuestionListView(generic.ListView):
    model = Question
    paginate_by = 10


def index(request):
    """View function for home page of site."""
    num_questions = Question.objects.all().count()
    num_answers = Answer.objects.all().count()
    num_authors = Author.objects.count()
    num_comments = Comment.objects.count()
    context = {
        'num_questions': num_questions,
        'num_answers': num_answers,
        'num_authors': num_authors,
        'num_comments': num_comments,
    }
    return render(request, 'index.html', context=context)
