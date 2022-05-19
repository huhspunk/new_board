from django.db import models


# Create your models here.
class Board(models.Model):
    author = models.CharField(max_length=10, null=False)
    title = models.CharField(max_length=100, null=False)
    content = models.TextField(null=False)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

class Comment(models.Model):
    post = models.ForeignKey(Board, on_delete=models.CASCADE, verbose_name='게시글')
    writer = models.CharField(max_length=10, null=False)
    content = models.TextField(verbose_name='댓글내용')
    created = models.DateTimeField(auto_now_add=True, verbose_name='작성일')
    deleted = models.BooleanField(default=False, verbose_name='삭제여부')
    
    def __str__(self):
        return self.content

    class Meta:
        db_table = '자유게시판 댓글'
        verbose_name = '자유게시판 댓글'
        verbose_name_plural = '자유게시판 댓글'
