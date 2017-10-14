

.. _logging:

==============
Journalisation
==============

PHPUnit peut produire plusieurs types de fichiers de journalisations (logs).

.. _logging.xml:

Résultats de test (XML)
#######################

Le fichier de journalisation XML pour les tests produits par PHPUnit est basé sur celui
qui est utilisé par la tâche
`JUnit
de l'outil Apache Ant <http://ant.apache.org/manual/Tasks/junit.html>`_. L'exemple suivant montre que le fichier
de journalisation XML généré pour les tests dans
``TestTableau``:

.. code-block:: bash

    <?xml version="1.0" encoding="UTF-8"?>
    <testsuites>
      <testsuite name="TestTableau"
                 file="/home/sb/TestTableau.php"
                 tests="2"
                 assertions="2"
                 failures="0"
                 errors="0"
                 time="0.016030">
        <testcase name="testLeNouveauTableauEstVide"
                  class="TestTableau"
                  file="/home/sb/TestTableau.php"
                  line="6"
                  assertions="1"
                  time="0.008044"/>
        <testcase name="testLeTableauContientUnElement"
                  class="TestTableau"
                  file="/home/sb/TestTableau.php"
                  line="15"
                  assertions="1"
                  time="0.007986"/>
      </testsuite>
    </testsuites>

Le fichier de journalisation XML suivant a été généré pour deux tests,
``testEchec`` et ``testErreur``,
à partir d'une classe de cas de test nommée ``EchecErreurTest`` et
montre comment les échecs et les erreurs sont signalés.

.. code-block:: bash

    <?xml version="1.0" encoding="UTF-8"?>
    <testsuites>
      <testsuite name="EchecErreurTest"
                 file="/home/sb/EchecErreurTest.php"
                 tests="2"
                 assertions="1"
                 failures="1"
                 errors="1"
                 time="0.019744">
        <testcase name="testFailure"
                  class="EchecErreurTest"
                  file="/home/sb/EchecErreurTest.php"
                  line="6"
                  assertions="1"
                  time="0.011456">
          <failure type="PHPUnit_Framework_ExpectationFailedException">
    testFailure(EchecErreurTest)
    Failed asserting that &lt;integer:2&gt; matches expected value &lt;integer:1&gt;.

    /home/sb/EchecErreurTest.php:8
    </failure>
        </testcase>
        <testcase name="testError"
                  class="EchecErreurTest"
                  file="/home/sb/EchecErreurTest.php"
                  line="11"
                  assertions="0"
                  time="0.008288">
          <error type="Exception">testError(EchecErreurTest)
    Exception:

    /home/sb/EchecErreurTest.php:13
    </error>
        </testcase>
      </testsuite>
    </testsuites>

.. _logging.tap:

Résultats de test (TAP)
#######################

Le protocole `Test Anything Protocol (TAP) <http://testanything.org/>`_
est une interface Perl simple au format texte entre les modules de test. L'exemple
suivant montre le fichier de journalisation TAP généré pour les tests de
``TableauTest``:

.. code-block:: bash

    TAP version 13
    ok 1 - testNouveauTableauEstVide(TableauTest)
    ok 2 - testTableauContientUnElement(TableauTest)
    1..2

Le fichier de journalisation TAP a été généré pour deux tests,
``testEchec`` et ``testErreur``
à partir d'une classe de cas de test nommée ``EchecErreurTest`` et
montre comme les échecs et les erreurs sont signalés.

.. code-block:: bash

    TAP version 13
    not ok 1 - Failure: testEchec(EchecErreurTest)
      ---
      message: 'Failed asserting that <integer:2> matches expected value <integer:1>.'
      severity: fail
      data:
        got: 2
        expected: 1
      ...
    not ok 2 - Error: testErreur(EchecErreurTest)
    1..2

.. _logging.json:

Résultats de test (JSON)
########################

La notation objet JavaScript (`JavaScript Object Notation ou JSON <http://www.json.org/>`_)
est un format léger d'échange de données. L'exemple suivant montre les messages JSON
générés pour les tests dans ``TableauTest``:

.. code-block:: bash

    {"event":"suiteStart","suite":"TableauTest","tests":2}
    {"event":"test","suite":"TableauTest",
     "test":"testNouveauTableauEstVide(TableauTest)","status":"pass",
     "time":0.000460147858,"trace":[],"message":""}
    {"event":"test","suite":"TableauTest",
     "test":"testTableauContientUnElement(TableauTest)","status":"pass",
     "time":0.000422954559,"trace":[],"message":""}

Les messages JSON suivants ont été générés pour deux tests,
``testEchec`` et ``testErreur``,
d'une classe de cas de test nommée ``EchecErreurTest`` et
monte comment les échecs et les erreurs sont signalées.

.. code-block:: bash

    {"event":"suiteStart","suite":"EchecErreurTest","tests":2}
    {"event":"test","suite":"EchecErreurTest",
     "test":"testEchec(EchecErreurTest)","status":"fail",
     "time":0.0082459449768066,"trace":[],
     "message":"Failed asserting that <integer:2> is equal to <integer:1>."}
    {"event":"test","suite":"EchecErreurTest",
     "test":"testErreur(EchecErreurTest)","status":"error",
     "time":0.0083.90152893066,"trace":[],"message":""}

.. _logging.codecoverage.xml:

Couverture de code (XML)
########################

La journalisation au format XML des informations de couverture de code produite par PHPUnit
est faiblement basé sur celui utilisé par `Clover <http://www.atlassian.com/software/clover/>`_. L'exemple suivant montre le fichier de journalisation XML
généré pour les tests dans ``CompteBancaireTest``:

.. code-block:: bash

    <?xml version="1.0" encoding="UTF-8"?>
    <coverage generated="1184835473" phpunit="4.8.0">
      <project name="CompteBancaireTest" timestamp="1184835473">
        <file name="/home/sb/CompteBancaire.php">
          <class name="CompteBancaireException">
            <metrics methods="0" coveredmethods="0" statements="0"
                     coveredstatements="0" elements="0" coveredelements="0"/>
          </class>
          <class name="CompteBancaire">
            <metrics methods="4" coveredmethods="4" statements="13"
                     coveredstatements="5" elements="17" coveredelements="9"/>
          </class>
          <line num="77" type="method" count="3"/>
          <line num="79" type="stmt" count="3"/>
          <line num="89" type="method" count="2"/>
          <line num="91" type="stmt" count="2"/>
          <line num="92" type="stmt" count="0"/>
          <line num="93" type="stmt" count="0"/>
          <line num="94" type="stmt" count="2"/>
          <line num="96" type="stmt" count="0"/>
          <line num="105" type="method" count="1"/>
          <line num="107" type="stmt" count="1"/>
          <line num="109" type="stmt" count="0"/>
          <line num="119" type="method" count="1"/>
          <line num="121" type="stmt" count="1"/>
          <line num="123" type="stmt" count="0"/>
          <metrics loc="126" ncloc="37" classes="2" methods="4" coveredmethods="4"
                   statements="13" coveredstatements="5" elements="17"
                   coveredelements="9"/>
        </file>
        <metrics files="1" loc="126" ncloc="37" classes="2" methods="4"
                 coveredmethods="4" statements="13" coveredstatements="5"
                 elements="17" coveredelements="9"/>
      </project>
    </coverage>

.. _logging.codecoverage.text:

Couverture de code (TEXTE)
##########################

Sortie de couverture de code humainement lisible pour la ligne de commandes ou un fichier texte.

Le but de ce format de sortie est de fournir un aperçu rapide de couverture
en travaillant sur un petit ensemble de classes. Pour des projets plus grand
cette sortie peut être utile pour obtenir un aperçu rapide de la couverture
des projets ou quand il est utilisé avec la fonctionnalité
``--filter``.
Quand c'est utilisé à partir de la ligne de commande en écrivant sur
``php://stdout``, cela prend en compte le réglage
``--colors``.
Ecrire sur la sortie standard est l'option par défaut quand on utilise la ligne
de commandes.
Par défaut, ceci ne montrera que les fichiers qui ont au moins une ligne couverte.
Ceci peut être modifié via l'option de configuration xml
``showUncoveredFiles``
Voir :ref:`appendixes.configuration.logging`.

.. _code-coverage-analysis.figures.Code_Coverage4.png:

Sortie de couverture de code en couleurs sur la ligne de commandes
==================================================================


