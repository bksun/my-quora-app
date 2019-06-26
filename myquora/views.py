from django.shortcuts import render

# Create your views here.

from myquora.models import Question, Answer, Comment, Author

from django.views import generic


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
        return context

class AnswerListView(generic.ListView):
    model = Answer
    paginate_by = 3

    



class QuestionListView(generic.ListView):
    model = Question
    paginate_by = 3


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