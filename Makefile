.PHONY: rhoV rhoR
rhoV:
	clear
	python3 ./sort.py 380
	python3 ./rho_v_arranger.py 380
rhoR:
	clear
	python3 ./sort.py 380
	python3 ./rho_r_arranger.py 380