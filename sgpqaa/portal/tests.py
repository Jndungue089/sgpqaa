from datetime import date

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import MemberProfile, MonthlyQuota, PaymentRecord, Vehicle


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

    def test_treasurer_can_generate_quotas_for_active_vehicles(self):
        self.client.login(username='tesoureiro', password='SenhaForte#2026')

        response = self.client.post(
            reverse('portal:treasurer_dashboard'),
            {
                'action': 'generate_quotas',
                'reference_month': '2026-06-01',
                'due_date': '2026-06-10',
                'amount': '25000.00',
            },
        )

        self.assertRedirects(response, reverse('portal:treasurer_dashboard'))
        self.assertTrue(
            MonthlyQuota.objects.filter(vehicle=self.vehicle, reference_month=date(2026, 6, 1)).exists()
        )

    def test_member_can_simulate_payment_for_pending_quota(self):
        quota = MonthlyQuota.objects.create(
            vehicle=self.vehicle,
            reference_month=date(2026, 6, 1),
            due_date=date(2026, 6, 10),
            amount_due='25000.00',
            status=MonthlyQuota.Status.PENDING,
        )
        self.client.login(username='carlos', password='SenhaForte#2026')

        response = self.client.post(
            reverse('portal:simulate_payment', args=[quota.id]),
            {
                'method': PaymentRecord.Method.MULTICAIXA,
                'notes': 'Pagamento de teste',
            },
        )

        self.assertRedirects(response, reverse('portal:quotas'))
        quota.refresh_from_db()
        self.assertEqual(quota.status, MonthlyQuota.Status.AWAITING_VALIDATION)
        self.assertTrue(PaymentRecord.objects.filter(quota=quota, status=PaymentRecord.Status.SIMULATED).exists())

    def test_treasurer_can_validate_simulated_payment(self):
        quota = MonthlyQuota.objects.create(
            vehicle=self.vehicle,
            reference_month=date(2026, 6, 1),
            due_date=date(2026, 6, 10),
            amount_due='25000.00',
            status=MonthlyQuota.Status.AWAITING_VALIDATION,
        )
        payment = PaymentRecord.objects.create(
            quota=quota,
            method=PaymentRecord.Method.CASH,
            status=PaymentRecord.Status.SIMULATED,
            amount_paid='25000.00',
            payment_date='2026-06-02T10:00:00Z',
        )
        self.client.login(username='tesoureiro', password='SenhaForte#2026')

        response = self.client.post(reverse('portal:validate_payment', args=[payment.id]))

        self.assertRedirects(response, reverse('portal:treasurer_dashboard'))
        payment.refresh_from_db()
        quota.refresh_from_db()
        self.assertEqual(payment.status, PaymentRecord.Status.VALIDATED)
        self.assertEqual(payment.validated_by, self.treasurer_profile)
        self.assertEqual(quota.status, MonthlyQuota.Status.PAID)
