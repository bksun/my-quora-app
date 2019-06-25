from django.shortcuts import render

# Create your views here.

from myquora.models import Question, Answer, Comment, Author

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