from forum.models import Thread, Response

def latestposts(request):
	return {
		'latestthreads': Thread.objects.order_by('-pub_date')[:5],
		'latestresponses': Response.objects.order_by('-pub_date')[:5],
	}
