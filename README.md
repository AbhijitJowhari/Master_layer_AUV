# Master_layer_AUV

This repository contains the implementation of Behaviour tree for Anahita, The Autonomous Underwater Vehicle developed by team AUV-IITK. The Behaviour tree(reffered as BT hereafter) is specific to our target competition Singapore Autonomous Underwater Vehicle Challenge (SAUVC) in April 2024 and is currently under simulation testing. Here, I have made available the 2 files namely Behaviours.py and Tree.py which fully constitute the Behaviour tree of our AUV. This repository also contains visual representation for the BT. The requirements to run this module is pytrees and rospy libraries. This code is written in python. 

### Behaviours.py

* This file contains the 4 behaviours used in the behaviour tree which are namely an 'Action_node','Conditional_Node','Always_SUCCESS' and 'Always_FAILURE'.The Latter two nodes always return SUCCESS and FAILURE repectively.This was requiered by the Behaviour Tree of our AUV.

### Tree.py
* This file contains the main code for the BT of out bot. reiterating, the BT is specific for our target competition. The code for the BT is very modular and is written in an object oriented manner.
