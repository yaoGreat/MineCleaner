#!/usr/bin/python
import game

class MineRunner(object):
	def __init__(self):
		self.__g = None

	@property
	def g(self):
		return self.__g

	def run(self, size, rate, f):
		self.__g = game.MineGame()
		self.__g.Init(size, rate)
		step = 0
		while self.__g.result == game.MG_PLAYING:
			x, y = f(self.__g)
			#print("get from f: %d, %d" % (x, y))
			self.__g.do_click(x, y)
			step += 1

		score = 0
		if self.__g.result == game.MG_WIN:
			score = size * size * 2 - step
		else:
			score = step

		return score

class FooTest(object):
	def __init__(self):
		self.x = 0
		self.y = 0

	def f(self, g):
		self.x += 1
		if self.x == g.size:
			self.x = 0
			self.y += 1
			if self.y == g.size:
				self.y = 0
		return self.x, self.y

if __name__=='__main__':
	runner = MineRunner()
	test = FooTest()
	sum_score = 0
	count = 1000
	for i in range(count):
		score = runner.run(10, 0.05, test.f)
		sum_score += score
	avg_score = float(sum_score) / count
	print("avg_score: %f" % (avg_score))
