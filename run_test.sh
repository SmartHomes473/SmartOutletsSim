#!/bin/bash

TESTS=(	sim.tests.coordinator sim.tests.outlets )

for test in ${TESTS[*]}; do
	python -m ${test}
	echo
done;
echo Tests completed
