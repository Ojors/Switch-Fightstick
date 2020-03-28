#!/usr/bin/env python
#-*-coding:utf-8-*-

import sys
sys.path.append("../example")

from NXController import Controller


class EggHatcher(object):
	""" 初始化需要背包队伍为空，蛋箱满
	"""
	def __init__(self, cycle):
		super(EggHatcher, self).__init__()
		self.m_Cycle = cycle
		self.m_CurCol = 0
		self.m_nxCtrl = Controller(printout = True)
		self.m_nxCtrl.LS()
		self.m_nxCtrl.pause(2)

	def start_hatch_egg(self):
		while self.m_CurCol <= 6:
			print("Cur Round: %s" % self.m_CurCol)
			# 取蛋
			self.pick_egg()
			if self.m_CurCol == 6:
				break
			# 孵蛋
			all_range = int(self.m_Cycle / 10)
			for i in range(all_range):
				# 5rang=10周期
				for j in range(5):
					print("周期: %s" % (i*10+j*2))
					self.run_round()
			self.m_nxCtrl.ls_r(-1)
			self.m_nxCtrl.ls_u(-1)
			for cnt in range(20 * 5):
				self.m_nxCtrl.B()
				self.m_nxCtrl.pause(0.8)
				self.m_nxCtrl.ls_r(-1)
				self.m_nxCtrl.ls_u(-1)
			self.m_nxCtrl.pause(6.5)
			self.m_nxCtrl.release()
			# 列数+1
			self.m_CurCol = self.m_CurCol + 1
		print("Patch Egg Finished!!!")

	def run_round(self):
		self.m_nxCtrl.ls_l(-1)
		self.m_nxCtrl.ls_u(-1)
		self.m_nxCtrl.pause(5.6)
		self.m_nxCtrl.release()
		# back
		self.m_nxCtrl.ls_r(-1)
		self.m_nxCtrl.ls_u(-1)
		self.m_nxCtrl.pause(6.3)
		self.m_nxCtrl.release()

	def switch_2_box(self):
		self.m_nxCtrl.X()
		self.m_nxCtrl.pause(1)
		self.m_nxCtrl.A()
		self.m_nxCtrl.pause(2)
		self.m_nxCtrl.R()
		self.m_nxCtrl.pause(2)
		self.m_nxCtrl.Y()
		self.m_nxCtrl.pause(0.1)
		self.m_nxCtrl.Y()
		self.m_nxCtrl.pause(0.1)
		self.m_nxCtrl.l()
		self.m_nxCtrl.pause(0.1)

	def back_2_road(self):
		for i in range(3):
			self.m_nxCtrl.B(2)
			self.m_nxCtrl.pause(0.1)

	def move_2_follow(self):
		self.m_nxCtrl.r()
		self.m_nxCtrl.pause(0.01)
		self.m_nxCtrl.A()
		self.m_nxCtrl.pause(0.01)
		self.m_nxCtrl.u()
		self.m_nxCtrl.pause(0.01)
		self.m_nxCtrl.A()
		self.m_nxCtrl.pause(0.01)
		for i in range(self.m_CurCol+1):
			self.m_nxCtrl.l()
			self.m_nxCtrl.pause(0.01)
		self.m_nxCtrl.d()
		self.m_nxCtrl.pause(0.01)
		self.m_nxCtrl.A()
		self.m_nxCtrl.pause(0.01)

	def move_2_box(self):
		self.m_nxCtrl.d()
		self.m_nxCtrl.pause(0.01)
		self.m_nxCtrl.A()
		self.m_nxCtrl.pause(0.01)
		for i in range(2):
			self.m_nxCtrl.u()
			self.m_nxCtrl.pause(0.01)
		self.m_nxCtrl.A()
		self.m_nxCtrl.pause(0.01)
		for i in range(self.m_CurCol):
			self.m_nxCtrl.r()
			self.m_nxCtrl.pause(0.01)
		self.m_nxCtrl.u()
		self.m_nxCtrl.pause(0.01)
		self.m_nxCtrl.A()
		self.m_nxCtrl.pause(0.01)

	def pick_egg(self):
		print(f"Picking {self.m_CurCol + 1}th egg(s)")
		self.switch_2_box()
		if self.m_CurCol != 0:
			self.move_2_box()
		if self.m_CurCol != 6:
			self.move_2_follow()
		self.back_2_road()

	def close_controller(self):
		self.m_nxCtrl.release()
		self.m_nxCtrl.close()


def main():
	cycle = 20	# 孵蛋周期
	eggHatcher = EggHatcher(cycle)
	try:
		eggHatcher.start_hatch_egg()
		eggHatcher.close_controller()
	except Exception as e:
		print("Rethrow Exception:\n%s" % e)
	finally:
		eggHatcher.close_controller()


if __name__ == "__main__":
	main()
