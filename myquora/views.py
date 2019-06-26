from django.shortcuts import render

# Create your views here.

from myquora.models import Question, Answer, Comment, Author

from django.views import generic

class AnswerListView(generic.ListView):
    model = Answer
    paginate_by = 4


class QuestionListView(generic.ListView):
    model = Question
    paginate_by = 4

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