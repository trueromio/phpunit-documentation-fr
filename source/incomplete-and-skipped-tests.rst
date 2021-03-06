

.. _incomplete-and-skipped-tests:

==========================
Tests incomplets et sautés
==========================

.. _incomplete-and-skipped-tests.incomplete-tests:

Tests incomplets
################

Quand vous travaillez sur une nouvelle classe de cas de test, vous pourriez vouloir
commencer en écrivant des méthodes de test vides comme

.. code-block:: php

    public function testQuelquechose()
    {
    }

pour garder la trace des tests que vous avez à écrire. Le problème avec
les méthodes de test vides est qu'elles sont interprétées comme étant réussies par le
framework PHPUnit. Cette mauvaise interprétation fait que le rapport de tests devient
inutile -- vous ne pouvez pas voir si un test est effectivement réussi ou s'il n'a tout
simplement pas été implémenté. Appeler
``$this->fail()`` dans une méthode de test non implémentée
n'aide pas davantage, puisqu'alors le test sera interprété comme étant un échec.
Ce serait tout aussi faux que d'interpréter un test non implémenté comme étant réussi.

Si nous pensons à un test réussi comme à un feu vert et à un échec de test
comme à un feu rouge, nous avons besoin d'un feu orange additionnel pour signaler
un test comme étant incomplet ou pas encore implémenté.
``PHPUnit_Framework_IncompleteTest`` est une interface de marquage
pour signaler une exception qui est levée par une méthode de test comme résultat
d'un test incomplet ou actuellement pas implémenté.
``PHPUnit_Framework_IncompleteTestError`` est l'implémentation
standard de cette interface.

:numref:`incomplete-and-skipped-tests.incomplete-tests.examples.SampleTest.php`
montre une classe de cas de tests, ``ExempleDeTest``, qui contient une unique méthode de test,
method, ``testSomething()``. En appelant la méthode pratique
``markTestIncomplete()`` (qui lève automatiquement
une exception ``PHPUnit_Framework_IncompleteTestError``)
dans la méthode de test, nous marquons le test comme étant incomplet.

.. code-block:: php
    :caption: Signaler un test comme incomplet
    :name: incomplete-and-skipped-tests.incomplete-tests.examples.SampleTest.php

    <?php
    class ExempleDeTest extends PHPUnit_Framework_TestCase
    {
        public function testeQuelquechose()
        {
            // Facultatif: testez tout ce que vous voulez ici.
            $this->assertTrue(TRUE, 'Ceci devrait toujours fonctionner.');

            // Cesser ici et marquer ce test comme incomplet.
            $this->markTestIncomplete(
              'Ce test n\'a pas encore été implémenté.'
            );
        }
    }
    ?>

Un test incomplet est signalé par un ``I`` sur la sortie écran
du lanceur de test en ligne de commandes PHPUnit, comme montré dans l'exemple
suivant.

.. code-block:: bash

    $ phpunit --verbose ExempleDeTest
    PHPUnit 6.4.0 by Sebastian Bergmann and contributors.

    I

    Time: 0 seconds, Memory: 3.95Mb

    There was 1 incomplete test:

    1) ExempleDeTest::testQuelquechose
    This test has not been implemented yet.

    /home/sb/ExempleDeTest.php:12
    OK, but incomplete or skipped tests!
    Tests: 1, Assertions: 1, Incomplete: 1.

:numref:`incomplete-and-skipped-tests.incomplete-tests.tables.api`
montre l'API pour marquer des tests comme incomplets.

.. rst-class:: table
.. list-table:: API pour les tests incomplets
    :name: incomplete-and-skipped-tests.incomplete-tests.tables.api
    :header-rows: 1

    * - Méthode
      - Signification
    * - ``void markTestIncomplete()``
      - Marque le test courant comme incomplet.
    * - ``void markTestIncomplete(string $message)``
      - Marque le test courant comme incomplet en utilisant ``$message`` comme message d'explication.

.. _incomplete-and-skipped-tests.skipping-tests:

Sauter des tests
################

Tous les tests ne peuvent pas être exécutés dans tous les environnements. Considérez,
par exemple, une couche d'abstraction de base de données qui possède différents pilotes
pour les différents systèmes de base de données qu'elle gère. Les tests pour le pilote
MySQL ne peuvent bien sûr être exécutés que si un serveur MySQL est disponible.

:numref:`incomplete-and-skipped-tests.skipping-tests.examples.DatabaseTest.php`
montre une classe de cas de tests, ``DatabaseTest``, qui contient une méthode de tests
``testConnection()``. Dans la méthode canevas ``setUp()``
de la classe du cas de test, nous pouvons contrôler si l'extension
MySQLi est disponible et utiliser la méthode ``markTestSkipped()``
pour sauter le test si ce n'est pas le cas.

.. code-block:: php
    :caption: Sauter un test
    :name: incomplete-and-skipped-tests.skipping-tests.examples.DatabaseTest.php

    <?php
    class DatabaseTest extends PHPUnit_Framework_TestCase
    {
        protected function setUp()
        {
            if (!extension_loaded('mysqli')) {
                $this->markTestSkipped(
                  'L\'extension MySQLi n\'est pas disponible.'
                );
            }
        }

        public function testConnection()
        {
            // ...
        }
    }
    ?>

Un test qui a été sauté est signalé par un ``S`` dans la sortie
écran du lanceur de tests en ligne de commande PHPUnit, comme montré dans
l'exemple suivant.

.. code-block:: bash

    $ phpunit --verbose DatabaseTest
    PHPUnit 6.4.0 by Sebastian Bergmann and contributors.

    S

    Time: 0 seconds, Memory: 3.95Mb

    There was 1 skipped test:

    1) DatabaseTest::testConnection
    The MySQLi extension is not available.

    /home/sb/DatabaseTest.php:9
    OK, but incomplete or skipped tests!
    Tests: 1, Assertions: 0, Skipped: 1.

:numref:`incomplete-and-skipped-tests.skipped-tests.tables.api`
montre l'API pour sauter des tests.

.. rst-class:: table
.. list-table:: API pour sauter des tests
    :name: incomplete-and-skipped-tests.skipped-tests.tables.api
    :header-rows: 1

    * - Méthode
      - Signification
    * - ``void markTestSkipped()``
      - Marque le test courant comme sauté.
    * - ``void markTestSkipped(string $message)``
      - Marque le test courant comme étant sauté en utilisant ``$message`` comme message d'explication.

.. _incomplete-and-skipped-tests.skipping-tests-using-requires:

Sauter des tests en utilisant @requires
#######################################

En plus des méthodes ci-dessus, il est également possible d'utiliser
l'annotation ``@requires`` pour exprimer les préconditions communes pour un cas de test.

.. rst-class:: table
.. list-table:: Usages possibles de @requires
    :name: incomplete-and-skipped-tests.requires.tables.api
    :header-rows: 1

    * - Type
      - Valeurs possibles
      - Exemple
      - Autre exemple
    * - ``PHP``
      - Tout identifiant de version PHP
      - @requires PHP 5.3.3
      - @requires PHP 7.1-dev
    * - ``PHPUnit``
      - Tout identifiant de version PHPUnit
      - @requires PHPUnit 3.6.3
      - @requires PHPUnit 4.6
    * - ``function``
      - Tout paramètre valide pour `function_exists <http://php.net/function_exists>`_
      - @requires function imap_open
      - @requires function ReflectionMethod::setAccessible
    * - ``extension``
      - Tout nom d'extension
      - @requires extension mysqli
      - @requires extension curl

.. code-block:: php
    :caption: Sauter des cas de tests en utilisant @requires
    :name: incomplete-and-skipped-tests.skipping-tests.examples.DatabaseClassSkippingTest.php

    <?php
    /**
     * @requires extension mysqli
     */
    class DatabaseTest extends PHPUnit_Framework_TestCase
    {
        /**
         * @requires PHP 5.3
         */
        public function testConnection()
        {
            // Test qui nécessite l'extension mysqli et PHP >= 5.3
        }

        // ... Tous les autres tests nécessitent l'extension mysqli
    }
    ?>

Si vous utilisez une syntaxe qui ne compile pas avec une version données de PHP, regardez
dans la configuration xml pour les inclusions dépendant de la version dans
:ref:`appendixes.configuration.testsuites`


