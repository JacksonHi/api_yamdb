import csv
import os

from django.core.management.base import BaseCommand

from reviews.models import Comments, Review
from titles.models import Category, Genre, Title, TitleGenre
from users.models import User


def file_load(model_orm, file_name_csv):
    with open(file_name_csv, encoding='utf8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if 'category' in row:
                row['category'] = Category.objects.get(id=row['category'])
            if 'author' in row:
                row['author'] = User.objects.get(id=row['author'])
            if 'title_id' in row:
                row['title'] = Title.objects.get(id=row['title_id'])
            if 'review_id' in row:
                row['review'] = Review.objects.get(id=row['review_id'])
            if 'genre_id' in row:
                row['genre'] = Genre.objects.get(id=row['genre_id'])

            print(row)
            if not model_orm.objects.filter(pk=row['id']).exists():
                obj = model_orm.objects.create(**row)
            # obj, created = model_orm.objects.update_or_create(**row)
            # if created:
                print(obj)


class Command(BaseCommand):
    help = ('Load data from csv. Если не проходят миграции или загрузка данных'
            ' нужно выполить python manage.py migrate titles zero')

    def add_arguments(self, parser):
        parser.add_argument(
            'file_path',
            type=str,
            help='Путь к csv файлам, из которого будут загружаться данные'
        )

    def handle(self, *args, **options):
        file_path = options['file_path']
        file_list = []
        for (root, dirs, files) in os.walk(file_path):
            for file in files:
                if not (file.endswith('.csv')):
                    continue
                file_list.append(file)
        if 'category.csv' in file_list:
            self.stdout.write('category')
            file_load(Category, file_path + '\\category.csv')

        if 'genre.csv' in file_list:
            self.stdout.write('genre')
            file_load(Genre, file_path + '\\genre.csv')

        if 'users.csv' in file_list:
            self.stdout.write('users')
            file_load(User, file_path + '\\users.csv')

        if 'titles.csv' in file_list:
            self.stdout.write('titles')
            file_load(Title, file_path + '\\titles.csv')

        if 'review.csv' in file_list:
            self.stdout.write('review')
            file_load(Review, file_path + '\\review.csv')

        if 'comments.csv' in file_list:
            self.stdout.write('***********comments')
            file_load(Comments, file_path + '\\comments.csv')

        if 'genre_title.csv' in file_list:
            self.stdout.write('*************genre_title')
            file_load(TitleGenre, file_path + '\\genre_title.csv')

        self.stdout.write('*************загрузка завершена**************')
