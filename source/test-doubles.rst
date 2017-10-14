

.. _test-doubles:

================
Doublure de test
================

Gerard Meszaros introduit le concept de doublure de test dans
:ref:`Meszaros2007` comme ceci:

    *Gerard Meszaros*:

    Parfois il est juste parfaitement difficile de tester un système en cours de test
    (SCT) parce qu'il dépend d'autres composants qui ne peuvent pas
    être utilisés dans l'environnement de test. Ceci peut provenir du fait
    qu'ils ne sont pas disponibles, qu'ils ne retournent pas les résultats
    nécessaires pour les tests ou parce que les exécuter pourrait avoir
    des effets de bord indésirables. Dans d'autres cas, notre stratégie de test
    nécessite que nous ayons plus de contrôle ou de visibilité sur le comportement
    interne du SCT.

    Quand nous écrivons un test dans lequel nous ne pouvons pas (ou ne voulons pas)
    utiliser un composant réel dont on dépend (depended-on component ou DOC), nous
    pouvons le remplacer avec une doublure de test. La doublure de test ne se comporte pas exactement
    comme un vrai DOC; elle a simplement à fournir la même API que le composant réel de telle
    sorte que le système testé pense qu'il s'agit du vrai !

La méthode ``getMock($nomClasse)`` fournit par PHPUnit peut être
utilisée dans un test pour générer automatiquement un objet qui peut agir comme une
doublure de test pour une classe originelle indiquée. Cette doublure de test peut être
utilisée dans tous les contextes où la classe originelle est attendue.

Par défaut, toutes les méthodes de la classe originelle sont remplacées
par une implémentation fictive qui se contente de retourner
``NULL`` (sans appeler la méthode originelle).
En utilisant la méthode ``will($this->returnValue())``
par exemple, vous pouvez configurer ces implémentations fictives pour
retourner une valeur donnée quand elles sont appelées.

.. admonition:: Limitations

   Merci de noter que les méthodes ``final``, ``private``
   et ``static`` ne peuvent pas être remplacées par un bouchon (stub) ou un simulacre (mock). Elles seront
   ignorées par la fonction de doublure de test de PHPUnit et conserveront leur comportement
   initial.

.. _test-doubles.stubs:

Bouchons
########

La pratique consistant à remplacer un objet par une doublure de test qui
retourne (de façon facultative) des valeurs de retour configurées est
appelée *bouchonnage*. Vous pouvez utiliser un *bouchon* pour
"remplacer un composant réel dont dépend le système testé de telle façon que
le test possède un point de contrôle sur les entrées indirectes dans le SCT. Ceci
permet au test de forcer le SCT à utiliser des chemins qu'il n'aurait pas
emprunté autrement".

:numref:`test-doubles.stubs.examples.StubTest.php` montre comment
la méthode de bouchonnage appelle et configure des valeurs de retour. Nous utilisons
d'abord la méthode ``getMock()`` qui est fournie par la classe
``PHPUnit_Framework_TestCase`` pour configurer un objet bouchon
qui ressemble à un objet de ``UneClasse``
(:numref:`test-doubles.stubs.examples.SomeClass.php`). Ensuite nous
utilisons `l'interface souple <http://martinfowler.com/bliki/FluentInterface.html>`_
que PHPUnit fournit pour indiquer le comportement de ce bouchon. En essence,
cela signifie que vous n'avez pas besoin de créer plusieurs objets temporaires
et les relier ensemble ensuite. Au lieu de cela, vous chaînez les appels de méthode
comme montré dans l'exemple. Ceci amène à un code plus lisible et "souple".

.. code-block:: php
    :caption: La classe que nous voulons bouchonner
    :name: test-doubles.stubs.examples.SomeClass.php

    <?php
    class UneClasse
    {
        public function faireQuelquechose()
        {
            // Faire quelque chose.
        }
    }
    ?>

.. code-block:: php
    :caption: Bouchonner un appel de méthode pour retourner une valeur fixée
    :name: test-doubles.stubs.examples.StubTest.php

    <?php
    require_once 'UneClasse.php';

    class BouchonTest extends PHPUnit_Framework_TestCase
    {
        public function testBouchon()
        {
            // Créer un bouchon pour la classe UneClasse.
            $bouchon = $this->getMock('UneClasse');

            // Configurer le bouchon.
            $bouchon->expects($this->any())
                 ->method('faireQuelquechose')
                 ->will($this->returnValue('foo'));

            // Appeler $bouchon->faireQuelquechose() va maintenant retourner
            // 'foo'.
            $this->assertEquals('foo', $bouchon->faireQuelquechose());
        }
    }
    ?>

"Derrière la scène", PHPUnit génère automatiquement une nouvelle classe qui
implémente le comportement souhaité quand la méthode ``getMock()``
est utilisée. La classe doublure de test peut être configurée via des
paramètres optionnels de la méthode ``getMock()``.

-

  Par défaut, toutes les méthodes d'une classe données sont remplacées par une doublure de test qui retourne simplement ``NULL`` à moins qu'une valeur de retour ne soit configurée en utilisant ``will($this->returnValue())``, par exemple.

-

  Quand le deuxième paramètre (facultatif) est fourni, seules les méthodes dont les noms sont dans le tableau sont remplacées par une doublure de test configurable. Le comportement des autres méthodes n'est pas modifié.

-

  Le troisième paramètre (facultatif) peut contenir un tableau de paramètre qui est passé dans le constructeur de la classe originelle (qui n'est pas remplacé par une implémentation fictive par défaut).

-

  Le quatrième paramètre (facultatif) peut être utilisé pour indiquer un nom de classe pour la classe de doublure de test générée.

-

  Le cinquième paramètre (facultatif) peut être utilisée pour désactiver l'appel du constructeur de la classe originelle.

-

  Le sixième paramètre (facultatif) peut être utilisé pour désactiver l'appel au constructeur du clone de la classe originelle.

-

  Le septième paramètre (facultatif) peut être utilisé pour désactiver ``__autoload()`` lors de la génération de la classe de doublure de test.

Alternativement, l'API Mock Builder peut être utilisé pour configurer la classe
de doublure de test générée.
:numref:`test-doubles.stubs.examples.StubTest2.php`
montre un exemple. Ici, il y a une liste de méthodes qui peuvent être utilisées
avec l'interface de Mock Builder:

-

  ``setMethods(array $methodes)`` peut être appelée sur l'objet Mock Builder pour indiquer les méthodes qui doivent être remplacées par une doublure de test configurable. Le comportement des autres méthodes n'est pas modifié.

-

  ``setConstructorArgs(array $parametres)`` peut être appelé pour fournir un paramètre tableau qui est passé au constructeur de la classe originelle (qui n'est pas remplacé par une implémentation fictive par défaut).

-

  ``setMockClassName($nom)`` peut être utilisée pour indiquer un nom de classe pour la classe de doublure de test générée.

-

  ``disableOriginalConstructor()`` peut être utilisé pour désactiver l'appel au constructeur de la classe originelle.

-

  ``disableOriginalClone()`` peut être utilisé pour désactiver l'appel au constructeur clone de la classe originelle.

-

  ``disableAutoload()`` peut être utilisée pour désactiver ``__autoload()`` lors de la génération de la classe de doublure de test.

.. code-block:: php
    :caption: Utiliser l'API Mock Builder pour configurer la classe de doublure de test générée.
    :name: test-doubles.stubs.examples.StubTest2.php

    <?php
    require_once 'UneClasse.php';

    class BouchonTest extends PHPUnit_Framework_TestCase
    {
        public function testBouchon()
        {
            // Créer un bouchon pour la classe UneClasse.
            $bouchon = $this->getMockBuilder('UneClasse')
                         ->disableOriginalConstructor()
                         ->getMock();

            // Configure le bouchon.
            $bouchon->expects($this->any())
                 ->method('faireQuelquechose')
                 ->will($this->returnValue('foo'));

            // Appeler $bouchon->faireQuelquechose() retournera maintenant
            // 'foo'.
            $this->assertEquals('foo', $bouchon->faireQuelquechose());
        }
    }
    ?>

Parfois vous voulez renvoyer l'un des paramètres d'un appel de méthode
(non modifié) comme résultat d'un appel méthode bouchon.
:numref:`test-doubles.stubs.examples.StubTest3.php` montre comment vous
pouvez obtenir ceci en utilisant ``returnArgument()`` à la place de
``returnValue()``.

.. code-block:: php
    :caption: Bouchonner un appel de méthode pour renvoyer un des paramètres
    :name: test-doubles.stubs.examples.StubTest3.php

    <?php
    require_once 'UneClasse.php';

    class BouchonTest extends PHPUnit_Framework_TestCase
    {
        public function testReturnArgumentBouchon()
        {
            // Créer un bouchon pour la classe UneClasse.
            $bouchon = $this->getMock('UneClasse');

            // Configurer le bouchon.
            $bouchon->expects($this->any())
                 ->method('faireQuelquechose')
                 ->will($this->returnArgument(0));

            // $bouchon->faireQuelquechose('foo') retourne 'foo'
            $this->assertEquals('foo', $bouchon->faireQuelquechose('foo'));

            // $bouchon->faireQuelquechose('bar') retourne 'bar'
            $this->assertEquals('bar', $bouchon->faireQuelquechose('bar'));
        }
    }
    ?>

Quand on teste interface souple, il est parfois utile que la méthode bouchon
retourne une référence à l'objet bouchon.
:numref:`test-doubles.stubs.examples.StubTest4.php` illustre comment vous
pouvez utiliser ``returnSelf()`` pour accomplir cela.

.. code-block:: php
    :caption: Bouchonner un appel de méthode pour renvoyer une référence de l'objet bouchon.
    :name: test-doubles.stubs.examples.StubTest4.php

    <?php
    require_once 'UneClasse.php';

    class BouchonTest extends PHPUnit_Framework_TestCase
    {
        public function testReturnSelf()
        {
            // Créer un bouchon pour la classe UneClasse.
            $bouchon = $this->getMock('UneClasse');

            // Configurer le bouchon.
            $bouchon->expects($this->any())
                 ->method('faireQuelquechose')
                 ->will($this->returnSelf());

            // $bouchon->faireQuelquechose() retourne $bouchon
            $this->assertSame($bouchon, $bouchon->faireQuelquechose());
        }
    }
    ?>

Parfois, une méthode bouchon doit retourner différentes valeurs selon
une liste prédéfinie d'arguments. Vous pouvez utiliser
``returnValueMap()`` pour créer un mappage qui associe des
paramètres aux valeurs de retour correspondantes. Voir
:numref:`test-doubles.stubs.examples.StubTest5.php` pour
un exemple.

.. code-block:: php
    :caption: Bouchonner un appel de méthode pour retourner la valeur à partir d'un mappage
    :name: test-doubles.stubs.examples.StubTest5.php

    <?php
    require_once 'UneClasse.php';

    class BouchonTest extends PHPUnit_Framework_TestCase
    {
        public function testReturnValueMapBouchon()
        {
            // Créer un bouchon pour la classe UneClasse.
            $bouchon = $this->getMock('UneClasse');

            // Créer un mappage des arguments
            // et des valeurs de retour.
            $map = array(
              array('a', 'b', 'c', 'd'),
              array('e', 'f', 'g', 'h')
            );

            // Configurer le bouchon.
            $bouchon->expects($this->any())
                 ->method('faireQuelquechose')
                 ->will($this->returnValueMap($map));

            // $bouchon->faireQuelquechose() retourne
            // différentes valeurs selon les paramètres
            // fournis.
            $this->assertEquals('d', $bouchon->faireQuelquechose('a', 'b', 'c'));
            $this->assertEquals('h', $bouchon->faireQuelquechose('e', 'f', 'g'));
        }
    }
    ?>

Quand l'appel méthode bouchonné doit retourner une valeur calculée au lieu
d'une valeur fixée (voir ``returnValue()``) ou un paramètre
(non modifié) (voir ``returnArgument()``), vous pouvez utiliser
``returnCallback()`` pour que la méthode retourne le résultat
d'une fonction ou méthode de rappel. Voir
:numref:`test-doubles.stubs.examples.StubTest6.php` pour un exemple.

.. code-block:: php
    :caption: Bouchonner un appel de méthode pour retourner une valeur à partir d'un rappel
    :name: test-doubles.stubs.examples.StubTest6.php

    <?php
    require_once 'UneClasse.php';

    class BouchonTest extends PHPUnit_Framework_TestCase
    {
        public function testReturnCallbackBouchon()
        {
            // Créer un bouchon pour la classe UneClasse.
            $bouchon = $this->getMock('UneClasse');

            // Configurer le bouchon.
            $bouchon->expects($this->any())
                 ->method('faireQuelquechose')
                 ->will($this->returnCallback('str_rot13'));

            // $bouchon->faireQuelquechose($argument) retourne str_rot13($argument)
            $this->assertEquals('fbzrguvat', $bouchon->faireQuelquechose('quelqueChose'));
        }
    }
    ?>

Une alternative plus simple pour configurer une méthode de rappel peut
consister à indiquer une liste de valeurs désirées. Vous pouvez faire
ceci avec la méthode ``onConsecutiveCalls()``. Voir
:numref:`test-doubles.stubs.examples.StubTest7.php` pour
un exemple.

.. code-block:: php
    :caption: Bouchonner un appel de méthode pour retourner une liste de valeurs dans l'ordre indiqué
    :name: test-doubles.stubs.examples.StubTest7.php

    <?php
    require_once 'UneClasse.php';

    class BouchonTest extends PHPUnit_Framework_TestCase
    {
        public function testOnConsecutiveCallsBouchon()
        {
            // Créer un bouchon pour la classe UneClasse.
            $bouchon = $this->getMock('UneClasse');

            // Configurer le bouchon.
            $bouchon->expects($this->any())
                 ->method('faireQuelquechose')
                 ->will($this->onConsecutiveCalls(2, 3, 5, 7));

            // $bouchon->faireQuelquechose() retourne une valeur différente à chaque fois
            $this->assertEquals(2, $bouchon->faireQuelquechose());
            $this->assertEquals(3, $bouchon->faireQuelquechose());
            $this->assertEquals(5, $bouchon->faireQuelquechose());
        }
    }
    ?>

Au lieu de retourner une valeur, une méthode bouchon peut également lever
une exception. :numref:`test-doubles.stubs.examples.StubTest8.php`
montre comme utiliser ``throwException()`` pour faire cela.

.. code-block:: php
    :caption: Bouchonner un appel de méthode pour lever une exception
    :name: test-doubles.stubs.examples.StubTest8.php

    <?php
    require_once 'UneClasse.php';

    class BouchonTest extends PHPUnit_Framework_TestCase
    {
        public function testThrowExceptionBouchon()
        {
            // Créer un bouchon pour la classe UneClasse.
            $bouchon = $this->getMock('UneClasse');

            // Configurer le bouchon.
            $bouchon->expects($this->any())
                 ->method('faireQuelquechose')
                 ->will($this->throwException(new Exception));

            // $bouchon->faireQuelquechose() lance l'Exception
            $bouchon->faireQuelquechose();
        }
    }
    ?>

Alternativement, vous pouvez écrire le bouchon vous-même et améliorer
votre conception ce-faisant. Des ressources largement utilisées sont
accédées via une unique façade, de telle sorte que vous pouvez facilement
remplacer la ressource avec le bouchon. Par exemple, au lieu d'avoir
des appels directs à la base de données éparpillés dans tout le code,
vous avez un unique objet ``Database``, une implémentation de
l'interface ``IDatabase``. Ensuite, vous pouvez créer
une implémentation bouchon de ``IDatabase`` et l'utiliser pour
vos tests. Vous pouvez même créer une option pour lancer les tests dans la
base de données bouchon ou la base de données réelle, de telle sorte que vous
pouvez utiliser vos tests à la fois pour tester localement pendant le développement
et en intégration avec la vraie base de données.

Les fonctionnalités qui nécessitent d'être bouchonnées tendent à se regrouper
dans le même objet, améliorant la cohésion. En représentant la fonctionnalité
avec une unique interface cohérente, vous réduisez le couplage avec le reste
du système.

.. _test-doubles.mock-objects:

Objets simulacres (Mock Objects)
################################

La pratique consistant à remplacer un objet avec une doublure de test
qui vérifie des attentes, par exemple en faisant l'assertion qu'une méthode
a été appelée, est appelée *simulacre*.

Vous pouvez utiliser un *objet simulacre* "comme un point d'observation
qui est utilisé pour vérifier les sorties indirectes du système quand il est
testé. Typiquement, le simulacre inclut également la fonctionnalité
d'un bouchon de test, en ce sens qu'il doit retourner les valeurs du système
testé s'il n'a pas déjà fait échouer les tests mais l'accent est mis sur la
vérification des sorties indirectes. Ainsi, un simulacre est un beaucoup plus
qu'un simple bouchon avec des assertions; il est utilisé d'une manière
fondamentalement différente".

Voici un exemple: supposons que vous voulez tester que la méthode correcte,
``update()`` dans notre exemple, est appelée d'un objet qui observe un autre objet.
:numref:`test-doubles.mock-objects.examples.SUT.php`
illustre le code pour les classes ``Sujet`` et ``Observateur``
qui sont une partie du système testé (SUT).

.. code-block:: php
    :caption: Les classes Sujet et Observateur qui sont une partie du système testé
    :name: test-doubles.mock-objects.examples.SUT.php

    <?php
    class Sujet
    {
        protected $observateurs = array();

        public function attache(Observateur $observateur)
        {
            $this->observateurs[] = $observateur;
        }

        public function faireQuelquechose()
        {
            // Faire quelque chose.
            // ...

            // Avertir les observateurs que nous faisons quelque chose.
            $this->notify('quelque chose');
        }

        public function faireQuelquechoseMal()
        {
            foreach ($this->observateurs as $observateur) {
                $observateur->reportError(42, 'Quelque chose de mal est arrivé', $this);
            }
        }

        protected function notify($paramètre)
        {
            foreach ($this->observateurs as $observateur) {
                $observateur->update($paramètre);
            }
        }

        // Autres méthodes.
    }

    class Observateur
    {
        public function update($paramètre)
        {
            // Faire quelque chose.
        }

        public function reportError($codeErreur, $messageErreur, Sujet $sujet)
        {
            // Faire quelque chose
        }

        // Autres méthodes.
    }
    ?>

:numref:`test-doubles.mock-objects.examples.SubjectTest.php`
illustre comment utiliser un simulacre pour tester l'interaction entre
les objets ``Sujet`` et ``Observateur``.

Nous utilisons d'abord la méthode ``getMock()`` qui est fournie par
la classe ``PHPUnit_Framework_TestCase`` pour configurer un simulacre
pour l'``Observateur``. Puisque nous donnons un tableau comme second
paramètre (facultatif) pour la méthode ``getMock()``,
seule la méthode ``update()`` de la classe ``Observateur`` est
remplacée par une implémentation d'un simulacre.

.. code-block:: php
    :caption: Tester qu'une méthode est appelée une fois et avec un paramètre indiqué
    :name: test-doubles.mock-objects.examples.SubjectTest.php

    <?php

    require_once 'Sujet.php';

    class SujetTest extends PHPUnit_Framework_TestCase
    {
        public function testLesObservateursSontMisAJour()
        {
            // Créer un simulacre pour la classe Observateur,
            // ne touchant que la méthode update().
            $observateur = $this->getMock('Observateur', array('update'));

            // Configurer l'attente de la méthode update()
            // d'être appelée une seule fois et avec la chaîne 'quelquechose'
            // comme paramètre.
            $observateur->expects($this->once())
                     ->method('update')
                     ->with($this->equalTo('quelque chose'));

            // Créer un objet Sujet et y attacher l'objet Observateur
            // simulé
            $sujet = new Sujet;
            $sujet->attache($observateur);

            // Appeler la méthode faireQuelquechose() sur l'objet $sujet
            // que nous attendons voir appeler la méthode update() de l'objet
            // simulé Observateur avec la chaîne 'quelqueChose'.
            $sujet->faireQuelquechose();
        }
    }
    ?>

La méthode ``with()`` peut prendre n'importe quel
nombre de paramètres, correspondant au nombre de paramètres des méthodes
étant simulées. Vous pouvez indiquer des contraintes plus avancées
sur les paramètres de méthode qu'une simple correspondance.

.. code-block:: php
    :caption: Tester qu'une méthode est appelée avec un nombre de paramètres contraints de différentes manières
    :name: test-doubles.mock-objects.examples.MultiParameterTest.php

    <?php
    class SubjectTest extends PHPUnit_Framework_TestCase
    {
        public function testRapportErreur()
        {
            // Créer un simulacre pour la classe Observateur, en simulant
            // la méthode rapportErreur()
            $observateur = $this->getMock('Observateur', array('rapportErreur'));

            $observateur->expects($this->once())
                     ->method('rapportErreur')
                     ->with($this->greaterThan(0),
                            $this->stringContains('Quelquechose'),
                            $this->anything());

            $sujet = new Subject;
            $sujet->attach($observateur);

            // La méthode faireQuelquechoseDeMal doit rapporter une erreur à l'observateur
            // via la méthode rapportErreur()
            $sujet->faireQuelquechoseDeMal();
        }
    }
    ?>

:ref:`writing-tests-for-phpunit.assertions.assertThat.tables.constraints`
montre les contraintes qui peuvent être appliquées aux paramètres de méthode et
:numref:`test-doubles.mock-objects.tables.matchers`
montre les matchers qui sont disponibles pour indiquer le nombre d'
invocations.

.. rst-class:: table
.. list-table:: Matchers
    :name: test-doubles.mock-objects.tables.matchers
    :header-rows: 1

    * - Matcher
      - Signification
    * - ``PHPUnit_Framework_MockObject_Matcher_AnyInvokedCount any()``
      - Retourne un matcher qui correspond quand la méthode pour laquelle il est évalué est exécutée zéro ou davantage de fois.
    * - ``PHPUnit_Framework_MockObject_Matcher_InvokedCount never()``
      - Retourne un matcher qui correspond quand la méthode pour laquelle il est évalué n'est jamais exécutée.
    * - ``PHPUnit_Framework_MockObject_Matcher_InvokedAtLeastOnce atLeastOnce()``
      - Retourne un matcher qui correspond quand la méthode pour laquelle il est évalué est exécutée au moins une fois.
    * - ``PHPUnit_Framework_MockObject_Matcher_InvokedCount once()``
      - Retourne un matcher qui correspond quand la méthode pour laquelle il est évalué est exécutée exactement une fois.
    * - ``PHPUnit_Framework_MockObject_Matcher_InvokedCount exactly(int $nombre)``
      - Retourne un matcher qui correspond quand la méthode pour laquelle il est évalué est exécutée exactement ``$nombre`` fois.
    * - ``PHPUnit_Framework_MockObject_Matcher_InvokedAtIndex at(int $index)``
      - Retourne un matcher qui correspond quand la méthode pour laquelle il est évalué est invoquée pour l'``$index`` spécifié.

La méthode ``getMockForAbstractClass()`` retourne un simulacre
pour une classe abstraite. Toutes les méthodes abstraites d'une classe simulacre
donnée sont simulées. Ceci permet de tester les méthodes concrètes d'une classe
abstraite.

.. code-block:: php
    :caption: Tester les méthodes concrêtes d'une classe abstraite
    :name: test-doubles.mock-objects.examples.AbstractClassTest.php

    <?php
    abstract class ClasseAbstraite
    {
        public function methodeConcrete()
        {
            return $this->methodeAbstraite();
        }

        public abstract function methodeAbstraite();
    }

    class ClasseAbstraiteTest extends PHPUnit_Framework_TestCase
    {
        public function testConcreteMethod()
        {
            $stub = $this->getMockForAbstractClass('ClasseAbstraite');
            $stub->expects($this->any())
                 ->method('methodeAbstraite')
                 ->will($this->returnValue(TRUE));

            $this->assertTrue($stub->methodeConcrete());
        }
    }
    ?>

.. _test-doubles.prophecy:

Prophecy
########

`Prophecy <https://github.com/phpspec/prophecy>`_ est un
"framework de librairie de mock pour object PHP fortement arrêtée dans
ses options mais tout du moins très puissant et flexible. Créé en premier
lieu pour satisfaire les besoins de phpspec2, il est assez flexible pour
être utilisé dans n'importe quel framework de test, avec très peu
d'efforts".

PHPUnit supporte nativement l'utilisation de Prophecy pour créer des
doublures depuis la version 4.5. :numref:`test-doubles.prophecy.examples.SubjectTest.php`
montre comment le même test peut écrit dans :numref:`test-doubles.mock-objects.examples.SubjectTest.php`
en utilisant la philosophy des prophéties et des révélations:

.. code-block:: php
    :caption: Tester qu'une méthode est appelée une fois avec un argument spécifique
    :name: test-doubles.prophecy.examples.SubjectTest.php

    <?php
    class SubjectTest extends PHPUnit_Framework_TestCase
    {
        public function testObserversAreUpdated()
        {
            $subject = new Subject('My subject');

            // Créer une prohétie pour une classe Observer.
            $observer = $this->prophesize('Observer');

            // Configurer le comportement attendu pour la méthode update()
            // afin qu'elle soit appellée qu'une fois, avec la string 'something'
            // comme paramètre.
            $observer->update('something')->shouldBeCalled();

            // Révéler la prophetie et attacher le mock à l'object Subject.
            $subject->attach($observer->reveal());

            // Appeler la méthode doSomething() sur l'object $subject
            // qui s'attend à appeler sur le mock d'objet Observer
            // la méthod update() avec la string 'something'.
            $subject->doSomething();
        }
    }
    ?>

Référez-vous s'il vous plait à la `documentation <https://github.com/phpspec/prophecy#how-to-use-it>`_
pour Prophecy pour plus de détails concernant la création, la configuration,
et l'utilisation de stubs (doublures), spies (espions) et mocks (bouchons)
en utilisation cette alternative de framework de doublure de test.

.. _test-doubles.stubbing-and-mocking-web-services:

Bouchon et simulacre pour Web Services
######################################

Quand votre application interagit avec un web service, vous voulez le
tester sans vraiment interagir avec le web service. Pour rendre facile
la création de bouchon ou de simulacre de web services,
``getMockFromWsdl()`` peut être utilisée de la même façon que
``getMock()`` (voir plus haut). La seule différence est que
``getMockFromWsdl()`` retourne un bouchon ou un simulacre
basé sur la description en WSDL d'un web service tandis que ``getMock()``
retourne un bouchon ou un simulacre basé sur une classe ou une interface PHP.

:numref:`test-doubles.stubbing-and-mocking-web-services.examples.GoogleTest.php`
montre comment ``getMockFromWsdl()`` peut être utilisé pour faire un bouchon,
par exemple, d'un web service décrit dans :file:`GoogleSearch.wsdl`.

.. code-block:: php
    :caption: Bouchonner un web service
    :name: test-doubles.stubbing-and-mocking-web-services.examples.GoogleTest.php

    <?php
    class GoogleTest extends PHPUnit_Framework_TestCase
    {
        public function testSearch()
        {
            $googleSearch = $this->getMockFromWsdl(
              'GoogleSearch.wsdl', 'GoogleSearch'
            );

            $directoryCategory = new stdClass;
            $directoryCategory->fullViewableName = '';
            $directoryCategory->specialEncoding = '';

            $element = new stdClass;
            $element->summary = '';
            $element->URL = 'http://www.phpunit.de/';
            $element->snippet = '...';
            $element->title = '<b>PHPUnit</b>';
            $element->cachedSize = '11k';
            $element->relatedInformationPresent = TRUE;
            $element->hostName = 'www.phpunit.de';
            $element->directoryCategory = $directoryCategory;
            $element->directoryTitle = '';

            $result = new stdClass;
            $result->documentFiltering = FALSE;
            $result->searchComments = '';
            $result->estimatedTotalResultsCount = 3.9000;
            $result->estimateIsExact = FALSE;
            $result->resultElements = array($element);
            $result->searchQuery = 'PHPUnit';
            $result->startIndex = 1;
            $result->endIndex = 1;
            $result->searchTips = '';
            $result->directoryCategories = array();
            $result->searchTime = 0.248822;

            $googleSearch->expects($this->any())
                         ->method('doGoogleSearch')
                         ->will($this->returnValue($result));

            /**
             * $googleSearch->doGoogleSearch() va maintenant retourner un result bouchon et
             * la méthode doGoogleSearch() du web service ne sera pas invoquée.
             */
            $this->assertEquals(
              $result,
              $googleSearch->doGoogleSearch(
                '00000000000000000000000000000000',
                'PHPUnit',
                0,
                1,
                FALSE,
                '',
                FALSE,
                '',
                '',
                ''
              )
            );
        }
    }
    ?>

.. _test-doubles.mocking-the-filesystem:

Simuler le système de fichiers
##############################

`vfsStream <https://github.com/mikey179/vfsStream>`_
est un `encapsuleur de flux <http://www.php.net/streams>`_ pour un
`système de fichiers
virtuel <http://en.wikipedia.org/wiki/Virtual_file_system>`_ qui peut s'avérer utile dans des tests unitaires pour simuler
le vrai système de fichiers.

Pour installer vfsStream, le canal PEAR
(pear.bovigo.org) qui est utilisé pour
sa distribution doit être enregistré dans l'environnement local PEAR:

.. code-block:: bash

    $ pear channel-discover pear.bovigo.org

Ceci ne doit être fait qu'une seule fois. Maintenant, l'installeur PEAR
peut être utilisé pour installer vfsStream.

.. code-block:: bash

    $ pear install bovigo/vfsStream-beta

:numref:`test-doubles.mocking-the-filesystem.examples.Example.php`
montre une classe qui interagit avec le système de fichiers.

.. code-block:: php
    :caption: Une classe qui interagit avec le système de fichiers
    :name: test-doubles.mocking-the-filesystem.examples.Example.php

    <?php
    class Exemple
    {
        protected $id;
        protected $repertoire;

        public function __construct($id)
        {
            $this->id = $id;
        }

        public function setRepertoire($repertoire)
        {
            $this->repertoire = $repertoire . DIRECTORY_SEPARATOR . $this->id;

            if (!file_exists($this->repertoire)) {
                mkdir($this->repertoire, 0700, TRUE);
            }
        }
    }?>

Sans un système de fichiers virtuel tel que vfsStream, nous ne pouvons
pas tester la méthode ``setDirectory()`` en isolation des influences
extérieures (voir :numref:`test-doubles.mocking-the-filesystem.examples.ExampleTest.php`).

.. code-block:: php
    :caption: Tester une classe qui interagoit avec le système de fichiers
    :name: test-doubles.mocking-the-filesystem.examples.ExampleTest.php

    <?php
    require_once 'Exemple.php';

    class ExempleTest extends PHPUnit_Framework_TestCase
    {
        protected function setUp()
        {
            if (file_exists(dirname(__FILE__) . '/id')) {
                rmdir(dirname(__FILE__) . '/id');
            }
        }

        public function testReprtoireEstCree()
        {
            $example = new Exemple('id');
            $this->assertFalse(file_exists(dirname(__FILE__) . '/id'));

            $example->setRepertoire(dirname(__FILE__));
            $this->assertTrue(file_exists(dirname(__FILE__) . '/id'));
        }

        protected function tearDown()
        {
            if (file_exists(dirname(__FILE__) . '/id')) {
                rmdir(dirname(__FILE__) . '/id');
            }
        }
    }
    ?>

L'approche précédente possède plusieurs inconvénients :

-

  Comme avec les ressources externes, il peut y a voir des problèmes intermittents avec le système de fichiers. Ceci rend les tests qui interagissent avec lui peu fiables.

-

  Dans les méthodes ``setUp()`` et ``tearDown()``, nous avons à nous assurer que le répertoire n'existe pas avant et après le test.

-

  Si l'exécution du test s'achève avant que la méthode ``tearDown()`` n'ait été appelée, le répertoire va rester dans le système de fichiers.

:numref:`test-doubles.mocking-the-filesystem.examples.ExampleTest2.php`
montre comment vfsStream peut être utilisé pour simuler le système de fichiers dans un test
pour une classe qui interagit avec le système de fichiers.

.. code-block:: php
    :caption: Simuler le système de fichiers dans un test pour une classe qui interagit avec le système de fichiers
    :name: test-doubles.mocking-the-filesystem.examples.ExampleTest2.php

    <?php
    require_once 'vfsStream/vfsStream.php';
    require_once 'Exemple.php';

    class ExempleTest extends PHPUnit_Framework_TestCase
    {
        public function setUp()
        {
            vfsStreamWrapper::register();
            vfsStreamWrapper::setRoot(new vfsStreamDirectory('exempleRepertoire'));
        }

        public function testRepertoireEstCree()
        {
            $exemple = new Exemple('id');
            $this->assertFalse(vfsStreamWrapper::getRoot()->hasChild('id'));

            $exemple->setRepertoire(vfsStream::url('exempleRepertoire'));
            $this->assertTrue(vfsStreamWrapper::getRoot()->hasChild('id'));
        }
    }
    ?>

Ceci présente plusieurs avantages :

-

  Le test lui-même est plus concis.

-

  vfsStream donne au développeur du test le plein contrôle sur la façon dont le code testé voit l'environnement du système de fichiers.

-

  Puisque les opérations du système de fichiers n'opèrent plus sur le système de fichiers réel, les opérations de nettoyage dans la méthode ``tearDown()`` ne sont plus nécessaires.


