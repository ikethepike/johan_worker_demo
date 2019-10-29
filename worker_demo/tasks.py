from worker_demo.celery import app
from players.models import Player


@app.task(bind=True)
def process_row(self, row):
    players = Player.objects.all()
    total = sum(map(lambda player: player.height, players))
    height =  row[' "Height(inches)"']
    average = 0

    if height:
        average = height 
    else: 
        height = 0 

    if len(players):
        average = total / len(players)

    try:
        Player.objects.create(
            name=row["Name"],
            height=height,
            current_average_height=average,
        )
    except Exception as e:
        print(e)
        print("Uh-oh we had an error, better deal with it gracefully")
        pass

    return True

