from django.shortcuts import render

# Create your views here
from .forms import MainProjectForm
from django.http import HttpResponse

import threading
from queue import Queue
from mainapp.helpers.spider import Spider
from mainapp.helpers.domain import get_domain_name, get_sub_domain_name
from mainapp.helpers.general import (
        create_dir,
        create_data_files,
        write_file,
        append_to_file,
        delete_file_contents,
        file_to_set,
        set_to_file
    )

# Create your views here.


def index(request):

    form = MainProjectForm()

    if request.method == 'POST':
        form = MainProjectForm(request.POST)

        if form.is_valid():
            form.save(commit=False)
            form.save()


            DOMAIN_NAME = get_domain_name(str(request.POST['HOMEPAGE']))
            QUEUE_FILE = str(request.POST['PROJECT_NAME']) + '/queue.txt'
            CRAWLED_FILE = str(request.POST['PROJECT_NAME']) + '/crawled.txt'
            NUMBER_OF_THREADS = 8
            queue = Queue()
            Spider(str(request.POST['PROJECT_NAME']), str(request.POST['HOMEPAGE']), DOMAIN_NAME)

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
                queued_links = len(file_to_set(QUEUE_FILE))
                if queued_links > 0:
                    print(f'{queued_links} links in the queue')
                    create_jobs()

            create_workers()
            crawl()

            return HttpResponse('We have started crawling the website.')
        else:
            return HttpResponse('Something went wrong while submitting the URL, please check again?')

    return render(request, 'index.html', {'form': form})
