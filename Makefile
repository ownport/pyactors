
graph:
	@ dot -T png docs/actors-hierarchy.gv -o docs/actors-hierarchy.png && eog docs/actors-hierarchy.png

clean-tmp-files:
	@ rm logs/*
	
test:
	@ echo 'Remove old log files'
	@ touch logs/tmp.log
	@ rm logs/*.log
	@ echo 'Running tests'
	@ nosetests
	@ echo 'Tests completed'
    
test-with-coverage:
	@ echo 'Remove old log files'
	@ touch logs/tmp.log
	@ rm logs/*.logs
	@ echo 'Running tests'
	@ nosetests --with-coverage
	@ echo 'Tests completed'

