from django.db import models
from datetime import datetime

# Create your models here.

from organization.models import CourseOrg,Teacher
from DjangoUeditor.models import UEditorField


class Course(models.Model):
    course_org = models.ForeignKey(CourseOrg,on_delete=models.CASCADE,verbose_name='所属课程机构',null=True,blank=True)
    teacher = models.ForeignKey(Teacher,on_delete=models.CASCADE,verbose_name='授课老师',null=True,blank=True)
    name = models.CharField(max_length=50,verbose_name='课程名')
    desc = models.CharField(max_length=300,verbose_name='课程描述')
    detail = UEditorField(verbose_name='产品介绍', width=1000, height=600, imagePath='courses/ueditor/',
                          filePath='courses/ueditor/', default='')
    is_banner = models.BooleanField(default=False,verbose_name='是否轮播')
    degree = models.CharField(max_length=10,choices=(('cj','初级'),('zj','中级'),('gj','高级')),verbose_name='难度')
    learn_times = models.IntegerField(default=0,verbose_name='学习时长(分钟数)')
    student = models.IntegerField(default=0,verbose_name='学习人数')
    fav_nums = models.IntegerField(default=0,verbose_name='收藏')
    image = models.ImageField(upload_to='courses/%Y/%m',verbose_name='封面图',max_length=100)
    click_nums = models.IntegerField(default=0,verbose_name='点击数')
    category = models.CharField(default='后端开发',max_length=20,verbose_name='课程类别')
    tag = models.CharField(default='',verbose_name='课程标签',max_length=10)
    your_know = models.CharField(default='',max_length=300,verbose_name='课程须知')
    teacher_know = models.CharField(default='',max_length=300,verbose_name='老师告诉你')
    add_time = models.DateTimeField(default=datetime.now,verbose_name='添加时间')

    class Meta:
        verbose_name = '课程'
        verbose_name_plural = verbose_name

    def get_zj_nums(self):
        #获取课程章节数
        all_lessons = self.lesson_set.all().count()
        return all_lessons
    get_zj_nums.short_description = '章节数'

    def go_to(self):
        from django.utils.safestring import mark_safe
        return mark_safe('<a href="http://www.baidu.com">跳转</a>')

    go_to.short_description = '跳转'

    def get_learn_users(self):
        return self.usercourse_set.all()[:5]

    def get_course_lesson(self):
        return self.lesson_set.all()

    def __str__(self):
        return self.name


class Lesson(models.Model):
    course = models.ForeignKey(Course,on_delete=models.CASCADE,verbose_name='课程')
    name = models.CharField(max_length=100,verbose_name='章节名')
    add_time = models.DateTimeField(default=datetime.now,verbose_name='添加时间')

    class Meta:
        verbose_name = '章节'
        verbose_name_plural = verbose_name

    def get_lesson_video(self):
        return self.video_set.all()

    def __str__(self):
        return self.name


class Video(models.Model):
    lesson = models.ForeignKey(Lesson,on_delete=models.CASCADE,verbose_name='章节')
    name = models.CharField(max_length=100,verbose_name='视频名')
    learn_times = models.IntegerField(default=0, verbose_name='学习时长(分钟数)')
    url = models.URLField(max_length=200,default='',verbose_name='访问网址')
    add_time = models.DateTimeField(default=datetime.now,verbose_name='添加时间')

    class Meta:
        verbose_name = '视频'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseResource(models.Model):
    course = models.ForeignKey(Course,on_delete=models.CASCADE,verbose_name='课程')
    name = models.CharField(max_length=100,verbose_name='名称')
    download = models.FileField(upload_to='course/resource/%Y/%m',verbose_name='资源名称',max_length=100)
    add_time = models.DateTimeField(default=datetime.now,verbose_name='添加时间')

    class Meta:
        verbose_name = '课程资源'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

