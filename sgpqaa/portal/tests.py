from datetime import date

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from .models import MemberProfile, MonthlyQuota, PaymentRecord, QuotaConfig, Vehicle


class HomePageTests(TestCase):
    def test_home_page_loads(self):
        response = self.client.get(reverse('portal:home'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Controle as quotas dos associados')


class AuthenticationFlowTests(TestCase):
    def test_register_creates_user_and_profile(self):
        response = self.client.post(
            reverse('portal:register'),
            {
                'first_name': 'Ana',
                'last_name': 'Silva',
                'username': 'ana',
                'email': 'ana@example.com',
                'member_number': 'ANATA-001',
                'phone': '923000000',
                'identity_card': '123456LA042',
                'password1': 'SenhaForte#2026',
                'password2': 'SenhaForte#2026',
            },
        )

        self.assertRedirects(response, reverse('portal:dashboard'))
        self.assertTrue(User.objects.filter(username='ana').exists())
        self.assertTrue(MemberProfile.objects.filter(member_number='ANATA-001').exists())

    def test_login_allows_access_to_dashboard(self):
        user = User.objects.create_user(username='maria', password='SenhaForte#2026')
        MemberProfile.objects.create(user=user, member_number='ANATA-002')

        response = self.client.post(
            reverse('portal:login'),
            {'username': 'maria', 'password': 'SenhaForte#2026'},
        )

        self.assertRedirects(response, reverse('portal:dashboard'))

    def test_dashboard_requires_login(self):
        response = self.client.get(reverse('portal:dashboard'))
        self.assertEqual(response.status_code, 302)

    def test_superuser_is_redirected_to_django_admin(self):
        user = User.objects.create_superuser(username='rootadmin', email='root@example.com', password='SenhaForte#2026')
        self.client.login(username='rootadmin', password='SenhaForte#2026')

        response = self.client.get(reverse('portal:dashboard'))

        self.assertRedirects(response, '/admin/')


class VehicleFlowTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='joao', password='SenhaForte#2026')
        self.profile = MemberProfile.objects.create(user=self.user, member_number='ANATA-003')

    def test_authenticated_user_can_register_vehicle(self):
        self.client.login(username='joao', password='SenhaForte#2026')

        response = self.client.post(
            reverse('portal:vehicles'),
            {
                'plate_number': 'LD-45-90-AA',
                'model': 'Toyota Corolla',
                'year': 2020,
                'color': 'Branco',
            },
        )

        self.assertRedirects(response, reverse('portal:vehicles'))
        self.assertTrue(Vehicle.objects.filter(owner=self.profile, plate_number='LD-45-90-AA').exists())

    def test_user_can_deactivate_own_vehicle(self):
        vehicle = Vehicle.objects.create(
            owner=self.profile,
            plate_number='LD-55-10-BB',
            model='Hyundai i10',
            year=2019,
            color='Cinza',
        )
        self.client.login(username='joao', password='SenhaForte#2026')

        response = self.client.post(reverse('portal:vehicle_deactivate', args=[vehicle.id]))

        self.assertRedirects(response, reverse('portal:vehicles'))
        vehicle.refresh_from_db()
        self.assertFalse(vehicle.is_active)


class QuotaAndTreasuryFlowTests(TestCase):
    def setUp(self):
        self.member_user = User.objects.create_user(username='carlos', password='SenhaForte#2026')
        self.member_profile = MemberProfile.objects.create(
            user=self.member_user,
            member_number='ANATA-004',
            role=MemberProfile.Role.MEMBER,
        )
        self.treasurer_user = User.objects.create_user(username='tesoureiro', password='SenhaForte#2026')
        self.treasurer_profile = MemberProfile.objects.create(
            user=self.treasurer_user,
            member_number='ANATA-T01',
            role=MemberProfile.Role.TREASURER,
        )
        self.vehicle = Vehicle.objects.create(
            owner=self.member_profile,
            plate_number='LD-88-11-CC',
            model='Kia Rio',
            year=2021,
            color='Preto',
        )

    def test_active_quota_config_generates_quotas_automatically(self):
        QuotaConfig.objects.create(
            amount='25000.00',
            late_fee_percentage='10.00',
            effective_from=date(2026, 6, 10),
            is_active=True,
        )

        self.assertTrue(
            MonthlyQuota.objects.filter(vehicle=self.vehicle, reference_month=date(2026, 6, 1)).exists()
        )

    def test_treasury_report_shows_overdue_quota_with_fine(self):
        QuotaConfig.objects.create(
            amount='25000.00',
            late_fee_percentage='10.00',
            effective_from=date(2026, 6, 10),
            is_active=True,
        )
        quota = MonthlyQuota.objects.create(
            vehicle=self.vehicle,
            reference_month=date(2026, 5, 1),
            due_date=date(2026, 5, 10),
            amount_due='25000.00',
            status=MonthlyQuota.Status.PENDING,
        )
        self.client.login(username='tesoureiro', password='SenhaForte#2026')

        response = self.client.get(reverse('portal:treasury_reports'))

        self.assertEqual(response.status_code, 200)
        quota.refresh_from_db()
        self.assertEqual(quota.status, MonthlyQuota.Status.OVERDUE)
        self.assertContains(response, '2500,00 AOA')
        self.assertContains(response, 'Debitos e multas por atraso')

    def test_treasurer_is_redirected_to_treasury_dashboard(self):
        self.client.login(username='tesoureiro', password='SenhaForte#2026')

        response = self.client.get(reverse('portal:dashboard'))

        self.assertRedirects(response, reverse('portal:treasurer_dashboard'))

    def test_member_can_submit_transfer_proof_for_pending_quota(self):
        quota = MonthlyQuota.objects.create(
            vehicle=self.vehicle,
            reference_month=date(2026, 6, 1),
            due_date=date(2026, 6, 10),
            amount_due='25000.00',
            status=MonthlyQuota.Status.PENDING,
        )
        self.client.login(username='carlos', password='SenhaForte#2026')
        proof = SimpleUploadedFile('comprovante.pdf', b'%PDF-1.4 comprovante bancario', content_type='application/pdf')

        response = self.client.post(
            reverse('portal:simulate_payment', args=[quota.id]),
            {
                'notes': 'Pagamento de teste',
                'proof_file': proof,
            },
        )

        self.assertRedirects(response, reverse('portal:quotas'))
        quota.refresh_from_db()
        self.assertEqual(quota.status, MonthlyQuota.Status.AWAITING_VALIDATION)
        self.assertTrue(PaymentRecord.objects.filter(quota=quota, status=PaymentRecord.Status.SUBMITTED).exists())

    def test_member_cannot_submit_non_pdf_transfer_proof(self):
        quota = MonthlyQuota.objects.create(
            vehicle=self.vehicle,
            reference_month=date(2026, 6, 1),
            due_date=date(2026, 6, 10),
            amount_due='25000.00',
            status=MonthlyQuota.Status.PENDING,
        )
        self.client.login(username='carlos', password='SenhaForte#2026')
        proof = SimpleUploadedFile('comprovante.png', b'fake image', content_type='image/png')

        response = self.client.post(
            reverse('portal:simulate_payment', args=[quota.id]),
            {
                'notes': 'Pagamento de teste',
                'proof_file': proof,
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'O comprovante deve ser enviado em formato PDF.')

    def test_treasurer_can_validate_transfer_payment(self):
        quota = MonthlyQuota.objects.create(
            vehicle=self.vehicle,
            reference_month=date(2026, 6, 1),
            due_date=date(2026, 6, 10),
            amount_due='25000.00',
            status=MonthlyQuota.Status.AWAITING_VALIDATION,
        )
        payment = PaymentRecord.objects.create(
            quota=quota,
            method=PaymentRecord.Method.BANK_TRANSFER,
            status=PaymentRecord.Status.SUBMITTED,
            amount_paid='25000.00',
            payment_date='2026-06-02T10:00:00Z',
            proof_file=SimpleUploadedFile('comprovante.pdf', b'%PDF-1.4 comprovante', content_type='application/pdf'),
        )
        self.client.login(username='tesoureiro', password='SenhaForte#2026')

        review_response = self.client.get(reverse('portal:review_payment', args=[payment.id]))
        response = self.client.post(reverse('portal:validate_payment', args=[payment.id]))

        self.assertEqual(review_response.status_code, 200)
        self.assertContains(review_response, 'Abrir PDF')
        self.assertRedirects(response, reverse('portal:treasurer_dashboard'))
        payment.refresh_from_db()
        quota.refresh_from_db()
        self.assertEqual(payment.status, PaymentRecord.Status.VALIDATED)
        self.assertEqual(payment.validated_by, self.treasurer_profile)
        self.assertEqual(quota.status, MonthlyQuota.Status.PAID)

    def test_treasurer_can_mark_cash_payment_as_paid(self):
        quota = MonthlyQuota.objects.create(
            vehicle=self.vehicle,
            reference_month=date(2026, 6, 1),
            due_date=date(2026, 6, 10),
            amount_due='25000.00',
            status=MonthlyQuota.Status.PENDING,
        )
        self.client.login(username='tesoureiro', password='SenhaForte#2026')

        response = self.client.post(reverse('portal:mark_cash_payment', args=[quota.id]))

        self.assertRedirects(response, reverse('portal:treasurer_dashboard'))
        quota.refresh_from_db()
        payment = PaymentRecord.objects.get(quota=quota)
        self.assertEqual(quota.status, MonthlyQuota.Status.PAID)
        self.assertEqual(payment.method, PaymentRecord.Method.CASH)
        self.assertEqual(payment.status, PaymentRecord.Status.VALIDATED)

    def test_member_can_view_payment_history_and_receipt(self):
        quota = MonthlyQuota.objects.create(
            vehicle=self.vehicle,
            reference_month=date(2026, 6, 1),
            due_date=date(2026, 6, 10),
            amount_due='25000.00',
            status=MonthlyQuota.Status.PAID,
        )
        payment = PaymentRecord.objects.create(
            quota=quota,
            method=PaymentRecord.Method.CASH,
            status=PaymentRecord.Status.VALIDATED,
            amount_paid='25000.00',
            payment_date='2026-06-02T10:00:00Z',
            validated_by=self.treasurer_profile,
            validated_at='2026-06-02T10:05:00Z',
        )
        self.client.login(username='carlos', password='SenhaForte#2026')

        history_response = self.client.get(reverse('portal:payment_history'))
        receipt_response = self.client.get(reverse('portal:payment_receipt', args=[payment.id]))

        self.assertEqual(history_response.status_code, 200)
        self.assertContains(history_response, 'Historico de pagamentos')
        self.assertEqual(receipt_response.status_code, 200)
        self.assertContains(receipt_response, 'Recibo de pagamento')
