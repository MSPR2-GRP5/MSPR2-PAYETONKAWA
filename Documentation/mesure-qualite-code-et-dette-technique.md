# Mesure de la qualité du code et de la dette technique

## Contexte et problématique

Les APIs étant critiques et une indisponibilité des APIs impactant le chiffre d’affaires, la société
PayeTonKawa souhaite s’assurer de la qualité des livrables pour s’assurer que ses revendeurs ainsi que le
Webshop puissent commander à tout instant.

Il faudra donc mettre en place des outils afin de pouvoir s’assurer de la qualité des livrables, ainsi qu’un
outil permettant de mesurer la qualité du code source et la dette technique des applications ainsi que les
alertes de sécurité potentielles (OWASP TOP 10 sera le référentiel que la société souhaite utiliser).

## Options considérées

* SonarQube
* Zed Attack Proxy

## Décision

Option choisie : "SonarQube".

SonarQube est l'outil de référence pour le suivi de la dette technique en plus de couvrir la sécurité et d'autres
facettes de la qualité de code. Bien que ZAP soit plus précis dans l'analyse de sécurité, il ne couvre pas
autant de facette et ne procure pas de visualisation aussi propre que Sonar.
