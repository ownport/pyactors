
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
	@ for log in `ls logs`;do [ ! -s logs/$$log ] && rm logs/$$log; done
	@ echo 'Tests completed'
	@ echo 'Created logs:'
	@ ls -l logs/
    
test-with-coverage:
	@ echo 'Remove old log files'
	@ touch logs/tmp.log
	@ rm logs/*.log
	@ echo 'Running tests'
	@ nosetests --with-coverage
	@ echo 'Tests completed'
	@ for log in `ls logs`;do [ ! -s logs/$$log ] && rm logs/$$log; done
	@ echo 'Created logs:'
	@ ls -l logs/

