
graph:
	@ dot -T png docs/actors-hierarchy.gv -o docs/actors-hierarchy.png && eog docs/actors-hierarchy.png
	@ dot -T png docs/pyactors-msg-flow.gv -o docs/pyactors-msg-flow.png && eog docs/pyactors-msg-flow.png

clean-tmp-files:
	@ rm logs/*
	
run-tests:
	@ echo 'Remove old log files'
	@ touch logs/tmp.log
	@ rm logs/*.log
	@ tests/echoserver.py start 
	@ echo 'Running tests'
	@ nosetests
	@ echo 'Tests completed'
	@ tests/echoserver.py stop 
	@ for log in `ls logs/`; do [ ! -s logs/$$log ] && rm logs/$$log; done
	@ echo 'Created logs:'
	@ ls -l logs/
    
run-tests-with-coverage:
	@ echo 'Remove old log files'
	@ touch logs/tmp.log
	@ rm logs/*.log
	@ tests/echoserver.py start 
	@ echo 'Running tests'
	@ nosetests --with-coverage
	@ echo 'Tests completed'
	@ tests/echoserver.py stop 
	@ for log in `ls logs/`; do [ ! -s logs/$$log ] && rm logs/$$log; done
	@ echo 'Created logs:'
	@ ls -l logs/

update-ext-deps:
	@ echo 'Update external dependencies'
	@ echo '- pyservice.py'
	@ curl -s https://raw.github.com/ownport/pyservice/master/pyservice.py -o tests/packages/pyservice.py
	@ pip freeze
    	

