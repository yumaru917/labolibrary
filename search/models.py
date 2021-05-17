from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils import timezone

from accounts.models import User
from mypage.models import Laboratory

# Create your models here.


class LaboratoryInfo(models.Model):
    # 研究室(ここを変える。)
    laboratory = models.OneToOneField(Laboratory,
                                      on_delete=models.CASCADE, related_name='info_of_laboratory')
    # 学科専攻HP
    department_website = models.URLField(blank=True)
    # キャンパス
    campus = models.CharField(max_length=100, blank=True)
    # 担当教授（必須）
    professor_name = models.CharField(max_length=100)
    # 生徒数
    all_student_count = models.IntegerField(default=0, blank=True)
    master_count = models.IntegerField(default=0, blank=True)
    doctor_count = models.IntegerField(default=0, blank=True)
    # 進学先、就職先
    after_graduation = models.CharField(max_length=100, blank=True)
    # 研究テーマ・キーワード
    research_keywords = models.CharField(max_length=100, blank=True)
    # 研究詳細（必須）
    research_info = models.TextField()
    # 研究室HPのURL
    laboratory_website = models.URLField(blank=True)
    # 院試の時期
    entrance_examination_date = models.TextField(blank=True)
    # 院試の詳細
    entrance_examination_info = models.TextField(blank=True)
    # 院生受け入れ詳細
    master_acceptance = models.BooleanField(null=True)
    doctor_acceptance = models.BooleanField(null=True)
    adult_graduate_student_acceptance = models.BooleanField(null=True)
    # 院試難易度
    degree_of_difficulty = models.IntegerField(default=0, blank=True)
    # 研究室の空気
    environment = models.IntegerField(default=0, blank=True)
    # 内部生外部生の割合
    students_rate = models.IntegerField(default=0, blank=True)
    # 就職しやすい空気か
    Employment_rate = models.IntegerField(default=0, blank=True)
    # 口コミ
    free_comment = models.TextField(blank=True)
    # ページ作成日時（必須）
    page_create_date = models.DateField(auto_now=True)
    # 更新日時
    page_update_date = models.DateTimeField(auto_now=True)
    # 情報元webページ（必須）
    information_source = models.URLField()
    # 情報の確認
    confirmation = models.BooleanField(null=True)

    def publish(self):
        self.create_date = timezone.now()
        self.save()

    def __str__(self):
        return self.laboratory.laboratory_name

    class Meta:
        verbose_name = '記載研究室'
        verbose_name_plural = '記載研究室一覧'


class SearchText(models.Model):
    """
    検索された内容を格納するモデル
    """
    search_item = models.CharField('検索ワード', max_length=100)

    def __str__(self):
        return self.search_item

    class Meta:
        verbose_name = '検索ワード'
        db_table = 'search'


class ResearchPaper(models.Model):
    """
    検索された内容を格納するモデル
    """
    paper_title = models.CharField('論文タイトル', max_length=100)
    paper_kind = models.CharField('論文の種類', null=True, blank=True, max_length=100)
    paper_info = models.TextField(blank=True)
    laboratory = models.ForeignKey(LaboratoryInfo, on_delete=models.CASCADE,
                                   related_name='uploaded_paper')

    paper_file = models.FileField(
        upload_to='uploads/',
        verbose_name='研究論文',
        validators=[FileExtensionValidator(['pdf', ])],
    )
    paper_uploader = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='upload_paper'
    )

    def __str__(self):
        return self.paper_title

    class Meta:
        verbose_name = '論文'
        db_table = 'research_paper'
