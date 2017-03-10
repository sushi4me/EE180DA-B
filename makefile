SUB_DIRS=Modules \
	Modules/IMU \
	Modules/IMU/gesture_data \
	location \
	locations_data \
	position_estimation \
	reference_database \
	Miscellaneous \

.SILENT:

Default:
	@echo Nothing to make

clean:
	rm -f .*~ *~ *.pyc 
	$(foreach var,$(SUB_DIRS),rm -f $(var)/.*~ $(var)/*~ $(var)/*.pyc;)
