from django.shortcuts import render

# "Static" pages
def schedule(request):
	return render(request, 'statics/schedule.html')

def gallery(request):
	return render(request, 'statics/gallery.html')
def larp_lore(request):
	return render(request, 'statics/larp_lore.html')
def larp_info(request):
	return render(request, 'statics/larp_info.html')
