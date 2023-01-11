import faker
from django.core.management import BaseCommand
from django.db import transaction, IntegrityError

from products.models import Product, Category
from shop.constants import DECIMAL_PLACES


class Command(BaseCommand):
    help = "Create fake product in the database"

    def add_arguments(self, parser):
        parser.add_argument('-c', '--count', default=3, type=int)

    def handle(self, *args, **options):
        fake = faker.Faker()

        # category_name = fake.word()
        def callback():
            self.stdout.write(
                self.style.SUCCESS('OK'))

        for i in range(options['count']):
            try:
                with transaction.atomic():
                    transaction.on_commit(callback)
                    c = Category.objects.create(
                        name=fake.word(),
                        **{'description': fake.sentence()}
                    )
                    name = fake.word()
                    if i == 3:
                        name = None
                    product = Product.objects.create(
                        category=c,
                        name=name,
                        description=fake.sentence(),
                        price=fake.pydecimal(
                            min_value=1,
                            left_digits=DECIMAL_PLACES,
                            right_digits=DECIMAL_PLACES,
                        ),
                    )
            except IntegrityError:
                self.stdout.write(
                    self.style.ERROR('Error'))
                continue
            self.stdout.write(
                self.style.SUCCESS('Successfully create "%s"' % product.name))
