SUB_DIRS=Modules Modules/9dofBlock Modules/9dofBlock/gesture_data locations_data position_estimation reference_database 

Default:
	@echo Nothing to make

clean:
	rm -f .*~ *~ *.pyc 
	$(foreach var,$(SUB_DIRS),rm -f $(var)/.*~ $(var)/*~ $(var)/*.pyc;)
