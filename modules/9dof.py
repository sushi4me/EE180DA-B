import pyupm_lsm9ds0 as 9DOF
import sys

# TESTING

class dofsensor:
	dof = dofsensor.LSM9DS0()

	a_x = dofsensor.new_floatp()
	a_y = dofsensor.new_floatp()
	a_z = dofsensor.new_floatp()

	g_x = dofsensor.new_floatp()
	g_y = dofsensor.new_floatp()
	g_z = dofsensor.new_floatp()

	def update_values():
		dof.init()
		sensor.update()

		sensor.getAccelerometer(a_x, a_y, a_z)
		sensor.getGyroscope(g_x, g_y, g_z)
