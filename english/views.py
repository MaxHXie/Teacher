from django.views import generic

# Create your views here.
class IndexView(generic.ListView):
    template_name = 'english/index.html'
    context_object_name = 'latest_question_list'
