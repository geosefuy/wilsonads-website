from django_cron import CronJobBase, Schedule
from .models import *
from datetime import datetime, timedelta

class MyCronJob(CronJobBase):
    RUN_EVERY_MINS = 5

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'eshop.my_cron_job'    # a unique code

    def do(self):
        time_threshold = datetime.now() - timedelta(minutes=15)
        orders = Order.objects.filter(status='Pending',date_ordered__lte=time_threshold)
        
        for order in orders:
            items = order.orderitem_set.all()
            for item in items:
                product = Product.objects.get(id=item.product.id)
                product.stock = product.stock + item.quantity
                product.save()
        
        orders.delete()
                



