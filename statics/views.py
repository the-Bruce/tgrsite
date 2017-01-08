from django.shortcuts import render

# Create your views here.
def schedule(request):
	return render(request, 'statics/schedule.html')

def gallery(request):
	return render(request, 'statics/gallery.html')