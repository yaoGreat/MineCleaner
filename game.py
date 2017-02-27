#!/usr/bin/python
import random

MS_COVER = 0
MS_SHOW = 1
MS_MINE_FLAG = 2

MD_MINE = -1

MG_PLAYING = 0
MG_WIN = 1
MG_LOSE = 2

class MineGame(object):
	def __init__(self):
		self.__SIZE = 0
		self.__data = None
		self.__status = None
		self.__around_idx = [(-1, -1), (-1, 0), (-1, 1), \
							(0, -1), (0, 1), \
							(1, -1), (1, 0), (1, 1)]
		self.__result = MG_PLAYING

	@property
	def size(self):
		return self.__SIZE

	@property
	def result(self):
		return self.__result

	def Init(self, _size, _rate):
		self.__SIZE = _size
		self.__data = [[self.__randomCell(_rate) for x in range(_size)] for y in range(_size)]
		self.__status = [[0 for x in range(_size)] for y in range(_size)]
		for x in range(self.__SIZE):
			for y in range(self.__SIZE):
				self.__calMineNumber(x, y)
		self.__result = MG_PLAYING

	def do_click(self, x, y):
		if self.__status[y][x] == MS_COVER:
			self.__status[y][x] = MS_SHOW

			if self.__data[y][x] == MD_MINE:
				self.__result = MG_LOSE
				return

			if self.__check_win():
				self.__result = MG_WIN
				return

			if self.__data[y][x] == 0:
				for xx, yy in self.__around_xy(x, y):
					if self.__data[yy][xx] != MD_MINE and self.__status[yy][xx] == MS_COVER:
						self.do_click(xx, yy)

	def do_flag(self, x, y):
		if self.__status[y][x] == MS_COVER:
			self.__status[y][x] = MS_MINE_FLAG
		elif self.__status[y][x] == MS_MINE_FLAG:
			self.__status[y][x] = MS_COVER

	def do_auto_click(self, x, y):
		if self.__status[y][x] == MS_SHOW and self.__data[y][x] > 0:
			flag_cnt = 0
			for xx, yy in self.__around_xy(x, y):
				if self.__status[yy][xx] == MS_MINE_FLAG:
					flag_cnt += 1
			if flag_cnt != self.__data[y][x]:
				return
			for xx, yy in self.__around_xy(x, y):
				if self.__status[yy][xx] != MS_MINE_FLAG:
					self.do_click(xx, yy)

	def print_data(self):
		for row in self.__data:
			line = ""
			for d in row:
				if d == MD_MINE:
					line += " X "
				elif d == 0:
					line += "   "
				else:
					line += " %d " % (d)
			print(line)

	def print_status(self, cx = -1, cy = -1):
		for y in range(self.__SIZE):
			line = ""
			for x in range(self.__SIZE):
				c = self.get_tile_status(x, y)

				if x == cx and y == cy:
					line += "[%s]" % (c)
				else:
					line += " %s " % (c)
			print(line)

	def get_tile_status(self, x, y):
		s = self.__status[y][x]
		c = ""
		if s == MS_COVER:
			c = "_"
		elif s == MS_SHOW:
			if self.__data[y][x] == MD_MINE:
				c = "X"
			else:
				c = "%d" % (self.__data[y][x])
		elif s == MS_MINE_FLAG:
			c = "F"
		return c

	def __randomCell(self, _rate):
		if random.random() < _rate:
			return MD_MINE
		else:
			return 0

	def __calMineNumber(self, x, y):
		if self.__data[y][x] == MD_MINE:
			return
		c = 0
		for xx, yy in self.__around_xy(x, y):
			if self.__data[yy][xx] == MD_MINE:
				c = c + 1
		self.__data[y][x] = c

	def __around_xy(self, x, y):
		for xx, yy in [(x + ax, y + ay) for (ax, ay) in self.__around_idx]:
			if xx < 0 or yy < 0 or xx > self.__SIZE - 1 or yy > self.__SIZE - 1:
				continue
			yield xx, yy

	def __check_win(self):
		for x in range(self.__SIZE):
			for y in range(self.__SIZE):
				if self.__data[y][x] != MD_MINE and self.__status[y][x] != MS_SHOW:
					return False
		return True

