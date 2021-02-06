function deletePost(url) {
	if (confirm('Are you sure you want to delete this blog post?')) {
		window.location.pathname = url
	}
}