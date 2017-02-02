import pyupm_lsm9ds0 as dofObj
import sys

# TESTING

class DOFsensor:
	dof = dofObj.LSM9DS0()	

	a_x = dofObj.new_floatp()
	a_y = dofObj.new_floatp()
	a_z = dofObj.new_floatp()

	g_x = dofObj.new_floatp()
	g_y = dofObj.new_floatp()
	g_z = dofObj.new_floatp()

	def update_values(self):
		self.dof.init()
		self.dof.update()

		self.dof.getAccelerometer(self.a_x, self.a_y, self.a_z)
		self.dof.getGyroscope(self.g_x, self.g_y, self.g_z)

	def getAX(self):
		return dofObj.floatp_value(self.a_x)

	def getAY(self):
		return dofObj.floatp_value(self.a_y)

	def getAZ(self):
		return dofObj.floatp_value(self.a_z)

	def getGX(self):
		return dofObj.floatp_value(self.g_x)

	def getGY(self):
		return dofObj.floatp_value(self.g_y)

	def getGZ(self):
		return dofObj.floatp_value(self.g_z)

