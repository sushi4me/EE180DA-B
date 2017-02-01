from upm import pyupm_lsm9ds0 as DOFsensor
import sys

# TESTING

class DOFsensor:
	dof = DOFsensor.LSM9DS0()

	def __init__(self):
		a_x = DOFsensor.new_floatp()
		a_y = DOFsensor.new_floatp()
		a_z = DOFsensor.new_floatp()

		g_x = DOFsensor.new_floatp()
		g_y = DOFsensor.new_floatp()
		g_z = DOFsensor.new_floatp()

	def update_values():
		dof.init()
		dof.update()

		dof.getAccelerometer(a_x, a_y, a_z)
		dof.getGyroscope(g_x, g_y, g_z)
