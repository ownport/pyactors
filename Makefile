
graph:
	@ dot -T png docs/actors-hierarchy.gv -o docs/actors-hierarchy.png && eog docs/actors-hierarchy.png

clean-tmp-files:
	@ rm logs/*
	

