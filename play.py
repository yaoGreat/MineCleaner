#!/usr/bin/python
import game
import os
from getch import getch

SIZE = 10
RATE = 0.05

def play():
	g = game.MineGame()
	g.Init(SIZE, RATE)
	cx = 0
	cy = 0

	def show():
		os.system('clear')
		#g.print_data()
		g.print_status(cx, cy)

	show()
	while True:
		c = getch()
		if c == "x" or c == "X":
			break
		if c == "a":
			if cx > 0:
				cx -= 1
		elif c == "s":
			if cy < g.size - 1:
				cy += 1
		elif c == "d":
			if cx < g.size - 1:
				cx += 1
		elif c == "w":
			if cy > 0:
				cy -= 1
		elif c == "j":
			g.do_click(cx, cy)
		elif c == "k":
			g.do_flag(cx, cy)
		elif c == "l":
			g.do_auto_click(cx, cy)
		show()
		if g.result == game.MG_WIN:
			print("you win!")
			break
		elif g.result == game.MG_LOSE:
			print("you lose!")
			break

play()
