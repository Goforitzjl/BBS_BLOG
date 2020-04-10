from django import template
from app1.models import *
from django.db.models import Count, Avg, Min, Max

register = template.Library()


@register.inclusion_tag("classification.html")
def Classfication(user):
    # 将每一个站点的category的title和category中的文章数量给分组查询出来
    category_list = Category.objects.filter(blog=user.blog).values("pk").annotate(
        c=Count("article__title")).values_list("title", "c")
    # 将每一个站点的tag的title和tag中的文章数量给分组查询出来
    tag_list = Tag.objects.filter(blog=user.blog).values("pk").annotate(
        c=Count("article__title")).values_list("title", "c")
    # 将每一个站点的文章按年月来分类,
    # 方法1
    # y_m_date = Article.objects.extra(select={
    #     "y_m_date": "date_format(create_time,'%%Y-%%m')"}).values_list("title", "y_m_date")
    # 方法2
    from django.db.models.functions import TruncMonth
    date_list = Article.objects.filter(user=user).annotate(month=TruncMonth("create_time")
                                                           ).values("month").annotate(c=Count("nid")).values_list(
        "month", "c")
    return {"category_list": category_list, "tag_list": tag_list, "date_list": date_list,"user":user}
