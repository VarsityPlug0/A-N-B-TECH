from django.core.management.base import BaseCommand
from applications.models import Application
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Add test card data to existing applications for testing purposes'

    def add_arguments(self, parser):
        parser.add_argument(
            '--email',
            type=str,
            help='Email of the user to add test card data to (optional)',
        )
        parser.add_argument(
            '--all',
            action='store_true',
            help='Add test card data to all applications',
        )

    def handle(self, *args, **options):
        if options['email']:
            # Add test card data to specific user
            try:
                user = User.objects.get(email=options['email'])
                application = user.application
                self.add_test_card_data(application)
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully added test card data to {user.email}')
                )
            except User.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'User with email {options["email"]} not found')
                )
            except Application.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'Application not found for user {options["email"]}')
                )
        elif options['all']:
            # Add test card data to all applications
            applications = Application.objects.all()
            count = 0
            for application in applications:
                if not application.card_number:  # Only add if no card data exists
                    self.add_test_card_data(application)
                    count += 1
            self.stdout.write(
                self.style.SUCCESS(f'Successfully added test card data to {count} applications')
            )
        else:
            # Add test card data to first application without card data
            try:
                application = Application.objects.filter(card_number__isnull=True).first()
                if application:
                    self.add_test_card_data(application)
                    self.stdout.write(
                        self.style.SUCCESS(f'Successfully added test card data to {application.user.email}')
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING('No applications without card data found')
                    )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Error: {str(e)}')
                )

    def add_test_card_data(self, application):
        """
        Add test card data to an application
        """
        # Test card data
        test_card_data = {
            'card_number': '4111 1111 1111 1111',
            'card_expiry_month': '12',
            'card_expiry_year': '2025',
            'card_cvv': '123',
            'card_last4': '1111',
            'payment_method': 'card_verification',
            'payment_duration': 24
        }
        
        # Update application with test card data
        for field, value in test_card_data.items():
            setattr(application, field, value)
        
        application.save()
        
        self.stdout.write(
            f'Added test card data to application {application.id}: '
            f'Card: {test_card_data["card_number"]}, '
            f'Expiry: {test_card_data["card_expiry_month"]}/{test_card_data["card_expiry_year"]}, '
            f'CVV: {test_card_data["card_cvv"]}'
        ) 