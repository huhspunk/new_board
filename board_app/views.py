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
    board = get_object_or_404(Board, pk=pk)
    session_cookie = 'AnonymousUser'
    cookie_name = F'free_hits:{session_cookie}'
    comment = Comment.objects.filter(post=pk).order_by('created')
    # comment_count = comment.count()
    comment_count = comment.exclude(deleted=True).count()
    print(comment)
    reply = comment.exclude(reply='0')
    print(reply)

    if request.user == board.author:
        free_auth = True
    else:
        free_auth = False

    context = {
        'board': board,
        'free_auth': free_auth,
        'comments': comment,
        'comment_count': comment_count,
        'replys': reply,
    }
    response = render(request, 'detail.html', context)

    if request.COOKIES.get(cookie_name) is not None:
        cookies = request.COOKIES.get(cookie_name)
        cookies_list = cookies.split('|')
        if str(pk) not in cookies_list:
            response.set_cookie(cookie_name, cookies + f'|{pk}', expires=None)
            board.hits += 1
            board.save()
            return response
    else:
        response.set_cookie(cookie_name, pk, expires=None)
        board.hits += 1
        board.save()
        return response
    return render(request, 'detail.html', context)

def comment_write_view(request, pk):
    post = get_object_or_404(Board, id=pk)
    writer = request.POST.get('writer')
    content = request.POST.get('content')
    reply = request.POST.get('reply')
    print("========")
    print(reply)
    if content:
        comment = Comment.objects.create(post=post, content=content, writer=request.user, reply=reply)
        print(comment.id)
        comment_count = Comment.objects.filter(post=pk).exclude(deleted=True).count()
        post.comments = comment_count
        post.save()
        data = {
            'writer': writer,
            'content': content,
            'created': '방금 전',
            'comment_count': comment_count,
            'comment_id': comment.id
        }
        if request.user == post.author:
            data['self_comment'] = '(글쓴이)'

        return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder), content_type = "application/json")


