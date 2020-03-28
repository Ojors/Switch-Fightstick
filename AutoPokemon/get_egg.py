#!/usr/bin/env python
#-*-coding:utf-8-*-

import sys
sys.path.append("../example")

from NXController import Controller


class EggGetter(object):
	""" 起始位置定在npc左边，背包pm要全满
	"""
	def __init__(self, eggCount):
		super(EggGetter, self).__init__()
		self.m_EggCount = eggCount
		self.m_nxCtrl = Controller(printout = True)
		self.m_nxCtrl.LS()
		self.m_nxCtrl.pause(2)
		
	def start_get_egg(self):
		for i in range(self.m_EggCount):
			print("Current Egg: %s" % (i + 1))
			for j in range(4):
				self.ls_left_up(2.8)
				self.ls_right_up(2.83)
				self.m_nxCtrl.release()
			self.ask_egg()
		print("Get Egg Finished!!!")

	def ask_egg(self):
		self.m_nxCtrl.pause(1.5)
		self.m_nxCtrl.A()
		self.m_nxCtrl.pause(0.5)
		self.m_nxCtrl.A()
		self.m_nxCtrl.pause(3.5)
		self.m_nxCtrl.B()
		self.m_nxCtrl.pause(1.5)
		self.m_nxCtrl.B()
		self.m_nxCtrl.pause(1.5)
		self.m_nxCtrl.B()
		self.m_nxCtrl.pause(0.5)

	def ls_left_up(self, duration = 0.1):
		self.m_nxCtrl.send('LX MIN\r\nLY MIN', duration)

	def ls_right_up(self, duration = 0.1):
		self.m_nxCtrl.send('LX MAX\r\nLY MIN', duration)

	def close_controller(self):
		self.m_nxCtrl.release()
		self.m_nxCtrl.close()


def main():
	eggCount = 30
	eggGetter = EggGetter(eggCount)
	try:
		eggGetter.start_get_egg()
		eggGetter.close_controller()
	except Exception as e:
		print("Rethrow Exception:\n%s" % e)
	finally:
		eggGetter.close_controller()


if __name__ == "__main__":
	main()
