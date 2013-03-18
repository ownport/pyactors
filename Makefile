
graph:
	@ dot -T png docs/actors-hierarchy.gv -o docs/actors-hierarchy.png && eog docs/actors-hierarchy.png
	@ dot -T png docs/pyactors-msg-flow.gv -o docs/pyactors-msg-flow.png && eog docs/pyactors-msg-flow.png

clean-tmp-files:
	@ rm logs/*
	
test:
	@ echo 'Remove old log files'
	@ touch logs/tmp.log
	@ rm logs/*.log
	@ echo 'Running tests'
	@ nosetests
	@ echo 'Tests completed'
	@ for log in `ls logs/`; do [ ! -s logs/$$log ] && rm logs/$$log; done
	@ echo 'Created logs:'
	@ ls -l logs/
    
test-with-coverage:
	@ echo 'Remove old log files'
	@ touch logs/tmp.log
	@ rm logs/*.log
	@ echo 'Running tests'
	@ nosetests --with-coverage
	@ echo 'Tests completed'
	@ for log in `ls logs/`; do [ ! -s logs/$$log ] && rm logs/$$log; done
	@ echo 'Created logs:'
	@ ls -l logs/

update-ext-deps:
	@ echo 'Update external dependencies'
	@ echo '- bottle.py'
	@ curl -s https://raw.github.com/defnull/bottle/master/bottle.py -o tests/packages/bottle.py
	@ echo '- pyservice.py'
	@ curl -s https://raw.github.com/ownport/pyservice/master/pyservice.py -o tests/packages/pyservice.py
	

