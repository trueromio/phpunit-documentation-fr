

.. _writing-tests-for-phpunit:

=========================
Writing Tests for PHPUnit
=========================

.. code-block:: php
    :caption: Using the ``@depends`` annotation to express dependencies
    :name: writing-tests-for-phpunit.examples.StackTest2.php

    <?php
    use PHPUnit\Framework\TestCase;

    class StackTest extends TestCase
    {
        public function testEmpty()
        {
            $stack = [];
            $this->assertEmpty($stack);

            return $stack;
        }

        /**
         * @depends testEmpty
         */
        public function testPush(array $stack)
        {
            array_push($stack, 'foo');
            $this->assertEquals('foo', $stack[count($stack)-1]);
            $this->assertNotEmpty($stack);

            return $stack;
        }

        /**
         * @depends testPush
         */
        public function testPop(array $stack)
        {
            $this->assertEquals('foo', array_pop($stack));
            $this->assertEmpty($stack);
        }
    }
    ?>


