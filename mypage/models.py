from django.db import models
from django.utils import timezone

from accounts.models import User

# Create your models here.


class UniversityArea(models.Model):
    university_area = models.CharField(max_length=100)

    def __str__(self):
        return self.university_area

    class Meta:
        verbose_name = '都道府県'
        verbose_name_plural = '都道府県一覧'


class University(models.Model):
    university = models.CharField(max_length=100)
    # 学校が国立か私立か
    university_system = models.IntegerField(
        verbose_name='大学法人',
        choices=(
            (0, '国立'),
            (1, '公立'),
            (2, '私立'),
            (3, 'その他'),
        ),
        blank=False)
    # 学校HP
    university_website = models.URLField(blank=True)
    # 学校の都道府県(必須)
    university_area = models.ForeignKey(UniversityArea, on_delete=models.CASCADE, related_name='university_in_area')

    def __str__(self):
        return self.university

    class Meta:
        verbose_name = '大学'
        verbose_name_plural = '大学一覧'


class Faculty(models.Model):
    faculty = models.CharField(max_length=100)
    # 所属している大学
    belong_university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='faculty_in_university')

    def __str__(self):
        return self.faculty

    class Meta:
        verbose_name = '学部'
        verbose_name_plural = '学部一覧'


class Department(models.Model):
    department = models.CharField(max_length=100)
    # 所属している専攻
    belong_faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='department_in_faculty')

    def __str__(self):
        return self.department

    class Meta:
        verbose_name = '学科・専攻'
        verbose_name_plural = '学科・専攻一覧'


class Laboratory(models.Model):
    # 研究室名（必須）
    laboratory_name = models.CharField(max_length=100)
    # 所属している学校（必須）
    belong_university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='lab_in_university')
    # 所属している学部(必須)
    belong_faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='lab_in_faculty')
    # 所属している学科専攻（必須）
    belong_department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='lab_in_department')
    # ページ作成日時（必須）
    create_date = models.DateField(auto_now=True)

    def publish(self):
        self.create_date = timezone.now()
        self.save()

    def __str__(self):
        return self.laboratory_name

    class Meta:
        verbose_name = '研究室'
        verbose_name_plural = '研究室一覧'


class ExaminationInfo(models.Model):
    # 入試の専攻
    department = models.OneToOneField(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        related_name='examination_info'
    )
    # 院試日時
    examination_date = models.DateField(blank=True, null=True)
    # 院試詳細
    detail_info = models.TextField()
    # ページ作成日時（必須）
    page_create_date = models.DateField(auto_now=True)
    # 更新日時
    page_update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.department.__str__() + '入試情報'

    class Meta:
        verbose_name = '学科・専攻入試情報'
        verbose_name_plural = '学科・専攻入試情報一覧'


class NotificationsForLaboratory(models.Model):
    # タイトル
    title = models.CharField(max_length=100)
    # 通知の種類
    kind_of_notification = models.CharField(max_length=100)
    # 研究室
    laboratory = models.ForeignKey(
        Laboratory,
        on_delete=models.CASCADE,
        related_name='notification_for_laboratory'
    )
    # 通知作成日時
    create_date = models.DateField(auto_now=True)
    # 通知内容
    notification_detail = models.TextField()
    # 送信者
    send_user = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='send_for_laboratory'
    )

    def __str__(self):
        return '研究室通知   ' + ' ' + self.title

    class Meta:
        verbose_name = '研究室通知メッセージ'
        verbose_name_plural = '研究室通知メッセージ一覧'


class NotificationsForUser(models.Model):
    # タイトル
    title = models.CharField(max_length=100)
    # 通知の種類
    kind_of_notification = models.CharField(max_length=100)
    # 研究室
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notification_for_user'
    )
    # 通知作成日時
    create_date = models.DateField(auto_now=True)
    # 通知内容
    notification_detail = models.TextField()
    # 送信者
    send_user = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='send_for_user'
    )

    def __str__(self):
        return '通知   ' + self.user.__str__() + ' ' + self.title

    class Meta:
        verbose_name = '通知メッセージ'
        verbose_name_plural = '通知メッセージ一覧'
