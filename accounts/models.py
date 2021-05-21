from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone


class CustomUserManager(UserManager):
    """ユーザーマネージャー"""
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('status_position', 100)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """カスタムユーザーモデル."""

    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=False)
    last_name = models.CharField(_('last name'), max_length=150, blank=False)
    # 所属している大学
    university = models.ForeignKey(
        'mypage.University',
        on_delete=models.PROTECT,
        related_name='user_belong_to_university')
    # 所属している学部
    faculty = models.ForeignKey(
        'mypage.Faculty',
        on_delete=models.PROTECT,
        related_name='user_belong_to_faculty')
    # 所属している学科・専攻
    department = models.ForeignKey(
        'mypage.Department',
        on_delete=models.PROTECT,
        related_name='user_belong_to_department')
    # 所属している研究室
    laboratory = models.ForeignKey(
        'mypage.Laboratory',
        on_delete=models.PROTECT,
        related_name='user_belong_to_laboratory',
        blank=True,
        null=True)
    status_position = models.IntegerField(
        _('身分'),
        choices=(
            (0, '学部1年生'),
            (1, '学部2年生'),
            (2, '学部3年生'),
            (3, '学部4年生'),
            (4, '学部5年生'),
            (5, '学部6年生'),
            (6, '修士1年生'),
            (7, '修士2年生'),
            (8, '博士1年生'),
            (9, '博士2年生'),
            (10, '博士3年生'),
            (11, '研究室関係者(教員)'),
            (12, 'その他'),
        ),
        blank=False)
    # 研究室関係者かどうか
    is_lab_member = models.BooleanField(
        _('研究室関係者'),
        default=False,
        help_text=_(
            'True: 研究室関係者, False: 学生'
        )
    )
    # お気に入り研究室
    favorite_laboratory = models.ManyToManyField(
        'search.LaboratoryInfo',
        blank=True,
        verbose_name='お気に入り研究室',
        related_name='person_favorite_laboratory_info'
    )
    # お気に入り登録の通知
    favorite_laboratory_notification = models.BooleanField(
        _('お気に入り登録の通知'),
        default=True,
    )

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = CustomUserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        """Return the first_name plus the last_name, with a space in
        between."""
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    @property
    def username(self):
        """username属性のゲッター

        他アプリケーションが、username属性にアクセスした場合に備えて定義
        メールアドレスを返す
        """
        return self.email


class UniversityEmail(models.Model):
    university = models.ForeignKey(
        'mypage.University',
        on_delete=models.PROTECT,
        related_name='email_of_university')
    university_email_domain = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.university.university + '『' + self.university_email_domain + '』'

    class Meta:
        verbose_name = '認証用大学メールアドレス'
        verbose_name_plural = '認証用大学メールアドレス一覧'


class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name='ユーザープロフィール',
        related_name='profile'
    )

    # ニックネーム
    nickname = models.CharField(blank=True, null=True, max_length=50)
    # 自信が行っている研究内容
    research_detail = models.TextField(blank=True, null=True)
    # 興味のある研究
    interested_area = models.TextField(blank=True, null=True)
    # 予定進路
    future_works = models.TextField(blank=True, null=True)
    # 自由記入
    free_comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.last_name + 'プロフィール'

    class Meta:
        verbose_name = 'プロフィール'
        verbose_name_plural = 'プロフィール一覧'
