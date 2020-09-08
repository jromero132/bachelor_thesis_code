base = 2 ** 8
def get_hash(text):
	ans = 0
	for c in text:
		ans *= base
		ans += ord(c)
	return ans