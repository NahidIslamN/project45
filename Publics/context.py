
from management.models import Notification





#fjasdfjsdjflds

def notification(request):
    try:
        user = request.user
        notification = Notification.objects.filter(recever = user, seen_status = False).count()           
    except:
        notification = 0

    return {'nn':notification}