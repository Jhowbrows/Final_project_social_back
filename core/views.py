
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import git

@csrf_exempt
def update(request):
    if request.method == "POST":
        repo = git.Repo('/home/Jhowjhow/Final_project_social_back')
        origin = repo.remotes.origin
        origin.pull()
        return HttpResponse("Servidor atualizado com sucesso!")
    else:
        return HttpResponse("Método não permitido.", status=405)