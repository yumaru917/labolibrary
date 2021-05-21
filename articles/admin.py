from django.contrib import admin

from articles.models import ArticleCategory, ArticleTag, ArticlePost, ArticleContentImage, ArticleComment, ArticleReply


class ArticleContentImageInline(admin.TabularInline):
    model = ArticleContentImage
    extra = 1


class ArticlePostAdmin(admin.ModelAdmin):
    inlines = [
        ArticleContentImageInline,
    ]


admin.site.register(ArticleCategory)
admin.site.register(ArticleTag)
admin.site.register(ArticlePost, ArticlePostAdmin)
admin.site.register(ArticleComment)
admin.site.register(ArticleReply)
