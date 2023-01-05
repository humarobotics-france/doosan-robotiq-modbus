<a href="https://www.humarobotics.com/">
    <img src="../images/Logo_HR_bleu.png" alt="HumaRobotics logo" title="HumaRobotics" align="right" height="80" />
</a>

# Doosan Robotiq Modbus

<p align="left">
  <a href="../README.md">English</a> •
  <a href="./README-fr.md">Français</a>
</p>

--------------

Interface Modbus permettant d'utiliser une pince Robotiq avec un robot Doosan

Ce projet est développé par [HumaRobotics](https://www.humarobotics.com/).

Cette classe a été téstée sur une pince Robotiq *2F-85*.

## Conditions requises

- Un **robot Doosan**
- Une **pince Robotiq** (2F-85 ou 2F-140)

## Mode d'emploi

- Configurer l'adresse IP du robot pour être sous le même sous réseau que la pince (par défaut: "192.168.1.X")

- Créez un `Custom Code` et importez le fichier [DoosanRobotiqModbus.py](../DoosanRobotiqModbus.py) (il faut remplacer le .py par .txt pour importer le fichier dans un Doosan).

- Ensuite, regardez les exemples dans le dossier "examples" pous savoir comment utiliser la classe DoosanSick. Vous pouvez commencer par importer le fichier [ex_doosan_robotiq_modbus.txt](../examples/ex_doosan_robotiq_modbus.txt) dans le Doosan.

## Exemples

- [ex_doosan_robotiq_modbus.txt](../examples/ex_doosan_robotiq_modbus.txt): Exemple basique de communication entre la pince Robotiq et le robot Doosan.

<div align = "center" >
    <img src="../images/Logo_HR_bleu.png" alt="HumaRobotics logo" title="HumaRobotics" height="200" />
</div>