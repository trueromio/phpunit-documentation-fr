

.. _code-coverage-analysis:

=============================
Analyse de couverture de code
=============================

    *Murali Nandigama*:

    La beauté du test ne se trouve pas dans l'effort mais dans l'efficience.

    Savoir ce qui doit être testé est magnifique, et savoir ce qui est testé
    est magnifique.

Dans ce chapitre, vous apprendrez tout sur la fonctionnalité de couverture
de code de PHPUnit qui fournit une vision interne des parties du code de
production qui sont exécutées quand les tests sont exécutés. Cela aide à
répondre à des questions comme :

-

  Comment trouvez-vous le code qui n'est pas encore testé - ou, en d'autres mots, pas
  encore *couvert* par un test ?

-

  Comment mesurez-vous la complétude du test ?

Un exemple de ce que peuvent signifier des statistiques de couverture de code est,
s'il y a une méthode avec 100 lignes de code, et seulement 75 de ces lignes sont réellement
exécutées quand les tests sont lancés, alors la méthode est considérée comme ayant une couverture
de code de 75 pour cent.

La fonctionnalité de couverture de code de PHPUnit fait usage du composant
`PHP_CodeCoverage <http://github.com/sebastianbergmann/php-code-coverage>`_
qui, à son tour, tire partie de la fonctionnalité de couverture d'instructions
fournie par l'extension `Xdebug <http://www.xdebug.org/>`_
de PHP.

Générons un rapport de couverture de code pour la classe ``CompteBancaire``
de :ref:`test-driven-development.bankaccount-example.examples.BankAccount2.php`.

.. code-block:: bash

    $ phpunit --coverage-html ./rapport CompteBancaireTest
    PHPUnit 6.4.0 by Sebastian Bergmann and contributors.

    ...

    Time: 0 seconds

    OK (3 tests, 3 assertions)

    Generating report, this may take a moment.

:numref:`code-coverage-analysis.figures.Code_Coverage.png` montre
un extrait du rapport de couverture de code. Les lignes de code qui ont été
exécutés pendant le fonctionnement des tests sont surlignés en vert, les lignes
de code qui sont exécutables mais n'ont pas été exécutées sont surlignées en rouge
et le "code mort" est surligné en gris. Le nombre à gauche du numéro de la ligne de code
indique combien de tests couvrent cette ligne.

.. _code-coverage-analysis.figures.Code_Coverage.png:

Couverture de code pour setBalance()
####################################

Cliquer sur le numéro de ligne d'une ligne couverte ouvrira un panneau (voir
:numref:`code-coverage-analysis.figures.Code_Coverage2.png`) qui
montre les cas de test qui couvrent cette ligne.

.. _code-coverage-analysis.figures.Code_Coverage2.png:

Panneau avec l'information des tests couvrant la ligne
######################################################

Le rapport de couverture de code de notre exemple ``CompteBancaire``
montre que nous n'avons actuellement aucun test qui appellent les méthodes
``setBalance()``, ``deposerArgent()`` et
``retirerArgent()`` avec des valeurs acceptables.
:numref:`code-coverage-analysis.examples.BankAccountTest.php`
montre un test qui peut être ajouté à la classe de cas de test
``BankAccountTest`` pour couvrir complètement la classe
``CompteBancaire``.

.. code-block:: php
    :caption: Test manquant pour atteindre la couverture de code complète
    :name: code-coverage-analysis.examples.BankAccountTest.php

    <?php
    require_once 'CompteBancaire.php';

    class BankAccountTest extends PHPUnit_Framework_TestCase
    {
        // ...

        public function testDeposerRetirerArgent()
        {
            $this->assertEquals(0, $this->compte_bancaire->getBalance());
            $this->compte_bancaire->deposerArgent(1);
            $this->assertEquals(1, $this->compte_bancaire->getBalance());
            $this->compte_bancaire->retirerArgent(1);
            $this->assertEquals(0, $this->compte_bancaire->getBalance());
        }
    }
    ?>

:numref:`code-coverage-analysis.figures.Code_Coverage3.png` montre
la couverture de code de la méthode ``setBalance()`` avec le test
additionnel.

.. _code-coverage-analysis.figures.Code_Coverage3.png:

Couverture de code pour ``setBalance()`` avec un test additionnel
#################################################################

.. _code-coverage-analysis.specifying-covered-methods:

Spécifier les méthodes couvertes
################################

L'annotation ``@covers`` (voir
:ref:`appendixes.annotations.covers.tables.annotations`) peut être
utilisée dans le code de test pour indiquer quelle(s) méthode(s) une méthode de test
veut test. Si elle est fournie, seules les informations de couverture de code pour
la(les) méthode(s) indiquées seront prises en considération.
:numref:`code-coverage-analysis.specifying-covered-methods.examples.BankAccountTest.php`
montre un exemple.

.. code-block:: php
    :caption: Tests qui indiquent quelle(s) méthode(s) ils veulent couvrir
    :name: code-coverage-analysis.specifying-covered-methods.examples.BankAccountTest.php

    <?php
    require_once 'CompteBancaire.php';

    class CompteBancaireTest extends PHPUnit_Framework_TestCase
    {
        protected $compte_bancaire;

        protected function setUp()
        {
            $this->compte_bancaire = new CompteBancaire;
        }

        /**
         * @covers CompteBancaire::getBalance
         */
        public function testBalanceEstInitialementZero()
        {
            $this->assertEquals(0, $this->compte_bancaire->getBalance());
        }

        /**
         * @covers CompteBancaire::retirerArgent
         */
        public function testBalanceNePeutPasDevenirNegative()
        {
            try {
                $this->compte_bancaire->retirerArgent(1);
            }

            catch (CompteBancaireException $e) {
                $this->assertEquals(0, $this->compte_bancaire->getBalance());

                return;
            }

            $this->fail();
        }

        /**
         * @covers CompteBancaire::deposerArgent
         */
        public function testBalanceNePeutPasDevenirNegative2()
        {
            try {
                $this->compte_bancaire->deposerArgent(-1);
            }

            catch (CompteBancaireException $e) {
                $this->assertEquals(0, $this->compte_bancaire->getBalance());

                return;
            }

            $this->fail();
        }

        /**
         * @covers CompteBancaire::getBalance
         * @covers CompteBancaire::deposerArgent
         * @covers CompteBancaire::retirerArgent
         */

        public function testDeposerArgent()
        {
            $this->assertEquals(0, $this->compte_bancaire->getBalance());
            $this->compte_bancaire->deposerArgent(1);
            $this->assertEquals(1, $this->compte_bancaire->getBalance());
            $this->compte_bancaire->retirerArgent(1);
            $this->assertEquals(0, $this->compte_bancaire->getBalance());
        }
    }
    ?>

Il est également possible d'indiquer qu'un test ne doit couvrir
*aucune* méthode en utilisant l'annotation
``@coversNothing`` (voir
:ref:`appendixes.annotations.coversNothing`). Ceci peut être
utile quand on écrit des tests d'intégration pour s'assurer que vous
ne générez une couverture de code avec des tests unitaires.

.. code-block:: php
    :caption: Un test qui indique qu'aucune méthode ne doit être couverte
    :name: code-coverage-analysis.specifying-covered-methods.examples.GuestbookIntegrationTest.php

    <?php
    class IntegrationLivreDOrTest extends PHPUnit_Extensions_Database_TestCase
    {
        /**
         * @coversNothing
         */
        public function testAjouteEntree()
        {
            $livre_d_or = new LivredOr();
            $livre_d_or->addEntry("suzy", "Hello world!");

            $queryTable = $this->getConnection()->createQueryTable(
                'livre_d_or', 'SELECT * FROM livre_d_or'
            );
            $expectedTable = $this->createFlatXmlDataSet("expectedBook.xml")
                                  ->getTable("livre_d_or");
            $this->assertTablesEqual($expectedTable, $queryTable);
        }
    }
    ?>

.. _code-coverage-analysis.ignoring-code-blocks:

Ignorer des blocs de code
#########################

Parfois, vous avez des blocs de code que vous ne pouvez pas tester et que
voulez ignorer lors de l'analyse de couverture de code. PHPUnit vous permet
de faire cela en utilisant les annotations
``@codeCoverageIgnore``,
``@codeCoverageIgnoreStart`` et
``@codeCoverageIgnoreEnd`` comme montré dans
:numref:`code-coverage-analysis.ignoring-code-blocks.examples.Sample.php`.

.. code-block:: php
    :caption: Utiliser les annotations ``@codeCoverageIgnore``, ``@codeCoverageIgnoreStart`` et ``@codeCoverageIgnoreEnd``
    :name: code-coverage-analysis.ignoring-code-blocks.examples.Sample.php

    <?php
    /**
     * @codeCoverageIgnore
     */
    class Foo
    {
        public function bar()
        {
        }
    }

    class Bar
    {
        /**
         * @codeCoverageIgnore
         */
        public function foo()
        {
        }
    }

    if (FALSE) {
        // @codeCoverageIgnoreStart
        print '*';
        // @codeCoverageIgnoreEnd
    }
    ?>

Les lignes de code qui sont marquées comme devant être ignorées en utilisant
les annotations sont comptées comme exécutées (si elles sont exécutables) et ne
seront pas surlignées.

.. _code-coverage-analysis.including-excluding-files:

Inclure et exclure des fichiers
###############################

Par défaut, tous les fichiers de code source qui contiennent au moins une ligne
de code qui a été exécutée (et seulement ces fichiers) sont inclus dans le rapport.
Les fichiers de code source qui sont inclus dans le rapport peuvent être filtrés en
utilisant une approche par liste noire ou liste blanche.

La liste noire est pré-remplie avec tous les fichiers de code source de
PHPUnit lui-même ainsi que les tests. Quand la liste blanche est vide (par
défaut), le filtrage par liste noire est utilisé. Quand la liste blanche
n'est pas vide, le filtrage par liste blanche est utilisé. Chaque fichier
de la liste blanche est ajouté au rapport de couverture de code, qu'il ait
été exécuté ou pas. Toutes les lignes d'un tel fichier, incluant celles qui
ne sont pas exécutables, sont comptées comme non exécutées.

Quand vous configurez
``processUncoveredFilesFromWhitelist="true"``
dans votre configuration PHPUnit (voir :ref:`appendixes.configuration.blacklist-whitelist`) alors ces fichiers
seront à inclure par PHP_CodeCoverage pour calculer correctement le nombre
de lignes exécutables.

.. admonition:: Note

   Merci de noter que le chargement des fichiers de code source réalisé
   quand ``processUncoveredFilesFromWhitelist="true"`` est positionné,
   peut poser des problèmes quand un fichier de code source contient du code hors de la portée
   d'une classe ou d'une fonction, par exemple.

Le fichier de configuration XML de PHPUnit (voir :ref:`appendixes.configuration.blacklist-whitelist`)
peut être utilisé pour contrôler les listes noires et blanches. Utiliser une liste
blanche est recommandé comme meilleure pratique pour contrôler la liste des fichiers inclus dans
le rapport de couverture de code.

.. _code-coverage-analysis.edge-cases:

Cas limites
###########

Dans la plupart des cas, on peut dire sans risque que PHPUnit offre
une information de couverture de code "basée sur les lignes" mais du fait
de la façon dont l'information est collectée, il existe quelques cas limites
qui valent la peine d'être mentionnés.

.. code-block:: php
    :name: code-coverage-analysis.edge-cases.examples.Sample.php

    <?php
    // Parce qu'il s'agit d'une couverture "basée sur les lignes" et pas sur les instructions
    // une ligne aura toujours un état de couverture donné
    if(false) cet_appel_de_fonction_sera_compte_comme_couvert();

    // Du fait de la façon dont la couverture de code fonctionne en interne, ces deux lignes sont spéciales.
    / Cette ligne sera comptée comme non exécutable
    if(false)
        // Cette ligne sera comptée comme couverte car c'est en fait la
        // couverture de l'instruction if dans la ligne au-dessus qui
        // sera montrée ici !
        sera_egalement_comptee_comme_couverte();

    // Pour éviter cela, il est nécessaire d'utiliser des accolades
    if(false) {
        cet_appel_ne_sera_jamais_compte_comme_couvert();
    }
    ?>


