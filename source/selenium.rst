

.. _selenium:

===================
PHPUnit et Selenium
===================

.. _selenium.selenium-rc:

Selenium Server
###############

`Selenium Server <http://seleniumhq.org/>`_ est un
outil de test qui vous permet d'écrire des tests automatisés de
l'interface utilisateur d'applications web dans n'importe quel langage
et menés sur n'importe quel site web HTTP en utilisant n'importe quel
navigateur courant. Il réalise des tâches automatisée dans le navigateur
en pilotant le processus du navigateur via le système d'exploitation.
Les tests Selenium s'exécutent directement dans un navigateur, exactement
comme des utilisateurs réels le feraient. Ces tests peuvent être utilisés
à la fois comme *tests de validation*
(en exécutant des tests au plus haut niveau sur le système intégré au lieu
de simplement tester chaque unité du système indépendamment) et des
*tests de compatibilité pour les navigateurs* (en testant l'application
web sur différents systèmes d'exploitation et différents navigateurs).

Le seul scénario géré par PHPUnit_Selenium est celui du serveur Selenium 2.x.
Le serveur peut être accédé via l'API classique Selenium RC déjà présente dans la version 1.x ou avec l'API serveur
WebDriver (partiellement implémentée) à partir de PHPUnit_Selenium 1.2.

La raison derrière cette décision est que Selenium 2 est rétro compatible et que Selenium RC n'est désormais plus
maintenu.

.. _selenium.installation:

Installation
############

Premièrement, installer Selenium Server:

#. Télécharger une archive du `Serveur Selenium <http://seleniumhq.org/download/>`_.

#. Dézipper l'archive et copier :file:`selenium-server-standalone-2.20.0.jar` (contrôler le suffixe de version) dans :file:`/usr/local/bin`, par exemple.

#. Lancer le serveur Selenium en exécutant $ java -jar /usr/local/bin/selenium-server-standalone-2.20.0.jar.

Deuxièmement, installer le paquet PHPUnit_Selenium, nécessaire pour accéder nativement au serveur Selenium depuis PHPUnit:

.. code-block:: bash

    $ pear install phpunit/PHPUnit_Selenium

Maintenant, nous pouvons envoyer des commandes au serveur Selenium en utilisant son protocole client/serveur.

.. _selenium.selenium2testcase:

PHPUnit_Extensions_Selenium2TestCase
####################################

Le cas de test ``PHPUnit_Extensions_Selenium2TestCase`` vous permet d'utiliser l'API WebDriver (partiellement implémentée).

:numref:`selenium.selenium2testcase.examples.WebTest.php` montre
comment tester le contenu de l'élément ``<title>``
du site web http://www.example.com/.

.. code-block:: php
    :caption: Exemple d'utilisation de PHPUnit_Extensions_Selenium2TestCase
    :name: selenium.selenium2testcase.examples.WebTest.php

    <?php
    class WebTest extends PHPUnit_Extensions_Selenium2TestCase
    {
        protected function setUp()
        {
            $this->setBrowser('firefox');
            $this->setBrowserUrl('http://www.example.com/');
        }

        public function testTitle()
        {
            $this->url('http://www.example.com/');
            $this->assertEquals('Example WWW Page', $this->title());
        }

    }
    ?>

.. code-block:: bash

    $ phpunit WebTest
    PHPUnit 6.4.0 by Sebastian Bergmann and contributors.

    F

    Time: 28 seconds, Memory: 3.00Mb

    There was 1 failure:

    1) WebTest::testTitle
    Failed asserting that two strings are equal.
    --- Expected
    +++ Actual
    @@ @@
    -'Example WWW Page'
    +'IANA — Example domains'

    /home/giorgio/WebTest.php:13

    FAILURES!
    Tests: 1, Assertions: 1, Failures: 1.

Les commandes de Selenium2TestCase sont implémentées via __call(). Merci de vous référer à `the end-to-end test for PHPUnit_Extensions_Selenium2TestCase <https://github.com/sebastianbergmann/phpunit-selenium/blob/master/Tests/Selenium2TestCaseTest.php>`_ pour la liste de toutes les fonctionnalités prises en charge.

.. _selenium.seleniumtestcase:

PHPUnit_Extensions_SeleniumTestCase
###################################

L'extension de cas de test ``PHPUnit_Extensions_SeleniumTestCase``
implémente le protocole client/serveur pour parler au serveur Selenium ainsi que
des méthodes de vérification spécialisées pour le test web.

:numref:`selenium.seleniumtestcase.examples.WebTest.php` montre
comment tester le contenu de l'élément ``<title>``
du site web http://www.example.com/.

.. code-block:: php
    :caption: Exemple d'utilisation de PHPUnit_Extensions_SeleniumTestCase
    :name: selenium.seleniumtestcase.examples.WebTest.php

    <?php
    require_once 'PHPUnit/Extensions/SeleniumTestCase.php';

    class WebTest extends PHPUnit_Extensions_SeleniumTestCase
    {
        protected function setUp()
        {
            $this->setBrowser('*firefox');
            $this->setBrowserUrl('http://www.example.com/');
        }

        public function testTitle()
        {
            $this->open('http://www.example.com/');
            $this->assertTitle('Example WWW Page');
        }
    }
    ?>

.. code-block:: bash

    $ phpunit WebTest
    PHPUnit 6.4.0 by Sebastian Bergmann and contributors.

    F

    Time: 9 seconds, Memory: 6.00Mb

    There was 1 failure:

    1) WebTest::testTitle
    Current URL: http://www.iana.org/domains/example/

    Failed asserting that 'IANA — Example domains' matches PCRE pattern "/Example WWW Page/".

    FAILURES!
    Tests: 1, Assertions: 1, Failures: 1.

Contrairement à la classe ``PHPUnit_Framework_TestCase``,
les classes de cas de test qui héritent de ``PHPUnit_Extensions_SeleniumTestCase``
doivent fournir une méthode ``setUp()``. Cette méthode est utilisée
pour configurer la session du serveur Selenium. Voir
:numref:`selenium.seleniumtestcase.tables.seleniumrc-api.setup`
pour la liste des méthodes qui sont disponibles pour cela.

.. rst-class:: table
.. list-table:: API de Selenium Server: configuration
    :name: selenium.seleniumtestcase.tables.seleniumrc-api.setup
    :header-rows: 1

    * - Méthode
      - Signification
    * - ``void setBrowser(string $navigateur)``
      - Règle le navigateur que le serveur Selenium Server doit utiliser.
    * - ``void setBrowserUrl(string $urlNavigateur)``
      - Règle l'URL de base pour les tests.
    * - ``void setHost(string $hote)``
      - Règle le nom d'hôte pour la connexion au serveur Selenium Server.
    * - ``void setPort(int $port)``
      - Règle le port pour la connexion au serveur Selenium Server.
    * - ``void setTimeout(int $delaiExpiration)``
      - Règle le délai d'expiration pour la connexion au serveur Selenium Server server.
    * - ``void setSleep(int $secondes)``
      - Règle le nombre de secondes durant lesquelles le client Selenium Server client doit attendre entre l'envoi de commandes au serveur Selenium Server.

PHPUnit peut facultativement faire une capture d'écran quand un test Selenium échoue. Pour
activer ceci, réglez ``$captureScreenshotOnFailure``,
``$screenshotPath`` et ``$screenshotUrl``
dans votre classe de cas de test comme montré dans
:numref:`selenium.seleniumtestcase.examples.WebTest2.php`.

.. code-block:: php
    :caption: Faire une capture d'écran quand un test échoue
    :name: selenium.seleniumtestcase.examples.WebTest2.php

    <?php
    require_once 'PHPUnit/Extensions/SeleniumTestCase.php';

    class WebTest extends PHPUnit_Extensions_SeleniumTestCase
    {
        protected $captureScreenshotOnFailure = TRUE;
        protected $screenshotPath = '/var/www/localhost/htdocs/screenshots';
        protected $screenshotUrl = 'http://localhost/screenshots';

        protected function setUp()
        {
            $this->setBrowser('*firefox');
            $this->setBrowserUrl('http://www.example.com/');
        }

        public function testTitle()
        {
            $this->open('http://www.example.com/');
            $this->assertTitle('Example WWW Page');
        }
    }
    ?>

.. code-block:: bash

    $ phpunit WebTest
    PHPUnit 6.4.0 by Sebastian Bergmann and contributors.

    F

    Time: 7 seconds, Memory: 6.00Mb

    There was 1 failure:

    1) WebTest::testTitle
    Current URL: http://www.iana.org/domains/example/
    Screenshot: http://localhost/screenshots/334b080f2364b5.21568ee1c7f6742c9.png

    Failed asserting that 'IANA — Example domains' matches PCRE pattern "/Example WWW Page/".

    FAILURES!
    Tests: 1, Assertions: 1, Failures: 1.

Vous pouvez exécuter chaque test en utilisant une série de navigateurs : au lieu
d'utiliser ``setBrowser()`` pour indiquer un seul navigateur, vous déclarez
un tableau ``public static`` nommé ``$browsers``
dans votre classe de cas de test. Chaque élément de ce tableau décrit la configuration
d'un navigateur. Chacun de ces navigateurs peut être hébergé par différents serveurs
Selenium Server.
:numref:`selenium.seleniumtestcase.examples.WebTest3.php` montre
un exemple.

.. code-block:: php
    :caption: Régler la configuration de multiples navigateurs
    :name: selenium.seleniumtestcase.examples.WebTest3.php

    <?php
    require_once 'PHPUnit/Extensions/SeleniumTestCase.php';

    class WebTest extends PHPUnit_Extensions_SeleniumTestCase
    {
        public static $browsers = array(
          array(
            'name'    => 'Firefox sur Linux',
            'browser' => '*firefox',
            'host'    => 'ma.box.linux',
            'port'    => 4444,
            'timeout' => 30000,
          ),
          array(
            'name'    => 'Safari sur MacOS X',
            'browser' => '*safari',
            'host'    => 'ma.box.macosx',
            'port'    => 4444,
            'timeout' => 30000,
          ),
          array(
            'name'    => 'Safari sur Windows XP',
            'browser' => '*custom C:\Program Files\Safari\Safari.exe -url',
            'host'    => 'ma.box.windowsxp',
            'port'    => 4444,
            'timeout' => 30000,
          ),
          array(
            'name'    => 'Internet Explorer sur Windows XP',
            'browser' => '*iexplore',
            'host'    => 'ma.box.windowsxp',
            'port'    => 4444,
            'timeout' => 30000,
          )
        );

        protected function setUp()
        {
            $this->setBrowserUrl('http://www.example.com/');
        }

        public function testTitle()
        {
            $this->open('http://www.example.com/');
            $this->assertTitle('Example Web Page');
        }
    }
    ?>

``PHPUnit_Extensions_SeleniumTestCase`` peut rassembler des informations
de couverture de code pour les tests lancés via Selenium:

#. Copier :file:`PHPUnit/Extensions/SeleniumTestCase/phpunit_coverage.php` dans le répertoire racine de votre serveur web.

#. Dans le fichier de configuration du serveur web :file:`php.ini`, configurez :file:`PHPUnit/Extensions/SeleniumTestCase/prepend.php` et :file:`PHPUnit/Extensions/SeleniumTestCase/append.php` respectivement comme ``auto_prepend_file`` et ``auto_append_file``.

#. Dans votre classe de cas de test qui hérite de ``PHPUnit_Extensions_SeleniumTestCase``, utilisez

   .. code-block:: php

       protected $coverageScriptUrl = 'http://host/phpunit_coverage.php';

   pour configurer l'URL pour le script :file:`phpunit_coverage.php`.

:numref:`selenium.seleniumtestcase.tables.assertions` liste les diverses méthodes
de vérification que ``PHPUnit_Extensions_SeleniumTestCase``
fournit.

.. rst-class:: table
.. list-table:: Assertions
    :name: selenium.seleniumtestcase.tables.assertions
    :header-rows: 1

    * - Assertion
      - Signification
    * - ``void assertElementValueEquals(string $localisateur, string $texte)``
      - Rapporte une erreur si la valeur de l'élément identifié par ``$localisateur`` n'est pas égale au ``$texte`` donné.
    * - ``void assertElementValueNotEquals(string $localisateur, string $texte)``
      - Rapporte une erreur si la valeur de l'élément identifié par ``$localisateur`` est égale au ``$texte`` donné.
    * - ``void assertElementValueContains(string $localisateur, string $texte)``
      - Rapporte une erreur si la valeur de l'élément identifié par ``$localisateur`` ne contient pas le ``$texte`` donné.
    * - ``void assertElementValueNotContains(string $localisateur, string $texte)``
      - Rapporte une erreur si la valeur de l'élément identifié par ``$localisateur`` contient le ``$texte`` donné.
    * - ``void assertElementContainsText(string $localisateur, string $texte)``
      - Rapporte une erreur si l'élément identifié par ``$localisateur`` ne contient pas le ``$texte`` donné.
    * - ``void assertElementNotContainsText(string $localisateur, string $texte)``
      - Rapporte une erreur si l'élément identifié par ``$localisateur`` contient le ``$texte`` donné.
    * - ``void assertSelectHasOption(string $localisateurDeSelect, string $option)``
      - Rapporte une erreur si l'option de liste déroulante donnée n'est pas disponible.
    * - ``void assertSelectNotHasOption(string $localisateurDeSelect, string $option)``
      - Rapporte une erreur si l'option de liste déroulante donnée est disponible.
    * - ``void assertSelected($localisateurDeSelect, $option)``
      - Rapporte une erreur si l'étiquette de liste déroulante donnée n'est pas sélectionnée.
    * - ``void assertNotSelected($localisateurDeSelect, $option)``
      - Rapporte une erreur si l'étiquette de liste déroulante donnée est sélectionnée.
    * - ``void assertIsSelected(string $localisateurDeSelect, string $valeur)``
      - Rapporte une erreur si la valeur donnée n'est pas sélectionnée dans la liste déroulante.
    * - ``void assertIsNotSelected(string $localisateurDeSelect, string $valeur)``
      - Rapporte une erreur si la valeur donnée est sélectionnée dans la liste déroulante.

:numref:`selenium.seleniumtestcase.tables.template-methods` montre
la méthode canevas de ``PHPUnit_Extensions_SeleniumTestCase``:

.. rst-class:: table
.. list-table:: Méthodes canevas
    :name: selenium.seleniumtestcase.tables.template-methods
    :header-rows: 1

    * - Méthode
      - Signification
    * - ``void defaultAssertions()``
      - Surcharge pour exécuter des assertions qui sont partagées par tous les tests d'un cas de test. Cette méthode est appelée après chaque commande qui est envoyée au serveur Selenium Server.

Merci de vous référer à la `documentation des commandes Selenium <http://release.seleniumhq.org/selenium-core/1.0.1/reference.html>`_
pour une référence des commandes disponibles et comment elles sont utilisées.

Les commandes de Selenium 1 sont implémentées dynamiquement via __call. Référez-vous également aux `documents de l'API pour PHPUnit_Extensions_SeleniumTestCase_Driver::__call() <https://github.com/sebastianbergmann/phpunit-selenium/blob/master/PHPUnit/Extensions/SeleniumTestCase/Driver.php#L410>`_ pour une liste de toutes les méthodes gérées du côté PHP, avec les paramètres et le type de retourné quand ils sont disponibles.

En utilisant la méthode ``runSelenese($filename)``, vous pouvez également
lancer un test Selenium à partir de ses spécifications Selenese/HTML. Plus encore,
en utilisant l'attribut statique ``$seleneseDirectory``, vous pouvez
créer automatiquement des objets tests à partir d'un répertoire qui contient
des fichiers Selenese/HTML. Le répertoire indiqué est parcouru récursivement
à la recherche de fichiers ``.htm`` qui sont supposés contenir du Selenese/HTML.
:numref:`selenium.seleniumtestcase.examples.WebTest4.php` montre un
exemple.

.. code-block:: php
    :caption: Utiliser un répertoire de fichiers Selenese/HTML comme tests
    :name: selenium.seleniumtestcase.examples.WebTest4.php

    <?php
    require_once 'PHPUnit/Extensions/SeleniumTestCase.php';

    class SeleneseTests extends PHPUnit_Extensions_SeleniumTestCase
    {
        public static $seleneseDirectory = '/chemin/vers/fichiers';
    }
    ?>

A partir de Selenium 1.1.1, une fonctionnalité expérimentale est incluse permettant à un utilisateur de partager la session entre plusieurs tests. Le seul cas géré est le partage de session entre tous les tests quand un unique navigateur est utilisé.
Appelez ``PHPUnit_Extensions_SeleniumTestCase::shareSession(true)`` dans votre fichier amorce pour activer le partage de session.
La session sera réinitialisée dans le cas où un test échoue (en échec ou incomplet); c'est à la charge de l'utilisateur d'éviter les interactions entre des tests en réinitialisant des cookies ou en se déconnectant de l'application testée (avec une méthode tearDown()).


