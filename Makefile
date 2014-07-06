PY=/usr/bin/python
NOSE=/usr/bin/nosetests1.1 -s -v --with-xunit
GIT=/usr/bin/git
PYTHONPATH=.

# The TEST variable can be set to allow you to control which tests
# to run.  For example, if the current project has a test set defined at
# "tests/test_<name>.py", to run the "Test<class_name>" class:
#
# $ make test TEST=tests:Test<class_name>
#
# To run individual test cases within each test class:
#
# $ make test TEST=tests:Test<class_name>.test_<test_name>
#
# Note: for this to work you will need to import the test class into
# the current namespace via "tests/__init__.py"
TEST=oct_schema.tests:TestInheritedModel \
	oct_schema.tests:TestSession \
	oct_schema.model.tests:TestObjects \
	oct_schema.model.tests:TestOntology \
	oct_schema.model.tests:TestRelations

sdist:
	$(PY) setup.py sdist

rpm:
	$(PY) setup.py bdist_rpm --fix-python

docs:
	PYTHONPATH=$(PYTHONPATH) sphinx-1.0-build -b html doc/source doc/build

build: docs rpm

test:
	$(NOSE) $(TEST)

uninstall:
	$(RPM) -e python-oct-rest

install:
	$(RPM) -ivh dist/python-oct-rest-?.??-?.noarch.rpm

upgrade:
	$(RPM) -Uvh dist/python-oct-rest-?.??-?.noarch.rpm

clean:
	$(GIT) clean -xdf

.PHONY: docs rpm test
