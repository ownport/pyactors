
graph:
	@ dot -T png docs/actors-hierarchy.gv -o docs/actors-hierarchy.png && eog docs/actors-hierarchy.png

clean-tmp-files:
	@ rm logs/*
	
test:
	@ echo 'Remove old log files'
	@ rm logs/*
	@ echo 'Running tests'
	@ nosetests
	@ echo 'Tests completed'
    

