from .models import Tag
def menu(request):
    new_tags=Tag.objects.all()[:3]
    return {'new_tags':new_tags}