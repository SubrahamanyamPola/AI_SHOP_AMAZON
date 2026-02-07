from django.conf import settings

def revolut_link(request):
    return {"REVOLUT_ME_LINK": getattr(settings, "REVOLUT_ME_LINK", "")}
