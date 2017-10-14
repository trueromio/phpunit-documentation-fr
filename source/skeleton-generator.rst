

.. _skeleton-generator:

=======================
Générateur de squelette
=======================

Le générateur de squelette de PHPUnit (Skeleton Generator) est un outil qui
peut générer des squelettes de classes de test à partir des classes de code
de production et vice versa. Il peut être installé en utilisant la commande
suivante :

.. code-block:: bash

    $ pear install phpunit/PHPUnit_SkeletonGenerator

.. _skeleton-generator.test:

Générer un squelettre de classe de cas de test
##############################################

Quand vous écrivez des tests pour du code existant, vous avez à écrire
les mêmes fragments de code tels que

.. code-block:: php

    public function testMethode()
    {
    }

encore et encore. Le générateur de squelette de PHPUnit peut vous aider
en analysant le code d'une classe existante et en générant pour elle un squelette de classe de cas
de test.

.. code-block:: php
    :caption: La classe Calculateur
    :name: skeleton-generator.examples.Calculator.php

    <?php
    class Calculateur
    {
        public function additionner($a, $b)
        {
            return $a + $b;
        }
    }
    ?>

L'exemple suivant montre comment générer un squelette de classe de de test
pour une classe appelée ``Calculateur``
(see :numref:`skeleton-generator.examples.Calculator.php`).

.. code-block:: bash

    $ phpunit-skelgen --test Calculateur
    PHPUnit Skeleton Generator 1.0.0 by Sebastian Bergmann.

    Wrote skeleton for "CalculateurTest" to "/home/sb/CalculateurTest.php".

Pour chaque méthode de la classe originelle, il y a aura un cas de
test incomplet (voir :ref:`incomplete-and-skipped-tests`) dans
la classe de cas de test générée.

.. admonition:: Classes sous espace de nom et le générateur de squelette

   Lorsque vous utilisez le générateur de squelette pour générer du code basé sur
   une classe qui est déclarée dans un `espace de nommage (namespace) <http://php.net/namespace>`_
   vous devez fournir le nom qualifié de la classe ainsi que le chemin d'accès
   au fichier source dans lequel elle est déclarée.

   Par exemple, pour une classe ``Calculateur`` qui est déclarée
   dans l'espace de nommage ``projet``, vous devez invoquer le
   générateur de squelette comme ceci :

   .. code-block:: bash

       $ phpunit-skelgen --test -- "projet\Calculateur" Calculateur.php
       PHPUnit Skeleton Generator 1.0.0 by Sebastian Bergmann.

       Wrote skeleton for "projet\CalculateurTest" to "/home/sb/CalculateurTest.php".

Ci-dessous se trouve la sortie écran produite par le lancement de la classe de cas de test générée.

.. code-block:: bash

    $ phpunit --bootstrap Calculateur.php --verbose CalculateurTest
    PHPUnit 6.4.0 by Sebastian Bergmann and contributors.

    I

    Time: 0 seconds, Memory: 3.50Mb

    There was 1 incomplete test:

    1) CalculateurTest::testAdditionner
    This test has not been implemented yet.

    /home/sb/CalculateurTest.php:38
    OK, but incomplete or skipped tests!
    Tests: 1, Assertions: 0, Incomplete: 1.

Vous pouvez utiliser l'annotation ``@assert`` dans le bloc
de documentation d'une méthode pour générer automatiquement des tests
simples mais significatifs au lieu de cas de tests incomplets.
:numref:`skeleton-generator.test.examples.Calculator.php`
montre un exemple.

.. code-block:: php
    :caption: La classe Calculateur avec des annotations @assert
    :name: skeleton-generator.test.examples.Calculator.php

    <?php
    class Calculateur
    {
        /**
         * @assert (0, 0) == 0
         * @assert (0, 1) == 1
         * @assert (1, 0) == 1
         * @assert (1, 1) == 2
         */
        public function additionner($a, $b)
        {
            return $a + $b;
        }
    }
    ?>

Chaque méthode de la classe originelle est contrôlée à la recherche d'annotations
``@assert``. Celles-ci sont transformées en code de test comme

.. code-block:: php

        /**
         * Generated from @assert (0, 0) == 0.
         */
        public function testAdditionner() {
            $o = new Calculateur;
            $this->assertEquals(0, $o->additionner(0, 0));
        }

Ci-dessous se trouve la sortie écran produite par le lancement de la classe de cas de test générée.

.. code-block:: bash

    $ phpunit --bootstrap Calculateur.php --verbose CalculateurTest
    PHPUnit 6.4.0 by Sebastian Bergmann and contributors.

    ....

    Time: 0 seconds, Memory: 3.50Mb

    OK (4 tests, 4 assertions)

:numref:`skeleton-generator.test.tables.assert-annotations`
montre les variantes gérées par l'annotation ``@assert``
et de quelle façon elles sont transformées en code de test.

.. rst-class:: table
.. list-table:: Variantes gérées par l'annotation @assert
    :name: skeleton-generator.test.tables.assert-annotations
    :header-rows: 1

    * - Annotation
      - Transformée en
    * - ``@assert (...) == X``
      - ``assertEquals(X, methode(...))``
    * - ``@assert (...) != X``
      - ``assertNotEquals(X, methode(...))``
    * - ``@assert (...) === X``
      - ``assertSame(X, methode(...))``
    * - ``@assert (...) !== X``
      - ``assertNotSame(X, methode(...))``
    * - ``@assert (...) > X``
      - ``assertGreaterThan(X, methode(...))``
    * - ``@assert (...) >= X``
      - ``assertGreaterThanOrEqual(X, methode(...))``
    * - ``@assert (...) < X``
      - ``assertLessThan(X, methode(...))``
    * - ``@assert (...) <= X``
      - ``assertLessThanOrEqual(X, methode(...))``
    * - ``@assert (...) throws X``
      - ``@expectedException X``

.. _skeleton-generator.class:

Générer un squelette de classe à partir d'une classe de cas de test
###################################################################

Lorsque vous pratiquez le développement dirigé par les tests (voir :ref:`test-driven-development`)
et que vous écrivez vos tests avant le code que les tests vérifient, PHPUnit peut
vous aider à générer des squelettes de classe à partir des classes de cas de test.

Suivant la convention selon laquelle les tests pour une classe ``Unit``
sont écrit dans une classe nommée ``UnitTest``, le source de la classe
de cas de test est inspecté à la recherche de variables qui référencent des objets
de la classe ``Unit`` puis est analysé pour savoir quelles méthodes
sont appelées sur ces objets. Par exemple, jetez un oeil à :numref:`skeleton-generator.class.examples.BowlingGame.php` qui a été généré en se
basant sur l'analyse de :numref:`skeleton-generator.class.examples.BowlingGameTest.php`.

.. code-block:: php
    :caption: La classe JeuDeBowlingTest
    :name: skeleton-generator.class.examples.BowlingGameTest.php

    <?php
    class JeuDeBowlingTest extends PHPUnit_Framework_TestCase
    {
        protected $jeu;

        protected function setUp()
        {
            $this->jeu = new JeuDeBowling;
        }

        protected function lancePlusieursEtRenverse($n, $quilles)
        {
            for ($i = 0; $i < $n; $i++) {
                $this->jeu->renverse($quilles);
            }
        }

        public function testScorePourJeuDansLaRigoleEst0()
        {
            $this->lancePlusieursEtRenverse(20, 0);
            $this->assertEquals(0, $this->jeu->score());
        }
    }
    ?>

.. code-block:: bash

    $ phpunit-skelgen --class JeuDeBowlingTest
    PHPUnit Skeleton Generator 1.0.0 by Sebastian Bergmann.

    Wrote skeleton for "JeuDeBowling" to "./JeuDeBowling.php".

.. code-block:: php
    :caption: Le squelette généré de la classe JeuDeBowling
    :name: skeleton-generator.class.examples.BowlingGame.php

    <?php
    /**
     * Generated by PHPUnit_SkeletonGenerator on 2012-01-09 at 16:55:58.
     */
    class JeuDeBowling
    {
        /**
         * @todo Implement renverse().
         */
        public function renverse()
        {
            // Remove the following line when you implement this method.
            throw new RuntimeException('Not yet implemented.');
        }

        /**
         * @todo Implement score().
         */
        public function score()
        {
            // Remove the following line when you implement this method.
            throw new RuntimeException('Not yet implemented.');
        }
    }
    ?>

Ci-dessous se trouve la sortie écran produite par le lancement de la classe de cas de test générée.

.. code-block:: bash

    $ phpunit --bootstrap JeuDeBowling.php JeuDeBowlingTest
    PHPUnit 6.4.0 by Sebastian Bergmann and contributors.

    E

    Time: 0 seconds, Memory: 3.50Mb

    There was 1 error:

    1) JeuDeBowlingTest::testScorePourJeuDansLaRigoleEst0
    RuntimeException: Not yet implemented.

    /home/sb/JeuDeBowling.php:13
    /home/sb/JeuDeBowlingTest.php:14
    /home/sb/JeuDeBowlingTest.php:20

    FAILURES!
    Tests: 1, Assertions: 0, Errors: 1.


