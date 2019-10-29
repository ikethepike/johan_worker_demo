import csv
from worker_demo.tasks import process_row
from django.http import HttpResponse


def index(request):

    # You wouldn't want to do this normally in a view...
    with open("mlb_players.csv", newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Let's send individual jobs to our task in tasks.py
            # ASYNC
            process_row.delay(row)

            # SYNCHRONOUS
            # process_row(row)

    return HttpResponse(
        "Worker queue started, as I do not have access to the sample data, \n we are going to use a basic example instead, finding out the average height of the MLB"
    )
