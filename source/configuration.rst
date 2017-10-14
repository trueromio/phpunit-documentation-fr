

.. _appendixes.configuration:

=========================================
Le fichier de configuration Configuration
=========================================

.. _appendixes.configuration.phpunit:

PHPUnit
#######

Les attributs d'un élément ``<phpunit>`` peuvent être
utilisés pour configurer les fonctionnalités du coeur de PHPUnit.

.. code-block:: bash

    <phpunit
             xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
             xsi:noNamespaceSchemaLocation="https://schema.phpunit.de/6.3/phpunit.xsd"
             backupGlobals="true"
             backupStaticAttributes="false"
             <!--bootstrap="/chemin/vers/amorce.php"-->
             cacheTokens="true"
             colors="false"
             convertErrorsToExceptions="true"
             convertNoticesToExceptions="true"
             convertWarningsToExceptions="true"
             forceCoversAnnotation="false"
             mapTestClassNameToCoveredClassName="false"
             printerClass="PHPUnit_TextUI_ResultPrinter"
             <!--printerFile="/chemin/vers/AfficheurResultat.php"-->
             processIsolation="false"
             stopOnError="false"
             stopOnFailure="false"
             stopOnIncomplete="false"
             stopOnSkipped="false"
             testSuiteLoaderClass="PHPUnit_Runner_StandardTestSuiteLoader"
             <!--testSuiteLoaderFile="/chemin/vers/ChargeurStandardDeSuiteDeTest.php"-->
             strict="false"
             verbose="false">
      <!-- ... -->
    </phpunit>

Le fichier de configuration XML ci-dessus correspond au comportement par
défaut du lanceur de tests TextUI documenté dans
:ref:`textui.clioptions`.

Des options supplémentaires qui ne sont pas disponibles en tant qu'option de ligne de commandes sont :

``convertNoticesToExceptions``, ``convertWarningsToExceptions``, ``convertErrorsToExceptions``

    Peuvent être utilisées pour désactiver la conversion automatique
    de toutes les erreurs, avertissement ou information de php en exception.

``forceCoversAnnotation``

    La couverture de code ne sera enregistrée que pour les tests qui
    utilisent l'annotation ``@covers`` documentée dans
    :ref:`appendixes.annotations.covers`.

.. _appendixes.configuration.testsuites:

Série de tests
##############

L'élément ``<testsuites>`` et son ou ses
fils ``<testsuite>`` peuvent être utilisés pour
composer une série de tests à partir des séries de test et des cas de test.

.. code-block:: bash

    <testsuites>
      <testsuite name="Ma suite de tests">
        <directory>/chemin/vers/fichiers *Test.php</directory>
        <file>/chemin/vers/MonTest.php</file>
        <exclude>/chemin/a/exclure</exclude>
      </testsuite>
    </testsuites>

En utilisant les attributs ``phpVersion`` et
``phpVersionOperator``, une version requise de PHP
peut être indiquée. L'exemple ci-dessous ne va ajouter que
les fichiers :file:`/chemin/vers/\*Test.php` et
:file:`/chemin/vers/MonTest.php` si la version de PHP est
au moins 5.3.0.

.. code-block:: bash

      <testsuites>
        <testsuite name="Ma suite de tests">
          <directory suffix="Test.php" phpVersion="5.3.0" phpVersionOperator=">=">/chemin/vers/fichiers</directory>
          <file phpVersion="5.3.0" phpVersionOperator=">=">/chemin/vers/MonTest.php</file>
        </testsuite>
      </testsuites>

L'attribut ``phpVersionOperator`` est facultatif et vaut par
défaut ``>=``.

.. _appendixes.configuration.groups:

Groupes
#######

L'élément ``<groups>`` et ses fils
``<include>``,
``<exclude>`` et
``<group>`` peuvent être utilisés pour choisir
des groupes de tests depuis une série de tests qui doivent (ou ne doivent pas)
être exécutés.

.. code-block:: bash

    <groups>
      <include>
        <group>nom</group>
      </include>
      <exclude>
        <group>nom</group>
      </exclude>
    </groups>

La configuration XML ci-dessus revient à appeler le lanceur de test TextUI
avec les options suivantes:

-

  ``--group nom``

-

  ``--exclude-group nom``

.. _appendixes.configuration.blacklist-whitelist:

Inclure et exclure des fichiers de la couverture de code
########################################################

L'élément ``<filter>`` et ses fils peuvent être
utilisés pour configurer les listes noires et les listes blanches pour les rapports
de couverture de code.

.. code-block:: bash

    <filter>
      <blacklist>
        <directory suffix=".php">/chemin/vers/fichiers</directory>
        <file>/chemin/vers/fichier</file>
        <exclude>
          <directory suffix=".php">/chemin/vers/fichiers</directory>
          <file>/chemin/vers/fichier</file>
        </exclude>
      </blacklist>
      <whitelist processUncoveredFilesFromWhitelist="true">
        <directory suffix=".php">/chemin/vers/fichiers</directory>
        <file>/chemin/vers/fichier</file>
        <exclude>
          <directory suffix=".php">/chemin/vers/fichiers</directory>
          <file>/chemin/vers/fichier</file>
        </exclude>
      </whitelist>
    </filter>

.. _appendixes.configuration.logging:

Journalisation
##############

L'élément ``<logging>`` et ses fils
``<log>`` peuvent être utilisés pour configurer
la journalisation de l'exécution des tests.

.. code-block:: bash

    <logging>
      <log type="coverage-html" target="/tmp/report" charset="UTF-8"
           yui="true" highlight="false"
           lowUpperBound="35" highLowerBound="70"/>
      <log type="coverage-clover" target="/tmp/coverage.xml"/>
      <log type="coverage-php" target="/tmp/coverage.serialized"/>
      <log type="coverage-text" target="php://stdout" showUncoveredFiles="false"/>
      <log type="json" target="/tmp/logfile.json"/>
      <log type="tap" target="/tmp/logfile.tap"/>
      <log type="junit" target="/tmp/logfile.xml" logIncompleteSkipped="false"/>
      <log type="testdox-html" target="/tmp/testdox.html"/>
      <log type="testdox-text" target="/tmp/testdox.txt"/>
    </logging>

La configuration XML ci-dessus revient à invoquer le lanceur de tests TextUI
avec les options suivantes :

-

  ``--coverage-html /tmp/report``

-

  ``--coverage-clover /tmp/coverage.xml``

-

  ``--coverage-php /tmp/coverage.serialized``

-

  ``--coverage-text``

-

  ``--log-json /tmp/logfile.json``

-

  ``> /tmp/logfile.txt``

-

  ``--log-tap /tmp/logfile.tap``

-

  ``--log-junit /tmp/logfile.xml``

-

  ``--testdox-html /tmp/testdox.html``

-

  ``--testdox-text /tmp/testdox.txt``

Les attributs ``charset``, ``yui``,
``highlight``, ``lowUpperBound``,
``highLowerBound``, ``logIncompleteSkipped``
and ``showUncoveredFiles``
n'ont pas d'options équivalentes pour le lanceur de tests TextUI.

-

  ``charset: encodage de caractères à utiliser pour les pages html générées``

-

  ``yui: améliore le rapport de couverture html en utilisant la bibliothèque yui.
          Par exemple, lorsque vous cliquez sur un numéro de ligne, un panneau YUI apparaît avec une liste de toutes les méthodes qui couvrent cette ligne.``

-

  ``highlight: Quand mis à vrai, les rapports de couverture de code bénéficient de la coloration syntaxique.``

-

  ``lowUpperBound: pourcentage de couverture maximum considérée comme étant faible.``

-

  ``highLowerBound: pourcentage de couverture minimum considérée comme étant forte.``

-

  ``showUncoveredFiles:
          Montre tous les fichiers en liste blanche dans la sortie --coverage-text et pas seulement ceux possédant des informations de couverture.``

.. _appendixes.configuration.test-listeners:

Moniteurs de tests
##################

L'élément ``<listeners>`` et ses fils
``<listener>`` peuvent être utilisés pour brancher des
moniteurs de tests additionnels lors de l'exécution des tests.

.. code-block:: bash

    <listeners>
      <listener class="MonMoniteur" file="/optionnel/chemin/vers/MonMoniteur.php">
        <arguments>
          <array>
            <element key="0">
              <string>Sebastian</string>
            </element>
          </array>
          <integer>22</integer>
          <string>April</string>
          <double>19.78</double>
          <null/>
          <object class="stdClass"/>
        </arguments>
      </listener>
    </listeners>

La configuration XML ci-dessus revient à brancher l'objet
``$moniteur`` (voir ci-dessous) à l'exécution des tests :

.. code-block:: bash

    $moniteur = new MonMoniteur(
      array('Sebastian'),
      22,
      'April',
      19.78,
      NULL,
      new stdClass
    );

.. _appendixes.configuration.php-ini-constants-variables:

Configurer les réglages de PHP INI, les constantes et les variables globales
############################################################################

L'élément ``<php>`` et ses fils peuvent être utilisés
pour configurer les réglages PHP, les constantes et les variables globales. Il peut
également être utilisé pour préfixer l'``include_path``.

.. code-block:: bash

    <php>
      <includePath>.</includePath>
      <ini name="foo" value="bar"/>
      <const name="foo" value="bar"/>
      <var name="foo" value="bar"/>
      <env name="foo" value="bar"/>
      <post name="foo" value="bar"/>
      <get name="foo" value="bar"/>
      <cookie name="foo" value="bar"/>
      <server name="foo" value="bar"/>
      <files name="foo" value="bar"/>
      <request name="foo" value="bar"/>
    </php>

La configuration XML ci-dessus correspond au code PHP suivant :

.. code-block:: bash

    ini_set('foo', 'bar');
    define('foo', 'bar');
    $GLOBALS['foo'] = 'bar';
    $_ENV['foo'] = 'bar';
    $_POST['foo'] = 'bar';
    $_GET['foo'] = 'bar';
    $_COOKIE['foo'] = 'bar';
    $_SERVER['foo'] = 'bar';
    $_FILES['foo'] = 'bar';
    $_REQUEST['foo'] = 'bar';

.. _appendixes.configuration.selenium-rc:

Configurer les navigateurs pour Selenium RC
###########################################

L'élément ``<selenium>`` et ses fils
``<browser>`` peuvent être utilisés pour
configurer une liste de serveurs Selenium RC.

.. code-block:: bash

    <selenium>
      <browser name="Firefox sur Linux"
               browser="*firefox /usr/lib/firefox/firefox-bin"
               host="ma.box.linux"
               port="4444"
               timeout="30000"/>
    </selenium>

La configuration XML ci-dessus correspond au code PHP suivant :

.. code-block:: bash

    class WebTest extends PHPUnit_Extensions_SeleniumTestCase
    {
        public static $browsers = array(
          array(
            'name'    => 'Firefox sur Linux',
            'browser' => '*firefox /usr/lib/firefox/firefox-bin',
            'host'    => 'ma.box.linux',
            'port'    => 4444,
            'timeout' => 30000
          )
        );

        // ...
    }


