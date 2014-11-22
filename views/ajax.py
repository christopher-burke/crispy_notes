from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def star(request):
    if request.is_ajax() and request.POST:
        data = {'message': "%s starred." % request.POST.get('note-star')}
        print data

        return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        raise Http404
