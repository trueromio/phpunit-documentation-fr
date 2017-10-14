

.. _writing-tests-for-phpunit:

=============================
Ecrire des tests pour PHPUnit
=============================

:numref:`writing-tests-for-phpunit.examples.StackTest.php` montre
comment nous pouvons écrire des tests en utilisant PHPUnit pour contrôler
les opérations PHP sur les tableaux. L'exemple introduit les conventions
et les étapes de base pour écrire des tests avec PHPUnit:

#.

   Les tests pour une classe ``Classe`` vont dans une classe ``ClasseTest``.

#.

   ``ClasseTest`` hérite (la plupart du temps) de ``PHPUnit_Framework_TestCase``.

#.

   Les tests sont des méthodes publiques qui sont appelées ``test*``.

   Alternativement, vous pouvez utiliser l'annotation ``@test`` dans le bloc de documentation d'une méthode pour la marquer comme étant une méthode de test.

#.

   A l'intérieur des méthodes de test, des méthodes d'assertion telles que ``assertEquals()`` (voir :ref:`writing-tests-for-phpunit.assertions`) sont utilisées pour affirmer qu'une valeur constatée correspond à une valeur attendue.

.. code-block:: php
    :caption: Tester des opérations de tableau avec PHPUnit
    :name: writing-tests-for-phpunit.examples.StackTest.php

    <?php
    class PileTest extends PHPUnit_Framework_TestCase
    {
        public function testerPushEtPop()
        {
            $pile = array();
            $this->assertEquals(0, count($pile));

            array_push($pile, 'foo');
            $this->assertEquals('foo', $pile[count($pile)-1]);
            $this->assertEquals(1, count($pile));

            $this->assertEquals('foo', array_pop($pile));
            $this->assertEquals(0, count($pile));
        }
    }
    ?>

    *Martin Fowler*:

    A chaque fois que vous avez la tentation de saisir quelque chose dans une
    instruction ``print`` ou dans une expression de débogage, écrivez le
    plutôt dans un test.

.. _writing-tests-for-phpunit.test-dependencies:

Dépendances des tests
#####################

    *Adrian Kuhn et. al.*:

    Les tests unitaires sont avant tout écrits comme étant une bonne pratique destinée
    à aider les développeurs à identifier et corriger les bugs, à refactoriser le code et à
    servir de documentation pour une unité du logiciel testé. Pour obtenir ces
    avantages, les tests unitaires doivent idéalement couvrir tous les chemins possibles
    du programme. Un test unitaire couvre usuellement un unique chemin particulier d'une
    seule fonction ou méthode. Cependant, une méthode de test n'est pas obligatoirement
    une entité encapsulée et indépendante. Souvent, il existe des dépendances implicites
    entre les méthodes de test, cachées dans l'implémentation du scénario d'un test.

PHPUnit gère la déclaration de dépendances explicites entre les méthodes
de test. De telles dépendances ne définissent pas l'ordre dans lequel les
méthodes de test doivent être exécutées, mais elles permettent l'envoi d'une
instance d'un composant de test par un producteur à des consommateurs qui
en dépendent.

-

  Un producteur est une méthode de test qui cède ses éléments testées comme valeur de sortie.

-

  Un consommateur est une méthode de test qui dépend d'un ou plusieurs producteurs et de leurs valeurs de retour.

:numref:`writing-tests-for-phpunit.examples.StackTest2.php` montre comment
utiliser l'annotation ``@depends`` pour exprimer des dépendances
entre des méthodes de test.

.. code-block:: php
    :caption: Utiliser l'annotation ``@depends`` pour exprimer des dépendances
    :name: writing-tests-for-phpunit.examples.StackTest2.php

    <?php
    class PileTest extends PHPUnit_Framework_TestCase
    {
        public function testVide()
        {
            $pile = array();
            $this->assertEmpty($pile);

            return $pile;
        }

        /**
         * @depends testVide
         */
        public function testPush(array $pile)
        {
            array_push($pile, 'foo');
            $this->assertEquals('foo', $pile[count($pile)-1]);
            $this->assertNotEmpty($pile);

            return $pile;
        }

        /**
         * @depends testPush
         */
        public function testPop(array $pile)
        {
            $this->assertEquals('foo', array_pop($pile));
            $this->assertEmpty($pile);
        }
    }
    ?>

Dans l'exemple ci-dessus, le premier test, ``testVide()``,
crée un nouveau tableau et affirme qu'il est vide. Le test renvoie ensuite
la fixture comme résultat. Le deuxième test, ``testPush()``,
dépend de ``testVide()`` et reçoit le résultat de ce test
dont il dépend comme argument. Enfin, ``testPop()``
dépend de ``testPush()``.

Pour localiser rapidement les défauts, nous voulons que notre attention soit
retenue par les tests en échecs pertinents. C'est pourquoi PHPUnit saute
l'exécution d'un test quand un test dont il dépend a échoué. Ceci améliore la
localisation des défauts en exploitant les dépendances entre les tests comme
montré dans
:numref:`writing-tests-for-phpunit.examples.DependencyFailureTest.php`.

.. code-block:: php
    :caption: Exploiter les dépendances entre les tests
    :name: writing-tests-for-phpunit.examples.DependencyFailureTest.php

    <?php
    class DependencyFailureTest extends PHPUnit_Framework_TestCase
    {
        public function testUn()
        {
            $this->assertTrue(FALSE);
        }

        /**
         * @depends testUn
         */
        public function testDeux()
        {
        }
    }
    ?>

.. code-block:: bash

    $ phpunit --verbose DependencyFailureTest
    PHPUnit 6.4.0 by Sebastian Bergmann and contributors.

    FS

    Time: 0 seconds, Memory: 5.00Mb

    There was 1 failure:

    1) DependencyFailureTest::testUn
    Failed asserting that false is true.

    /home/sb/DependencyFailureTest.php:6

    There was 1 skipped test:

    1) DependencyFailureTest::testDeux
    This test depends on "DependencyFailureTest::testUn" to pass.

    FAILURES!
    Tests: 1, Assertions: 1, Failures: 1, Skipped: 1.

Un test peut avoir plusieurs annotations ``@depends``.
PHPUnit ne change pas l'ordre dans lequel les tests sont exécutés, vous
devez donc vous assurer que les dépendances d'un test peuvent effectivement
être utilisables avant que le test ne soit lancé.

.. _writing-tests-for-phpunit.data-providers:

Fournisseur de données
######################

Une méthode de test peut recevoir des arguments arbitraires. Ces arguments doivent
être fournis par une méthode fournisseuse de données (``fournisseur()`` dans
:numref:`writing-tests-for-phpunit.data-providers.examples.DataTest.php`).
La méthode fournisseuse de données à utiliser est indiquée dans l'annotation
``@dataProvider`` annotation.

Une méthode fournisseuse de données doit être ``public`` et retourne, soit
un tableau de tableaux, soit un objet qui implémente l'interface ``Iterator``
et renvoie un tableau pour chaque itération. Pour chaque tableau qui est une partie de
l'ensemble, la méthode de test sera appelée avec comme arguments le contenu du tableau.

.. code-block:: php
    :caption: Utiliser un fournisseur de données qui renvoie un tableau de tableaux
    :name: writing-tests-for-phpunit.data-providers.examples.DataTest.php

    <?php
    class DataTest extends PHPUnit_Framework_TestCase
    {
        /**
         * @dataProvider fournisseur
         */
        public function testAdditionne($a, $b, $c)
        {
            $this->assertEquals($c, $a + $b);
        }

        public function fournisseur()
        {
            return array(
              array(0, 0, 0),
              array(0, 1, 1),
              array(1, 0, 1),
              array(1, 1, 3)
            );
        }
    }
    ?>

.. code-block:: bash

    $ phpunit DataTest
    PHPUnit 6.4.0 by Sebastian Bergmann and contributors.

    ...F

    Time: 0 seconds, Memory: 5.75Mb

    There was 1 failure:

    1) DataTest::testAdditionne with data set #3 (1, 1, 3)
    Failed asserting that 2 matches expected 3.

    /home/sb/DataTest.php:9

    FAILURES!
    Tests: 4, Assertions: 4, Failures: 1.

.. code-block:: php
    :caption: Utiliser un fournisseur de données qui renvoie un objet Iterator
    :name: writing-tests-for-phpunit.data-providers.examples.DataTest2.php

    <?php
    require 'CsvFileIterator.php';

    class DataTest extends PHPUnit_Framework_TestCase
    {
        /**
         * @dataProvider fournisseur
         */
        public function testAdditionne($a, $b, $c)
        {
            $this->assertEquals($c, $a + $b);
        }

        public function fournisseur()
        {
            return new CsvFileIterator('data.csv');
        }
    }
    ?>

.. code-block:: bash

    $ phpunit DataTest
    PHPUnit 6.4.0 by Sebastian Bergmann and contributors.

    ...F

    Time: 0 seconds, Memory: 5.75Mb

    There was 1 failure:

    1) DataTest::testAdditionne with data set #3 ('1', '1', '3')
    Failed asserting that 2 matches expected '3'.

    /home/sb/DataTest.php:11

    FAILURES!
    Tests: 4, Assertions: 4, Failures: 1.

.. code-block:: php
    :caption: La classe CsvFileIterator
    :name: writing-tests-for-phpunit.data-providers.examples.CsvFileIterator.php

    <?php
    class CsvFileIterator implements Iterator {
        protected $fichier;
        protected $key = 0;
        protected $current;

        public function __construct($fichier) {
            $this->fichier = fopen($fichier, 'r');
        }

        public function __destruct() {
            fclose($this->fichier);
        }

        public function rewind() {
            rewind($this->fichier);
            $this->current = fgetcsv($this->fichier);
            $this->key = 0;
        }

        public function valid() {
            return !feof($this->fichier);
        }

        public function key() {
            return $this->key;
        }

        public function current() {
            return $this->current;
        }

        public function next() {
            $this->current = fgetcsv($this->fichier);
            $this->key++;
        }
    }
    ?>

.. admonition:: Note

   Quand un test reçoit des entrées à la fois d'une méthode ``@dataProvider``
   et d'un ou plusieurs tests dont il ``@depends``, les arguments provenant du
   fournisseur de données arriveront avant ceux des tests dont il dépend.

.. admonition:: Note

   Quand un test dépend d'un test qui utilise des fournisseurs de données,
   le test dépendant sera exécuté quand le test dont il dépend réussira pour
   au moins un jeu de données. Le résultat d'un test qui utilise des fournisseurs
   de données ne peut pas être injecté dans un test dépendant.

.. admonition:: Note

   Tous les fournisseurs de données sont exécutés avant le premier appel
   à la fonction ``setUp``. De ce fait, vous ne pouvez accéder à
   aucune variable créée à cet endroit depuis un fournisseur de données.

.. _writing-tests-for-phpunit.exceptions:

Tester des exceptions
#####################

:numref:`writing-tests-for-phpunit.exceptions.examples.ExceptionTest.php`
montre comment utiliser l'annotation ``@expectedException`` pour tester
si une exception est levée à l'intérieur du code testé.

.. code-block:: php
    :caption: Utiliser l'annotation @expectedException
    :name: writing-tests-for-phpunit.exceptions.examples.ExceptionTest.php

    <?php
    class ExceptionTest extends PHPUnit_Framework_TestCase
    {
        /**
         * @expectedException InvalidArgumentException
         */
        public function testException()
        {
        }
    }
    ?>

.. code-block:: bash

    $ phpunit ExceptionTest
    PHPUnit 6.4.0 by Sebastian Bergmann and contributors.

    F

    Time: 0 seconds, Memory: 4.75Mb

    There was 1 failure:

    1) ExceptionTest::testException
    Expected exception InvalidArgumentException

    FAILURES!
    Tests: 1, Assertions: 1, Failures: 1.

Additionnellement, vous pouvez utiliser ``@expectedExceptionMessage``
et ``@expectedExceptionCode`` en combinaison de
``@expectedException`` pour tester le message d'exception et le code
d'exception comme montré dans
:numref:`writing-tests-for-phpunit.exceptions.examples.ExceptionTest2.php`.

.. code-block:: php
    :caption: Utiliser les annotations @expectedExceptionMessage et @expectedExceptionCode
    :name: writing-tests-for-phpunit.exceptions.examples.ExceptionTest2.php

    <?php
    class ExceptionTest extends PHPUnit_Framework_TestCase
    {
        /**
         * @expectedException        InvalidArgumentException
         * @expectedExceptionMessage Message correct
         */
        public function testExceptionPossedeLeBonMessage()
        {
            throw new InvalidArgumentException('Un message', 10);
        }

        /**
         * @expectedException     InvalidArgumentException
         * @expectedExceptionCode 20
         */
        public function testExceptionPossedeLeBonCode()
        {
            throw new InvalidArgumentException('Un message', 10);
        }
    }
    ?>

.. code-block:: bash

    $ phpunit ExceptionTest
    PHPUnit 6.4.0 by Sebastian Bergmann and contributors.

    FF

    Time: 0 seconds, Memory: 3.00Mb

    There were 2 failures:

    1) ExceptionTest::testExceptionPossedeLeBonMessage
    Failed asserting that exception message 'Un Message' contains 'Message correct'.

    2) ExceptionTest::testExceptionPossedeLeBonCode
    Failed asserting that expected exception code 20 is equal to 10.

    FAILURES!
    Tests: 2, Assertions: 4, Failures: 2.

Alternativement, vous pouvez utiliser la méthode ``setExpectedException()``
pour indiquer l'exception attendue comme montré dans :numref:`writing-tests-for-phpunit.exceptions.examples.ExceptionTest3.php`.

.. code-block:: php
    :caption: Attendre une exception qui doit être levée par le code testé
    :name: writing-tests-for-phpunit.exceptions.examples.ExceptionTest3.php

    <?php
    class ExceptionTest extends PHPUnit_Framework_TestCase
    {
        public function testException()
        {
            $this->setExpectedException('InvalidArgumentException');
        }

        public function testExceptionPossedeLeBonMessage()
        {
            $this->setExpectedException(
              'InvalidArgumentException', 'Message correct'
            );
            throw new InvalidArgumentException('Un message', 10);
        }

        public function testExceptionPossedeLeBonCode()
        {
            $this->setExpectedException(
              'InvalidArgumentException', 'Message correct', 20
            );
            throw new InvalidArgumentException('Message correct', 10);
        }
    }?>

.. code-block:: bash

    $ phpunit ExceptionTest
    PHPUnit 6.4.0 by Sebastian Bergmann and contributors.

    FFF

    Time: 0 seconds, Memory: 3.00Mb

    There were 3 failures:

    1) ExceptionTest::testException
    Expected exception InvalidArgumentException

    2) ExceptionTest::testExceptionPossedeLeBonMessage
    Failed asserting that exception message 'Un message' contains 'Message correct'.

    3) ExceptionTest::testExceptionPossedeLeBonCode
    Failed asserting that expected exception code 20 is equal to 10.

    FAILURES!
    Tests: 3, Assertions: 6, Failures: 3.

:numref:`writing-tests-for-phpunit.exceptions.tables.api`
montre les méthodes fournies pour tester des exceptions.

.. rst-class:: table
.. list-table:: Méthodes pour tester des exceptions
    :name: writing-tests-for-phpunit.exceptions.tables.api
    :header-rows: 1

    * - Méthode
      - Signification
    * - ``void setExpectedException(string $nomDeLException[, string $messageDeLException = '', integer $codeDeLException = NULL])``
      - Indiquer le ``$nomDeLException`` attendue, le ``$messageDeLException`` et le ``$codeDeLException.``
    * - ``String getExpectedException()``
      - Retourne le nom de l'exception attendue.

Vous pouvez également utiliser l'approche montrée dans
:numref:`writing-tests-for-phpunit.exceptions.examples.ExceptionTest4.php`
pour tester des exceptions.

.. code-block:: php
    :caption: Approche alternative pour tester des exceptions
    :name: writing-tests-for-phpunit.exceptions.examples.ExceptionTest4.php

    <?php
    class ExceptionTest extends PHPUnit_Framework_TestCase {
        public function testException() {
            try {
                // ... Code qui devrait lever une exception ...
            }

            catch (InvalidArgumentException $attendu) {
                return;
            }

            $this->fail('Une exception attendue n'a pas été levée.');
        }
    }
    ?>

Si le code qui devrait lever une exception dans :numref:`writing-tests-for-phpunit.exceptions.examples.ExceptionTest4.php`
ne lève pas l'exception attendue, l'appel induit à
``fail()`` va interrompre le test et signaler un problème pour ce test.
Si l'exception attendue est levée, le bloc ``catch``
sera exécuté et le test s'achèvera avec succès.

.. _writing-tests-for-phpunit.errors:

Tester les erreurs PHP
######################

Par défaut, PHPUnit convertit les erreurs, avertissements et remarques PHP
qui sont émises lors de l'exécution d'un test en exception. En utilisant ces
exceptions, vous pouvez, par exemple, attendre d'un test qu'il produise une erreur
PHP comme montré dans
:numref:`writing-tests-for-phpunit.exceptions.examples.ErrorTest.php`.

.. code-block:: php
    :caption: Attendre une erreur PHP en utilisant @expectedException
    :name: writing-tests-for-phpunit.exceptions.examples.ErrorTest.php

    <?php
    class ExpectedErrorTest extends PHPUnit_Framework_TestCase
    {
        /**
          @expectedException PHPUnit\Framework\Error
         */
        public function testEchecInclude()
        {
            include 'fichier_qui_n_existe_pas.php';
        }
    }
    ?>

.. code-block:: bash

    $ phpunit ExpectedErrorTest
    PHPUnit 6.4.0 by Sebastian Bergmann and contributors.

    .

    Time: 0 seconds, Memory: 5.25Mb

    OK (1 test, 1 assertion)

``PHPUnit\Framework\Error\Notice`` et
``PHPUnit\Framework\Error\Warning`` représentent respectivement
les remarques et les avertissements PHP.

.. admonition:: Note

   Vous devriez être aussi précis que possible lorsque vous testez des exceptions.
   Tester avec des classes qui sont trop génériques peut conduire à des effets de
   bord indésirables. C'est pourquoi tester la présence de la classe
   ``Exception`` avec ``@expectedException`` ou
   ``setExpectedException()`` n'est plus autorisé.

Quand les tests s'appuient sur des fonctions php qui déclenchent des erreurs
comme ``fopen``, il peut parfois être utile d'utiliser la
suppression d'erreur lors du test. Ceci permet de contrôler les valeurs de retour
en supprimant les remarques qui auraient conduit à une
``PHPUnit\Framework\Error\Notice`` de phpunit.

.. code-block:: php
    :caption: Tester des valeurs de retour d'un code source qui utilise des erreurs PHP
    :name: writing-tests-for-phpunit.exceptions.examples.TriggerErrorReturnValue.php

    <?php
    class ErrorSuppressionTest extends PHPUnit_Framework_TestCase
    {
        public function testEcritureFichier() {
            $writer = new FileWriter;
            $this->assertFalse(@$writer->ecrit('/non-accessible-en-ecriture/fichier', 'texte'));
        }
    }
    class FileWriter
    {
        public function ecrit($fichier, $contenu) {
            $fichier = fopen($fichier, 'w');
            if($fichier == false) {
                return false;
            }
            // ...
        }
    }

    ?>

.. code-block:: bash

    $ phpunit ErrorSuppressionTest
    PHPUnit 6.4.0 by Sebastian Bergmann and contributors.

    .

    Time: 1 seconds, Memory: 5.25Mb

    OK (1 test, 1 assertion)

Sans la suppression d'erreur, le test échouerait à rapporter
``fopen(/non-accessible-en-ecriture/fichier): failed to open stream:
    No such file or directory``.

.. _writing-tests-for-phpunit.output:

Tester la sortie écran
######################

Quelquefois, vous voulez affirmer que l'exécution d'une méthode, par
exemple, produit une sortie écran donnée (via ``echo`` ou
``print``, par exemple). La classe
``PHPUnit_Framework_TestCase`` utilise la fonctionnalité de
en tampon de PHP `mise en tampon de la sortie écran <http://www.php.net/manual/en/ref.outcontrol.php>`_ de PHP pour fournir la fonctionnalité qui est nécessaire pour cela.

:numref:`writing-tests-for-phpunit.output.examples.OutputTest.php`
montre comment utiliser la méthode ``expectOutputString()`` pour
indiquer la sortie écran attendue. Si la sortie écran attendue n'est pas générée, le test
sera compté comme étant en échec.

.. code-block:: php
    :caption: Tester la sortie écran d'une fonction ou d'une méthode
    :name: writing-tests-for-phpunit.output.examples.OutputTest.php

    <?php
    class OutputTest extends PHPUnit_Framework_TestCase
    {
        public function testFooAttenduFooObtenu()
        {
            $this->expectOutputString('foo');
            print 'foo';
        }

        public function testBarAttenduBazAttendu()
        {
            $this->expectOutputString('bar');
            print 'baz';
        }
    }
    ?>

.. code-block:: bash

    $ phpunit OutputTest
    PHPUnit 6.4.0 by Sebastian Bergmann and contributors.

    .F

    Time: 0 seconds, Memory: 5.75Mb

    There was 1 failure:

    1) OutputTest::testBarAttenduBazObtenu
    Failed asserting that two strings are equal.
    --- Expected
    +++ Actual
    @@ @@
    -'bar'
    +'baz'

    FAILURES!
    Tests: 2, Assertions: 2, Failures: 1.

:numref:`writing-tests-for-phpunit.output.tables.api`
montre les méthodes fournies pour tester les sorties écran

.. rst-class:: table
.. list-table:: Méthodes pour tester les sorties écran
    :name: writing-tests-for-phpunit.output.tables.api
    :header-rows: 1

    * - Méthode
      - Signification
    * - ``void expectOutputRegex(string $expressionRationnelle)``
      - Indique que l'on s'attend à ce que la sortie écran corresponde à une ``$expressionRationnelle``.
    * - ``void expectOutputString(string $attenduString)``
      - Indique que l'on s'attend que la sortie écran soit égale à une ``$chaineDeCaracteresAttendue``.
    * - ``bool setOutputCallback(callable $callback)``
      - Configure une fonction de rappel (callback) qui est utilisée, par exemple, formater la sortie écran effective.

.. admonition:: Note

   Merci de noter que PHPUnit absorbe toutes les sorties écran qui sont
   émises lors de l'exécution d'un test. En mode strict, un test qui
   produit une sortie écran échouera.

.. _writing-tests-for-phpunit.assertions:

Assertions
##########

Cette section liste les diverses méthodes d'assertion qui sont disponibles.

.. _writing-tests-for-phpunit.assertions.assertArrayHasKey:

assertArrayHasKey()
===================

``assertArrayHasKey(mixed $clef, array $tableau[, string $message = ''])``

Rapporte une erreur identifiée par un ``$message`` si le ``$tableau`` ne contient pas la ``$clef``.

``assertArrayNotHasKey()`` est l'inverse de cette assertion et prend les mêmes arguments.

.. code-block:: php
    :caption: Utilisation de assertArrayHasKey()
    :name: writing-tests-for-phpunit.assertions.assertArrayHasKey.example

    <?php
    class TableauPossedeUneClefTest extends PHPUnit_Framework_TestCase
    {
        public function testEchec()
        {
            $this->assertArrayHasKey('foo', array('bar' => 'baz'));
        }
    }
    ?>

.. code-block:: bash

    $ phpunit TableauPossedeUneClefTest
    PHPUnit 6.4.0 by Sebastian Bergmann and contributors.

    F

    Time: 0 seconds, Memory: 5.00Mb

    There was 1 failure:

    1) TableauPossedeUneClefTest::testEchec
    Failed asserting that an array has the key 'foo'.

    /home/sb/TableauPossedeUneClefTest.php:6

    FAILURES!
    Tests: 1, Assertions: 1, Failures: 1.

.. _writing-tests-for-phpunit.assertions.assertClassHasAttribute:

assertClassHasAttribute()
=========================

``assertClassHasAttribute(string $nomAttribut, string $nomClasse[, string $message = ''])``

Rapporte une erreur identifiée par un ``$message`` si ``$nomClasse::nomAttribut`` n'existe pas.

``assertClassNotHasAttribute()`` est l'inverse de cette assertion et prend les mêmes arguments.

.. code-block:: php
    :caption: Utilisation de assertClassHasAttribute()
    :name: writing-tests-for-phpunit.assertions.assertClassHasAttribute.example

    <?php
    class ClassePossedeUnAttributTest extends PHPUnit_Framework_TestCase
    {
        public function testEchec()
        {
            $this->assertClassHasAttribute('foo', 'stdClass');
        }
    }
    ?>

.. code-block:: bash

    $ phpunit ClassePossedeUnAttributTest
    PHPUnit 6.4.0 by Sebastian Bergmann and contributors.

    F

    Time: 0 seconds, Memory: 4.75Mb

    There was 1 failure:

    1) ClassePossedeUnAttributTest::testEchec
    Failed asserting that class "stdClass" has attribute "foo".

    /home/sb/ClassePossedeUnAttributTest.php:6

    FAILURES!
    Tests: 1, Assertions: 1, Failures: 1.

.. _writing-tests-for-phpunit.assertions.assertClassHasStaticAttribute:

assertClassHasStaticAttribute()
===============================

``assertClassHasStaticAttribute(string $nomAttribut, string $nomClasse[, string $message = ''])``

Rapporte une erreur identifiée par un ``$message`` si ``$nomClasse::nomAttribut`` n'existe pas.

``assertClassNotHasStaticAttribute()`` est l'inverse de cette assertion et prend les mêmes arguments.

.. code-block:: php
    :caption: Utilisation de assertClassHasStaticAttribute()
    :name: writing-tests-for-phpunit.assertions.assertClassHasStaticAttribute.example

    <?php
    class ClassePossedeUnAttributStatiqueTest extends PHPUnit_Framework_TestCase
    {
        public function testEchec()
        {
            $this->assertClassHasStaticAttribute('foo', 'stdClass');
        }
    }
    ?>

.. code-block:: bash

    $ phpunit ClassePossedeUnAttributStatiqueTest
    PHPUnit 6.4.0 by Sebastian Bergmann and contributors.

    F

    Time: 0 seconds, Memory: 4.75Mb

    There was 1 failure:

    1) ClassHasStaticAttributeTest::testEchec
    Failed asserting that class "stdClass" has static attribute "foo".

    /home/sb/ClassePossedeUnAttributStatiqueTest.php:6

    FAILURES!
    Tests: 1, Assertions: 1, Failures: 1.

.. _writing-tests-for-phpunit.assertions.assertContains:

assertContains()
================

``assertContains(mixed $aiguille, Iterator|array $meuleDeFoin[, string $message = ''])``

Rapporte une erreur identifiée par un ``$message`` si ``$aiguille`` n'est pas un élément de ``$meuleDeFoin``.

``assertNotContains()`` est l'inverse de cette assertion et prend les mêmes arguments.

``assertAttributeContains()`` et ``assertAttributeNotContains()`` sont des enrobeurs de commodité qui utilisent l'attribut ``public``, ``protected`` ou ``private`` d'une classe ou d'un objet comme meuleDeFoin.

.. code-block:: php
    :caption: Utilisation de assertContains()
    :name: writing-tests-for-phpunit.assertions.assertContains.example

    <?php
    class ContainsTest extends PHPUnit_Framework_TestCase
    {
        public function testEchec()
        {
            $this->assertContains(4, array(1, 2, 3));
        }
    }
    ?>

.. code-block:: bash

    $ phpunit ContainsTest
    PHPUnit 6.4.0 by Sebastian Bergmann and contributors.

    F

    Time: 0 seconds, Memory: 5.00Mb

    There was 1 failure:

    1) ContainsTest::testEchec
    Failed asserting that an array contains 4.

    /home/sb/ContainsTest.php:6

    FAILURES!
    Tests: 1, Assertions: 1, Failures: 1.

``assertContains(string $aiguille, string $meuleDeFoin[, string $message = '', boolean $ignorerLaCasse = FALSE])``

Rapporte une erreur identifiée par un ``$message`` si ``$aiguille`` n'est pas un sous chaîne de ``$meuleDeFoin``.

Si ``$ignorerLaCasse`` est ``TRUE``, le test sera insensible à la casse.

.. code-block:: php
    :caption: Utilisation de assertContains()
    :name: writing-tests-for-phpunit.assertions.assertContains.example2

    <?php
    class ContainsTest extends PHPUnit_Framework_TestCase
    {
        public function testEchec()
        {
            $this->assertContains('baz', 'foobar');
        }
    }
    ?>

.. code-block:: bash

    $ phpunit ContainsTest
    PHPUnit 6.4.0 by Sebastian Bergmann and contributors.

    F

    Time: 0 seconds, Memory: 5.00Mb

    There was 1 failure:

    1) ContainsTest::testEchec
    Failed asserting that 'foobar' contains "baz".

    /home/sb/ContainsTest.php:6

    FAILURES!
    Tests: 1, Assertions: 1, Failures: 1.

.. code-block:: php
    :caption: Usage of assertContains() with $ignoreCase
    :name: appendixes.assertions.assertContains.example3

    <?php
    class ContainsTest extends PHPUnit_Framework_TestCase
    {
        public function testEchec()
        {
            $this->assertContains('foo', 'FooBar');
        }

        public function testOK()
        {
            $this->assertContains('foo', 'FooBar', '', true);
        }
    }
    ?>

.. code-block:: bash

    $ phpunit ContainsTest
    PHPUnit 6.4.0 by Sebastian Bergmann and contributors.

    F.

    Time: 0 seconds, Memory: 2.75Mb

    There was 1 failure:

    1) ContainsTest::testEchec
    Failed asserting that 'FooBar' contains "foo".

    /home/sb/ContainsTest.php:6

    FAILURES!
    Tests: 2, Assertions: 2, Failures: 1.

.. _writing-tests-for-phpunit.assertions.assertContainsOnly:

assertContainsOnly()
====================

``assertContainsOnly(string $type, Iterator|array $meuleDeFoin[, boolean $estUnTypeNatif = NULL, string $message = ''])``

Rapporte une erreur identifiée par le ``$message`` si ``$meuleDeFoin`` ne contient pas que des variables du type ``$type``.

``$estUnTypeNatif`` est un drapeau qui indique si ``$type`` est un type natif de PHP ou pas.

``assertNotContainsOnly()`` est l'inverse de cette assertion et prend les mêmes arguments.

``assertAttributeContainsOnly()`` et ``assertAttributeNotContainsOnly()`` sont des enrobeurs de commodité qui utilisent un attribut ``public``, ``protected`` ou ``private`` d'une classe ou d'un objet en tant que valeur constatée.

.. code-block:: php
    :caption: Utilisation de assertContainsOnly()
    :name: writing-tests-for-phpunit.assertions.assertContainsOnly.example

    <?php
    class ContainsOnlyTest extends PHPUnit_Framework_TestCase
    {
        public function testEchec()
        {
            $this->assertContainsOnly('string', array('1', '2', 3));
        }
    }
    ?>

.. code-block:: bash

    $ phpunit ContainsOnlyTest
    PHPUnit 6.4.0 by Sebastian Bergmann and contributors.

    F

    Time: 0 seconds, Memory: 5.00Mb

    There was 1 failure:

    1) ContainsOnlyTest::testEchec
    Failed asserting that Array (
        0 => '1'
        1 => '2'
        2 => 3
    ) contains only values of type "string".

    /home/sb/ContainsOnlyTest.php:6

    FAILURES!
    Tests: 1, Assertions: 1, Failures: 1.

.. _writing-tests-for-phpunit.assertions.assertCount:

assertCount()
=============

``assertCount($nombreAttendu, $meuleDeFoin[, string $message = ''])``

Rapporte une erreur identifiée par ``$message`` si le nombre d'éléments dans ``$meuleDeFoin`` n'est pas ``$nombreAttendu``.

``assertNotCount()`` est l'inverse de cette assertion et prend les mêmes arguments.

.. code-block:: php
    :caption: Utilisation de assertCount()
    :name: writing-tests-for-phpunit.assertions.assertCount.example

    <?php
    class CountTest extends PHPUnit_Framework_TestCase
    {
        public function testEchec()
        {
            $this->assertCount(0, array('foo'));
        }
    }
    ?>

.. code-block:: bash

    $ phpunit CountTest
    PHPUnit 6.4.0 by Sebastian Bergmann and contributors.

    F

    Time: 0 seconds, Memory: 4.75Mb

    There was 1 failure:

    1) CountTest::testEchec
    Failed asserting that actual size 1 matches expected size 0.

    /home/sb/CountTest.php:6

    FAILURES!
    Tests: 1, Assertions: 1, Failures: 1.

.. _writing-tests-for-phpunit.assertions.assertEmpty:

assertEmpty()
=============

``assertEmpty(mixed $constate[, string $message = ''])``

Rapporte une erreur identifiée par ``$message`` si ``$constate`` n'est pas vide.

``assertNotEmpty()`` est l'inverse de cette assertion et prend les mêmes arguments.

``assertAttributeEmpty()`` et ``assertAttributeNotEmpty()`` sont des enrobeurs de commodité qui peuvent être appliqués à un attribut ``public``, ``protected`` ou ``private`` d'une classe ou d'un objet.

.. code-block:: php
    :caption: Utilisation de assertEmpty()
    :name: writing-tests-for-phpunit.assertions.assertEmpty.example

    <?php
    class VideTest extends PHPUnit_Framework_TestCase
    {
        public function testEchec()
        {
            $this->assertEmpty(array('foo'));
        }
    }
    ?>

.. code-block:: bash

    $ phpunit VideTest
    PHPUnit 6.4.0 by Sebastian Bergmann and contributors.

    F

    Time: 0 seconds, Memory: 4.75Mb

    There was 1 failure:

    1) VideTest::testEchec
    Failed asserting that an array is empty.

    /home/sb/VideTest.php:6

    FAILURES!
    Tests: 1, Assertions: 1, Failures: 1.

.. _writing-tests-for-phpunit.assertions.assertEqualXMLStructure:

assertEqualXMLStructure()
=========================

``assertEqualXMLStructure(DOMElement $elementAttendu, DOMElement $elementConstate[, boolean $verifieAttributs = FALSE, string $message = ''])``

Rapporte une erreur identifiée par ``$message`` si la structure XML de l'élément DOMElement de ``$elementConstate`` n'est pas égale à la structure de l'élément DOMElement de ``$elementAttendu``.

.. code-block:: php
    :caption: Utilisation de assertEqualXMLStructure()
    :name: writing-tests-for-phpunit.assertions.assertEqualXMLStructure.example

    <?php
    class StructuresXMLSontEgalesTest extends PHPUnit_Framework_TestCase
    {
        public function testEchecAvecDifferentsNomsdeNoeud()
        {
            $attendu = new DOMElement('foo');
            $constate = new DOMElement('bar');

            $this->assertEqualXMLStructure($attendu, $constate);
        }

        public function testEchecAvecDifferentsAttributsDeNoeud()
        {
            $attendu = new DOMDocument;
            $attendu->loadXML('<foo bar="true" />');

            $constate = new DOMDocument;
            $constate->loadXML('<foo/>');

            $this->assertEqualXMLStructure(
              $attendu->firstChild, $constate->firstChild, TRUE
            );
        }

        public function testEchecAvecDecompteDifferentdesNoeudsFils()
        {
            $attendu = new DOMDocument;
            $attendu->loadXML('<foo><bar/><bar/><bar/></foo>');

            $constate = new DOMDocument;
            $constate->loadXML('<foo><bar/></foo>');

            $this->assertEqualXMLStructure(
              $attendu->firstChild, $constate->firstChild
            );
        }

        public function testEchecAvecDesNoeudsFilsDifferents()
        {
            $attendu = new DOMDocument;
            $attendu->loadXML('<foo><bar/><bar/><bar/></foo>');

            $constate = new DOMDocument;
            $constate->loadXML('<foo><baz/><baz/><baz/></foo>');

            $this->assertEqualXMLStructure(
              $attendu->firstChild, $constate->firstChild
            );
        }
    }
    ?>

.. code-block:: bash

    $ phpunit StructuresXMLSontEgalesTest
    PHPUnit 6.4.0 by Sebastian Bergmann and contributors.

    FFFF

    Time: 0 seconds, Memory: 5.75Mb

    There were 4 failures:

    1) StructuresXMLSontEgalesTest::testEchecAvecDifferentsNomsdeNoeud
    Failed asserting that two strings are equal.
    --- Expected
    +++ Actual
    @@ @@
    -'foo'
    +'bar'

    /home/sb/StructuresXMLSontEgalesTest.php:9

    2) StructuresXMLSontEgalesTest::testEchecAvecDifferentsAttributsDeNoeud
    Number of attributes on node "foo" does not match
    Failed asserting that 0 matches expected 1.

    /home/sb/StructuresXMLSontEgalesTest.php:22

    3)  StructuresXMLSontEgalesTest::testEchecAvecDecompteDifferentdesNoeudsFils
    Number of child nodes of "foo" differs
    Failed asserting that 1 matches expected 3.

    /home/sb/StructuresXMLSontEgalesTest.php:35

    4)  StructuresXMLSontEgalesTest::testEchecAvecDesNoeudsFilsDifferents
    Failed asserting that two strings are equal.
    --- Expected
    +++ Actual
    @@ @@
    -'bar'
    +'baz'

    /home/sb/StructuresXMLSontEgalesTest.php:48

    FAILURES!
    Tests: 4, Assertions: 8, Failures: 4.

.. _writing-tests-for-phpunit.assertions.assertEquals:

assertEquals()
==============

``assertEquals(mixed $attendu, mixed $constate[, string $message = ''])``

Rapporte une erreur identifiée par le ``$message`` si les deux variables ``$attendu`` et ``$constate`` ne sont pas égales.

``assertNotEquals()`` est l'inverse de cette assertion et prend les mêmes paramètres.

``assertAttributeEquals()`` et ``assertAttributeNotEquals()`` sont des enrobeurs de commodité qui utilisent un attribut ``public``, ``protected`` ou ``private`` d'une classe ou d'un objet comme valeur constatée.

.. code-block:: php
    :caption: Utilisation de assertEquals()
    :name: writing-tests-for-phpunit.assertions.assertEquals.example

    <?php
    class EqualsTest extends PHPUnit_Framework_TestCase
    {
        public function testEchec()
        {
            $this->assertEquals(1, 0);
        }

        public function testEchec2()
        {
            $this->assertEquals('bar', 'baz');
        }

        public function testEchec3()
        {
            $this->assertEquals("foo\nbar\nbaz\n", "foo\nbah\nbaz\n");
        }
    }
    ?>

.. code-block:: bash

    $ phpunit EqualsTest
    PHPUnit 6.4.0 by Sebastian Bergmann and contributors.

    FFF

    Time: 0 seconds, Memory: 5.25Mb

    There were 3 failures:

    1) EqualsTest::testEchec
    Failed asserting that 0 matches expected 1.

    /home/sb/EqualsTest.php:6

    2) EqualsTest::testEchec2
    Failed asserting that two strings are equal.
    --- Expected
    +++ Actual
    @@ @@
    -'bar'
    +'baz'

    /home/sb/EqualsTest.php:11

    3) EqualsTest::testEchec3
    Failed asserting that two strings are equal.
    --- Expected
    +++ Actual
    @@ @@
     'foo
    -bar
    +bah
     baz
     '

    /home/sb/EqualsTest.php:16

    FAILURES!
    Tests: 3, Assertions: 3, Failures: 3.

Des comparaisons plus spécifiques sont utilisées pour des types d'arguments ``$attendu`` et ``$constate`` plus spécifiques, voir ci-dessous.

``assertEquals(float $attendu, float $constate[, string $message = '', float $delta = 0])``

Rapporte une erreur identifiée par le ``$message`` si les deux nombres à virgule flottante ``$attendu`` et ``$constate`` ne sont pas à moins de ``$delta`` l'un de l'autre.

Merci de lire `comparing floating-point numbers <http://en.wikipedia.org/wiki/IEEE_754#Comparing_floating-point_numbers>`_ pour comprendre pourquoi ``$delta`` est indispensable.

.. code-block:: php
    :caption: Utilisation de assertEquals() avec des nombres à virgule flottante
    :name: writing-tests-for-phpunit.assertions.assertEquals.example2

    <?php
    class EqualsTest extends PHPUnit_Framework_TestCase
    {
        public function testSucces()
        {
            $this->assertEquals(1.0, 1.1, '', 0.2);
        }

        public function testEchec()
        {
            $this->assertEquals(1.0, 1.1);
        }
    }
    ?>

.. code-block:: bash

    $ phpunit EqualsTest
    PHPUnit 6.4.0 by Sebastian Bergmann and contributors.

    .F

    Time: 0 seconds, Memory: 5.75Mb

    There was 1 failure:

    1) EqualsTest::testEchec
    Failed asserting that 1.1 matches expected 1.0.

    /home/sb/EqualsTest.php:11

    FAILURES!
    Tests: 2, Assertions: 2, Failures: 1.

``assertEquals(DOMDocument $attendu, DOMDocument $constate[, string $message = ''])``

Rapporte une erreur identifiée par le ``$message`` si la forme canonique non commentée des documents XML représentés par les deux objets DOMDocument objects ``$attendu`` et ``$constate`` ne sont pas égaux.

.. code-block:: php
    :caption: Utilisation de assertEquals() avec des objets DOMDocument
    :name: writing-tests-for-phpunit.assertions.assertEquals.example3

    <?php
    class EqualsTest extends PHPUnit_Framework_TestCase
    {
        public function testEchec()
        {
            $attendu = new DOMDocument;
            $attendu->loadXML('<foo><bar/></foo>');

            $constate = new DOMDocument;
            $constate->loadXML('<bar><foo/></bar>');

            $this->assertEquals($attendu, $constate);
        }
    }
    ?>

.. code-block:: bash

    $ phpunit EqualsTest
    PHPUnit 6.4.0 by Sebastian Bergmann and contributors.

    F

    Time: 0 seconds, Memory: 5.00Mb

    There was 1 failure:

    1) EqualsTest::testEchec
    Failed asserting that two DOM documents are equal.
    --- Expected
    +++ Actual
    @@ @@
     <?xml version="1.0"?>
    -<foo>
    -  <bar/>
    -</foo>
    +<bar>
    +  <foo/>
    +</bar>

    /home/sb/EqualsTest.php:12

    FAILURES!
    Tests: 1, Assertions: 1, Failures: 1.

``assertEquals(object $attendu, object $constate[, string $message = ''])``

Rapporte une erreur identifiée par le ``$message`` si les deux objets ``$attendu`` et ``$constate`` ne possède pas des valeurs d'attribut égales.

.. code-block:: php
    :caption: Utilisation de assertEquals() avec des objets
    :name: writing-tests-for-phpunit.assertions.assertEquals.example4

    <?php
    class EqualsTest extends PHPUnit_Framework_TestCase
    {
        public function testEchec()
        {
            $attendu = new stdClass;
            $attendu->foo = 'foo';
            $attendu->bar = 'bar';

            $constate = new stdClass;
            $constate->foo = 'bar';
            $constate->baz = 'bar';

            $this->assertEquals($attendu, $constate);
        }
    }
    ?>

.. code-block:: bash

    $ phpunit EqualsTest
    PHPUnit 6.4.0 by Sebastian Bergmann and contributors.

    F

    Time: 0 seconds, Memory: 5.25Mb

    There was 1 failure:

    1) EqualsTest::testEchec
    Failed asserting that two objects are equal.
    --- Expected
    +++ Actual
    @@ @@
     stdClass Object (
    -    'foo' => 'foo'
    -    'bar' => 'bar'
    +    'foo' => 'bar'
    +    'baz' => 'bar'
     )

    /home/sb/EqualsTest.php:14

    FAILURES!
    Tests: 1, Assertions: 1, Failures: 1.

``assertEquals(array $attendu, array $constate[, string $message = ''])``

Rapporte une erreur identifiée par le ``$message`` si les deux tableaux ``$attendu`` et ``$constate`` ne sont pas égaux.

.. code-block:: php
    :caption: Utilisation de assertEquals() avec des tableaux
    :name: writing-tests-for-phpunit.assertions.assertEquals.example5

    <?php
    class EqualsTest extends PHPUnit_Framework_TestCase
    {
        public function testEchec()
        {
            $this->assertEquals(array('a', 'b', 'c'), array('a', 'c', 'd'));
        }
    }
    ?>

.. code-block:: bash

    $ phpunit EqualsTest
    PHPUnit 6.4.0 by Sebastian Bergmann and contributors.

    F

    Time: 0 seconds, Memory: 5.25Mb

    There was 1 failure:

    1) EqualsTest::testEchec
    Failed asserting that two arrays are equal.
    --- Expected
    +++ Actual
    @@ @@
     Array (
         0 => 'a'
    -    1 => 'b'
    -    2 => 'c'
    +    1 => 'c'
    +    2 => 'd'
     )

    /home/sb/EqualsTest.php:6

    FAILURES!
    Tests: 1, Assertions: 1, Failures: 1.

.. _writing-tests-for-phpunit.assertions.assertFalse:

assertFalse()
=============

``assertFalse(bool $condition[, string $message = ''])``

Rapporte une erreur identifiée par le ``$message`` si la ``$condition`` est ``TRUE`` (VRAIE).

``assertNotFalse()`` est l'inverse de cette assertion et prend les mêmes arguments.

.. code-block:: php
    :caption: Utilisation de assertFalse()
    :name: writing-tests-for-phpunit.assertions.assertFalse.example

    <?php
    class FalseTest extends PHPUnit_Framework_TestCase
    {
        public function testEchec()
        {
            $this->assertFalse(TRUE);
        }
    }
    ?>

.. code-block:: bash

    $ phpunit FalseTest
    PHPUnit 6.4.0 by Sebastian Bergmann and contributors.

    F

    Time: 0 seconds, Memory: 5.00Mb

    There was 1 failure:

    1) FalseTest::testEchec
    Failed asserting that true is false.

    /home/sb/FalseTest.php:6

    FAILURES!
    Tests: 1, Assertions: 1, Failures: 1.

.. _writing-tests-for-phpunit.assertions.assertFileEquals:

assertFileEquals()
==================

``assertFileEquals(string $attendu, string $constate[, string $message = ''])``

Rapporte une erreur identifiée par le ``$message`` si le fichier identifié par ``$attendu`` ne possède pas le même contenu que le fichier identifié par ``$constate``.

``assertFileNotEquals()`` est l'inverse de cette assertion et prend les mêmes arguments.

.. code-block:: php
    :caption: Utilisation de assertFileEquals()
    :name: writing-tests-for-phpunit.assertions.assertFileEquals.example

    <?php
    class FileEqualsTest extends PHPUnit_Framework_TestCase
    {
        public function testEchec()
        {
            $this->assertFileEquals('/home/sb/attendu', '/home/sb/constate');
        }
    }
    ?>

.. code-block:: bash

    $ phpunit FileEqualsTest
    PHPUnit 6.4.0 by Sebastian Bergmann and contributors.

    F

    Time: 0 seconds, Memory: 5.25Mb

    There was 1 failure:

    1) FileEqualsTest::testEchec
    Failed asserting that two strings are equal.
    --- Expected
    +++ Actual
    @@ @@
    -'contenu attendu
    +'contenu constaté
     '

    /home/sb/FileEqualsTest.php:6

    FAILURES!
    Tests: 1, Assertions: 3, Failures: 1.

.. _writing-tests-for-phpunit.assertions.assertFileExists:

assertFileExists()
==================

``assertFileExists(string $nomfichier[, string $message = ''])``

Rapporte une erreur identifiée par le ``$message`` si le fichier désigné par ``$nomfichier`` n'existe pas.

``assertFileNotExists()`` est l'inverse de cette assertion et prend les mêmes arguments.

.. code-block:: php
    :caption: Utilisation de assertFileExists()
    :name: writing-tests-for-phpunit.assertions.assertFileExists.example

    <?php
    class FileExistsTest extends PHPUnit_Framework_TestCase
    {
        public function testEchec()
        {
            $this->assertFileExists('/chemin/vers/fichier');
        }
    }
    ?>

.. code-block:: bash

    $ phpunit FileExistsTest
    PHPUnit 6.4.0 by Sebastian Bergmann and contributors.

    F

    Time: 0 seconds, Memory: 4.75Mb

    There was 1 failure:

    1) FileExistsTest::testEchec
    Failed asserting that file "/chemin/vers/fichier" exists.

    /home/sb/FileExistsTest.php:6

    FAILURES!
    Tests: 1, Assertions: 1, Failures: 1.

.. _writing-tests-for-phpunit.assertions.assertGreaterThan:

assertGreaterThan()
===================

``assertGreaterThan(mixed $attendu, mixed $constate[, string $message = ''])``

Rapporte une erreur identifiée par le ``$message`` si la valeur de ``$constate`` n'est pas supérieure à la valeur de ``$attendu``.

``assertAttributeGreaterThan()`` est un enrobeur de commodité qui utilise un attribut ``public``, ``protected`` ou ``private`` d'une classe ou d'un objet comme valeur constatée.

.. code-block:: php
    :caption: Utilisation de assertGreaterThan()
    :name: writing-tests-for-phpunit.assertions.assertGreaterThan.example

    <?php
    class GreaterThanTest extends PHPUnit_Framework_TestCase
    {
        public function testEchec()
        {
            $this->assertGreaterThan(2, 1);
        }
    }
    ?>

.. code-block:: bash

    $ phpunit GreaterThanTest
    PHPUnit 6.4.0 by Sebastian Bergmann and contributors.

    F

    Time: 0 seconds, Memory: 5.00Mb

    There was 1 failure:

    1) GreaterThanTest::testEchec
    Failed asserting that 1 is greater than 2.

    /home/sb/GreaterThanTest.php:6

    FAILURES!
    Tests: 1, Assertions: 1, Failures: 1.

.. _writing-tests-for-phpunit.assertions.assertGreaterThanOrEqual:

assertGreaterThanOrEqual()
==========================

``assertGreaterThanOrEqual(mixed $attendu, mixed $constate[, string $message = ''])``

Rapporte une erreur identifiée par le ``$message`` si la valeur de ``$constate`` n'est pas supérieure ou égale à la valeur de ``$attendu``.

``assertAttributeGreaterThanOrEqual()`` est un enrobeur de commodité qui utilise un attribut ``public``, ``protected`` ou ``private`` d'une classe ou d'un objet comme valeur constatée.

.. code-block:: php
    :caption: Utilisation de assertGreaterThanOrEqual()
    :name: writing-tests-for-phpunit.assertions.assertGreaterThanOrEqual.example

    <?php
    class GreatThanOrEqualTest extends PHPUnit_Framework_TestCase
    {
        public function testEchec()
        {
            $this->assertGreaterThanOrEqual(2, 1);
        }
    }
    ?>

.. code-block:: bash

    $ phpunit GreaterThanOrEqualTest
    PHPUnit 6.4.0 by Sebastian Bergmann and contributors.

    F

    Time: 0 seconds, Memory: 5.25Mb

    There was 1 failure:

    1) GreatThanOrEqualTest::testEchec
    Failed asserting that 1 is equal to 2 or is greater than 2.

    /home/sb/GreaterThanOrEqualTest.php:6

    FAILURES!
    Tests: 1, Assertions: 2, Failures: 1.

.. _writing-tests-for-phpunit.assertions.assertInstanceOf:

assertInstanceOf()
==================

``assertInstanceOf($attendu, $constate[, $message = ''])``

Rapporte une erreur identifiée par le ``$message`` si ``$constate`` n'est pas une instance de ``$attendu``.

``assertNotInstanceOf()`` est l'inverse de cette assertion et prend les mêmes arguments.

``assertAttributeInstanceOf()`` et ``assertAttributeNotInstanceOf()`` sont des enrobeurs de commodité qui peuvent être appliqué à un attribut ``public``, ``protected`` ou ``private`` d'une classe ou d'un objet.

.. code-block:: php
    :caption: Utilisation de assertInstanceOf()
    :name: writing-tests-for-phpunit.assertions.assertInstanceOf.example

    <?php
    class InstanceOfTest extends PHPUnit_Framework_TestCase
    {
        public function testEchec()
        {
            $this->assertInstanceOf('RuntimeException', new Exception);
        }
    }
    ?>

.. code-block:: bash

    $ phpunit InstanceOfTest
    PHPUnit 6.4.0 by Sebastian Bergmann and contributors.

    F

    Time: 0 seconds, Memory: 5.00Mb

    There was 1 failure:

    1) InstanceOfTest::testEchec
    Failed asserting that Exception Object (...) is an instance of class "RuntimeException".

    /home/sb/InstanceOfTest.php:6

    FAILURES!
    Tests: 1, Assertions: 1, Failures: 1.

.. _writing-tests-for-phpunit.assertions.assertInternalType:

assertInternalType()
====================

``assertInternalType($attendu, $constate[, $message = ''])``

Rapporte une erreur identifiée par le ``$message`` si ``$constate`` n'est pas du type ``$attendu``.

``assertNotInternalType()`` est l'inverse de cette assertion et prend les mêmes arguments.

``assertAttributeInternalType()`` et ``assertAttributeNotInternalType()`` sont des enrobeurs de commodité qui peuvent être appliqués à un attribut ``public``, ``protected`` ou ``private`` d'une classe ou d'un objet.

.. code-block:: php
    :caption: Utilisation de assertInternalType()
    :name: writing-tests-for-phpunit.assertions.assertInternalType.example

    <?php
    class InternalTypeTest extends PHPUnit_Framework_TestCase
    {
        public function testEchec()
        {
            $this->assertInternalType('string', 42);
        }
    }
    ?>

.. code-block:: bash

    $ phpunit InternalTypeTest
    PHPUnit 6.4.0 by Sebastian Bergmann and contributors.

    F

    Time: 0 seconds, Memory: 5.00Mb

    There was 1 failure:

    1) InternalTypeTest::testEchec
    Failed asserting that 42 is of type "string".

    /home/sb/InternalTypeTest.php:6

    FAILURES!
    Tests: 1, Assertions: 1, Failures: 1.

.. _writing-tests-for-phpunit.assertions.assertJsonFileEqualsJsonFile:

assertJsonFileEqualsJsonFile()
==============================

``assertJsonFileEqualsJsonFile(mixed $fichierAttendu, mixed $fichierConstate[, string $message = ''])``

Rapporte une erreur identifiée par ``$message`` si la valeur de ``$fichierConstate`` correspond
à la valeur de ``$fichierAttendu``.

.. code-block:: php
    :caption: Utilisation de assertJsonFileEqualsJsonFile()
    :name: writing-tests-for-phpunit.assertions.assertJsonFileEqualsJsonFile.example

    <?php
    class JsonFileEqualsJsonFile extends PHPUnit_Framework_TestCase
    {
        public function testFailure()
        {
            $this->assertJsonFileEqualsJsonFile(
              'chemin/vers/fixture/fichier', 'chemin/vers/constate/fichier');
        }
    }
    ?>

.. code-block:: bash

    $ phpunit JsonFileEqualsJsonFile
    PHPUnit 6.4.0 by Sebastian Bergmann and contributors.

    F

    Time: 0 seconds, Memory: 5.00Mb
    There was 1 failure:
    1) JsonFileEqualsJsonFile::testFailure
    Failed asserting that '{"Mascot":"Tux"}' matches JSON string "["Mascott", "Tux", "OS", "Linux"]".

    /lapistano/JsonFileEqualsJsonFile.php:5

    FAILURES!
    Tests: 1, Assertions: 3, Failures: 1.

.. _writing-tests-for-phpunit.assertions.assertJsonStringEqualsJsonFile:

assertJsonStringEqualsJsonFile()
================================

``assertJsonStringEqualsJsonFile(mixed $fichierAttendu, mixed $jsonConstate[, string $message = ''])``

Rapporte une erreur identifiée par ``$message`` si la valeur de ``$jsonConstate`` correspond à la valeur de
``$fichierAttendu``.

.. code-block:: php
    :caption: Utilisation de assertJsonStringEqualsJsonFile()
    :name: writing-tests-for-phpunit.assertions.assertJsonStringEqualsJsonFile.example

    <?php
    class JsonStringEqualsJsonFile extends PHPUnit_Framework_TestCase
    {
        public function testFailure()
        {
            $this->assertJsonStringEqualsJsonFile(
              'chemin/vers/fixture/fichier', json_encode(array("Mascot" => "ux"))
            );
        }
    }
    ?>

.. code-block:: bash

    $ phpunit JsonStringEqualsJsonFile
    PHPUnit 6.4.0 by Sebastian Bergmann and contributors.

    F

    Time: 0 seconds, Memory: 5.00Mb

    There was 1 failure:

    1) JsonStringEqualsJsonFile::testFailure
    Failed asserting that '{"Mascot":"ux"}' matches JSON string "{"Mascott":"Tux"}".

    /lapistano/JsonStringEqualsJsonFile.php:5

    FAILURES!
    Tests: 1, Assertions: 3, Failures: 1.

.. _writing-tests-for-phpunit.assertions.assertJsonStringEqualsJsonString:

assertJsonStringEqualsJsonString()
==================================

``assertJsonStringEqualsJsonString(mixed $jsonAttendu, mixed $jsonConstate[, string $message = ''])``

Rapporte une erreur identifiée par ``$message`` si la valeur de ``$jsonConstate`` correspond à la valeur de
``$jsonAttendu``.

.. code-block:: php
    :caption: Utilisation de assertJsonStringEqualsJsonString()
    :name: writing-tests-for-phpunit.assertions.assertJsonStringEqualsJsonString.example

    <?php
    class JsonStringEqualsJsonString extends PHPUnit_Framework_TestCase
    {
        public function testFailure()
        {
            $this->assertJsonStringEqualsJsonString(
              json_encode(array("Mascot" => "Tux")), json_encode(array("Mascott" => "ux"))
            );
        }
    }
    ?>

.. code-block:: bash

    $ phpunit JsonStringEqualsJsonString
    PHPUnit 6.4.0 by Sebastian Bergmann and contributors.

    F

    Time: 0 seconds, Memory: 5.00Mb

    There was 1 failure:

    1) JsonStringEqualsJsonString::testFailure
    Failed asserting that two objects are equal.
    --- Expected
    +++ Actual
    @@ @@
     stdClass Object (
     -    'Mascot' => 'Tux'
     +    'Mascot' => 'ux'
    )

    /lapistano/JsonStringEqualsJsonString.php:5

    FAILURES!
    Tests: 1, Assertions: 3, Failures: 1.

.. _writing-tests-for-phpunit.assertions.assertLessThan:

assertLessThan()
================

``assertLessThan(mixed $attendu, mixed $constate[, string $message = ''])``

Rapporte une erreur identifiée par le ``$message`` si la valeur de ``$constate`` n'est pas inférieure à la valeur de ``$attendu``.

``assertAttributeLessThan()`` est un enrobeur de commodité qui utilise un attribut ``public``, ``protected`` ou ``private`` d'une classe ou d'un objet comme valeur constatée.

.. code-block:: php
    :caption: Utilisation de assertLessThan()
    :name: writing-tests-for-phpunit.assertions.assertLessThan.example

    <?php
    class LessThanTest extends PHPUnit_Framework_TestCase
    {
        public function testEchec()
        {
            $this->assertLessThan(1, 2);
        }
    }
    ?>

.. code-block:: bash

    $ phpunit LessThanTest
    PHPUnit 6.4.0 by Sebastian Bergmann and contributors.

    F

    Time: 0 seconds, Memory: 5.00Mb

    There was 1 failure:

    1) LessThanTest::testEchec
    Failed asserting that 2 is less than 1.

    /home/sb/LessThanTest.php:6

    FAILURES!
    Tests: 1, Assertions: 1, Failures: 1.

.. _writing-tests-for-phpunit.assertions.assertLessThanOrEqual:

assertLessThanOrEqual()
=======================

``assertLessThanOrEqual(mixed $attendu, mixed $constate[, string $message = ''])``

Rapporte une erreur identifiée par le ``$message`` si la valeur de ``$constate`` n'est pas inférieure ou égale à la valeur de ``$attendu``.

``assertAttributeLessThanOrEqual()`` est un enrobeur de commodité qui utilise un attribut ``public``, ``protected`` ou ``private`` d'une classe ou d'un objet comme valeur attendue.

.. code-block:: php
    :caption: Utilisation de assertLessThanOrEqual()
    :name: writing-tests-for-phpunit.assertions.assertLessThanOrEqual.example

    <?php
    class LessThanOrEqualTest extends PHPUnit_Framework_TestCase
    {
        public function testEchec()
        {
            $this->assertLessThanOrEqual(1, 2);
        }
    }
    ?>

.. code-block:: bash

    $ phpunit LessThanOrEqualTest
    PHPUnit 6.4.0 by Sebastian Bergmann and contributors.

    F

    Time: 0 seconds, Memory: 5.25Mb

    There was 1 failure:

    1) LessThanOrEqualTest::testEchec
    Failed asserting that 2 is equal to 1 or is less than 1.

    /home/sb/LessThanOrEqualTest.php:6

    FAILURES!
    Tests: 1, Assertions: 2, Failures: 1.

.. _writing-tests-for-phpunit.assertions.assertNull:

assertNull()
============

``assertNull(mixed $variable[, string $message = ''])``

Rapporte une erreur identifiée par le ``$message`` si ``$variable`` n'est pas ``NULL``.

``assertNotNull()`` est l'inverse de cette assertion et prend les mêmes arguments.

.. code-block:: php
    :caption: Utilisation de assertNull()
    :name: writing-tests-for-phpunit.assertions.assertNull.example

    <?php
    class NullTest extends PHPUnit_Framework_TestCase
    {
        public function testEchec()
        {
            $this->assertNull('foo');
        }
    }
    ?>

.. code-block:: bash

    $ phpunit NotNullTest
    PHPUnit 6.4.0 by Sebastian Bergmann and contributors.

    F

    Time: 0 seconds, Memory: 5.00Mb

    There was 1 failure:

    1) NullTest::testEchec
    Failed asserting that 'foo' is null.

    /home/sb/NotNullTest.php:6

    FAILURES!
    Tests: 1, Assertions: 1, Failures: 1.

.. _writing-tests-for-phpunit.assertions.assertObjectHasAttribute:

assertObjectHasAttribute()
==========================

``assertObjectHasAttribute(string $nomAttribut, object $objet[, string $message = ''])``

Rapporte une erreur identifiée par le ``$message`` si ``$objet->nomAttribut`` n'existe pas.

``assertObjectNotHasAttribute()`` est l'inverse de cette assertion et prend les mêmes arguments.

.. code-block:: php
    :caption: Utilisation de assertObjectHasAttribute()
    :name: writing-tests-for-phpunit.assertions.assertObjectHasAttribute.example

    <?php
    class ObjectHasAttributeTest extends PHPUnit_Framework_TestCase
    {
        public function testEchec()
        {
            $this->assertObjectHasAttribute('foo', new stdClass);
        }
    }
    ?>

.. code-block:: bash

    $ phpunit ObjectHasAttributeTest
    PHPUnit 6.4.0 by Sebastian Bergmann and contributors.

    F

    Time: 0 seconds, Memory: 4.75Mb

    There was 1 failure:

    1) ObjectHasAttributeTest::testEchec
    Failed asserting that object of class "stdClass" has attribute "foo".

    /home/sb/ObjectHasAttributeTest.php:6

    FAILURES!
    Tests: 1, Assertions: 1, Failures: 1.

.. _writing-tests-for-phpunit.assertions.assertRegExp:

assertRegExp()
==============

``assertRegExp(string $motif, string $chaine[, string $message = ''])``

Rapporte une erreur identifiée par le ``$message`` si ``$chaine`` ne correspond pas à l'expression rationnelle ``$motif``.

``assertNotRegExp()`` est l'inverse de cette assertion et prend les mêmes arguments.

.. code-block:: php
    :caption: Utilisation de assertRegExp()
    :name: writing-tests-for-phpunit.assertions.assertRegExp.example

    <?php
    class RegExpTest extends PHPUnit_Framework_TestCase
    {
        public function testEchec()
        {
            $this->assertRegExp('/foo/', 'bar');
        }
    }
    ?>

.. code-block:: bash

    $ phpunit RegExpTest
    PHPUnit 6.4.0 by Sebastian Bergmann and contributors.

    F

    Time: 0 seconds, Memory: 5.00Mb

    There was 1 failure:

    1) RegExpTest::testEchec
    Failed asserting that 'bar' matches PCRE pattern "/foo/".

    /home/sb/RegExpTest.php:6

    FAILURES!
    Tests: 1, Assertions: 1, Failures: 1.

.. _writing-tests-for-phpunit.assertions.assertStringMatchesFormat:

assertStringMatchesFormat()
===========================

``assertStringMatchesFormat(string $format, string $chaine[, string $message = ''])``

Rapporte une erreur identifiée par le ``$message`` si la chaîne ``$chaine`` ne correspond pas à la chaîne de ``$format``.

``assertStringNotMatchesFormat()`` est l'inverse de cette assertion et prend les mêmes arguments.

.. code-block:: php
    :caption: Utilisation de assertStringMatchesFormat()
    :name: writing-tests-for-phpunit.assertions.assertStringMatchesFormat.example

    <?php
    class StringMatchesFormatTest extends PHPUnit_Framework_TestCase
    {
        public function testEchec()
        {
            $this->assertStringMatchesFormat('%i', 'foo');
        }
    }
    ?>

.. code-block:: bash

    $ phpunit StringMatchesFormatTest
    PHPUnit 6.4.0 by Sebastian Bergmann and contributors.

    F

    Time: 0 seconds, Memory: 5.00Mb

    There was 1 failure:

    1) StringMatchesFormatTest::testEchec
    Failed asserting that 'foo' matches PCRE pattern "/^[+-]?\d+$/s".

    /home/sb/StringMatchesFormatTest.php:6

    FAILURES!
    Tests: 1, Assertions: 1, Failures: 1.

La chaîne de format peut contenir les conteneurs suivants:

-

  ``%e``: Représente un séparateur de répertoire, par exemple ``/`` sur Linux.

-

  ``%s``: Un ou plusieurs caractères quelconque (y compris des espaces) à l'exception du caractère fin de ligne.

-

  ``%S``: Zéro ou plusieurs caractères quelconque (y compris des espaces) à l'exception du caractère fin de ligne.

-

  ``%a``: Un ou plusieurs caractères quelconque (y compris des espaces) y compris les caractères fin de ligne.

-

  ``%A``: Zéro ou plusieurs caractères quelconque (y compris des espaces) y compris les caractères fin de ligne.

-

  ``%w``: Zéro ou plusieurs espaces.

-

  ``%i``: Une valeur entière signée, par exemple ``+3142``, ``-3142``.

-

  ``%d``: Une valeur entière non signée, par exemple ``123456``.

-

  ``%x``: Un ou plusieurs caractères hexadécimaux. C'est-à-dire des caractères dans la plage ``0-9``, ``a-f``, ``A-F``.

-

  ``%f``: Un nombre en virgule flottante, par exemple: ``3.142``, ``-3.142``, ``3.142E-10``, ``3.142e+10``.

-

  ``%c``: Un unique caractère de n'importe quelle sorte.

.. _writing-tests-for-phpunit.assertions.assertStringMatchesFormatFile:

assertStringMatchesFormatFile()
===============================

``assertStringMatchesFormatFile(string $fichierFormat, string $chaine[, string $message = ''])``

Rapporte une erreur identifiée par le ``$message`` si la chaîne ``$chaine`` ne correspond pas au contenu de ``$fichierFormat``.

``assertStringNotMatchesFormatFile()`` est l'inverse de cette assertion et prend les mêmes arguments.

.. code-block:: php
    :caption: Utilisation de assertStringMatchesFormatFile()
    :name: writing-tests-for-phpunit.assertions.assertStringMatchesFormatFile.example

    <?php
    class StringMatchesFormatFileTest extends PHPUnit_Framework_TestCase
    {
        public function testEchec()
        {
            $this->assertStringMatchesFormatFile('/chemin/vers/attendu.txt', 'foo');
        }
    }
    ?>

.. code-block:: bash

    $ phpunit StringMatchesFormatFileTest
    PHPUnit 6.4.0 by Sebastian Bergmann and contributors.

    F

    Time: 0 seconds, Memory: 5.00Mb

    There was 1 failure:

    1) StringMatchesFormatFileTest::testEchec
    Failed asserting that 'foo' matches PCRE pattern "/^[+-]?\d+
    $/s".

    /home/sb/StringMatchesFormatFileTest.php:6

    FAILURES!
    Tests: 1, Assertions: 2, Failures: 1.

.. _writing-tests-for-phpunit.assertions.assertSame:

assertSame()
============

``assertSame(mixed $attendu, mixed $constate[, string $message = ''])``

Rapporte une erreur identifiée par le ``$message`` si les deux variables ``$attendu`` et ``$constate`` n'ont pas le même type et la même valeur.

``assertNotSame()`` est l'inverse de cette assertion et prend les mêmes arguments.

``assertAttributeSame()`` et ``assertAttributeNotSame()`` sont des enrobeurs de commodité qui utilisent un attribut ``public``, ``protected`` ou ``private`` d'une classe ou d'un objet comme valeur constatée.

.. code-block:: php
    :caption: Utilisation de assertSame()
    :name: writing-tests-for-phpunit.assertions.assertSame.example

    <?php
    class SameTest extends PHPUnit_Framework_TestCase
    {
        public function testEchec()
        {
            $this->assertSame('2204', 2204);
        }
    }
    ?>

.. code-block:: bash

    $ phpunit SameTest
    PHPUnit 6.4.0 by Sebastian Bergmann and contributors.

    F

    Time: 0 seconds, Memory: 5.00Mb

    There was 1 failure:

    1) SameTest::testEchec
    Failed asserting that 2204 is identical to '2204'.

    /home/sb/SameTest.php:6

    FAILURES!
    Tests: 1, Assertions: 1, Failures: 1.

``assertSame(object $attendu, object $constate[, string $message = ''])``

Rapporte une erreur identifiée par le ``$message`` si les deux variables ``$attendu`` et ``$constate`` ne référence pas le même objet.

.. code-block:: php
    :caption: Utilisation de assertSame() avec des objets
    :name: writing-tests-for-phpunit.assertions.assertSame.example2

    <?php
    class SameTest extends PHPUnit_Framework_TestCase
    {
        public function testEchec()
        {
            $this->assertSame(new stdClass, new stdClass);
        }
    }
    ?>

.. code-block:: bash

    $ phpunit SameTest
    PHPUnit 6.4.0 by Sebastian Bergmann and contributors.

    F

    Time: 0 seconds, Memory: 4.75Mb

    There was 1 failure:

    1) SameTest::testEchec
    Failed asserting that two variables reference the same object.

    /home/sb/SameTest.php:6

    FAILURES!
    Tests: 1, Assertions: 1, Failures: 1.

.. _writing-tests-for-phpunit.assertions.assertSelectCount:

assertSelectCount()
===================

``assertSelectCount(array $selecteur, integer $nombre, mixed $constate[, string $message = '', boolean $isHtml = TRUE])``

Rapporte une erreur identifiée par le ``$message`` si le sélecteur CSS ``$selecteur`` ne correspond pas à ``$nombre`` éléments du noeud DOM ``$constate``.

``$nombre`` peut avoir l'un des types suivants :

- ``booléen``: présuppose la présence d'éléments correspondant au sélecteur (``TRUE``) ou l'absence d'éléments (``FALSE``).

- ``nombre entier``: présuppose le nombre d'éléments.

- ``tableau``: présuppose que le nombre sera dans la plage indiquée en utilisant ``<``, ``>``, ``<=`` et ``>=`` comme clefs.

.. code-block:: php
    :caption: Utilisation de assertSelectCount()
    :name: writing-tests-for-phpunit.assertions.assertSelectCount.example

    <?php
    class SelectCountTest extends PHPUnit_Framework_TestCase
    {
        protected function setUp()
        {
            $this->xml = new DomDocument;
            $this->xml->loadXML('<foo><bar/><bar/><bar/></foo>');
        }

        public function testAbsenceEchec()
        {
            $this->assertSelectCount('foo bar', FALSE, $this->xml);
        }

        public function testPresenceEchec()
        {
            $this->assertSelectCount('foo baz', TRUE, $this->xml);
        }

        public function testCompteExactEchec()
        {
            $this->assertSelectCount('foo bar', 5, $this->xml);
        }

        public function testPlageEchec()
        {
            $this->assertSelectCount('foo bar', array('>'=>6, '<'=>8), $this->xml);
        }
    }
    ?>

.. code-block:: bash

    $ phpunit SelectCountTest
    PHPUnit 6.4.0 by Sebastian Bergmann and contributors.

    FFFF

    Time: 0 seconds, Memory: 5.50Mb

    There were 4 failures:

    1) SelectCountTest::testAbsenceEchec
    Failed asserting that true is false.

    /home/sb/SelectCountTest.php:12

    2) SelectCountTest::testPresenceEchec
    Failed asserting that false is true.

    /home/sb/SelectCountTest.php:17

    3) SelectCountTest::testCompteExactEchec
    Failed asserting that 3 matches expected 5.

    /home/sb/SelectCountTest.php:22

    4) SelectCountTest::testPlageEchec
    Failed asserting that false is true.

    /home/sb/SelectCountTest.php:27

    FAILURES!
    Tests: 4, Assertions: 4, Failures: 4.

.. _writing-tests-for-phpunit.assertions.assertSelectEquals:

assertSelectEquals()
====================

``assertSelectEquals(array $selecteur, string $contenu, integer $nombre, mixed $constate[, string $message = '', boolean $isHtml = TRUE])``

Rapporte une erreur identifiée par le ``$message`` si le sélecteur CSS ``$selecteur`` ne correspond pas à ``$nombre`` éléments dans le noeud DOM ``$constate`` possédant la valeur ``$contenu``.

``$nombre`` peut avoir l'un des types suivants :

- ``booléen``: présuppose la présence correspondant au sélecteur (``TRUE``) ou l'absence d'éléments (``FALSE``).

- ``nombre entier``: présuppose le nombre d'éléments.

- ``tableau``: présuppose que le nombre est dans une plage indiquée en utilisant ``<``, ``>``, ``<=`` et ``>=`` comme clefs.

.. code-block:: php
    :caption: Utilisation de assertSelectEquals()
    :name: writing-tests-for-phpunit.assertions.assertSelectEquals.example

    <?php
    class SelectEqualsTest extends PHPUnit_Framework_TestCase
    {
        protected function setUp()
        {
            $this->xml = new DomDocument;
            $this->xml->loadXML('<foo><bar>Baz</bar><bar>Baz</bar></foo>');
        }

        public function testAbsenceEchec()
        {
            $this->assertSelectEquals('foo bar', 'Baz', FALSE, $this->xml);
        }

        public function testPresenceEchec()
        {
            $this->assertSelectEquals('foo bar', 'Bat', TRUE, $this->xml);
        }

        public function testCompteExactEchec()
        {
            $this->assertSelectEquals('foo bar', 'Baz', 5, $this->xml);
        }

        public function testPlageEchec()
        {
            $this->assertSelectEquals('foo bar', 'Baz', array('>'=>6, '<'=>8), $this->xml);
        }
    }
    ?>

.. code-block:: bash

    $ phpunit SelectEqualsTest
    PHPUnit 6.4.0 by Sebastian Bergmann and contributors.

    FFFF

    Time: 0 seconds, Memory: 5.50Mb

    There were 4 failures:

    1) SelectEqualsTest::testAbsenceEchec
    Failed asserting that true is false.

    /home/sb/SelectEqualsTest.php:12

    2) SelectEqualsTest::testPresenceEchec
    Failed asserting that false is true.

    /home/sb/SelectEqualsTest.php:17

    3) SelectEqualsTest::testCompteExactEchec
    Failed asserting that 2 matches expected 5.

    /home/sb/SelectEqualsTest.php:22

    4) SelectEqualsTest::testPlageEchec
    Failed asserting that false is true.

    /home/sb/SelectEqualsTest.php:27

    FAILURES!
    Tests: 4, Assertions: 4, Failures: 4.

.. _writing-tests-for-phpunit.assertions.assertSelectRegExp:

assertSelectRegExp()
====================

``assertSelectRegExp(array $selecteur, string $motif, integer $nombre, mixed $constate[, string $message = '', boolean $isHtml = TRUE])``

Rapporte une erreur identifiée par le ``$message`` si le sélecteur CSS ``$selecteur`` ne correspond pas à ``$nombre`` éléments dans le noeud DOM ``$constate`` possédant une valeur qui correspond au ``$motif``.

``$nombre`` peut avoir l'un des types suivants :

- ``booléen``: présuppose la présence d'éléments correspondant au sélecteur (``TRUE``) ou l'absence d'éléments (``FALSE``).

- ``nombre entier``: présuppose le nombre d'éléments.

- ``tableau``: présuppose que le nombre est dans une plage indiquée en utilisant ``<``, ``>``, ``<=`` et ``>=`` comme clefs.

.. code-block:: php
    :caption: Utilisation de assertSelectRegExp()
    :name: writing-tests-for-phpunit.assertions.assertSelectRegExp.example

    <?php
    class SelectRegExpTest extends PHPUnit_Framework_TestCase
    {
        protected function setUp()
        {
            $this->xml = new DomDocument;
            $this->xml->loadXML('<foo><bar>Baz</bar><bar>Baz</bar></foo>');
        }

        public function testAbsenceEchec()
        {
            $this->assertSelectRegExp('foo bar', '/Ba.*/', FALSE, $this->xml);
        }

        public function testPresenceEchec()
        {
            $this->assertSelectRegExp('foo bar', '/B[oe]z]/', TRUE, $this->xml);
        }

        public function testCompteExactEchec()
        {
            $this->assertSelectRegExp('foo bar', '/Ba.*/', 5, $this->xml);
        }

        public function testPlageEchec()
        {
            $this->assertSelectRegExp('foo bar', '/Ba.*/', array('>'=>6, '<'=>8), $this->xml);
        }
    }
    ?>

.. code-block:: bash

    $ phpunit SelectRegExpTest
    PHPUnit 6.4.0 by Sebastian Bergmann and contributors.

    FFFF

    Time: 0 seconds, Memory: 5.50Mb

    There were 4 failures:

    1) SelectRegExpTest::testAbsenceEchec
    Failed asserting that true is false.

    /home/sb/SelectRegExpTest.php:12

    2) SelectRegExpTest::testPresenceEchec
    Failed asserting that false is true.

    /home/sb/SelectRegExpTest.php:17

    3) SelectRegExpTest::testCompteExactEchec
    Failed asserting that 2 matches expected 5.

    /home/sb/SelectRegExpTest.php:22

    4) SelectRegExpTest::testPlageEchec
    Failed asserting that false is true.

    /home/sb/SelectRegExpTest.php:27

    FAILURES!
    Tests: 4, Assertions: 4, Failures: 4.

.. _writing-tests-for-phpunit.assertions.assertStringEndsWith:

assertStringEndsWith()
======================

``assertStringEndsWith(string $suffixe, string $chaine[, string $message = ''])``

Rapporte une erreur identifiée par le ``$message`` si la ``$chaine`` ne se termine pas par ``$suffixe``.

``assertStringEndsNotWith()`` est l'inverse de cette assertion et prend les mêmes arguments.

.. code-block:: php
    :caption: Utilisation de assertStringEndsWith()
    :name: writing-tests-for-phpunit.assertions.assertStringEndsWith.example

    <?php
    class StringEndsWithTest extends PHPUnit_Framework_TestCase
    {
        public function testEchec()
        {
            $this->assertStringEndsWith('suffixe', 'foo');
        }
    }
    ?>

.. code-block:: bash

    $ phpunit StringEndsWithTest
    PHPUnit 6.4.0 by Sebastian Bergmann and contributors.

    F

    Time: 1 second, Memory: 5.00Mb

    There was 1 failure:

    1) StringEndsWithTest::testEchec
    Failed asserting that 'foo' ends with "suffixe".

    /home/sb/StringEndsWithTest.php:6

    FAILURES!
    Tests: 1, Assertions: 1, Failures: 1.

.. _writing-tests-for-phpunit.assertions.assertStringEqualsFile:

assertStringEqualsFile()
========================

``assertStringEqualsFile(string $fichierAttendu, string $chaineConstatee[, string $message = ''])``

Rapporte une erreur identifiée par le ``$message`` si le fichier indiqué par ``$fichierAttendu`` ne possède pas ``$chaineConstatee`` comme contenu.

``assertStringNotEqualsFile()`` est l'inverse de cette assertion et prend les mêmes arguments.

.. code-block:: php
    :caption: Utilisation de assertStringEqualsFile()
    :name: writing-tests-for-phpunit.assertions.assertStringEqualsFile.example

    <?php
    class StringEqualsFileTest extends PHPUnit_Framework_TestCase
    {
        public function testEchec()
        {
            $this->assertStringEqualsFile('/home/sb/attendu', 'constate');
        }
    }
    ?>

.. code-block:: bash

    $ phpunit StringEqualsFileTest
    PHPUnit 6.4.0 by Sebastian Bergmann and contributors.

    F

    Time: 0 seconds, Memory: 5.25Mb

    There was 1 failure:

    1) StringEqualsFileTest::testEchec
    Failed asserting that two strings are equal.
    --- Expected
    +++ Actual
    @@ @@
    -'attendu
    -'
    +'constate'

    /home/sb/StringEqualsFileTest.php:6

    FAILURES!
    Tests: 1, Assertions: 2, Failures: 1.

.. _writing-tests-for-phpunit.assertions.assertStringStartsWith:

assertStringStartsWith()
========================

``assertStringStartsWith(string $prefixe, string $chaine[, string $message = ''])``

Rapporte une erreur identifiée par le ``$message`` si la chaîne ``$chaine`` ne commence pas par ``$prefixe``.

``assertStringStartsNotWith()`` est l'inverse de cette assertion et prend les mêmes arguments.

.. code-block:: php
    :caption: Utilisation de assertStringStartsWith()
    :name: writing-tests-for-phpunit.assertions.assertStringStartsWith.example

    <?php
    class StringStartsWithTest extends PHPUnit_Framework_TestCase
    {
        public function testEchec()
        {
            $this->assertStringStartsWith('prefixe', 'foo');
        }
    }
    ?>

.. code-block:: bash

    $ phpunit StringStartsWithTest
    PHPUnit 6.4.0 by Sebastian Bergmann and contributors.

    F

    Time: 0 seconds, Memory: 5.00Mb

    There was 1 failure:

    1) StringStartsWithTest::testEchec
    Failed asserting that 'foo' starts with "prefixe".

    /home/sb/StringStartsWithTest.php:6

    FAILURES!
    Tests: 1, Assertions: 1, Failures: 1.

.. _writing-tests-for-phpunit.assertions.assertTag:

assertTag()
===========

``assertTag(array $matcheur, string $constate[, string $message = '', boolean $isHtml = TRUE])``

Rapporte une erreur identifiée par le ``$message`` si ``$constate`` n'établit pas de correspondance avec le ``$matcheur``.

``$matcheur`` est un tableau associatif qui indique les critères de correspondance pour l'assertion:

- ``id``: le noeud ayant l'attribut donné ``id`` doit correspondre à la valeur indiquée.

- ``tags``: le type du noeud doit correspondre à la valeur correspondante.

- ``attributes``: Les attributs du noeud doivent correspondre aux valeurs correspondantes dans le tableau associatif ``attributes``.

- ``content``: le contenu du texte doit correspondre à la valeur donnée.

- ``parent``: le père du noeud doit correspondre au tableau associatif ``parent``.

- ``child``: au moins un des fils directs du noeud doit satisfaire aux critères décrits dans le tableau associatif ``child``.

- ``ancestor``: au moins l'un des ancêtres du noeud doit satisfaire aux critères décrits par le tableau associatif ``ancestor``.

- ``descendant``: au moins l'un des descendants du noeud doit satisfaire les critères décrits dans le tableau associatif ``descendant``.

- ``children``: tableau associatif pour compter les enfants d'un noeud.

  - ``count``: le nombre d'enfants correspondants doit être égal à ce nombre.

  - ``less_than``: le nombre d'enfants correspondants doit être inférieur à ce nombre.

  - ``greater_than``: le nombre d'enfants correspondants doit être supérieur à ce nombre.

  - ``only``: un autre tableau associatif constitué de clefs à utiliser pour faire des correspondances avec les enfants, et seuls les enfants correspondants seront comptabilisés.

``assertNotTag()`` est l'inverse de cette assertion et prend les mêmes arguments.

.. code-block:: php
    :caption: Utilisation de assertTag()
    :name: writing-tests-for-phpunit.assertions.assertTag.example

    <?php
    // Matcher qui présuppose qu'il existe un élément avec un id="mon_id".
    $matcher = array('id' => 'mon_id');

    // Matcher qui présuppose qu'il existe un tag "span".
    $matcher = array('tag' => 'span');

    // Matcher qui présuppose qu'il existe un tag "span" contenant
    // "Hello World".
    $matcher = array('tag' => 'span', 'content' => 'Hello World');

    // Matcher qui présuppose qu'il existe un tag "span" dont le contenu correspond au
    // motif d'expression rationnelle
    $matcher = array('tag' => 'span', 'content' => '/Essayez P(HP|erl)/');

    // Matcher qui présuppose qu'il existe un "span"avec un attribut class class.
    $matcher = array(
      'tag'        => 'span',
      'attributes' => array('class' => 'list')
    );

    // Matcher qui présuppose qu'il existe un "span" à l'intérieur d'un "div".
    $matcher = array(
      'tag'    => 'span',
      'parent' => array('tag' => 'div')
    );

    // Matcher qui présuppose qu'il existe un "span" quelque part dans une "table".
    $matcher = array(
      'tag'      => 'span',
      'ancestor' => array('tag' => 'table')
    );

    // Matcher qui présuppose qu'il existe un "span" avec au moins un fils "em".
    $matcher = array(
      'tag'   => 'span',
      'child' => array('tag' => 'em')
    );

    // Matcher qui présuppose qu'il existe un "span" contenant un tag "strong"
    // (éventuellement imbriqué)
    $matcher = array(
      'tag'        => 'span',
      'descendant' => array('tag' => 'strong')
    );

    // Matcher qui présuppose qu'il existe un "span" contenant de 5 à 10 tags "em" comme
    // fils directs
    $matcher = array(
      'tag'      => 'span',
      'children' => array(
        'less_than'    => 11,
        'greater_than' => 4,
        'only'         => array('tag' => 'em')
      )
    );

    // Matcher qui présuppose qu'il existe un "div", avec un ancêtre "ul" et un "li"
    // parent (avec class="enum"), et contenant un descendant "span" qui contient
    // un élément avec id="mon_test" et le texte "Hello World".
    $matcher = array(
      'tag'        => 'div',
      'ancestor'   => array('tag' => 'ul'),
      'parent'     => array(
        'tag'        => 'li',
        'attributes' => array('class' => 'enum')
      ),
      'descendant' => array(
        'tag'   => 'span',
        'child' => array(
          'id'      => 'mon_test',
          'content' => 'Hello World'
        )
      )
    );

    // Utilise assertTag() pour appliquer un $matcher à un morceau de $html.
    $this->assertTag($matcher, $html);

    // Utilise assertTag() pour appliquer un matcher à un morceau de $xml.
    $this->assertTag($matcher, $xml, '', FALSE);
    ?>

.. _writing-tests-for-phpunit.assertions.assertThat:

assertThat()
============

Des assertions plus complexes peuvent être formulées en utilisant les classes
``PHPUnit_Framework_Constraint``. Elles peuvent être évaluées
en utilisant la méthode ``assertThat()``.
:numref:`writing-tests-for-phpunit.assertions.assertThat.example` montre comment
les contraintes ``logicalNot()`` et ``equalTo()``
peuvent être utilisées pour exprimer la même assertion que
``assertNotEquals()``.

``assertThat(mixed $valeur, PHPUnit_Framework_Constraint $contrainte[, $message = ''])``

Rapporte une erreur identifiée par le ``$message`` si la valeur ``$valeur`` ne correspond
pas à la ``$contrainte``.

.. code-block:: php
    :caption: Utilisation de assertThat()
    :name: writing-tests-for-phpunit.assertions.assertThat.example

    <?php
    class BiscuitTest extends PHPUnit_Framework_TestCase
    {
        public function testEquals()
        {
            $leBiscuit = new Biscuit('Ginger');
            $monBiscuit  = new Biscuit('Ginger');

            $this->assertThat(
              $leBiscuit,
              $this->logicalNot(
                $this->equalTo($monBiscuit)
              )
            );
        }
    }
    ?>

:numref:`writing-tests-for-phpunit.assertions.assertThat.tables.constraints` montre les
classes ``PHPUnit_Framework_Constraint`` disponibles.

.. rst-class:: table
.. list-table:: Contraintes
    :name: writing-tests-for-phpunit.assertions.assertThat.tables.constraints
    :header-rows: 1

    * - Contrainte
      - Signification
    * - ``PHPUnit_Framework_Constraint_Attribute attribute(PHPUnit_Framework_Constraint $contrainte, $nomAttribut)``
      - Contrainte qui applique une autre contrainte à l'attribut d'une classe ou d'un objet.
    * - ``PHPUnit_Framework_Constraint_IsAnything anything()``
      - Contrainte qui accepte n'importe quelle valeur en entrée.
    * - ``PHPUnit_Framework_Constraint_ArrayHasKey arrayHasKey(mixed $clef)``
      - Contrainte qui présuppose que le tableau pour lequel elle est évaluée possède une clef donnée..
    * - ``PHPUnit_Framework_Constraint_TraversableContains contains(mixed $valeur)``
      - Contrainte qui présuppose que le ``tableau`` ou l'objet qui implémente l'interface ``Iterator`` pour lequel elle est évaluée contient une valeur donnée..
    * - ``PHPUnit_Framework_Constraint_IsEqual equalTo($valeur, $delta = 0, $profondeurMax = 10)``
      - Contrainte qui vérifie si une valeur est égale à une autre.
    * - ``PHPUnit_Framework_Constraint_Attribute attributeEqualTo($nomAttribut, $valeur, $delta = 0, $profondeurMax = 10)``
      - Contrainte qui vérifie si une valeur est égale à l'attribut d'une classe ou d'un objet.
    * - ``PHPUnit_Framework_Constraint_FileExists fileExists()``
      - Contrainte qui vérifie si le (nom de) fichier pour lequel elle est évaluée existe.
    * - ``PHPUnit_Framework_Constraint_GreaterThan greaterThan(mixed $valeur)``
      - Contrainte qui présuppose que la valeur pour laquelle elle est évaluée est supérieure à une valeur donnée.
    * - ``PHPUnit_Framework_Constraint_Or greaterThanOrEqual(mixed $valeur)``
      - Contrainte qui présuppose que la valeur pour laquelle elle est évaluée et supérieure ou égale à une valeur donnée.
    * - ``PHPUnit_Framework_Constraint_ClassHasAttribute classHasAttribute(string $nomAttribut)``
      - Contrainte qui présuppose que la classe pour laquelle elle est évaluée possède un attribut donné.
    * - ``PHPUnit_Framework_Constraint_ClassHasStaticAttribute classHasStaticAttribute(string $nomAttribut)``
      - Contrainte qui présuppose que la classe pour laquelle elle est évaluée possède un attribut statique donné.
    * - ``PHPUnit_Framework_Constraint_ObjectHasAttribute hasAttribute(string $nomAttribut)``
      - Contrainte qui présuppose que l'objet pour lequel elle est évaluée possède un attribut donné.
    * - ``PHPUnit_Framework_Constraint_IsIdentical identicalTo(mixed $valeur)``
      - Contrainte qui présuppose qu'une valeur est identique à une autre.
    * - ``PHPUnit_Framework_Constraint_IsFalse isFalse()``
      - Contrainte qui présuppose que la valeur pour laquelle elle est évaluée est ``FALSE``.
    * - ``PHPUnit_Framework_Constraint_IsInstanceOf isInstanceOf(string $nomClasse)``
      - Contrainte qui présuppose que l'objet pour lequel elle est évaluée est une instance d'une classe donnée.
    * - ``PHPUnit_Framework_Constraint_IsNull isNull()``
      - Contrainte qui présuppose que la valeur pour laquelle elle est évaluée est ``NULL``.
    * - ``PHPUnit_Framework_Constraint_IsTrue isTrue()``
      - Contrainte qui présuppose que la valeur pour laquelle elle est évaluée est ``TRUE``.
    * - ``PHPUnit_Framework_Constraint_IsType isType(string $type)``
      - Contrainte qui présuppose que la valeur pour laquelle elle est évaluée est du type indiqué.
    * - ``PHPUnit_Framework_Constraint_LessThan lessThan(mixed $valeur)``
      - Contrainte qui présuppose que la valeur pour laquelle elle est évaluée est inférieure à la valeur donnée.
    * - ``PHPUnit_Framework_Constraint_Or lessThanOrEqual(mixed $valeur)``
      - Contrainte qui présuppose que la valeur pour laquelle elle est évaluée est inférieure ou égale à une valeur donnée.
    * - ``logicalAnd()``
      - ET logique (AND).
    * - ``logicalNot(PHPUnit_Framework_Constraint $contrainte)``
      - NON logique (NOT).
    * - ``logicalOr()``
      - OU logique (OU).
    * - ``logicalXor()``
      - OU exclusif logique (XOR).
    * - ``PHPUnit_Framework_Constraint_PCREMatch matchesRegularExpression(string $motif)``
      - Contrainte qui présuppose que la chaîne pour laquelle elle est évaluée correspond à une expression rationnelle.
    * - ``PHPUnit_Framework_Constraint_StringContains stringContains(string $chaine, bool $casse)``
      - Contrainte qui présuppose que la chaîne pour laquelle elle est évaluée contient une chaîne donnée.
    * - ``PHPUnit_Framework_Constraint_StringEndsWith stringEndsWith(string $suffixe)``
      - Contrainte qui présuppose que la chaîne pour laquelle elle est évaluée se termine avec un suffixe donné.
    * - ``PHPUnit_Framework_Constraint_StringStartsWith stringStartsWith(string $prefixe)``
      - Contrainte qui présuppose que la chaîne pour laquelle elle est évaluée commence par un préfixe donné.

.. _writing-tests-for-phpunit.assertions.assertTrue:

assertTrue()
============

``assertTrue(bool $condition[, string $message = ''])``

Rapporte une erreur identifiée par le ``$message`` si la ``$condition`` est ``FALSE``.

``assertNotTrue()`` est l'inverse de cette assertion et prend les mêmes arguments.

.. code-block:: php
    :caption: Utilisation de assertTrue()
    :name: writing-tests-for-phpunit.assertions.assertTrue.example

    <?php
    class TrueTest extends PHPUnit_Framework_TestCase
    {
        public function testEchec()
        {
            $this->assertTrue(FALSE);
        }
    }
    ?>

.. code-block:: bash

    $ phpunit TrueTest
    PHPUnit 6.4.0 by Sebastian Bergmann and contributors.

    F

    Time: 0 seconds, Memory: 5.00Mb

    There was 1 failure:

    1) TrueTest::testEchec
    Failed asserting that false is true.

    /home/sb/TrueTest.php:6

    FAILURES!
    Tests: 1, Assertions: 1, Failures: 1.

.. _writing-tests-for-phpunit.assertions.assertXmlFileEqualsXmlFile:

assertXmlFileEqualsXmlFile()
============================

``assertXmlFileEqualsXmlFile(string $fichierAttendu, string $fichierConstate[, string $message = ''])``

Rapporte une erreur identifiée par le ``$message`` si le document XML dans ``$fichierConstate`` n'est pas égal au document XML dans ``$fichierAttendu``.

``assertXmlFileNotEqualsXmlFile()`` est l'inverse de cette assertion et prend les mêmes arguments.

.. code-block:: php
    :caption: Utilisation de assertXmlFileEqualsXmlFile()
    :name: writing-tests-for-phpunit.assertions.assertXmlFileEqualsXmlFile.example

    <?php
    class XmlFileEqualsXmlFileTest extends PHPUnit_Framework_TestCase
    {
        public function testEchec()
        {
            $this->assertXmlFileEqualsXmlFile(
              '/home/sb/attendu.xml', '/home/sb/constate.xml');
        }
    }
    ?>

.. code-block:: bash

    $ phpunit XmlFileEqualsXmlFileTest
    PHPUnit 6.4.0 by Sebastian Bergmann and contributors.

    F

    Time: 0 seconds, Memory: 5.25Mb

    There was 1 failure:

    1) XmlFileEqualsXmlFileTest::testEchec
    Failed asserting that two DOM documents are equal.
    --- Expected
    +++ Actual
    @@ @@
     <?xml version="1.0"?>
     <foo>
    -  <bar/>
    +  <baz/>
     </foo>

    /home/sb/XmlFileEqualsXmlFileTest.php:7

    FAILURES!
    Tests: 1, Assertions: 3, Failures: 1.

.. _writing-tests-for-phpunit.assertions.assertXmlStringEqualsXmlFile:

assertXmlStringEqualsXmlFile()
==============================

``assertXmlStringEqualsXmlFile(string $fichierAttendu, string $xmlConstate[, string $message = ''])``

Rapporte une erreur identifiée par le ``$message`` si le document XML dans ``$xmlConstate`` n'est pas égal au document XML dans ``$fichierAttendu``.

``assertXmlStringNotEqualsXmlFile()`` est l'inverse de cette assertion et prend les mêmes arguments.

.. code-block:: php
    :caption: Utilisation de assertXmlStringEqualsXmlFile()
    :name: writing-tests-for-phpunit.assertions.assertXmlStringEqualsXmlFile.example

    <?php
    class XmlStringEqualsXmlFileTest extends PHPUnit_Framework_TestCase
    {
        public function testEchec()
        {
            $this->assertXmlStringEqualsXmlFile(
              '/home/sb/attendu.xml', '<foo><baz/></foo>');
        }
    }
    ?>

.. code-block:: bash

    $ phpunit XmlStringEqualsXmlFileTest
    PHPUnit 6.4.0 by Sebastian Bergmann and contributors.

    F

    Time: 0 seconds, Memory: 5.25Mb

    There was 1 failure:

    1) XmlStringEqualsXmlFileTest::testEchec
    Failed asserting that two DOM documents are equal.
    --- Expected
    +++ Actual
    @@ @@
     <?xml version="1.0"?>
     <foo>
    -  <bar/>
    +  <baz/>
     </foo>

    /home/sb/XmlStringEqualsXmlFileTest.php:7

    FAILURES!
    Tests: 1, Assertions: 2, Failures: 1.

.. _writing-tests-for-phpunit.assertions.assertXmlStringEqualsXmlString:

assertXmlStringEqualsXmlString()
================================

``assertXmlStringEqualsXmlString(string $xmlAttendu, string $xmlConstateXml[, string $message = ''])``

Rapporte une erreur identifiée par le ``$message`` si le document XML dans ``$xmlConstate`` n'est pas égal au document XML dans ``$xmlAttendu``.

``assertXmlStringNotEqualsXmlString()`` est l'inverse de cette assertion et prend les mêmes arguments.

.. code-block:: php
    :caption: Utilisation de assertXmlStringEqualsXmlString()
    :name: writing-tests-for-phpunit.assertions.assertXmlStringEqualsXmlString.example

    <?php
    class XmlStringEqualsXmlStringTest extends PHPUnit_Framework_TestCase
    {
        public function testEchec()
        {
            $this->assertXmlStringEqualsXmlString(
              '<foo><bar/></foo>', '<foo><baz/></foo>');
        }
    }
    ?>

.. code-block:: bash

    $ phpunit XmlStringEqualsXmlStringTest
    PHPUnit 6.4.0 by Sebastian Bergmann and contributors.

    F

    Time: 0 seconds, Memory: 5.00Mb

    There was 1 failure:

    1) XmlStringEqualsXmlStringTest::testEchec
    Failed asserting that two DOM documents are equal.
    --- Expected
    +++ Actual
    @@ @@
     <?xml version="1.0"?>
     <foo>
    -  <bar/>
    +  <baz/>
     </foo>

    /home/sb/XmlStringEqualsXmlStringTest.php:7

    FAILURES!
    Tests: 1, Assertions: 1, Failures: 1.


