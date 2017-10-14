

.. _installation:

=================
Installer PHPUnit
=================

PHPUnit doit être installé en utilisant l'installateur PEAR, la colonne vertébrale du
`dépôt d'extensions et d'applications PHP (PHP Extension and Application
Repository) <http://pear.php.net/>`_ qui apporte un système de distribution pour les paquets PHP.

.. caution::

   Selon votre distribution de système d'exploitation et/ou votre environnement PHP,
   vous pouvez avoir besoin d'installer PEAR ou de mettre à jour votre installation
   existante de PEAR avant de pouvoir suivre les instructions de ce chapitre.

   sudo pear upgrade PEAR suffit habituellement pour
   mettre à jour une installation PEAR existante. Le `manuel PEAR <http://pear.php.net/manual/en/installation.getting.php>`_ explique comment réaliser une nouvelle installation de PEAR.

.. admonition:: Note

   PHPUnit 4.6 nécessite PHP 5.4.8 (ou ultérieur) mais PHP 5.5.0 (ou ultérieur) est
   fortement recommandé.

   PHP_CodeCoverage, la bibliothèque qui est utilisée par PHPUnit pour rassembler et
   traiter les informations de couverture de code, dépend de Xdebug 2.2.1 (ou ultérieure) mais
   Xdebug 2.3.0 (ou ultérieur) est fortement recommandé.

Les deux commandes suivantes (que vous aurez peut-être à exécuter en tant que
super-administrateur, i.e. ``root`` )sont tout ce qui est nécessaire
pour installer PHPUnit en utilisant l'installateur PEAR:

.. code-block:: bash

    pear config-set auto_discover 1
    pear install pear.phpunit.de/PHPUnit

Les paquets facultatifs suivants sont disponibles :

``DbUnit``

    Portage de DbUnit pour PHP/PHPUnit destiné à gérer les tests interagissant avec des bases de données.

    Ce paquet peut être installé en utilisant la commande suivante :

    .. code-block:: bash

        pear install phpunit/DbUnit

``PHPUnit_Selenium``

    Intégration de Selenium RC pour PHPUnit.

    Ce paquet peut être installé en utilisant la commande suivante :

    .. code-block:: bash

        pear install phpunit/PHPUnit_Selenium

``PHPUnit_Story``

    Lanceur de tests basés sur des histoires pour les développements dirigés par le comportement (Behavior-Driven Development) avec PHPUnit.

    Ce paquet peut être installé en utilisant la commande suivante :

    .. code-block:: bash

        pear install phpunit/PHPUnit_Story

``PHPUnit_SkeletonGenerator``

    Outil qui permet de générer des squelettes de classes de test à partir des classes du code
    de production et vice versa.

    Ce paquet peut être installé en utilisant la commande suivante :

    .. code-block:: bash

        pear install phpunit/PHPUnit_SkeletonGenerator

``PHPUnit_TestListener_DBUS``

    Un moniteur de tests qui envoie des événements à DBUS.

    Ce paquet peut être installé en utilisant la commande suivante :

    .. code-block:: bash

        pear install phpunit/PHPUnit_TestListener_DBUS

``PHPUnit_TestListener_XHProf``

    Un moniteur de tests qui utilise XHProf pour profiler automatiquement le code testé.

    Ce paquet peut être installé en utilisant la commande suivante :

    .. code-block:: bash

        pear install phpunit/PHPUnit_TestListener_XHProf

``PHPUnit_TicketListener_Fogbugz``

    Un moniteur de tickets qui interagit avec l'API d'incidents de FogBugz.

    Ce paquet peut être installé en utilisant la commande suivante :

    .. code-block:: bash

        pear install phpunit/PHPUnit_TicketListener_Fogbugz

``PHPUnit_TicketListener_GitHub``

    Un moniteur de tickets qui interagit avec l'API d'incidents de GitHub.

    Ce paquet peut être installé en utilisant la commande suivante :

    .. code-block:: bash

        pear install phpunit/PHPUnit_TicketListener_GitHub

``PHPUnit_TicketListener_GoogleCode``

    Un moniteur de tickets qui interagit avec l'API d'incidents de Google Code.

    Ce paquet peut être installé en utilisant la commande suivante :

    .. code-block:: bash

        pear install phpunit/PHPUnit_TicketListener_GoogleCode

``PHPUnit_TicketListener_Trac``

    Un moniteur de tickets qui interagit avec l'API d'incidents de Trac.

    Ce paquet peut être installé en utilisant la commande suivante :

    .. code-block:: bash

        pear install phpunit/PHPUnit_TicketListener_Trac

``PHP_Invoker``

    Une classe utilitaire pour invoquer des appels avec un délai d'expiration. Ce paquet est
    nécessaire pour mettre en oeuvre des dépassements de délais pour les tests en mode strict.

    Ce paquet peut être installé en utilisant la commande suivante :

    .. code-block:: bash

        pear install phpunit/PHP_Invoker

Après l'installation, vous trouverez les fichiers du code source de PHPUnit dans votre
répertoire local PEAR; le chemin d'accès est habituellement
:file:`/usr/lib/php/PHPUnit`.

