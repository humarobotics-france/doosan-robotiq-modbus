# -*- coding: utf-8 -*-
"""
DoosanRobotiqModbus class is used for the dialogue between a Robotiq Gripper and a Doosan robot, using Modbus communication.
Please read the README.md file before use.
Copyright (C) 2022 HumaRobotics

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import time

class DoosanRobotiqModbus:
    """
    Interface to use Robotiq gripper with Doosan robot
    """

    def __init__(self, ip="192.168.1.11", port=502, model="2f85"):
        """
        Create the registers for the communication between the gripper and the robot and start the initialization sequence.

        Params:\n
            - 'ip': ip of Modbus slave 
            - 'port': port number of the Modbus slave
            - 'model': model of the Robotiq gripper (2f85 or 2f140)
        """

        self.ip = ip
        self.port = port
        if (model!="2f85") and (model!="2f140"):
            tp_popup("Le modèle choisi n'est pas compatible. Les modèles compatibles sont : 2f85 et 2f140")
            exit()
        else:
            self.model = model

        tp_log("Creation of the registers")
        add_modbus_signal(ip=self.ip, port=self.port, name="2F_AR_21",
                          reg_type=DR_HOLDING_REGISTER, index=0, value=0, slaveid=255)  # Action request
        add_modbus_signal(ip=self.ip, port=self.port, name="2F_PR_21",
                          reg_type=DR_HOLDING_REGISTER, index=1, value=0, slaveid=255)  # Position request
        add_modbus_signal(ip=self.ip, port=self.port, name="2F_SP_FO_21",
                          reg_type=DR_HOLDING_REGISTER, index=2, value=0, slaveid=255)  # Speed, Force
        add_modbus_signal(ip=self.ip, port=self.port, name="2F_GS_21",
                          reg_type=DR_INPUT_REGISTER, index=0, slaveid=255)  # Gripper status
        add_modbus_signal(ip=self.ip, port=self.port, name="2F_FS_PRE_21",
                          reg_type=DR_INPUT_REGISTER, index=1, slaveid=255)  # Fault status, Pos request echo
        add_modbus_signal(ip=self.ip, port=self.port, name="2F_PO_CU_21",
                          reg_type=DR_INPUT_REGISTER, index=2, slaveid=255)  # Position, Current
        set_modbus_output("2F_AR_21", 256) # set rACT to 1 (activate gripper)

        bin_status = self.get_gripper_object_status()
        gsta = bin_status[2] + bin_status[3]
        timer_start = time.time()
        timer = 0
        while gsta!="11" and timer<30:
            bin_status = self.get_gripper_object_status()
            gsta = bin_status[2] + bin_status[3]
            timer = time.time() - timer_start
        
        if timer>=30:
            tp_popup("Problème lors de l'initialisation du préhenseur")
            exit()
            
        wait(1)


    def close_gripper(self, speed = 50, force = 50):
        """
        Fully close the gripper with the speed and force entered.

        Params:\n
            - 'speed': desired speed for the movement of the gripper between 0% and 100% (default is 50%)
            - 'force': desired force for the gripper between 0% and 100% (default is 50%)
            
        Return:\n
            - '1' : The parameters are good, the motion command has been send
            - '-1' : Wrong parameters, the motion command has not been send
        """

        res = self.move_gripper(speed, force, 0)
        return res
        
            
    def open_gripper(self, speed = 50, force = 50):
        """
        Fully open the gripper with the speed and force entered.

        Params:\n
            - 'speed': desired speed for the movement of the gripper between 0% and 100% (default is 50%)
            - 'force': desired force for the gripper between 0% and 100% (default is 50%)
            
        Return:\n
            - '1' : The parameters are good, the motion command has been send
            - '-1' : Wrong parameters, the motion command has not been send
        """

        if (self.model == "2f85"):
            res = self.move_gripper(speed, force, 85)
        elif (self.model == "2f140"):
            res = self.move_gripper(speed, force, 140)
        return res


    def move_gripper(self, speed = 50, force = 50, position = 85):
        """
        Move the gripper to the desired position with the speed and force choosen.

        Params:\n
            - 'speed': desired speed for the movement of the gripper between 0% and 100% (default is 50%)
            - 'force': desired force for the gripper between 0% and 100% (default is 50%)
            - 'position' : desired position for the gripper between 0 mm and 85 mm for 2f85, and between 0 mm and 140 mm for 2f140 (0 = close, 85 or 140 = open, default is 85)
        
        Return:\n
            - '1' : The parameters are good, the motion command has been send
            - '-1' : Wrong parameters, the motion command has not been send
        """

        if (speed > 100):
            tp_popup("Wrong speed (>100%)")
            return -1
        elif (speed < 0):
            tp_popup("Wrong speed (<0)")
            return -1

        if (force > 100):
            tp_popup("Wrong force (>100%)")
            return -1
        elif (force < 0):
            tp_popup("Wrong force (<0)")
            return -1
        
        if (position > 85) and (self.model == "2f85"):
            tp_popup("Wrong position (>85 mm)")
            return -1
        elif (position > 140) and (self.model == "2f140"):
            tp_popup("Wrong position (>140 mm)")
            return -1
        elif (position < 0):
            tp_popup("Wrong position (<0 mm)")
            return -1
        
        bin_speed = format(round((speed/100)*255), 'b')
        while len(bin_speed)<8:
            bin_speed = "0" + bin_speed

        bin_force = format(round((force/100)*255), 'b')
        while len(bin_force)<8:
            bin_force = "0" + bin_force

        bin_speed_force = "0b" + bin_speed + bin_force
        speed_force = int(bin_speed_force, 2)

        if (self.model == "2f85"):
            pos = round(((85-position)/85)*255)
        elif (self.model == "2f140"):
            pos = round(((140-position)/140)*255)

        set_modbus_output("2F_AR_21", 2304) # Doosan modbus communication uses 16-bits bytes, so 2 bytes from the Robotiq registers (here, action request and reserved).
        set_modbus_output("2F_SP_FO_21", speed_force)
        set_modbus_output("2F_PR_21", pos)
        return 1


    def get_gripper_object_status(self):
        """
        Get the status of the gripper.
        
        Return:\n
            - 'binStatus' : string corresponding to the binary number (16 bits) from the Gripper Status and Reserved registers (bytes 0 and 1 of the Robot Input/Status registers)
        """
        
        status = get_modbus_input("2F_GS_21")   # status is an integer between 0 and 65535 (16 bits)
        bin_status = format(status, 'b')    # we transform status into a binary number (0bxxxxxx) and we slice the '0b' part
        difference = 16 - len(bin_status)     # if bin_status is less than 16 caracters, we need to fill it (adding zeros at the start) (bin_status = xxxxxb)
        
        if (difference > 0):
            while len(bin_status)<16:
                bin_status = "0" + bin_status     # we add 0 at the start of bin_status until it is 16 characters in length
        
        return bin_status
    

    def log_status(self):
        """
        Log the status of the gripper.
        """

        bin_status = self.get_gripper_object_status()
        gact = bin_status[7]     # activation status (rAct)
        ggto = bin_status[4]     # action status (rGTO)
        gsta = bin_status[2] + bin_status[3]  # gripper status 
        gobj = bin_status[0] + bin_status[1]  # object detection status

        if(gact == '1'):
            tp_log("Gripper activation")
        elif(gact == '0'):
            tp_log("Gripper reset")
        else:
            tp_log("Error : gACT is not binary")
        
        if(ggto == '1'):
            tp_log("Go to requested position")
        elif(ggto == '0'):
            tp_log("Gripper stopped")
        else:
            tp_log("Error : gGTO is not binary")
            
        if(gsta == '00'):
            tp_log("Gripper is in reset state")
        elif(gsta == '01'):
            tp_log("Ativation in progress")
        elif(gsta == '10'):
            tp_log("Not used")
        elif(gsta == '11'):
            tp_log("Activation is completed")
        else:
            tp_log("Error : gSTA is not binary")
        
        if(gobj == '00'):
            tp_log("Fingers are in motion towards requested position. No object detected.")
        elif(gobj == '01'):
            tp_log("Fingers have stopped due to a contact while opening before requested position. Object detected opening.")
        elif(gobj == '10'):
            tp_log("Fingers have stopped due to a contact while closing before requested position. Object detected closing.")
        elif(gobj == '11'):
            tp_log("Fingers are at requested position. No object detected or object has been loss / dropped.")
        else:
            tp_log("Error : gOBJ is not binary")

        
    def close_connexion(self):
        """
        Close the modbus signal/connexion created during the init.
        """

        del_modbus_signal("2F_AR_21")
        del_modbus_signal("2F_PR_21")
        del_modbus_signal("2F_SP_FO_21")
        del_modbus_signal("2F_GS_21")
        del_modbus_signal("2F_FS_PRE_21")
        del_modbus_signal("2F_PO_CU_21")
