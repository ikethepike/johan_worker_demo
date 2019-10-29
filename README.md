# Worker demonstration

I think that the most likely reason for the code timing out is simply due to the quantity of data being analyzed, and the constraints of python. In cases where a process runs the risk of timing out; or where running a process on the main thread would cause it to freeze up, it is generally good practice to distribute that work to a worker/queue. Effectively, a worker is a scalable, detached instance that runs on a separate thread that can handle smaller tasks asynchronously. A common example of a worker would be uploading an image to a social network, here multiple workers will begin to process the image. The first worker and primary worker will receive the upload, and quickly optimize the image for delivery. After this process is done, the image will be ready to view on the site. At this point, a second machine learning worker will kick in. This worker will analyze the optimized image using adverserial classification to suggest an alt tag, and/or for more nefarious advertising and or privacy invading reasons. Both these processes are cpu intensive, and would hold up processing on the main thread. Moreover, if there was a timeout (as seems to be the case with your code), there is very little in the way of elegant error handling, rather than to simply restart the process and hope for the best. Workers solve this, as they are handed small, bitesized chunks of a larger process. If a task fails within the queue (the items that get fed to the worker to get processed), we have graceful means of handling any errors and can re-process the job or move it to the back of the queue, allowing more items to be processed in between.

## Challenges and concepts

[Video outling how to use workers](https://www.youtube.com/watch?v=fg-JfZBetpM)

Worker tasks are **asynchronous** and quite often **bitesized**. In your data processing example it poses a somewhat interesting challenge, as each row needs an understanding of previous rows. These presents us with two paths forward, either we can manually set a lengthy timeout, allowing the worker to run to its natural conclusion with the same code as is currently written (just migrated over to a worker task file instead). Or we can dispatch a job for each of the rows from our `iterrows()` function, and use the database as an intermediary, to store all the data. The latter presents a possible complication, which is what happens when processing of an individual row fails.

### Dependencies

- [Celery](https://docs.celeryproject.org/en/latest/django/first-steps-with-django.html)
- [Django](https://docs.djangoproject.com/en/2.2/intro/tutorial01/)
- [Python 3](https://www.python.org/downloads/)
- [Pip 10+](https://pip.pypa.io/en/stable/installing/)
- [Redis](https://redislabs.com/blog/redis-on-windows-10/)  
  Redis is a pub/sub database that allows for socketed communication, if you have used something like Google firebase it is very similar. It's tricky to get running on windows. [Here is a tutorial using the linux subsystem on windows](https://redislabs.com/blog/redis-on-windows-10/). Normally I'd recommend running a setup like this in an virtualized environment like Docker, but it felt a bit overkill in a demo like this. Once the environment is set up, to verify that the install was successful run `celery -A worker_demo worker -l info`. If everything has been installed successfully, it should connect correctly and report back a successful connection to `redis://localhost:6379`.
- [A way of browsing DB lite](https://sqlitebrowser.org/dl/)

## Getting started

- Ensure that all dependencies are installed and verifiably work
- start django server by running `python manage.py runserver` in root dir
- ensure that redis instance is up and running (in wsl on windows)
- navigate to `http://localhost:8000/worker` and the view will dispatch worker jobs
- after processing is done, open database and records should be listed

## Key files

The wrapper for this demo project is `Django`, which is an [MVC](https://en.wikipedia.org/wiki/Model%E2%80%93view%E2%80%93controller). I'm using it here to have a basic scaffold and functionality to build on. As of such, a lot of the files here are largely unrelated to the nuts and bolts of our workers, the main files to explore are:

- `worker_demo/views.py`
- `worker_demo/tasks.py`
- `players/models.py`

In `tasks.py`, I've commented out an synchronous function call to process our rows. I would recommend toggling between these to see the difference in performance.
