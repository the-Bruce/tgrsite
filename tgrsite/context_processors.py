from forum.models import Thread, Response

def latestposts(request):
	print(Response.objects.order_by('pub_date'))
	print(Response.objects.all())

	return {
		'latestthreads': Thread.objects.order_by('-pub_date')[:5],
		'latestresponses': Response.objects.order_by('-pub_date')[:5],
	}
