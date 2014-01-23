#!/usr/bin/python
import sys, getopt

class market:
	def __init__(self, X, Y, name):
		self.X = X
		self.Y = Y
		self.p = None
		self.am = None
		# self.name = name
	def pr(self):
		print(self.X, self.Y, self.p, self.am)

class history:
	def __init__(self):
		self.data = []
		self.amount = []
		self.ts = []
		self.num = 200
		self.basic_mean = []
		self.expo_mean = [0]
		self.delta = []
		# self.expo_delta = [0]
	@staticmethod
	def equal_mean(data, length):
		return sum(data[-length:]) / len(data[-length:])
	def ready(self):
		return len(self.data) >= self.num
	def append(self, data, amount, ts):
		if amount < 1:
			return
		if len(self.data) > 0:
			if data == self.data[-1] and amount == self.amount[-1] and ts == self.ts[-1]:
				return
		self.data.append(data)
		self.amount.append(data)
		self.ts.append(data)
		bm = self.equal_mean(self.data, self.num)
		if self.ready():
			bm = self.expo_mean[-1]
		self.basic_mean.append(bm)
		self.delta.append(data - bm)
		prop = 0.02
		self.expo_mean.append((1 - prop) * self.expo_mean[-1]  + prop * data)
		# self.expo_delta.append((1 - prop) * self.expo_delta[-1]  + prop * (data - bm))
	def mean(self):
		return self.basic_mean[-1] + self.equal_mean(self.delta, round(self.num/2)) # self.expo_delta[-1]
		
d = 0.0025 	# delta = 0.25 %
min_deal = 0.01/(1-d)

def worth(summ):
	return abs(summ) >= min_deal

# def answerArbitrage(summ):
# 	if abs(summ) >= min_deal:
# 		print("%.8f,%.8f" % (summ, -summ))
# 	else: 
# 		print('no-op')
# 	sys.stdout.flush()
	
def give_answer(A,B):
	[a, b] = ['0'] * 2
	if worth(A):
		a = '%.8f' % (A*0.99999)
	if worth(B):
		b = '%.8f' % (B*0.99999)
	if not worth(A) and not worth(B):
		print('no-op')
	else: 
		print(a + ',' + b)
	sys.stdout.flush()

def usage():
	print("""
Get profit from nothing as banks usually do.
Resolventa, Changellenge Cup Technical, 2013.
  -a, --first=	- 	first parameter
  -b, --second=	- 	second parameter
	""")

def maxArbitrage(marketToBuyX, marketToSellX, maxPart):
	return min(marketToBuyX.Y*maxPart/marketToBuyX.p, marketToSellX.X*maxPart/(1-d), marketToBuyX.am, marketToSellX.am)

def maxBuy(market, maxPart):
	return min(market.Y*maxPart/market.p, market.am)

def maxSell(market, maxPart):
	return -min(market.X*maxPart, market.am)

def main():
	C = 1	# max sell on market A (alpha)
	Q = 0.455	# max sell on market B (beta) 
	
	log = open('log.txt','w')
	inp = open('input.txt', 'w')
	deal = open('deal.txt', 'w')

	try:
		opts, args = getopt.getopt(sys.argv[1:], "a:b:h", ["first=", "second=", "help"])
	except getopt.GetoptError as err:
		log.write(str(err)) # will print something like "option -a not recognized"
		usage()
		sys.exit(2)
	for o, arg in opts:
		if o in ("-h", "--help"):
			usage()
			sys.exit(0)
		elif o in ("-a", "--first"):
			C = float(arg)
		elif o in ("-b", "--second"):
			Q = float(arg)

	A = market(300, 0, 'A')
	B = market(0, 1000, 'B')
	pAh = history()
	pBh = history()
	profit = 0
	ts = 0
	# dd = (1-d)**2
	# num = 150
	# [prices, pA, pB]=[[], [], []]
	while True:
		line = sys.stdin.readline().strip()
		if line == 'END':
			sys.exit(0)
		elif line.startswith('ERROR'):
			log.write(line)
			log.write('\n')
			continue
		elif line.startswith('OK'):
			[A.X, A.Y, B.X, B.Y, profit] = map(float, line.split(',')[1:6])
			# inp.write('OK,%.8f,%.8f,%.8f,%.8f,%.8f\n' % (A.X, A.Y, B.X, B.Y, profit))
			deal.write('%d,%.8f,%.8f,%.8f,%.8f,%.8f\n' % (ts, A.X, A.Y, B.X, B.Y, profit))
			continue

		[ts, A.p, A.am, B.p, B.am] = map(float, line.split(','))
		if A.p < 0 or B.p < 0 or A.am < 0 or B.am < 0:
			log.write('ERROR: incorrect input\n')
			answerArbitrage(0)
			continue

		if len(pAh.data) > 0:
			log.write('%d,%.3f,%.3f,%.3f,%.3f,%.3f,%.3f,%.3f,%.3f,%.3f\n' % (ts, A.X, A.Y, B.X, B.Y, A.p, B.p, pAh.mean(), pBh.mean(), profit))
		inp.write('%d,%.3f,%.8f,%.3f,%.8f\n' % (ts, A.p, A.am, B.p, B.am))
		
		pAh.append(A.p, A.am, ts)
		pBh.append(B.p, B.am, ts)

		# p = A.p/B.p
		# if dd > p and worth(maxArbitrage(A, B, C)):
		# 	answerArbitrage(maxArbitrage(A, B, C)) # buy at A
		# 	# answerArbitrage(0) # skip
		# 	continue
		# elif p > 1/dd and worth(maxArbitrage(B, A, Q)):
		# 	answerArbitrage(-maxArbitrage(B, A, Q)) # buy at B
		# 	# answerArbitrage(0) # skip
		# 	continue

		[a, b] = [0, 0]
		s = 0.01

		if A.p > pAh.mean() / (1 - s):
			a = maxSell(A, C)
		elif A.p < pAh.mean() * (1 - s):
			a = maxBuy(A, C)
		
		if B.p > pBh.mean() / (1 - s):
			b = maxSell(B, C)
		elif B.p < pBh.mean() * (1 - s):
			b = maxBuy(B, C)

		give_answer(a, b)
		continue
	log.close()
	inp.close()
	deal.close()

if __name__ == "__main__":
	main()
