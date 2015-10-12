import matplotlib.pyplot as plt

buckets = [0] * 100
newBuckets = [0] * 100

def hdhash(s, n):
	return sum(map(ord,s)) % n

def run():
	for i in range(50000):
		s = "TI"+str(i).zfill(5)
		b = hdhash(s, 100)
		buckets[b] = buckets[b] + 1
		nb = newhash(s, 100)
		newBuckets[nb] = newBuckets[nb] + 1

def showGraph(buckets):
	index = [ x for x in range(100)]
	plt.bar(index, buckets)
	plt.show()

def calCost(buckets):
	cost = 0
	for i in range(100):
		cost += buckets[i] ** 2
	return cost

def newhash(s, n):
	s = s[2 :]
	d = int(s)
	return d / 500

run()
print buckets
print calCost(buckets)
showGraph(buckets)
print newBuckets
print calCost(newBuckets)
showGraph(newBuckets)



