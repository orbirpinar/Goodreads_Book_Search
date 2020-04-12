import os
#https://stackoverflow.com/a/34115677
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "library.settings")
import django
django.setup()
import csv

from books.models import Books


def main():

	with open('books.csv','r') as f:
		reader = csv.reader(f)

		next(reader)

		for row in reader:
			created = Books.objects.get_or_create(
				isbn = row[0],
				title = row[1],
				author = row[2],
				year = row[3]
				)
if __name__=='__main__':
	main()
