'''
$ celery -A sagas.cloud.app_sagas worker -l info
'''
from __future__ import absolute_import, unicode_literals

from celery import Celery

app = Celery('sagas',
             broker='amqp://',
             backend='amqp://',
             include=['sagas.cloud.simple'])

# Optional configuration, see the application user guide.
app.conf.update(
    result_expires=3600,
)

if __name__ == '__main__':
    app.start()

