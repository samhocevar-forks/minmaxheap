class MinMaxHeap(object):
	"""
	Implementation of a Min-max heap following Atkinson, Sack, Santoro, and
	Strothotte (1986): https://doi.org/10.1145/6617.6621
	"""
	def __init__(self, reserve=0):
		self.a = [None] * reserve
		self.size = 0

	def __len__(self):
		return self.size

	def insert(self, key):
		"""
		Insert key into heap. Complexity: O(log(n))
		"""
		if len(self.a) < self.size + 1:
			self.a.append(key)
		insert(self.a, key, self.size)
		self.size += 1

	def peekmin(self):
		"""
		Get minimum element. Complexity: O(1)
		"""
		return peekmin(self.a, self.size)

	def peekmax(self):
		"""
		Get maximum element. Complexity: O(1)
		"""
		return peekmax(self.a, self.size)

	def popmin(self):
		"""
		Remove and return minimum element. Complexity: O(log(n))
		"""
		m, self.size = removemin(self.a, self.size)
		return m

	def popmax(self):
		"""
		Remove and return maximum element. Complexity: O(log(n))
		"""
		m, self.size = removemax(self.a, self.size)
		return m


def level(i):
	return (i+1).bit_length() - 1


def comparer(i):
	if level(i) % 2 == 0:  # min level
		return lambda x, y: x < y
	else:
		return lambda x, y: x > y


def trickledown(array, i, size):
	cmp = comparer(i)

	while size > i * 2 + 1:  # i has children
		m = i * 2 + 1
		if m + 1 < size and cmp(array[m+1], array[m]):
			m += 1
		child = True
		for j in range(i*4+3, min(i*4+7, size)):
			if cmp(array[j], array[m]):
				m = j
				child = False

		if cmp(array[m], array[i]):
			array[i], array[m] = array[m], array[i]

		if child:
			break

		if cmp(array[(m-1) // 2], array[m]):
			array[m], array[(m-1)//2] = array[(m-1)//2], array[m]
		i = m


def bubbleup(array, i):
	cmp = comparer(i)
	if i > 0:
		m = (i - 1) // 2
		if cmp(array[m], array[i]):
			array[i], array[m] = array[m], array[i]
			i = m
			cmp = comparer(i)

	while i > 2:
		m = (i - 3) // 4
		if cmp(array[m], array[i]):
			break
		array[i], array[m] = array[m], array[i]
		i = m


def peekmin(array, size):
	assert size > 0
	return array[0]


def peekmax(array, size):
	assert size > 0
	if size == 1:
		return array[0]
	elif size == 2:
		return array[1]
	else:
		return max(array[1], array[2])


def removemin(array, size):
	assert size > 0
	elem = array[0]
	array[0] = array[size-1]
	# array = array[:-1]
	trickledown(array, 0, size - 1)
	return elem, size-1


def removemax(array, size):
	assert size > 0
	if size == 1:
		return array[0], size - 1
	elif size == 2:
		return array[1], size - 1
	else:
		i = 1 if array[1] > array[2] else 2
		elem = array[i]
		array[i] = array[size-1]
		# array = array[:-1]
		trickledown(array, i, size - 1)
		return elem, size-1


def insert(array, k, size):
	array[size] = k
	bubbleup(array, size)


def minmaxheapproperty(array, size):
	for i, k in enumerate(array[:size]):
		# check children and grandchildren to be larger (min level) or smaller (max level)
		cmp = comparer(i)
		children = range(2 * i + 1, min(2 * i + 3, size))
		grandchildren = range(4 * i + 3, min(4 * i + 7, size))
		for j in [*children, *grandchildren]:
			if cmp(array[j], k):
				print(array, j, i, array[j], array[i], level(i))
				return False

	return True


def test(n):
	from random import randint
	a = [-1] * n
	l = []
	size = 0
	for _ in range(n):
		x = randint(0, 5 * n)
		insert(a, x, size)
		size += 1
		l.append(x)
		assert minmaxheapproperty(a, size)

	assert size == len(l)
	print(a)

	while size > 0:
		assert min(l) == peekmin(a, size)
		assert max(l) == peekmax(a, size)
		if randint(0, 1):
			e, size = removemin(a, size)
			assert e == min(l)
		else:
			e, size = removemax(a, size)
			assert e == max(l)
		l[l.index(e)] = l[-1]
		l.pop(-1)
		assert len(a[:size]) == len(l)
		assert minmaxheapproperty(a, size)

	print("OK")


def test_heap(n):
	from random import randint
	heap = MinMaxHeap(n)
	l = []
	for _ in range(n):
		x = randint(0, 5 * n)
		heap.insert(x)
		l.append(x)
		assert minmaxheapproperty(heap.a, len(heap))

	assert len(heap) == len(l)
	print(heap.a)

	while len(heap) > 0:
		assert min(l) == heap.peekmin()
		assert max(l) == heap.peekmax()
		if randint(0, 1):
			e = heap.popmin()
			assert e == min(l)
		else:
			e = heap.popmax()
			assert e == max(l)
		l[l.index(e)] = l[-1]
		l.pop(-1)
		assert len(heap) == len(l)
		assert minmaxheapproperty(heap.a, len(heap))

	print("OK")
