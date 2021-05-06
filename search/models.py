from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils import timezone

from accounts.models import User

# Create your models here.


class Laboratory(models.Model):
    # 研究室名（必須）
    laboratory_name = models.CharField(max_length=100)
    # 学校（必須）
    university = models.CharField(max_length=100)
    # 学校の都道府県
    university_area = models.IntegerField(default=0, blank=True)
    # 学校が国立か私立か
    university_system = models.IntegerField(default=0, blank=True)
    # 学校HP
    university_website = models.URLField(blank=True)
    # 学部
    faculty = models.CharField(max_length=100, blank=True)
    # 学科専攻（必須）
    department = models.CharField(max_length=100)
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
    create_date = models.DateField(auto_now=True)
    # 更新日時
    update_date = models.DateTimeField(auto_now=True)
    # 情報元webページ（必須）
    information_source = models.URLField()
    # 情報の確認
    confirmation = models.BooleanField(null=True)
    # 作成者情報
    uploader = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='uploader')

    def publish(self):
        self.create_date = timezone.now()
        self.save()

    def __str__(self):
        return self.laboratory_name

    class Meta:
        verbose_name = '研究室'
        verbose_name_plural = '研究室一覧'


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
    paper_info = models.TextField(blank=True)
    laboratory = models.ForeignKey(Laboratory, on_delete=models.CASCADE,
                                   blank=True, null=True, related_name='paper_uploader')

    paper_file = models.FileField(
        upload_to='uploads/',
        verbose_name='研究論文',
        validators=[FileExtensionValidator(['pdf', ])],
    )

    def __str__(self):
        return self.paper_title

    class Meta:
        verbose_name = '論文'
        db_table = 'research_paper'
