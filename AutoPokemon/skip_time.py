#!/usr/bin/env python
#-*-coding:utf-8-*-

import sys
import datetime
sys.path.append("../example")

from NXController import Controller


class TimeSkipper(object):
	"""
	过帧控制，起始状态要在坑前定位
	"""
	def __init__(self, startDate, skipFrameNum):
		super(TimeSkipper, self).__init__()
		self.m_curDate = startDate
		self.m_skipFrameNum = skipFrameNum
		self.m_nxCtrl = Controller(printout = True)
		self.m_nxCtrl.LS()
		self.m_nxCtrl.pause(2)
		self.m_timeClickDuration = 0.005
		self.m_nxCtrl.buttondelay = 0.02
	
	def start_skip_frame(self):
		self.save(collectWatt=False)
		firstOpenTime = True
		for i in range(self.m_skipFrameNum):
			print("Current Skip = %s, Date = %s" % (i, self.m_curDate))
			self.skip_one_frame(firstOpenTime)
			firstOpenTime = False
			self.m_curDate = self.m_curDate + datetime.timedelta(days=1)
			# 1.1/4.1/8.1各保存一次，防崩溃
			if self.m_curDate.day == 1 and (self.m_curDate.month == 1 or self.m_curDate.month == 4 or self.m_curDate.month == 8):
				print("Save Date = %s" % self.m_curDate)
				self.save()
				firstOpenTime = True
		self.save()
		print("Skip Frame Finished!!!")

	def close_controller(self):
		self.m_nxCtrl.release()
		self.m_nxCtrl.close()

	def skip_one_frame(self, firstOpenTime=False):
		self.m_nxCtrl.A(0.15)
		self.m_nxCtrl.pause(0.1)
		self.skip_time_from_year(firstOpenTime)

	def skip_time_from_year(self, firstOpenTime=False):
		tmpDate = self.m_curDate + datetime.timedelta(days=1)
		# 跨年，年跳1
		if tmpDate.year > self.m_curDate.year:
			# 不是首次点开时间，要回退到年位置
			if not firstOpenTime:
				for i in range(5):
					self.m_nxCtrl.l()
					self.pause_skip_time()
				firstOpenTime = True
			self.m_nxCtrl.u()
			self.pause_skip_time()
		if firstOpenTime:
			self.m_nxCtrl.r()
			self.pause_skip_time()
		self.skip_time_from_month(firstOpenTime)

	def skip_time_from_month(self, firstOpenTime=False):
		# 跨月，月跳1
		lastMonthDay = self.last_day_of_month(self.m_curDate)
		if self.m_curDate.day == lastMonthDay.day:
			# 不是首次点开时间，回退到月位置
			if not firstOpenTime:
				for i in range(4):
					self.m_nxCtrl.l()
					self.pause_skip_time()
				firstOpenTime = True
			self.m_nxCtrl.u()
			self.pause_skip_time()
			# 补全由于月份跳动没有加到的日
			appendDay = 0
			if self.m_curDate.day == 28:
				appendDay = 3
			elif self.m_curDate.day == 29:
				appendDay = 2
			elif self.m_curDate.day == 30:
				appendDay = 1
			# 回到日位置
			if appendDay > 0:
				self.m_nxCtrl.r()
				self.pause_skip_time()
			# 日修正
			for i in range(appendDay):
				self.m_nxCtrl.u()
				self.pause_skip_time()
			# 回月位置
			if appendDay > 0:
				self.m_nxCtrl.l()
				self.pause_skip_time()
		if firstOpenTime:
			self.m_nxCtrl.r()
			self.pause_skip_time()
		self.skip_time_from_day(firstOpenTime)

	def skip_time_from_day(self, firstOpenTime=False):
		# 不是首次点开时间，要回退到月位置
		if not firstOpenTime:
			for i in range(3):
				self.m_nxCtrl.l()
				self.pause_skip_time()
			firstOpenTime = True
		# 日跳1
		self.m_nxCtrl.u()
		self.pause_skip_time()
		for i in range(3):
			self.m_nxCtrl.r()
			self.pause_skip_time()
		self.m_nxCtrl.A(0.15)
		self.m_nxCtrl.pause(0.1)

	def pause_skip_time(self):
		self.m_nxCtrl.pause(self.m_timeClickDuration)

	def save(self, collectWatt=True):
		# 回桌面进游戏
		self.m_nxCtrl.h(0.1)
		self.m_nxCtrl.pause(1)
		self.m_nxCtrl.A(0.1)
		self.m_nxCtrl.pause(2)
		# 收瓦特
		if collectWatt:
			self.collect_watt()
		# 保存
		self.m_nxCtrl.X(0.5)
		self.m_nxCtrl.pause(2)
		self.m_nxCtrl.R(0.5)
		self.m_nxCtrl.pause(2)
		self.m_nxCtrl.A(0.5)
		self.m_nxCtrl.pause(3)
		print("Save!!!")
		# 回桌面进时间界面
		self.m_nxCtrl.h(0.1)
		self.m_nxCtrl.pause(0.5)
		self.m_nxCtrl.d(0.1)
		self.m_nxCtrl.pause(0.5)
		for i in range(4):
			self.m_nxCtrl.r(0.1)
			self.m_nxCtrl.pause(0.05)
		self.m_nxCtrl.A(0.1)
		self.m_nxCtrl.pause(1)
		self.m_nxCtrl.d(-1)
		self.m_nxCtrl.pause(2)
		self.m_nxCtrl.release()
		self.m_nxCtrl.r(0.1)
		self.m_nxCtrl.pause(0.05)
		# 定位到时间上
		for i in range(4):
			self.m_nxCtrl.d(0.1)
			self.m_nxCtrl.pause(0.05)
		self.m_nxCtrl.A(0.1)
		self.m_nxCtrl.pause(0.5)
		for i in range(2):
			self.m_nxCtrl.d(0.1)
			self.m_nxCtrl.pause(0.05)

	def collect_watt(self):
		self.m_nxCtrl.A(0.1)
		self.m_nxCtrl.pause(2)
		for i in range(5):
			self.m_nxCtrl.B(0.1)
			self.m_nxCtrl.pause(1)

	def last_day_of_month(self, any_day):
		next_month = any_day.replace(day=28) + datetime.timedelta(days=4)  # this will never fail
		return next_month - datetime.timedelta(days=next_month.day)


def main():
	startDate = datetime.date(2020, 3, 29)
	skipFrameNum = 100
	timeSkipper = TimeSkipper(startDate, skipFrameNum)
	try:
		timeSkipper.start_skip_frame()
		timeSkipper.close_controller()
	except Exception as e:
		print("Rethrow Exception:\n%s" % e)
	finally:
		timeSkipper.close_controller()


if __name__ == "__main__":
	main()
