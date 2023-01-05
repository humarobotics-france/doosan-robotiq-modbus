<a href="https://www.humarobotics.com/">
    <img src="./images/Logo_HR_bleu.png" alt="HumaRobotics logo" title="HumaRobotics" align="right" height="80" />
</a>

# Doosan Robotiq Modbus

<p align="left">
  <a href="./README.md">English</a> •
  <a href="docs/README-fr.md">Français</a>
</p>

--------------

Modbus interface to control a Robotiq gripper from a Doosan robot

This project is developed by [HumaRobotics](https://www.humarobotics.com/).

This class has been tested on a Robotiq gripper *2F-85*.

## Requirements

- A **Doosan robot**
- A **Robotiq gripper** (2F-85 or 2F-140)

## How to use

- Configure the IP of the robot to match the subnetwork "192.168.1.X".

- Create a `Custom Code` and import the [DoosanRobotiqModbus.py](./DoosanRobotiqModbus.py) file (replace .py by .txt to import in the Doosan).

- Then, look at the examples in the "examples" folder to see how to use the DoosanRobotiqModbus class. You can begin with importing the [ex_doosan_robotiq_modbus.txt](./examples/ex_doosan_robotiq_modbus.txt) into the Doosan.

## Examples files

- [ex_doosan_robotiq_modbus.txt](./examples/ex_doosan_robotiq_modbus.txt): Basic example for the communication between Robotiq gripper and Doosan robot.

<div align = "center" >
<img src="./images/Logo_HR_bleu.png" alt="HumaRobotics logo" title="HumaRobotics" height="200" />
</div>