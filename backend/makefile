REQ_DIR = .
# common make vars and targets:
export LINTER = flake8
export PYLINTFLAGS = --exclude=__main__.py

export CLOUD_MONGO = 0

PYTHONFILES = $(shell ls *.py)
PYTESTFLAGS = -vv --verbose --cov-branch --cov-report term-missing --tb=short -W ignore::FutureWarning

FORCE:

tests: lint pytests

lint: $(patsubst %.py,%.pylint,$(PYTHONFILES))

%.pylint:
	$(LINTER) $(PYLINTFLAGS) $*.py

pytests: FORCE
	pytest $(PYTESTFLAGS) --cov=$(PKG)

# test a python file:
%.py: FORCE
	$(LINTER) $(PYLINTFLAGS) $@
	pytest $(PYTESTFLAGS) tests/test_$*.py

FORCE:

prod: all_tests github

github: FORCE
	- git commit -a
	git push origin main

all_tests: FORCE
	# cd $(CITIES_DIR); make tests
	# cd $(SEC_DIR); make tests
	# cd $(SERVER_DIR); make tests

dev_env: FORCE
	pip install -r $(REQ_DIR)/requirements-dev.txt
	@echo "You should set PYTHONPATH to: "
	@echo $(shell pwd)

prod_env: FORCE
	pip install -r $(REQ_DIR)/requirements.txt
