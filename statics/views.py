from django.shortcuts import render

# "Static" pages
def schedule(request):
	return render(request, 'statics/schedule.html')

def gallery(request):
	return render(request, 'statics/gallery.html')
