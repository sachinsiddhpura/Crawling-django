from django.shortcuts import render

# Create your views here
from .forms import MainProjectForm
from django.http import HttpResponse

import threading
from queue import Queue
from mainapp.helpers.spider import Spider
from mainapp.helpers.domain import *
from mainapp.helpers.general import *

# Create your views here.


def index(request):

    form = MainProjectForm()

    if request.method == 'POST':
        form = MainProjectForm(request.POST)

        if form.is_valid():
            form.save(commit=False)
            form.save()

            PROJECT_NAME = str(request.POST['PROJECT_NAME'])
            HOMEPAGE = str(request.POST['HOMEPAGE'])

            PROJECT_NAME_APP = PROJECT_NAME
            HOMEPAGE_APP = HOMEPAGE
            DOMAIN_NAME = get_domain_name(HOMEPAGE_APP)
            QUEUE_FILE = PROJECT_NAME_APP + '/queue.txt'
            CRAWLED_FILE = PROJECT_NAME_APP + '/crawled.txt'
            NUMBER_OF_THREADS = 8
            queue = Queue()
            Spider(PROJECT_NAME_APP, HOMEPAGE_APP, DOMAIN_NAME)

            # Create worker threads (will die when main exits)
            def create_workers():
                for _ in range(NUMBER_OF_THREADS):
                    t = threading.Thread(target=work)
                    t.daemon = True
                    t.start()

            # Do the next job in the queue
            def work():
                while True:
                    url = queue.get()
                    Spider.crawl_page(threading.current_thread().name, url)
                    queue.task_done()

            # Each queued link is a new job
            def create_jobs():
                for link in file_to_set(QUEUE_FILE):
                    queue.put(link)
                queue.join()
                crawl()

            # Check if there are items in the queue, if so crawl them
            def crawl():
                queued_links = file_to_set(QUEUE_FILE)
                if len(queued_links) > 0:
                    print(str(len(queued_links)) + ' links in the queue')
                    create_jobs()

            create_workers()
            crawl()

            return HttpResponse('We have started crawling the website.')
        else:
            return HttpResponse('Something went wrong while submitting the URL, please check again?')

    return render(request, 'index.html', {'form': form})
