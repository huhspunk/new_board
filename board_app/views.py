from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.serializers.json import DjangoJSONEncoder
from .models import *
import json


# Create your views here.
def index(request):
    boards = {'boards': Board.objects.all()}
    return render(request, 'list.html', boards)


def post(request):
    if request.method == "POST":
        author = request.POST['author']
        title = request.POST['title']
        content = request.POST['content']
        board = Board(author=author, title=title, content=content)
        board.save()
        return HttpResponseRedirect(reverse('board:index'))
    else:
        return render(request, 'post.html')

def delete(request, pk):
    board = Board.objects.get(id=pk)
    board.delete()
    return redirect('board:index')

def detail(request, pk):
    try:
        board = Board.objects.get(id=pk)
    except Board.DoesNotExist:
        raise Http404("Does not exist!")
    return render(request, 'detail.html', {'board': board})

def comment_write_view(request, pk):
    post = get_object_or_404(Board, id=pk)
    writer = request.POST.get('writer')
    content = request.POST.get('content')
    print(request.user)
    if content:
        comment = Comment.objects.create(post=post, content=content, writer=request.user)
        post.save()
        data = {
            'writer': writer,
            'content': content,
            'created': '방금 전',
            'comment_id': comment.id
        }
        if request.user == 'Anonymous':
            data['self_comment'] = '익명'

        return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder), content_type = "application/json")


