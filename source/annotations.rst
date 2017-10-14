

.. _appendixes.annotations:

===========
Annotations
===========

Une annotation est une forme spéciale de méta donnée syntaxique qui peut
être ajoutée au code source de certains langages de programmation. Bien que
PHP n'ait pas de fonctionnalité dédiée à l'annotation du code source, l'utilisation
d'étiquettes telles que ``@annotation paramètres`` dans les blocs de documentation
s'est établi dans la communauté PHP pour annoter le code source. En PHP, les blocs de
documentation sont réflexifs: ils peuvent être accédés via la méthode de l'API de réflexivité
``getDocComment()`` au niveau des fonctions, classes, méthodes et attributs.
Des applications telles que PHPUnit utilisent ces informations durant l'exécution pour
adapter leur comportement.

Cette annexe montre toutes les sortes d'annotations gérées par PHPUnit.

.. _appendixes.annotations.author:

@author
#######

L'annotation ``@author`` est un alias pour l'annotation
``@group`` (voir :ref:`appendixes.annotations.group`) et permet de filtrer des tests selon
leurs auteurs.

.. _appendixes.annotations.backupGlobals:

@backupGlobals
##############

Les opérations de sauvegarde et de restauration des variables globales peuvent
être complètement désactivées pour tous les tests d'une classe de cas de test
comme ceci :

.. code-block:: php

    /**
     * @backupGlobals disabled
     */
    class MonTest extends PHPUnit_Framework_TestCase
    {
        // ...
    }

L'annotation ``@backupGlobals`` peut également être utilisée sur les opérations
de sauvegarde et de restauration :

.. code-block:: php

    /**
     * @backupGlobals disabled
     */
    class MonTest extends PHPUnit_Framework_TestCase
    {
        /**
         * @backupGlobals enabled
         */
        public function testQuiIntergitAvecDesVariablesGlobales()
        {
            // ...
        }
    }

.. _appendixes.annotations.backupStaticAttributes:

@backupStaticAttributes
#######################

Les opérations de sauvegarde et de restauration pour les attributs statiques
des classes peuvent être complètement désactivés pour tous les tests d'une classe
de cas de test comme ceci :

.. code-block:: php

    /**
     * @backupStaticAttributes disabled
     */
    class MonTest extends PHPUnit_Framework_TestCase
    {
        // ...
    }

L'annotation ``@backupStaticAttributes`` peut également être utilisée au
niveau d'une méthode de test. Ceci permet une configuration plus fine des opérations
de sauvegarde et de restauration:

.. code-block:: php

    /**
     * @backupStaticAttributes disabled
     */
    class MonTest extends PHPUnit_Framework_TestCase
    {
        /**
         * @backupStaticAttributes enabled
         */
        public function testQuiInteragitAvecDesAttributsStatiques()
        {
            // ...
        }
    }

.. _appendixes.annotations.codeCoverageIgnore:

@codeCoverageIgnore*
####################

Les annotations ``@codeCoverageIgnore``,
``@codeCoverageIgnoreStart`` et
``@codeCoverageIgnoreEnd`` peuvent être utilisées pour
exclure des lignes de code de l'analyse de couverture.

Pour la manière de les utiliser, voir :ref:`code-coverage-analysis.ignoring-code-blocks`.

.. _appendixes.annotations.covers:

@covers
#######

L'annotation ``@covers`` peut être utilisée dans le code de test pour
indique quelle(s) méthode(s) un test veut tester:

.. code-block:: php

    /**
     * @covers CompteBancaire::getBalance
     */
    public function testBalanceEstInitiallementAZero()
    {
        $this->assertEquals(0, $this->ba->getBalance());
    }

Si elle est fournie, seule l'information de couverture de code pour
la(les) méthode(s) sera prise en considération.

:numref:`appendixes.annotations.covers.tables.annotations` montre
la syntaxe de l'annotation ``@covers``.

.. rst-class:: table
.. list-table:: Annotations pour indiquer quelles méthodes sont couvertes par un test
    :name: appendixes.annotations.covers.tables.annotations
    :header-rows: 1

    * - Annotation
      - Description
    * - ``@covers NomClasse::nomMethode``
      - ``Indique que la méthode de test annotée couvre la méthode indiquée.``
    * - ``@covers NomClasse``
      - ``Indique que la méthode de test annotée couvre toutes les méthodes d'une classe donnée.``
    * - ``@covers NomClasse<extended>``
      - ``Indique que la méthode de test annotée couvre toutes les méthodes d'une classe donnée ainsi que les classe(s) et interface(s) parentes.``
    * - ``@covers NomClasse::<public>``
      - ``Indique que la méthode de test annotée couvre toutes les méthodes publiques d'une classe donnée.``
    * - ``@covers NomClasse::<protected>``
      - ``Indique que la méthode de test annotée couvre toutes les méthodes protected d'une classe donnée.``
    * - ``@covers NomClasse::<private>``
      - ``Indique que la méthode de test annotée couvre toutes les méthodes privées d'une classe donnée.``
    * - ``@covers NomClasse::<!public>``
      - ``Indique que la méthode de test annotée couvre toutes les méthodes d'une classe donnée qui ne sont pas publiques.``
    * - ``@covers NomClasse::<!protected>``
      - ``Indique que la méthode de test annotée couvre toutes les méthodes d'une classe donnée qui ne sont pas protected.``
    * - ``@covers NomClasse::<!private>``
      - ``Indique que la méthode de test annotée couvre toutes les méthodes d'une classe donnée qui ne sont pas privées.``

.. _appendixes.annotations.coversNothing:

@coversNothing
##############

L'annotation ``@coversNothing`` peut être utilisée dans le code de test
pour indiquer qu'aucune information de couverture de code ne sera enregistrée pour le
cas de test annoté.

Ceci peut être utilisé pour le test d'intégration. Voir
:ref:`code-coverage-analysis.specifying-covered-methods.examples.GuestbookIntegrationTest.php`
pour un exemple.

L'annotation peut être utilisée au niveau de la classe et de la méthode
et sera surchargée par toute étiquette ``@covers``.

.. _appendixes.annotations.dataProvider:

@dataProvider
#############

Une méthode de test peut accepter des paramètres arbitraires. Ces paramètres
peuvent être fournis pas une méthode fournisseuse de données (
(``provider()`` dans
:ref:`writing-tests-for-phpunit.data-providers.examples.DataTest.php`).
La méthode fournisseur de données peut être indiquée en utilisant l'annotation
``@dataProvider``.

Voir :ref:`writing-tests-for-phpunit.data-providers` pour plus de
détails.

.. _appendixes.annotations.depends:

@depends
########

PHPUnit gère la déclaration des dépendances explicites entre les méthodes
de test. De telles dépendances ne définissent pas l'ordre dans lequel les
méthodes de test doivent être exécutées mais elles permettent de retourner
l'instance d'une fixture de test par un producteur et de la passer aux
consommateurs dépendants.
:ref:`writing-tests-for-phpunit.examples.StackTest2.php` montre
comment utiliser l'annotation ``@depends`` pour exprimer des
dépendances entre méthodes de test.

Voir :ref:`writing-tests-for-phpunit.test-dependencies` pour plus de
détails.

.. _appendixes.annotations.expectedException:

@expectedException
##################

:ref:`writing-tests-for-phpunit.exceptions.examples.ExceptionTest.php`
montre comment utiliser l'annotation ``@expectedException`` pour tester
si une exception est levée dans le code testé.

Voir :ref:`writing-tests-for-phpunit.exceptions` pour plus de
détails.

.. _appendixes.annotations.expectedExceptionCode:

@expectedExceptionCode
######################

L'annotation ``@expectedExceptionCode``, en conjonction avec
``@expectedException`` permet de faire des assertions sur le
code d'erreur d'une exception levée ce qui permet de cibler une exception
particulière.

.. code-block:: php

    class MonTest extends PHPUnit_Framework_TestCase
    {
        /**
         * @expectedException     MonException
         * @expectedExceptionCode 20
         */
        public function testExceptionAUnCodeErreur20()
        {
            throw new MonException('Un message', 20);
        }
    }

Pour faciliter les tests et réduire la duplication, un raccourci peut être utilisé pour
indiquer une constante de classe comme un
``@expectedExceptionCode`` en utilisant la syntaxe
"``@expectedExceptionCode ClassName::CONST``".

.. code-block:: php

    class MonTest extends PHPUnit_Framework_TestCase
      {
          /**
            * @expectedException     MonException
            * @expectedExceptionCode MaClasse::CODE_ERREUR
            */
          public function testExceptionAUnCodeErreur20()
          {
            throw new MonException('Un message', 20);
          }
      }
      class MaClasse
      {
          const CODE_ERREUR = 20;
      }

.. _appendixes.annotations.expectedExceptionMessage:

@expectedExceptionMessage
#########################

L'annotation ``@expectedExceptionMessage`` fonctionne de manière
similaire à ``@expectedExceptionCode`` en ce qu'il vous permet de
faire une assertion sur le message d'erreur d'une exception.

.. code-block:: php

    class MonTest extends PHPUnit_Framework_TestCase
    {
        /**
         * @expectedException        MonException
         * @expectedExceptionMessage Un message
         */
        public function testExceptionALeBonMessage()
        {
            throw new MonException('Un message', 20);
        }
    }

Le message attendu peut être une partie d'une chaîne d'un message d'exception.
Ceci peut être utile pour faire une assertion sur le fait qu'un nom ou un
paramètre qui est passé s'affiche dans une exception sans fixer la totalité
du message d'exception dans le test.

.. code-block:: php

    class MonTest extends PHPUnit_Framework_TestCase
    {
         /**
          * @expectedException        MonException
          * @expectedExceptionMessage cassé
          */
         public function testExceptionALeBonMessage()
         {
             $param = "cassé";
             throw new MonException('Paramètre "'.$param.'" incorrect.', 20);
         }
    }

Pour faciliter les tests et réduire la duplication, un raccourci peut être utilisé pour
indiquer une constante de classe comme un
``@expectedExceptionCode`` en utilisant la syntaxe
"``@expectedExceptionCode ClassName::CONST``".
Un exemple peut être trouvé dans :ref:`appendixes.annotations.expectedExceptionCode`.

.. _appendixes.annotations.group:

@group
######

Un test peut être marqué comme appartement à un ou plusieurs groupes en utilisant
l'annotation ``@group`` comme ceci

.. code-block:: php

    class MonTest extends PHPUnit_Framework_TestCase
    {
        /**
         * @group specification
         */
        public function testQuelquechose()
        {
        }

        /**
         * @group regresssion
         * @group bug2204
         */
        public function testAutreChose()
        {
        }
    }

Des tests peuvent être sélectionnés pour l'exécution en se basant sur les groupes
en utilisant les options ``--group`` et ``--exclude-group``
du lanceur de test en ligne de commandes ou en utilisant les directives respectives du
fichier de configuration XML.

.. _appendixes.annotations.requires:

@requires
#########

L'annotation ``@requires`` peut être utilisée pour sauter des tests lorsque
des pré-requis communs, comme la version de PHP ou des extensions installées, ne sont pas
fournis.

Une liste complète des possibilités et des exemples peuvent être trouvés à
:ref:`incomplete-and-skipped-tests.requires.tables.api`

.. _appendixes.annotations.runTestsInSeparateProcesses:

@runTestsInSeparateProcesses
############################

.. code-block:: php

.. _appendixes.annotations.runInSeparateProcess:

@runInSeparateProcess
#####################

.. code-block:: php

.. _appendixes.annotations.test:

@test
#####

Comme alternative à préfixer vos noms de méthodes de test avec
``test``, vous pouvez utiliser l'annotation ``@test``
dans le bloc de documentation d'une méthode pour la marquer comme méthode de test.

.. code-block:: php

    /**
     * @test
     */
    public function balanceInitialeDoitEtre0()
    {
        $this->assertEquals(0, $this->ba->getBalance());
    }

.. _appendixes.annotations.testdox:

@testdox
########

.. code-block:: php

.. _appendixes.annotations.ticket:

@ticket
#######

.. code-block:: php


