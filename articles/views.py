from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView

from articles.forms import CommentForm, ReplyForm
from articles.models import ArticlePost, ArticleCategory, ArticleTag, ArticleComment, ArticleReply


class PostDetailView(DetailView):
    model = ArticlePost

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if not obj.is_public and not self.request.user.is_authenticated:
            raise Http404
        return obj

    def get_context_data(self, queryset=None, **kwargs):
        obj = super().get_object(queryset=queryset)
        images_query = obj.images_of_article_post.all()
        print(images_query)
        context = super().get_context_data(**kwargs)
        n = 0
        for image_query in images_query:
            context['image_{}'.format(n)] = image_query
            n += 1
            print(image_query.content_image)
        print(context)
        return context


class IndexView(ListView):
    model = ArticlePost
    template_name = 'articles/index.html'
    paginate_by = 3


class CategoryPostView(ListView):
    model = ArticlePost
    template_name = 'articles/category_post.html'

    def get_queryset(self):
        category_slug = self.kwargs['category_slug']
        self.category = get_object_or_404(ArticleCategory, slug=category_slug)
        qs = super().get_queryset().filter(category=self.category)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


class TagPostView(ListView):
    model = ArticlePost
    template_name = 'articles/tag_post.html'

    def get_queryset(self):
        tag_slug = self.kwargs['tag_slug']
        self.tag = get_object_or_404(ArticleTag, slug=tag_slug)
        qs = super().get_queryset().filter(tags=self.tag)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.tag
        return context


class SearchPostView(ListView):
    model = ArticlePost
    template_name = 'articles/search_post.html'
    paginate_by = 3

    def get_queryset(self):
        query = self.request.GET.get('q', None)
        lookups = (
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(category__name__icontains=query) |
            Q(tags__name__icontains=query)
        )
        if query is not None:
            qs = super().get_queryset().filter(lookups).distinct()
            return qs
        qs = super().get_queryset()
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q')
        context['query'] = query
        return context


class CategoryListView(ListView):
    queryset = ArticleCategory.objects.annotate(
        num_posts=Count('articlepost', filter=Q(articlepost__is_public=True)))


class TagListView(ListView):
    queryset = ArticleTag.objects.annotate(num_posts=Count(
        'articlepost', filter=Q(articlepost__is_public=True)))


class CommentFormView(CreateView):
    model = ArticleComment
    form_class = CommentForm

    def form_valid(self, form):
        comment = form.save(commit=False)
        post_pk = self.kwargs['pk']
        comment.post = get_object_or_404(ArticlePost, pk=post_pk)
        comment.save()
        return redirect('articles:post_detail', pk=post_pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post_pk = self.kwargs['pk']
        context['articlepost'] = get_object_or_404(ArticlePost, pk=post_pk)
        return context


@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(ArticleComment, pk=pk)
    comment.approve()
    return redirect('articles:post_detail', pk=comment.post.pk)


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(ArticleComment, pk=pk)
    comment.delete()
    return redirect('articles:post_detail', pk=comment.post.pk)


class ReplyFormView(CreateView):
    model = ArticleReply
    form_class = ReplyForm

    def form_valid(self, form):
        reply = form.save(commit=False)
        comment_pk = self.kwargs['pk']
        reply.comment = get_object_or_404(ArticleComment, pk=comment_pk)
        reply.save()
        return redirect('articles:post_detail', pk=reply.comment.post.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comment_pk = self.kwargs['pk']
        context['articlecomment'] = get_object_or_404(ArticleComment, pk=comment_pk)
        return context


@login_required
def reply_approve(request, pk):
    reply = get_object_or_404(ArticleReply, pk=pk)
    reply.approve()
    return redirect('articles:post_detail', pk=reply.comment.post.pk)


@login_required
def reply_remove(request, pk):
    reply = get_object_or_404(ArticleReply, pk=pk)
    reply.delete()
    return redirect('articles:post_detail', pk=reply.comment.post.pk)
