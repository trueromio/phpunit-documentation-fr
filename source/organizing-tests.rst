

.. _organizing-tests:

===================
Organiser les tests
===================

L'un des objectifs de PHPUnit est que les tests
soient combinables: nous voulons pouvoir exécuter n'importe quel nombre ou combinaison
de tests ensembles, par exemple tous les tests pour le projet entier, ou
les tests pour toutes les classes d'un composant qui constitue une partie du projet ou
simplement les tests d'une seule classe particulière.

PHPUnit gère différente façon d'organiser les tests et de les combiner en une
suite de tests. Ce chapitre montre les approches les plus communément utilisées.

.. _organizing-tests.filesystem:

Composer une suite de tests en utilisant le système de fichiers
###############################################################

La façon probablement la plus simple de composer une suite de tests est de conserver
tous les fichiers sources des cas de test dans un répertoire test. PHPUnit peut
automatiquement trouver et exécuter les tests en parcourant récursivement le répertoire test.

Jetons un oeil à la suite de tests de la bibliothèque `Object_Freezer <http://github.com/sebastianbergmann/php-object-freezer/>`_. En regardant la structure des répertoires du projet, nous voyons que
les classes de cas de test dans le répertoire :file:`Tests` reflètent la structure des
paquetages et des classes du système en cours de test (SCT, System Under Test ou SUT) dans le répertoire
:file:`Object`:

.. code-block:: bash

    Object                              Tests
    |-- Freezer                         |-- Freezer
    |   |-- HashGenerator               |   |-- HashGenerator
    |   |   `-- NonRecursiveSHA1.php    |   |   `-- NonRecursiveSHA1Test.php
    |   |-- HashGenerator.php           |   |
    |   |-- IdGenerator                 |   |-- IdGenerator
    |   |   `-- UUID.php                |   |   `-- UUIDTest.php
    |   |-- IdGenerator.php             |   |
    |   |-- LazyProxy.php               |   |
    |   |-- Storage                     |   |-- Storage
    |   |   `-- CouchDB.php             |   |   `-- CouchDB
    |   |                               |   |       |-- WithLazyLoadTest.php
    |   |                               |   |       `-- WithoutLazyLoadTest.php
    |   |-- Storage.php                 |   |-- StorageTest.php
    |   `-- Util.php                    |   `-- UtilTest.php
    `-- Freezer.php                     `-- FreezerTest.php

Pour exécuter tous les tests de la bibliothèque, nous n'avons qu'à faire
pointer le lanceur de tests en ligne de commandes de PHPUnit sur ce
répertoire test :

.. code-block:: bash

    $ phpunit Tests
    PHPUnit 6.4.0 by Sebastian Bergmann and contributors.

    ............................................................ 60 / 75
    ...............

    Time: 0 seconds

    OK (75 tests, 164 assertions)

.. admonition:: Note

   Si vous pointez le lanceur de tests en ligne de commandes de PHPUnit sur
   un répertoire, il va chercher les fichiers
   :file:`*Test.php`.

Pour n'exécuter que les tests déclarés dans la classe de cas de test
``Object_FreezerTest`` dans :file:`Tests/FreezerTest.php`,
nous pouvons utiliser la commande suivante :

.. code-block:: bash

    $ phpunit Tests/FreezerTest
    PHPUnit 6.4.0 by Sebastian Bergmann and contributors.

    ............................

    Time: 0 seconds

    OK (28 tests, 60 assertions)

Pour un contrôle plus fin sur les tests à exécuter, nous pouvons utiliser
l'option ``--filter``:

.. code-block:: bash

    $ phpunit --filter testFreezingAnObjectWorks Tests
    PHPUnit 6.4.0 by Sebastian Bergmann and contributors.

    .

    Time: 0 seconds

    OK (1 test, 2 assertions)

.. admonition:: Note

   Un inconvénient de cette approche est que nous n'avons pas de contrôle sur
   l'ordre dans lequel les tests sont exécutés. Ceci peut conduire à des problèmes
   concernant les dépendances des tests, voir
   :ref:`writing-tests-for-phpunit.test-dependencies`.
   Dans la prochaine section, nous verrons comment nous pouvons rendre
   l'ordre d'exécution des tests explicité en utilisant le fichier de
   configuration XML.

.. _organizing-tests.xml-configuration:

Composer une suite de tests en utilisant la configuration XML
#############################################################

Le fichier de configuration XML de PHPUnit (:ref:`appendixes.configuration`)
peut aussi être utilisé pour composer une suite de tests.
:numref:`organizing-tests.xml-configuration.examples.phpunit.xml`
montre un exemple minimaliste qui va ajouter toutes les classes ``*Test``
trouvées dans les fichiers :file:`*Test.php` quand
:file:`Tests` est parcouru récursivement.

.. code-block:: php
    :caption: Composer une suite de tests en utilisant la configuration XML
    :name: organizing-tests.xml-configuration.examples.phpunit.xml

    <phpunit>
      <testsuites>
        <testsuite name="Object_Freezer">
          <directory>Tests</directory>
        </testsuite>
      </testsuites>
    </phpunit>

L'ordre dans lequel les tests sont exécutés peut être rendu explicite :

.. code-block:: php
    :caption: Composer une suite de tests en utilisant la configuration XML
    :name: organizing-tests.xml-configuration.examples.phpunit.xml2

    <phpunit>
      <testsuites>
        <testsuite name="Object_Freezer">
          <file>Tests/Freezer/HashGenerator/NonRecursiveSHA1Test.php</file>
          <file>Tests/Freezer/IdGenerator/UUIDTest.php</file>
          <file>Tests/Freezer/UtilTest.php</file>
          <file>Tests/FreezerTest.php</file>
          <file>Tests/Freezer/StorageTest.php</file>
          <file>Tests/Freezer/Storage/CouchDB/WithLazyLoadTest.php</file>
          <file>Tests/Freezer/Storage/CouchDB/WithoutLazyLoadTest.php</file>
        </testsuite>
      </testsuites>
    </phpunit>


