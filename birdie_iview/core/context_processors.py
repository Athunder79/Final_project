from .models import Round


# context processor to display return to incomplete round link on all pages
def incomplete_rounds(request):
    if request.user.is_authenticated:
        return {'incomplete_rounds': Round.objects.filter(user=request.user, round_completed=False)}
    else:
        return {'incomplete_rounds': None}
