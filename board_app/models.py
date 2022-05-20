from django.db import models
from django.utils import timezone
from datetime import datetime, timedelta


# Create your models here.
class Board(models.Model):
    author = models.CharField(max_length=10, null=False)
    title = models.CharField(max_length=100, null=False)
    content = models.TextField(null=False)
    modified_date = models.DateTimeField(auto_now=True)
    registered_date = models.DateTimeField(auto_now_add=True, verbose_name='등록시간')
    hits = models.PositiveIntegerField(verbose_name='조회수', default=0)
    comments = models.PositiveIntegerField(verbose_name='댓글수', null=True)

    @property
    def created_string(self):
        time = datetime.now(tz=timezone.utc).replace(tzinfo=None) - self.registered_date

        if time < timedelta(minutes=1):
            return '방금 전'
        elif time < timedelta(hours=1):
            return str(int(time.seconds / 60)) + '분 전'
        elif time < timedelta(days=1):
            return str(int(time.seconds / 3600)) + '시간 전'
        elif time < timedelta(days=7):
            time = datetime.now(tz=timezone.utc).date() - self.registered_date.date()
            return str(time.days) + '일 전'
        else:
            return False

    class Meta:
        db_table = '자유게시판'
        verbose_name = '자유게시판'
        verbose_name_plural = '자유게시판'

class Comment(models.Model):
    post = models.ForeignKey(Board, on_delete=models.CASCADE, verbose_name='게시글')
    writer = models.CharField(max_length=10, null=True, verbose_name='댓글작성자')
    content = models.TextField(verbose_name='댓글내용')
    created = models.DateTimeField(auto_now_add=True, verbose_name='작성일')
    deleted = models.BooleanField(default=False, verbose_name='삭제여부')
    reply = models.IntegerField(verbose_name='답글위치', default=0, null=True)
    
    def __str__(self):
        return self.content

    @property
    def created_string(self):
        time = datetime.now(tz=timezone.utc).replace(tzinfo=None) - self.created

        if time < timedelta(minutes=1):
            return '방금 전'
        elif time < timedelta(hours=1):
            return str(int(time.seconds / 60)) + '분 전'
        elif time < timedelta(days=1):
            return str(int(time.seconds / 3600)) + '시간 전'
        elif time < timedelta(days=7):
            time = datetime.now(tz=timezone.utc).date() - self.created.date()
            return str(time.days) + '일 전'
        else:
            return False 
    class Meta:
        db_table = '자유게시판 댓글'
        verbose_name = '자유게시판 댓글'
        verbose_name_plural = '자유게시판 댓글'
