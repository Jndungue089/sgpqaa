from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import MemberProfile, Vehicle


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
