

.. _textui:

=========================================
Le lanceur de tests en ligne de commandes
=========================================

Le lanceur de tests en ligne de commandes de PHPUnit peut être appelé via
la commande :file:`phpunit`. Le code suivant montre comment exécuter
des tests avec le lanceur de tests en ligne de commandes de PHPUnit:

.. code-block:: bash

    $ phpunit ArrayTest
    PHPUnit 6.4.0 by Sebastian Bergmann and contributors.

    ..

    Time: 0 seconds

    OK (2 tests, 2 assertions)

Pour chaque test exécuté, l'outil en ligne de commandes de PHPUnit affiche un
caractère pour indiquer l'avancement:

``.``

    Affiché quand le test a réussi.

``F``

    Affiché quand une assertion échoue lors de l'exécution d'une méthode de test.

``E``

    Affiché quand une erreur survient pendant l'exécution d'une méthode de test.

``S``

    Affiché quand le test a été sauté (voir
    :ref:`incomplete-and-skipped-tests`).

``I``

    Affiché quand le test est marqué comme incomplet ou pas encore
    implémenté (voir :ref:`incomplete-and-skipped-tests`).

PHPUnit différencie les *échecs* et les
*erreurs*. Un échec est une assertion PHPUnit violée
comme un appel en échec de ``assertEquals()``.
Une erreur est une exception inattendue ou une erreur PHP. Parfois
cette distinction s'avère utile car les erreurs tendent à être plus faciles
à corriger que les échecs. Si vous avez une longue liste de problèmes, il vaut
mieux éradiquer d'abord les erreurs pour voir s'il reste encore des échecs
uen fois qu'elles ont été corrigées.

.. _textui.clioptions:

Options de la ligne de commandes
################################

Jetons un oeil aux options du lanceur de tests en ligne de commandes
dans le code suivant :

.. code-block:: bash

    $ phpunit --help
    PHPUnit 6.4.0 by Sebastian Bergmann and contributors.

    Usage: phpunit [options] UnitTest [UnitTest.php]
           phpunit [options] <directory>

    Code Coverage Options:

      --coverage-clover <file>  Generate code coverage report in Clover XML format.
      --coverage-crap4j <file>  Generate code coverage report in Crap4J XML format.
      --coverage-html <dir>     Generate code coverage report in HTML format.
      --coverage-php <file>     Export PHP_CodeCoverage object to file.
      --coverage-text=<file>    Generate code coverage report in text format.
                                Default: Standard output.
      --coverage-xml <dir>      Generate code coverage report in PHPUnit XML format.

    Logging Options:

      --log-junit <file>        Log test execution in JUnit XML format to file.
      --log-tap <file>          Log test execution in TAP format to file.
      --log-json <file>         Log test execution in JSON format.
      --testdox-html <file>     Write agile documentation in HTML format to file.
      --testdox-text <file>     Write agile documentation in Text format to file.

    Test Selection Options:

      --filter <pattern>        Filter which tests to run.
      --testsuite <pattern>     Filter which testsuite to run.
      --group ...               Only runs tests from the specified group(s).
      --exclude-group ...       Exclude tests from the specified group(s).
      --list-groups             List available test groups.
      --test-suffix ...         Only search for test in files with specified
                                suffix(es). Default: Test.php,.phpt

    Test Execution Options:

      --report-useless-tests    Be strict about tests that do not test anything.
      --strict-coverage         Be strict about unintentionally covered code.
      --strict-global-state     Be strict about changes to global state
      --disallow-test-output    Be strict about output during tests.
      --enforce-time-limit      Enforce time limit based on test size.
      --disallow-todo-tests     Disallow @todo-annotated tests.

      --process-isolation       Run each test in a separate PHP process.
      --no-globals-backup       Do not backup and restore $GLOBALS for each test.
      --static-backup           Backup and restore static attributes for each test.

      --colors=<flag>           Use colors in output ("never", "auto" or "always").
      --columns <n>             Number of columns to use for progress output.
      --columns max             Use maximum number of columns for progress output.
      --stderr                  Write to STDERR instead of STDOUT.
      --stop-on-error           Stop execution upon first error.
      --stop-on-failure         Stop execution upon first error or failure.
      --stop-on-risky           Stop execution upon first risky test.
      --stop-on-skipped         Stop execution upon first skipped test.
      --stop-on-incomplete      Stop execution upon first incomplete test.
      -v|--verbose              Output more verbose information.
      --debug                   Display debugging information during test execution.

      --loader <loader>         TestSuiteLoader implementation to use.
      --repeat <times>          Runs the test(s) repeatedly.
      --tap                     Report test execution progress in TAP format.
      --testdox                 Report test execution progress in TestDox format.
      --printer <printer>       TestListener implementation to use.

    Configuration Options:

      --bootstrap <file>        A "bootstrap" PHP file that is run before the tests.
      -c|--configuration <file> Read configuration from XML file.
      --no-configuration        Ignore default configuration file (phpunit.xml).
      --include-path <path(s)>  Prepend PHP's include_path with given path(s).
      -d key[=value]            Sets a php.ini value.

    Miscellaneous Options:

      -h|--help                 Prints this usage information.
      --version                 Prints the version and exits.

``phpunit UnitTest``

    Exécute les tests qui sont fournis par la classe
    ``UnitTest``. Cette classe est supposée être déclarée
    dans le fichier source :file:`UnitTest.php`.

    ``UnitTest`` doit soit être une classe qui hérite
    de ``PHPUnit_Framework_TestCase`` soit une classe qui
    fournit une méthode ``public static suite()`` retournant
    un objet ``PHPUnit_Framework_Test``, par exemple
    une instance de la classe
    ``PHPUnit_Framework_TestSuite``.

``phpunit UnitTest UnitTest.php``

    Exécute les tests qui sont fournis par la classe
    ``UnitTest``. Cette classe est supposée être déclarée
    dans le fichier source indiqué.

``--log-junit``

    Génère un fichier de log au format JUnit XML pour les tests exécutés.
    Voir :ref:`logging` pour plus de détails.

``--log-tap``

    Génère un fichier de log utilisant le format `Test Anything Protocol (Protocol de test universel ou TAP) <http://testanything.org/>`_
    pour les tests exécutés. Voir :ref:`logging` pour plus de détails.

``--log-json``

    Génère un fichier de log en utilisant le format
    `JSON <http://www.json.org/>`_.
    Voir :ref:`logging` pour plus de détails.

``--coverage-html``

    Génère un rapport de couverture de code au format HTML. Voir
    :ref:`code-coverage-analysis` pour plus de détails.

    Merci de noter que cette fonctionnalité n'est seulement disponible que
    lorsque les extensions tokenizer et Xdebug sont installées.

``--coverage-clover``

    Génère un fichier de log au format XML avec les informations de couverture de code
    pour les tests exécutés. Voir :ref:`logging` pour plus de détails.

    Merci de noter que cette fonctionnalité n'est seulement disponible que
    lorsque les extensions tokenizer et Xdebug sont installées.

``--coverage-php``

    Génère un objet sérialisé PHP_CodeCoverage contenant les
    informations de couverture de code.

    Merci de noter que cette fonctionnalité n'est seulement disponible que
    lorsque les extensions tokenizer et Xdebug sont installées.

``--coverage-text``

    Génère un fichier de log ou une sortie écran sur la ligne de commandes
    en format humainement lisible avec les informations de couverture de code
    pour les tests exécutés.
    Voir :ref:`logging` pour plus de détails.

    Merci de noter que cette fonctionnalité n'est seulement disponible que
    lorsque les extensions tokenizer et Xdebug sont installées.

``--testdox-html`` et ``--testdox-text``

    Génère la documentation agile au format HTML ou texte pur pour les
    tests exécutés. Voir :ref:`other-uses-for-tests` pour
    plus de détails.

``--filter``

    Exécute seulement les tests dont le nom correspond au motif donné. Le motif
    peut être soit le nom d'un test particulier, soit une
    `expression rationnelle <http://www.php.net/pcre>`_
    qui correspond à plusieurs noms de tests.

``--group``

    Exécute seulement les tests appartenant à un/des groupe(s) indiqué(s). Un test
    peut être signalé comme appartenant à un groupe en utilisant l'annotation
    ``@group``.

    L'annotation ``@author`` est un alias pour
    ``@group`` permettant de filtrer les tests en se basant
    sur leurs auteurs.

``--exclude-group``

    Exclut les tests d'un/des groupe(s) indiqué(s). Un test peut être signalé
    comme appartenant à un groupe en utilisant l'annotation ``@group``.

``--list-groups``

    Liste les groupes de tests disponibles.

``--loader``

    Indique l'implémentation de ``PHPUnit_Runner_TestSuiteLoader``
    à utiliser.

    Le chargeur standard de suite de tests va chercher les fichiers source
    dans le répertoire de travail actuel et dans chaque répertoire qui
    est indiqué dans la directive de configuration PHP ``include_path``.
    Suivant les conventions de nommage PEAR, le nom d'une classe tel que
    ``Projet_Paquetage_Classe`` est calqué sur le nom de fichier source
    :file:`Projet/Paquetage/Classe.php`.

``--printer``

    Indique l'afficheur de résultats à utiliser. Cette classe d'afficheur doit
    hériter de ``PHPUnit_Util_Printer`` et implémenter l'interface
    ``PHPUnit_Framework_TestListener``.

``--repeat``

    Répéter l'exécution du(des) test(s) le nombre indiqué de fois.

``--tap``

    Rapporte l'avancement des tests en utilisant le `Test Anything Protocol (TAP) <http://testanything.org/>`_.
    Voir :ref:`logging` pour plus de détails.

``--testdox``

    Rapporte l'avancement des tests sous forme de documentation agile. Voir
    :ref:`other-uses-for-tests` pour plus de détails.

``--colors``

    Utilise des couleurs pour l'affichage.

``--stderr``

    Utilise optionnellement ``STDERR`` au lieu de
    ``STDOUT`` pour l'affichage.

``--stop-on-error``

    Arrête l'exécution à la première erreur.

``--stop-on-failure``

    Arrête l'exécution à la première erreur ou au premier échec.

``--stop-on-skipped``

    Arrête l'exécution au premier test sauté.

``--stop-on-incomplete``

    Arrête l'exécution au premier test incomplet.

``--verbose``

    Affiche des informations plus détaillées, par exemple le nom des tests
    qui sont incomplets ou qui ont été sautés.

``--process-isolation``

    Exécute chaque test dans un processus PHP distinct.

``--no-globals-backup``

    Ne pas sauvegarder et restaurer $GLOBALS. Voir :ref:`fixtures.global-state`
    pour plus de détails.

``--static-backup``

    Sauvegarde et restaure les attributs statiques des classes définies par l'utilisateur.
    Voir :ref:`fixtures.global-state` pour plus de détails.

``--bootstrap``

    Un fichier PHP "amorce" ("bootstrap") est exécuté avant les tests.

``--configuration``, ``-c``

    Lit la configuration dans un fichier XML.
    Voir :ref:`appendixes.configuration` pour plus de détails.

    Si :file:`phpunit.xml` ou
    :file:`phpunit.xml.dist` (dans cet ordre) existent dans le
    répertoire de travail actuel et que ``--configuration`` n'est
    *pas* utilisé, la configuration sera automatiquement
    lue dans ce fichier.

``--no-configuration``

    Ignorer :file:`phpunit.xml` et
    :file:`phpunit.xml.dist` du répertoire de travail actuel.

``--include-path``

    Préfixe l'``include_path`` PHP avec le(s) chemin(s) donné(s).

``-d``

    Fixe la valeur des options de configuration PHP données.

``--debug``

    Affiche des informations de débogage telles que le nom d'un test quand
    son exécution démarre.


