

.. _extending-phpunit:

===============
Etendre PHPUnit
===============

PHPUnit peut être étendu de multiples façon pour rendre l'écriture des
tests plus facile et personnaliser le retour que vous obtenez des tests
exécutés. Voici les points de départs communs pour étendre PHPUnit.

.. _extending-phpunit.PHPUnit_Framework_TestCase:

Sous-classe PHPUnit_Framework_TestCase
######################################

Ecrivez des assertions personnalisées et des méthodes utilitaires dans une
sous classe abstraite de
``PHPUnit_Framework_TestCase`` et faites hériter vos classes
de cas de test de cette classe. C'est une des façon les plus faciles pour
étendre PHPUnit.

.. _extending-phpunit.custom-assertions:

Ecrire des assertions personnalisées
####################################

Lorsqu'on écrit des assertions personnalisées, une bonne pratique
consiste à suivre la façon dont PHPUnit implémente ses propres assertions.
Comme vous pouvez le voir dans
:numref:`extending-phpunit.examples.Assert.php`, la méthode
``assertTrue()`` n'est qu'un enrobeur des méthodes
``isTrue()`` et ``assertThat()``:
``isTrue()`` crée un objet de correspondance qui est passé à
``assertThat()`` pour évaluation.

.. code-block:: php
    :caption: Les méthodes assertTrue() et isTrue() de la classe PHPUnit_Framework_Assert
    :name: extending-phpunit.examples.Assert.php

    <?php
    abstract class PHPUnit_Framework_Assert
    {
        // ...

        /**
         * Asserts that a condition is true.
         *
         * @param  boolean $condition
         * @param  string  $message
         * @throws PHPUnit_Framework_AssertionFailedError
         */
        public static function assertTrue($condition, $message = '')
        {
            self::assertThat($condition, self::isTrue(), $message);
        }

        // ...

        /**
         * Returns a PHPUnit_Framework_Constraint_IsTrue matcher object.
         *
         * @return PHPUnit_Framework_Constraint_IsTrue
         * @since  Method available since Release 3.3.0
         */
        public static function isTrue()
        {
            return new PHPUnit_Framework_Constraint_IsTrue;
        }

        // ...
    }?>

:numref:`extending-phpunit.examples.IsTrue.php` montre comment
``PHPUnit_Framework_Constraint_IsTrue`` étend la classe
abstraite de base pour des objets de correspondance (ou des contraintes),
``PHPUnit_Framework_Constraint``.

.. code-block:: php
    :caption: La classe PHPUnit_Framework_Constraint_IsTrue
    :name: extending-phpunit.examples.IsTrue.php

    <?php
    class PHPUnit_Framework_Constraint_IsTrue extends PHPUnit_Framework_Constraint
    {
        /**
         * Evaluates the constraint for parameter $other. Returns TRUE if the
         * constraint is met, FALSE otherwise.
         *
         * @param mixed $other Value or object to evaluate.
         * @return bool
         */
        public function evaluate($other)
        {
            return $other === TRUE;
        }

        /**
         * Returns a string representation of the constraint.
         *
         * @return string
         */
        public function toString()
        {
            return 'is true';
        }
    }?>

L'effort d'implémentation des méthodes ``assertTrue()`` et
``isTrue()`` ainsi que la classe
``PHPUnit_Framework_Constraint_IsTrue`` tire bénéfice du fait que
``assertThat()`` prend automatiquement soin d'évaluer l'assertion et
les tâches de suivi comme le décompte à des fins de statistique.
Plus encore, la méthode ``isTrue()`` peut être utilisée comme un matcher
lors de la configuration d'objets simulacres.

.. _extending-phpunit.PHPUnit_Framework_TestListener:

Implémenter PHPUnit_Framework_TestListener
##########################################

:numref:`extending-phpunit.examples.SimpleTestListener.php`
montre une implémentation simple de l'interface ``PHPUnit_Framework_TestListener``.

.. code-block:: php
    :caption: Un simple moniteur de test
    :name: extending-phpunit.examples.SimpleTestListener.php

    <?php
    class SimpleTestListener implements PHPUnit_Framework_TestListener
    {
        public function addError(PHPUnit_Framework_Test $test, Exception $e, $time)
        {
            printf("Error while running test '%s'.\n", $test->getName());
        }

        public function addFailure(PHPUnit_Framework_Test $test, PHPUnit_Framework_AssertionFailedError $e, $time)
        {
            printf("Test '%s' failed.\n", $test->getName());
        }

        public function addIncompleteTest(PHPUnit_Framework_Test $test, Exception $e, $time)
        {
            printf("Test '%s' is incomplete.\n", $test->getName());
        }

        public function addRiskyTest(PHPUnit_Framework_Test $test, Exception $e, $time)
        {
            printf("Test '%s' is deemed risky.\n", $test->getName());
        }

        public function addSkippedTest(PHPUnit_Framework_Test $test, Exception $e, $time)
        {
            printf("Test '%s' has been skipped.\n", $test->getName());
        }

        public function startTest(PHPUnit_Framework_Test $test)
        {
            printf("Test '%s' started.\n", $test->getName());
        }

        public function endTest(PHPUnit_Framework_Test $test, $time)
        {
            printf("Test '%s' ended.\n", $test->getName());
        }

        public function startTestSuite(PHPUnit_Framework_TestSuite $suite)
        {
            printf("TestSuite '%s' started.\n", $suite->getName());
        }

        public function endTestSuite(PHPUnit_Framework_TestSuite $suite)
        {
            printf("TestSuite '%s' ended.\n", $suite->getName());
        }
    }
    ?>

Dans :ref:`appendixes.configuration.test-listeners` vous pouvez voir
comment configurer PHPUnit pour brancher votre moniteur de test lors de l'exécution des tests.

.. _extending-phpunit.PHPUnit_Extensions_TestDecorator:

Sous classer PHPUnit_Extensions_TestDecorator
#############################################

Vous pouvez encapsuler des cas de test ou des séries de tests dans une
sous-classe de ``PHPUnit_Extensions_TestDecorator`` et utiliser
le Design Pattern Decorator pour réaliser certaines actions avant et après
que les tests sont exécutés.

PHPUnit apporte deux décorateurs de test concrets:
``PHPUnit_Extensions_RepeatedTest`` et
``PHPUnit_Extensions_TestSetup``. Le premier est utilisé pour
exécuter de manière répétée un test et ne le comptabiliser comme succès que si
toutes les itérations ont réussi. Le second est discuté dans :ref:`fixtures`.

:numref:`extending-phpunit.examples.RepeatedTest.php`
montre une version raccourcie du décorateur de test
``PHPUnit_Extensions_RepeatedTest`` qui illustre comment
écrire vos propres décorateurs de tests.

.. code-block:: php
    :caption: Le décorateur RepeatedTest
    :name: extending-phpunit.examples.RepeatedTest.php

    <?php
    require_once 'PHPUnit/Extensions/TestDecorator.php';

    class PHPUnit_Extensions_RepeatedTest extends PHPUnit_Extensions_TestDecorator
    {
        private $timesRepeat = 1;

        public function __construct(PHPUnit_Framework_Test $test, $timesRepeat = 1)
        {
            parent::__construct($test);

            if (is_integer($timesRepeat) &&
                $timesRepeat >= 0) {
                $this->timesRepeat = $timesRepeat;
            }
        }

        public function count()
        {
            return $this->timesRepeat * $this->test->count();
        }

        public function run(PHPUnit_Framework_TestResult $result = NULL)
        {
            if ($result === NULL) {
                $result = $this->createResult();
            }

            for ($i = 0; $i < $this->timesRepeat && !$result->shouldStop(); $i++) {
                $this->test->run($result);
            }

            return $result;
        }
    }
    ?>

.. _extending-phpunit.PHPUnit_Framework_Test:

Implémenter PHPUnit_Framework_Test
##################################

L'interface ``PHPUnit_Framework_Test`` est restreinte et
facile à implémenter. Vous pouvez écrire une implémentation de
``PHPUnit_Framework_Test`` qui est plus simple que
``PHPUnit_Framework_TestCase`` et qui exécute
*des tests dirigés par les données*, par exemple.

:numref:`extending-phpunit.examples.DataDrivenTest.php`
montre une classe de cas de test dirigé par les tests qui compare les
valeurs d'un fichier contenant des valeurs séparées par des virgules (CSV).
Chaque ligne d'un tel fichier ressemble à
``foo;bar``, où la première valeur est celle que nous attendons
et la seconde valeur celle constatée.

.. code-block:: php
    :caption: Un test dirigé par les données
    :name: extending-phpunit.examples.DataDrivenTest.php

    <?php
    class DirigeParLesDonneesTest implements PHPUnit_Framework_Test
    {
        private $lines;

        public function __construct($dataFile)
        {
            $this->lines = file($dataFile);
        }

        public function count()
        {
            return 1;
        }

        public function run(PHPUnit_Framework_TestResult $result = NULL)
        {
            if ($result === NULL) {
                $result = new PHPUnit_Framework_TestResult;
            }

            foreach ($this->lines as $line) {
                $result->startTest($this);
                PHP_Timer::start();
                $stopTime = NULL;

                list($expected, $actual) = explode(';', $line);

                try {
                    PHPUnit_Framework_Assert::assertEquals(
                      trim($expected), trim($actual)
                    );
                }

                catch (PHPUnit_Framework_AssertionFailedError $e) {
                    $stopTime = PHP_Timer::stop();
                    $result->addFailure($this, $e, $stopTime);
                }

                catch (Exception $e) {
                    $stopTime = PHP_Timer::stop();
                    $result->addError($this, $e, $stopTime);
                }

                if ($stopTime === NULL) {
                    $stopTime = PHP_Timer::stop();
                }

                $result->endTest($this, $stopTime);
            }

            return $result;
        }
    }

    $test = new DataDrivenTest('fichier_donnees.csv');
    $resultat = PHPUnit_TextUI_TestRunner::run($test);
    ?>

.. code-block:: bash

    PHPUnit 6.4.0 by Sebastian Bergmann and contributors.

    .F

    Time: 0 seconds

    There was 1 failure:

    1) DirigeParLesDonneesTest
    Failed asserting that two strings are equal.
    expected string <bar>
    difference      <  x>
    got string      <baz>
    /home/sb/DirigeParLesDonneesTest.php:32
    /home/sb/DirigeParLesDonneesTest.php:53

    FAILURES!
    Tests: 2, Failures: 1.


