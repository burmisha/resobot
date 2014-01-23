#!/usr/bin/python
import sys

d = 0.0025 	# delta = 0.25%
C = 0.3 	# max sell

class market:
	def __init__(self, X, Y):
		self.X = X
		self.Y = Y
		self.p = None
		self.am = None
	def pr(self):
		print self.X, self.Y, self.p, self.am

A = market(300, 0)
B = market(0, 1000)
# profit = 0

log = open('log.txt','w')

def answer(summ):
	if summ >= 0.01/(1-d):
		print summ
		sys.stdout.flush()
		return summ
	elif summ <= -0.01/(1-d):
		print summ
		sys.stdout.flush()
		return summ
	else: 
		print 'no-op'
		sys.stdout.flush()
		return 0

while True:
	line = sys.stdin.readline().strip()
	if line == 'END':
		sys.exit(0)
	if line.startswith('OK'):
		[A.X, A.Y, B.X, B.Y, profit] = map(float, line.split(',')[1:6])
		# log.write('OK!\n')
		# log.write(' '.join(map(str,[A.X, A.Y, B.X, B.Y, profit, '\n'])))
		continue
	log.write(line)
	[ts, A.p, A.am, B.p, B.am] = map(float, line.split(','))
	if B.p*(1-d)**2 > A.p:
		# log.write(' '.join(map(str, ['buy X at A is min of',A.Y*C/A.p, B.X*C/(1-d), A.am, B.am*(1-d), '\n'])))
	 	s = min(A.Y*C/A.p, B.X*C/(1-d), A.am, B.am)
	 	a = answer(s)
	# 	A.X += a * (1-d)
	# 	A.Y += -a * A.p
	# 	B.X += -a * (1-d)
	# 	B.Y += a * (1-d)**2 * B.p
	# 	profit += a * (B.p*(1-d)**2 - A.p)
	elif A.p*(1-d)**2 > B.p:
		# log.write(' '.join(map(str, ['buy X at B is min of', B.Y*C/B.p, A.X*C/(1-d), B.am, A.am*(1-d), '\n'])))
	 	s = min(B.Y*C/B.p, A.X*C/(1-d), B.am, A.am)		 # why not A.am/(1-d) ??
		a = -answer(-s)
	#	B.X += a * (1-d)
	#	B.Y += -a * B.p
	#	A.X += -a * (1-d)
	#	A.Y += a * (1-d)**2 * A.p
	#	profit += a * (A.p*(1-d)**2 - B.p)
	else:
		a = answer(0)
		
# log.write("===\nProfit: %f" % profit)
log.close()

