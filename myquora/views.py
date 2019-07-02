from django.shortcuts import render
# Create your views here.
from myquora.models import Question, Answer, Comment, Author
from django.views import generic
from django.shortcuts import redirect

from django.urls import reverse_lazy, reverse
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


class UpdateAnswer(LoginRequiredMixin, UpdateView):
    model = Answer
    fields = ['answer_text']
    success_url = reverse_lazy('questions')
    template_name = 'myquora/answer_update_form.html'


class UpdateQuestion(LoginRequiredMixin, UpdateView):
    model = Question
    fields = ['question_text']
    success_url = reverse_lazy('questions')
    template_name = 'myquora/question_update_form.html'


class CommentCreate(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['author', 'answer', 'comment_text']

    def get(self, request, *args, **kwargs):
        print('Form - Get Request')
        a_id = self.kwargs['pk']
        return render(request, 'myquora/comment_form.html',{"a_id" : a_id })

    def post(self, request, *args, **kwargs):
        print('Comment Form - Post Request')
        request_path = request.path
        print('Path: ', request_path)
        # print('Path detail: ', request_path.__dict__)
        comment_text = request.POST.get('comment_text')
        print(comment_text)
        print(self.request.user)

        print('-------------------------')
        params = self.kwargs['pk']
        print('Id of answer: ', params)
        author = Author.objects.get(user=self.request.user)
        
        print('Author detail: ', author.__dict__)
        answer = Answer.objects.get(id=params)
        print('Answer detail: ', answer.__dict__)
        comment = Comment.objects.create(author=author, answer=answer, comment_text=comment_text)
        print(comment.__dict__)
        print('-------------------------')
        print("Comment created successfully!")
        response = redirect(reverse('question-detail', kwargs={'pk': answer.question.id}))
        return response


class UpvoteCreate(LoginRequiredMixin, CreateView):
    model = Answer
    fields = ['answer_text', 'id', 'upvote']

    def post(self, request, *args, **kwargs):
        print('Upvote - Form - Post Request')
        print('Username: ', self.request.user)
        answer_id = self.kwargs['pk']
        print('Answer id: ', answer_id)
        print('----')

        print('Author detail: ', Author.objects.filter(user=self.request.user).__dict__)
        answer = Answer.objects.get(id=answer_id)
        answer.upvote += + 1
        answer.save() 
        print('Answer detail: ', answer.__dict__)
        print('-------------------------')
        print("Answer upvoted successfully!")
        response = redirect(reverse('question-detail', kwargs={'pk': answer.question.id}))
        return response


class DownvoteCreate(LoginRequiredMixin, CreateView):
    model = Answer
    fields = ['answer_text', 'id', 'downvote']

    def post(self, request, *args, **kwargs):
        print('Downvote - Form - Post Request')
        print('Username: ', self.request.user)
        answer_id = self.kwargs['pk']
        print('Answer id: ', answer_id)
        print('----')

        print('Author detail: ', Author.objects.filter(user = self.request.user).__dict__)
        answer = Answer.objects.get(id = answer_id)
        answer.downvote += + 1
        answer.save() 
        print('Answer detail: ' , answer.__dict__)
        print('-------------------------')
        print("Answer downvoted successfully!")
        response = redirect(reverse('question-detail', kwargs={'pk': answer.question.id}))
        return response


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
    fields = ['answer_text']
    
    def get(self, request, *args, **kwargs):
        print('Form - Get Request')
        q_id = self.kwargs['pk']
        print(q_id)
        print('request get', request.GET.__dict__)
        return render(request, 'myquora/answer_form.html',{"q_id" : q_id })

    def post(self, request, *args, **kwargs):
        print('Form - Post Request')
        answer_text = request.POST.get('answer_text')
        print(answer_text)
        print(self.request.user)

        print('----')
        print('Id of question: ', self.kwargs['pk'])
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
        question_id = self.kwargs['pk']
        print(question_id)
        question = Question.objects.get(id=question_id)
        answer_list = Answer.objects.filter(question=question)

        print('Question: ', question)
        print('Question Type: ', type(question))
        print('Answer list: ', answer_list)
        print('Answer list is ready')
        # answer = Answer.objects.get(answer_text = 'Why US was not able to pressurize India to not buy the S-400 missiles from Russia?')
        # print('Answer: ', answer.__dict__)
  
        print('Finding comments for answer...')
        comment_dictionary = { ans.id: Comment.objects.filter(answer=ans) for ans in answer_list}

        # for ans in iter(answer_list):
        #     print('Answer: ', ans)
        #     print('Answer Id: ', ans.id)
        #     print('Answer Type: ', type(ans))
        #     comment_list = Comment.objects.filter(answer = ans)
        #     print('Comment List: ', comment_list)
        #     comment_dictionary[ans.id] = comment_list
        #     # ans['comments'] = comment_list
            # print('---------------------------------------')
            
        print('Comment list is ready')

        print('printing comment dictionary:', comment_dictionary)
        # keys,values in cars.items()
        for keys, values in comment_dictionary.items():
            print(keys, " -> ", values)
        print('Comments print is over')

        context['answer_list'] = answer_list
        context['answer_url'] = '/myquora/question/' + str(question_id) + '/answer/'
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