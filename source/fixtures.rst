

.. _fixtures:

========
Fixtures
========

L'une des parties les plus consommatrices en temps lors de l'écriture
de tests est d'écrire le code pour configurer le monde dans un état connu
puis de le remettre dans son état initial quand le test est terminé. Cet état
connu est appelé la *fixture* du test.

Dans :ref:`writing-tests-for-phpunit.examples.StackTest.php`, la
fixture était simplement le tableau sauvegardé dans la variable ``$fixture``.
La plupart du temps, cependant, la fixture sera beaucoup plus complexe
qu'un simple tableau, et le volume de code nécessaire pour la mettre en place
croîtra dans les mêmes proportions. Le contenu effectif du test sera perdu
dans le bruit de configuration de la fixture. Ce problème s'aggrave quand
vous écrivez plusieurs tests doté de fixtures similaires. Sans l'aide du
framework de test, nous aurions à dupliquer le code qui configure la fixture
pour chaque test que nous écrivons.

PHPUnit gère le partage du code de configuration. Avant qu'une méthode de test ne soit
lancée, une méthode canevas appelée ``setUp()`` est invoquée.
``setUp()`` est l'endroit où vous créez les objets sur lesquels
vous allez passer les tests. Une fois que la méthode de test est finie, qu'elle ait
réussi ou échoué, une autre méthode canevas appelée
``tearDown()`` est invoquée. ``tearDown()``
est l'endroit où vous nettoyez les objets sur lesquels vous avez passé les tests.

Dans :ref:`writing-tests-for-phpunit.examples.StackTest2.php` nous avons
utilisé la relation producteur-consommateur entre les tests pour partager une fixture. Ce
n'est pas toujours souhaitable ni même possible. :numref:`fixtures.examples.StackTest.php`
montre comme nous pouvons écrire les tests de ``PileTest`` de telle façon
que ce n'est pas la fixture elle-même qui est réutilisée mais le code qui l'a créée.
D'abord nous déclarons la variable d'instance, ``$pile``, que nous
allons utiliser à la place d'une variable locale à la méthode. Puis nous plaçons
la création de la fixture ``tableau`` dans la méthode
``setUp()``. Enfin, nous supprimons le code redondant des méthodes
de test et nous utilisons la variable d'instance nouvellement introduite.
``$this->pile``, à la place de la variable locale à la méthode
``$pile`` avec la méthode d'assertion ``assertEquals()``.

.. code-block:: php
    :caption: Using setUp() to create the stack fixture
    :name: fixtures.examples.StackTest.php

    <?php
    class PileTest extends PHPUnit_Framework_TestCase
    {
        protected $pile;

        protected function setUp()
        {
            $this->pile = array();
        }

        public function testVide()
        {
            $this->assertTrue(empty($this->pile));
        }

        public function testPush()
        {
            array_push($this->pile, 'foo');
            $this->assertEquals('foo', $this->pile[count($this->pile)-1]);
            $this->assertFalse(empty($this->pile));
        }

        public function testPop()
        {
            array_push($this->pile, 'foo');
            $this->assertEquals('foo', array_pop($this->pile));
            $this->assertTrue(empty($this->pile));
        }
    }
    ?>

Les méthodes canevas ``setUp()`` et ``tearDown()``
sont exécutées une fois pour chaque méthode de test (et pour les nouvelles instances)
de la classe de cas de test.

De plus, les méthodes canevas ``setUpBeforeClass()`` et
``tearDownAfterClass()`` sont appelées respectivement avant
que le premier test de la classe de cas de test ne soit exécuté et après
que le dernier test de la classe de test a été exécuté.

L'exemple ci-dessous montre toutes les méthodes canevas qui sont disponibles
dans une classe de cas de test.

.. code-block:: php
    :caption: Exemple montrant toutes les méthodes canevas disponibles
    :name: fixtures.examples.TemplateMethodsTest.php

    <?php
    class TemplateMethodsTest extends PHPUnit_Framework_TestCase
    {
        public static function setUpBeforeClass()
        {
            fwrite(STDOUT, __METHOD__ . "\n");
        }

        protected function setUp()
        {
            fwrite(STDOUT, __METHOD__ . "\n");
        }

        protected function assertPreConditions()
        {
            fwrite(STDOUT, __METHOD__ . "\n");
        }

        public function testOne()
        {
            fwrite(STDOUT, __METHOD__ . "\n");
            $this->assertTrue(TRUE);
        }

        public function testTwo()
        {
            fwrite(STDOUT, __METHOD__ . "\n");
            $this->assertTrue(FALSE);
        }

        protected function assertPostConditions()
        {
            fwrite(STDOUT, __METHOD__ . "\n");
        }

        protected function tearDown()
        {
            fwrite(STDOUT, __METHOD__ . "\n");
        }

        public static function tearDownAfterClass()
        {
            fwrite(STDOUT, __METHOD__ . "\n");
        }

        protected function onNotSuccessfulTest(Exception $e)
        {
            fwrite(STDOUT, __METHOD__ . "\n");
            throw $e;
        }
    }
    ?>

.. code-block:: bash

    $ phpunit TemplateMethodsTest
    PHPUnit 6.4.0 by Sebastian Bergmann and contributors.

    TemplateMethodsTest::setUpBeforeClass
    TemplateMethodsTest::setUp
    TemplateMethodsTest::assertPreConditions
    TemplateMethodsTest::testOne
    TemplateMethodsTest::assertPostConditions
    TemplateMethodsTest::tearDown
    .TemplateMethodsTest::setUp
    TemplateMethodsTest::assertPreConditions
    TemplateMethodsTest::testTwo
    TemplateMethodsTest::tearDown
    TemplateMethodsTest::onNotSuccessfulTest
    FTemplateMethodsTest::tearDownAfterClass

    Time: 0 seconds, Memory: 5.25Mb

    There was 1 failure:

    1) TemplateMethodsTest::testTwo
    Failed asserting that <boolean:false> is true.
    /home/sb/TemplateMethodsTest.php:30

    FAILURES!
    Tests: 2, Assertions: 2, Failures: 1.

.. _fixtures.more-setup-than-teardown:

Plus de setUp() que de tearDown()
#################################

``setUp()`` et ``tearDown()`` sont sympathiquement
symétriques en théorie mais pas en pratique. En pratique, vous n'avez besoin
d'implémenter ``tearDown()`` que si vous avez alloué
des ressources externes telles que des fichiers ou des sockets dans
``setUp()``. Si votre ``setUp()`` ne crée simplement
que de purs objets PHP, vous pouvez généralement ignorer ``tearDown()``.
Cependant, si vous créez de nombreux objets dans votre ``setUp()``, vous
pourriez vouloir libérer (``unset()``) les variables pointant vers
ces objets dans votre ``tearDown()`` de façon à ce qu'ils puissent être
récupérés par le ramasse-miettes. Le nettoyage des objets de cas de test n'est pas
prévisible.

.. _fixtures.variations:

Variantes
#########

Que se passe-t'il si vous avez deux tests avec deux setups légèrement
différents ? Il y a deux possibilités :

-

  Si le code des ``setUp()`` ne diffère que légèrement, extrayez le
  code qui diffère du code de ``setUp()`` pour le mettre dans la méthode
  de test.

-

  Si vous avez vraiment deux ``setUp()`` différentes, vous
  avez besoin de classes de cas de test différentes. Nommez les classes selon
  les différences constatées dans les setup.

.. _fixtures.sharing-fixture:

Partager les Fixtures
#####################

Il existe quelques bonnes raisons pour partager des fixtures entre les tests,
mais dans la plupart des cas la nécessité de partager une fixture entre plusieurs
tests résulte d'un problème de conception non résolu.

Un bon exemple de fixture qu'il est raisonnable de partager entre plusieurs
tests est une connexion à une base de données : vous vous connectez une fois
à la base de données et vous réutilisez cette connexion au lieu d'en créer
une nouvelle pour chaque test. Ceci rend vos tests plus rapides.

:numref:`fixtures.sharing-fixture.examples.DatabaseTest.php`
utilise les méthodes canevas ``setUpBeforeClass()`` et
``tearDownAfterClass()`` pour respectivement établir la connexion à la
base de données avant le premier test de la classe de cas de test et pour
de déconnecter de la base de données après le dernier test du cas de test.

.. code-block:: php
    :caption: Partager les fixtures entre les tests d'une série de tests
    :name: fixtures.sharing-fixture.examples.DatabaseTest.php

    <?php
    class DatabaseTest extends PHPUnit_Framework_TestCase
    {
        protected static $dbh;

        public static function setUpBeforeClass()
        {
            self::$dbh = new PDO('sqlite::memory:');
        }

        public static function tearDownAfterClass()
        {
            self::$dbh = NULL;
        }
    }
    ?>

On n'insistera jamais assez sur le fait que partager les fixtures
entre les tests réduit la valeur de ces tests. Le problème de conception
sous-jacent est que les objets ne sont pas faiblement couplés. Vous pourrez
obtenir de meilleurs résultats en résolvant le problème de conception
sous-jacent puis en écrivant des tests utilisant des bouchons
(voir :ref:`test-doubles`), plutôt qu'en créant
des dépendances entre les tests à l'exécution et en ignorant l'opportunité
d'améliorer votre conception.

.. _fixtures.global-state:

Etat global
###########

`Il est difficile de tester du code qui utilise des singletons. <http://googletesting.blogspot.com/2008/05/tott-using-dependancy-injection-to.html>`_
La même chose est vraie pour le code qui utilise des variables globales. Typiquement,
le code que vous voulez tester est fortement couplé avec une variable globale et
vous ne pouvez pas contrôler sa création. Un problème additionnel réside dans le fait
qu'un test qui modifie une variable globale peut faire échouer un autre test.

En PHP, les variables globales fonctionnent comme ceci :

-

  Une variable globale ``$foo = 'bar';`` est enregistrée comme ``$GLOBALS['foo'] = 'bar';``.

-

  La variable ``$GLOBALS`` est une variable appelée *super-globale*.

-

  Les variables super-globales sont des variables internes qui sont toujours disponibles dans toutes les portées.

-

  Dans la portée d'une fonction ou d'une méthode, vous pouvez accéder à la variable globale ``$foo`` soit en accédant directement à ``$GLOBALS['foo']`` soit en utilisant ``global $foo;`` pour créer une variable locale faisant référence à la variable globale.

A part les variables globales, les attributs statiques des classes font
également partie de l'état global.

Par défaut, PHPUnit exécute vos tests de façon à ce que des modifications
aux variables globales et super-globales (
``$GLOBALS``,
``$_ENV``, ``$_POST``,
``$_GET``, ``$_COOKIE``,
``$_SERVER``, ``$_FILES``,
``$_REQUEST``) n'affectent pas les autres tests. Optionnellement,
cette indépendance peut être étendue aux attributs statiques des classes.

.. admonition:: Note

   L'implémentation des opérations de sauvegarde et de restauration des attributs
   statiques des classes nécessite PHP 5.3 (ou supérieur).

   L'implémentation des opérations de sauvegarde et de restauration des variables
   globales et des attributs statiques des classes utilise
   ``serialize()`` et ``unserialize()``.

   Les objets de certaines classes qui sont fournis pas PHP lui-même, tel que
   ``PDO`` par exemple, ne peuvent pas être sérialisés si bien que
   l'opération de sauvegarde va échouer quand un tel objet sera enregistré dans le tableau
   ``$GLOBALS``, par exemple.

L'annotation ``@backupGlobals`` qui est discutée dans
:ref:`appendixes.annotations.backupGlobals` peut être utilisée pour
contrôler les opérations de sauvegarde et de restauration des variables globales.
Alternativement, vous pouvez fournir une liste noire des variables globales qui doivent
être exclues des opérations de sauvegarde et de restauration comme ceci :

.. code-block:: php

    class MonTest extends PHPUnit_Framework_TestCase
    {
        protected $backupGlobalsBlacklist = array('globalVariable');

        // ...
    }

.. admonition:: Note

   Merci de noter que le réglage de l'attribut ``$backupGlobalsBlacklist``
   à l'intérieur de la méthode ``setUp()``, par exemple, n'a aucun effet.

L'annotation ``@backupStaticAttributes`` qui est discutée dans
:ref:`appendixes.annotations.backupStaticAttributes` peut être utilisée pour
contrôler les opérations de sauvegarde et de restauration des attributs statiques.
Alternativement, vous pouvez fournir une liste noire des attributs statiques qui doivent
être exclus des opérations de sauvegarde et de restauration comme ceci :

.. code-block:: php

    class MonTest extends PHPUnit_Framework_TestCase
    {
        protected $backupStaticAttributesBlacklist = array(
          'className' => array('attributeName')
        );

        // ...
    }

.. admonition:: Note

   Merci de noter que le réglage de l'attribut ``$backupStaticAttributesBlacklist``
   à l'intérieur de la méthode ``setUp()``, par exemple, n'a aucun effet.


