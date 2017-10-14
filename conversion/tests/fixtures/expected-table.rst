

.. _writing-tests-for-phpunit:

=========================
Writing Tests for PHPUnit
=========================

.. rst-class:: table
.. list-table:: Methods for testing output
    :name: writing-tests-for-phpunit.output.tables.api
    :header-rows: 1

    * - Method
      - Meaning
    * - ``void expectOutputRegex(string $regularExpression)``
      - Set up the expectation that the output matches a ``$regularExpression``.
    * - ``void expectOutputString(string $expectedString)``
      - Set up the expectation that the output is equal to an ``$expectedString``.
    * - ``bool setOutputCallback(callable $callback)``
      - Sets up a callback that is used to, for instance, normalize the actual output.
    * - ``string getActualOutput()``
      - Get the actual output.

