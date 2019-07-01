from django.shortcuts import render
# Create your views here.
from myquora.models import Question, Answer, Comment, Author
from django.views import generic
from django.shortcuts import redirect

from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.http import HttpResponseForbidden
from django.urls import reverse

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render

from django.contrib.auth.hashers import PBKDF2PasswordHasher
from django.contrib.auth.mixins import LoginRequiredMixin

class QuestionCreate(LoginRequiredMixin, CreateView):
    model = Question
    fields = ['question_text', 'credits']

    def get(self, request, *args, **kwargs):
        print('Form - Get Request')
        return render(request, 'myquora/question_form.html')

    def post(self, request, *args, **kwargs):
        print('Form - Post Request')
        question_text = request.POST.get('question_text')
        print(question_text)
        print(self.request.user)

        print('----')
        print(Author.objects.filter(user = self.request.user).__dict__)
        question = Question.objects.create(author = Author.objects.get(user = self.request.user ), question_text = question_text)
        print(question.__dict__)
        print('-------------------------')
        print("Question created successfully!")
        response = redirect('/myquora/questions')
        return response


class AnswerCreate(LoginRequiredMixin, CreateView):
    model = Answer
    fields = ['answer_text', 'credits']

    def get(self, request, *args, **kwargs):
        print('Form - Get Request')
        qId = request.GET.get('qId')
        return render(request, 'myquora/answer_form.html',{"pk_ans" : qId })

    def post(self, request, *args, **kwargs):
        print('Form - Post Request')
        answer_text = request.POST.get('answer_text')
        print(answer_text)
        print(self.request.user)

        print('----')
        print(Author.objects.filter(user = self.request.user).__dict__)
        answer = Answer.objects.create(author = Author.objects.get(user = self.request.user ), question=Question.objects.get(id = self.kwargs['pk']), answer_text = answer_text)
        print(answer.__dict__)
        print('-------------------------')
        print("Answer created successfully!")
        response = redirect('/myquora/questions')
        return response


class AuthorCreate(CreateView):
    model = Author
    fields = ['email', 'credits']

    def get(self, request, *args, **kwargs):
        print('Form - Get Request')
        return render(request, 'myquora/author_form.html')

    def post(self, request, *args, **kwargs):
        print('Form - Post Request')
        username = request.POST.get('username')
        print(username)
        password1  = request.POST.get('password1')
        password2  = request.POST.get('password2')
        email = request.POST.get('email')

        if password1 == password2 : 
            hasher = PBKDF2PasswordHasher()
            password = hasher.encode(password=password1,
                                  salt='salt',
                                  iterations=150000)

            user = User.objects.create(username = username, password = password)
            author = Author.objects.create(user = user, email = email, )
            print(author.__dict__)
            print(user.__dict__)
            print('-------------------------')
            print("User created successfully!")
            response = redirect('/myquora/questions')
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
    """Generic class-based detail view for a Answer."""
    model = Author
    paginate_by = 3


    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     author_id = self.kwargs['pk']
    #     context['author'] = Author.objects.filter(id=author_id)
    #     print(author_id)
    #     print(context['author'])
    #     return context


class QuestionDetailView(generic.DetailView):
    """Generic class-based detail view for a Answer."""
    model = Question
    paginate_by = 3
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(context)
        questionId = self.kwargs['pk']
        print(questionId)
        question = Question.objects.get(id=questionId)
        context['answer_list'] = Answer.objects.filter(question=question)
        context['answer_url'] = '/myquora/question/' + str(questionId) + '/answer'
        context['upvote_url'] = '/myquora/question/' + str(questionId) + '/answer'
        context['downvote_url'] = '/myquora/question/' + str(questionId) + '/answer'
        context["qId"] = questionId
        
        return context


class AnswerListView(generic.ListView):
    model = Answer
    paginate_by = 3


class UpvoteDetailView(generic.DetailView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(context)
        questionId = self.kwargs['pk']
        print(questionId)
        question = Question.objects.get(id=questionId)
        context['answer_list'] = Answer.objects.filter(question=question)
        context['answer_url'] = '/myquora/question/' + str(questionId) + '/answer'
        context['upvote_url'] = '/myquora/question/' + str(questionId) + '/answer'
        context['downvote_url'] = '/myquora/question/' + str(questionId) + '/answer'
        
        return context


class QuestionListView(generic.ListView):
    model = Question
    paginate_by = 10


    # def get_queryset(self):
    #     return Question.objects.filter()[:5] # Get 5 questions containing the title war


def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_questions = Question.objects.all().count()
    num_answers = Answer.objects.all().count()
    num_authors = Author.objects.count()
    num_comments = Comment.objects.count()
    # The 'all()' is implied by default. 
    
    context = {
        'num_questions': num_questions,
        'num_answers': num_answers,
        'num_authors': num_authors,
        'num_comments': num_comments,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)