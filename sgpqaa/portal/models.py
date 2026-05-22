from django.contrib.auth.models import User
from django.db import models


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class MemberProfile(TimeStampedModel):
    class Role(models.TextChoices):
        MEMBER = 'member', 'Associado'
        TREASURER = 'treasurer', 'Tesoureiro'
        ADMIN = 'admin', 'Administrador'

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='member_profile')
    member_number = models.CharField('Numero de associado', max_length=30, unique=True)
    phone = models.CharField('Telefone', max_length=20, blank=True)
    identity_card = models.CharField('BI', max_length=30, blank=True)
    staff_name = models.CharField('Staff', max_length=120, blank=True)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.MEMBER)
    is_active_member = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'perfil de associado'
        verbose_name_plural = 'perfis de associados'

    def __str__(self):
        return f'{self.user.get_full_name() or self.user.username} ({self.member_number})'


class Vehicle(TimeStampedModel):
    owner = models.ForeignKey(MemberProfile, on_delete=models.PROTECT, related_name='vehicles')
    plate_number = models.CharField('Matricula', max_length=20, unique=True)
    model = models.CharField('Modelo', max_length=100)
    year = models.PositiveIntegerField('Ano')
    color = models.CharField('Cor', max_length=50)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'veiculo'
        verbose_name_plural = 'veiculos'
        ordering = ['plate_number']

    def __str__(self):
        return f'{self.plate_number} - {self.model}'


class QuotaConfig(TimeStampedModel):
    amount = models.DecimalField('Valor da quota', max_digits=10, decimal_places=2)
    late_fee_percentage = models.DecimalField(
        'Percentagem de multa',
        max_digits=5,
        decimal_places=2,
        default=0,
    )
    effective_from = models.DateField('Vigora a partir de')
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'configuracao de quota'
        verbose_name_plural = 'configuracoes de quota'
        ordering = ['-effective_from']

    def __str__(self):
        return f'Quota {self.amount} AOA desde {self.effective_from}'


class MonthlyQuota(TimeStampedModel):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pendente'
        AWAITING_VALIDATION = 'awaiting_validation', 'Aguarda validacao'
        PAID = 'paid', 'Paga'
        OVERDUE = 'overdue', 'Em atraso'

    vehicle = models.ForeignKey(Vehicle, on_delete=models.PROTECT, related_name='monthly_quotas')
    reference_month = models.DateField('Mes de referencia')
    due_date = models.DateField('Data de vencimento')
    amount_due = models.DecimalField('Valor a pagar', max_digits=10, decimal_places=2)
    status = models.CharField(max_length=30, choices=Status.choices, default=Status.PENDING)
    generated_automatically = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'quota mensal'
        verbose_name_plural = 'quotas mensais'
        ordering = ['-reference_month', 'vehicle__plate_number']
        unique_together = ('vehicle', 'reference_month')

    def __str__(self):
        return f'{self.vehicle.plate_number} - {self.reference_month:%m/%Y}'


class PaymentRecord(TimeStampedModel):
    class Method(models.TextChoices):
        CASH = 'cash', 'Pagamento em maos'
        BANK_TRANSFER = 'bank_transfer', 'Transferencia bancaria'

    class Status(models.TextChoices):
        PENDING = 'pending', 'Pendente'
        SUBMITTED = 'submitted', 'Comprovante submetido'
        VALIDATED = 'validated', 'Validado'
        REJECTED = 'rejected', 'Rejeitado'

    quota = models.ForeignKey(MonthlyQuota, on_delete=models.PROTECT, related_name='payments')
    method = models.CharField(max_length=20, choices=Method.choices)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    amount_paid = models.DecimalField('Valor pago', max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField('Data do pagamento')
    simulated_reference = models.CharField(max_length=50, blank=True)
    proof_file = models.FileField(upload_to='payment_proofs/', blank=True)
    validated_by = models.ForeignKey(
        MemberProfile,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='validated_payments',
    )
    validated_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField('Observacoes', blank=True)

    class Meta:
        verbose_name = 'registo de pagamento'
        verbose_name_plural = 'registos de pagamento'
        ordering = ['-payment_date']

    def __str__(self):
        return f'Pagamento {self.quota} - {self.get_method_display()}'
