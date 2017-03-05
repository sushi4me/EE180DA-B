SUB_DIRS=Modules locations_data position_estimation reference_database 

Default:
	@echo Nothing to make

clean:
	rm -f .*~ *~ *.pyc 
	$(foreach var,$(SUB_DIRS),rm -f $(var)/.*~ $(var)/*~ $(var)/*.pyc;)
