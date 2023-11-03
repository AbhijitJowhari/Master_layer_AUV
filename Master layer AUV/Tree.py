from calendar import c
import py_trees
import behaviours.py
import rospy
from std_msgs.msg import Float64, Bool

# Variables' list and their respective values
#############
action_list = ['ball_3','ball_2','ball_1','move_right','pass_the_gate','detect_the_gate','avoid_flare']
Rem_time = 9000
action = None
Action_flag_AOF = False
Action_flag_gate = False
Action_flag_pass = False
Action_flag_right = False
Action_flag_ball_1 = False
Action_flag_ball_2 = False
Action_flag_ball_3 = False
step_count_x = 0
step_count_y = 0
X_0 = 27
##############

# codes for various actions
# Deadfloat = 451461215120
# Stop_the_AUV = 19201516208512122

py_trees.blackboard.Blackboard().set('action_list', ['ball_3','ball_2','ball_1','move_right','pass_the_gate','detect_the_gate','avoid_flare'])
py_trees.blackboard.Blackboard().set('Rem_time' , 9000)
py_trees.blackboard.Blackboard().set('action' , None)
py_trees.blackboard.Blackboard().set('Action_flag_AOF' , False)
py_trees.blackboard.Blackboard().set('Action_flag_gate' , False)
py_trees.blackboard.Blackboard().set('Action_flag_pass' , False)
py_trees.blackboard.Blackboard().set('Action_flag_right' , False)
py_trees.blackboard.Blackboard().set('Action_flag_ball_1' , False)
py_trees.blackboard.Blackboard().set('Action_flag_ball_2' , False)
py_trees.blackboard.Blackboard().set('Action_flag_ball_3' , False)
py_trees.blackboard.Blackboard().set('step_count_x' , 0)
py_trees.blackboard.Blackboard().set('step_count_y' , 0)
py_trees.blackboard.Blackboard().set('X_0' , 27)

def create_root() -> py_trees.behaviour.Behaviour :
    
    """

    Returns:
        the root of the tree
    """
    py_trees.blackboard.Blackboard().get('action_list')
    current_action = action_list.pop()
    py_trees.blackboard.Blackboard().set('action_lsit', action_list)
    
    if(current_action == 'avoid_flare'):
        current_start_node = avoid_flare()
        curr_action_flag = py_trees.blackboard.Blackboard().get('Action_flag_AOF')
    elif(current_action == 'detect_the_gate'):
        current_start_node = detect_the_gate()
        curr_action_flag = py_trees.blackboard.Blackboard().get('Action_flag_gate')
    elif(current_action == 'pass_the_gate'):
        current_start_node = pass_the_gate()
        curr_action_flag = py_trees.blackboard.Blackboard().get('Action_flag_pass')
    elif(current_action == 'move_right'):
        current_start_node = move_right()
        curr_action_flag = py_trees.blackboard.Blackboard().get('Action_flag_right')
    elif(current_action == 'ball_1'):
        current_start_node = knockdown_ball('Action_flag_ball_1')
        curr_action_flag = py_trees.blackboard.Blackboard().get('Action_flag_ball_1')
    elif(current_action == 'ball_2'):
        current_start_node = knockdown_ball('Action_flag_ball_2')
        curr_action_flag = py_trees.blackboard.Blackboard().get('Action_flag_ball_2')
    elif(current_action == 'ball_3'):
        current_start_node = knockdown_ball('Action_flag_ball_3')
        curr_action_flag = py_trees.blackboard.Blackboard().get('Action_flag_ball_3')

    def condition_function_root_decorator():
        if curr_action_flag:
            return False

    Root_decorator = py_trees.decorators.ConditionalDecoratorLoop(name = 'detect_the_gate_fallback_decorator_1',condition_function = condition_function_root_decorator)

    Root_decorator.add_child(current_start_node)

    return Root_decorator
    

def avoid_flare():

    avoid_flare_start_fallback = py_trees.composites.selector(memory = True, name = 'avoid_flare')
    avoid_flare_fallback_sequence_1 = py_trees.composites.sequence(memory = True, name='avoid_flare_fallback_sequence_1')
    avoid_flare_fallback_sequence_2 = py_trees.composites.sequence(memory = True, name ='avoid_flare_fallback_sequence_2')

    avoid_flare_action_node = py_trees.Behaviours.Action_node(publish_topic_name = 'MovementAction_y',
                                                              subscribe_topic_name = 'MovementAction_y_reply',
                                                              publish_data = 14,
                                                              blackboard_bool = True,
                                                              Action_flag = 'Action_flag_AOF',
                                                              blackboard_data_flag = True,
                                                              var = 'step_count_y',
                                                              blackboard_data_var = 14)
    

    avoid_flare_fallback_sequence_1_Check_Rem_time = py_trees.Behaviours.CustomConditional(topic_name = 'Rem_time',blackboard_bool = False)
    avoid_flare_fallback_sequence_1_Deadfloat = py_trees.Behaviours.Action_node(publish_topic_name = 'DeadfloatAction',subscribe_topic_name = 'Deadfloatreply',publish_data = 451461215120,blackboard_bool = False) # write the publish_data accordingly
    avoid_flare_fallback_sequence_2_check_orange_flare = py_trees.Behaviours.CustomConditional(topic_name = 'SightOfOrangeFlare', blackboard_bool = False)

    avoid_flare_fallback_sequence_2_move_right = py_trees.Behaviours.Action_node(publish_topic_name = 'MovementAction_x',
                                                                                 subscribe_topic_name = 'MovementAction_x_reply',
                                                                                 publish_data = X_0,
                                                                                 blackboard_bool = True,
                                                                                 Action_flag = 'Action_flag_AOF',
                                                                                 var = 'step_count_x',
                                                                                 blackboard_data_flag = False,
                                                                                 blackboard_data_var = X_0
                                                                                 )
    

    
    avoid_flare_start_fallback.add_children([avoid_flare_fallback_sequence_1 , avoid_flare_fallback_sequence_2, avoid_flare_action_node])
    avoid_flare_fallback_sequence_1.add_children([avoid_flare_fallback_sequence_1_Check_Rem_time , avoid_flare_fallback_sequence_1_Deadfloat])
    avoid_flare_fallback_sequence_2.add_children([avoid_flare_fallback_sequence_2_check_orange_flare , avoid_flare_fallback_sequence_2_move_right])

    return avoid_flare_start_fallback


def detect_the_gate():
    detect_the_gate_start_fallback = py_trees.composites.selector(memory = True, name = 'detect_the_gate')
    detect_the_gate_fallback_sequence_1 = py_trees.composites.sequence(memory = True, name='detect_the_gate_fallback_sequence_1')
    detect_the_gate_fallback_sequence_1_Check_Rem_time = py_trees.Behaviours.CustomConditional(topic_name = 'Rem_time',blackboard_bool = False)
    detect_the_gate_fallback_sequence_1_Deadfloat = py_trees.Behaviours.Action_node(publish_topic_name = 'DeadfloatAction',subscribe_topic_name = 'Deadfloatreply',publish_data =451461215120 ,blackboard_bool = False) # write the publish_data accordingly
    detect_the_gate_fallback_sequence_2 = py_trees.composites.sequence(memory = True, name='detect_the_gate_fallback_sequence_2')
    curr_step_count_x = py_trees.blackboard.Blackboard().get('step_count_x')

    if(curr_step_count_x > 0):
        detect_the_gate_fallback_sequence_2_condition_node = py_trees.Behaviours.AlwaysSuccess()
    else:
        detect_the_gate_fallback_sequence_2_condition_node = py_trees.Behaviours.AlwaysFailure()
    


    def condition_function_decorator_1():
        Rem_time = py_trees.blackboard.Blackboard().get('Rem_time')
        Action_flag_gate = py_trees.blackboard.Blackboard().get('Action_flag_gate')
        curr_step_count_x = py_trees.blackboard.Blackboard().get('step_count_x')

        if Rem_time == 120:
            publisher = rospy.Publisher('DeadfloatAction', Float64, queue_size=10)
            publish_data = 451461215120
            publisher.publish(publish_data)
            exit()
        elif(Action_flag_gate):
            return False
        elif curr_step_count_x == -27:
            return False
    

    detect_the_gate_fallback_sequence_2_decorator = py_trees.decorators.ConditionalDecoratorLoop(name = 'detect_the_gate_fallback_decorator_1',condition_function = condition_function_decorator_1)

    detect_the_gate_fallback_sequence_2_decorator_sequence = py_trees.composites.sequence(memory = True, name='detect_the_gate_fallback_sequence_2_decorator_sequence')
    detect_the_gate_fallback_sequence_2_decorator_sequence_action_1 = py_trees.Behaviours.Action_node(publish_topic_name = 'MovementAction_x',
                                                                                                      subscribe_topic_name = 'MovementAction_x_reply',
                                                                                                      publish_data =-1 ,
                                                                                                      blackboard_bool = True,
                                                                                                      var = 'step_count_x',
                                                                                                      blackboard_data_var = curr_step_count_x - 1
                                                                                                      )
    
    detect_the_gate_fallback_sequence_2_decorator_sequence_condition = py_trees.Behaviours.CustomConditional(topic_name = 'SightOfGate',blackboard_bool = False)
    detect_the_gate_fallback_sequence_2_decorator_sequence_action_2 = py_trees.Behaviours.Action_node(publish_topic_name = 'Stop_the_AUV',
                                                                                                      subscribe_topic_name = 'Stop_the_AUV_reply',
                                                                                                      publish_data = 19201516208512122,
                                                                                                      blackboard_bool = True,
                                                                                                      Action_flag = 'Action_flag_gate',
                                                                                                      blackboard_data_flag = True
                                                                                                      )
    



    def condition_function_decorator_2():
        Rem_time = py_trees.blackboard.Blackboard().get('Rem_time')
        Action_flag_gate = py_trees.blackboard.Blackboard().get('Action_flag_gate')
        curr_step_count_x = py_trees.blackboard.Blackboard().get('step_count_x')

        if Rem_time == 120:
            publisher = rospy.Publisher('DeadfloatAction', Float64, queue_size=10)
            publish_data = 451461215120
            publisher.publish(publish_data)
            exit()
        elif(Action_flag_gate):
            return False
        elif curr_step_count_x == 27:
            return False
    

    detect_the_gate_fallback_decorator = py_trees.decorators.ConditionalDecoratorLoop(name = 'detect_the_gate_fallback_decorator',condition_function = condition_function_decorator_2)

    detect_the_gate_fallback_decorator_sequence = py_trees.composites.sequence(memory = True, name='detect_the_gate_fallback_decorator_sequence')

    detect_the_gate_fallback_decorator_sequence_action_1 = py_trees.Behaviours.Action_node(publish_topic_name = 'MovementAction_x',
                                                                                                      subscribe_topic_name = 'MovementAction_x_reply',
                                                                                                      publish_data = 1,
                                                                                                      blackboard_bool = True,
                                                                                                      var = 'step_count_x',
                                                                                                      blackboard_data_var = curr_step_count_x + 1
                                                                                                      )
    
    detect_the_gate_fallback_decorator_sequence_condition = py_trees.Behaviours.CustomConditional(topic_name = 'SightOfGate',blackboard_bool = False)

    detect_the_gate_fallback_decorator_sequence_action_2 = py_trees.Behaviours.Action_node(publish_topic_name = 'Stop_the_AUV',
                                                                                                      subscribe_topic_name = 'Stop_the_AUV_reply',
                                                                                                      publish_data = 19201516208512122,
                                                                                                      blackboard_bool = True,
                                                                                                      Action_flag = 'Action_flag_gate',
                                                                                                      blackboard_data_flag = True
                                                                                                      )
    

    
    detect_the_gate_start_fallback.add_children([detect_the_gate_fallback_sequence_1 , detect_the_gate_fallback_sequence_2 , detect_the_gate_fallback_decorator])
    detect_the_gate_fallback_sequence_1.add_children([detect_the_gate_fallback_sequence_1_Check_Rem_time , detect_the_gate_fallback_sequence_1_Deadfloat])
    detect_the_gate_fallback_sequence_2.add_children([detect_the_gate_fallback_sequence_2_condition_node , detect_the_gate_fallback_sequence_2_decorator])
    detect_the_gate_fallback_sequence_2_decorator.add_child(detect_the_gate_fallback_sequence_2_decorator_sequence)
    detect_the_gate_fallback_sequence_2_decorator_sequence.add_children([detect_the_gate_fallback_sequence_2_decorator_sequence_action_1 , detect_the_gate_fallback_sequence_2_decorator_sequence_condition , detect_the_gate_fallback_sequence_2_decorator_sequence_action_2])
    detect_the_gate_fallback_decorator.add_child(detect_the_gate_fallback_decorator_sequence)
    detect_the_gate_fallback_decorator_sequence.add_children([detect_the_gate_fallback_decorator_sequence_action_1 , detect_the_gate_fallback_decorator_sequence_condition , detect_the_gate_fallback_decorator_sequence_action_2])


    return detect_the_gate_start_fallback
    

def pass_the_gate():
    pass_the_gate_start_fallback = py_trees.composites.selector(memory = True, name = 'pass_the_gate')
    pass_the_gate_fallback_sequence_1 = py_trees.composites.sequence(memory = True, name='pass_the_gate_fallback_sequence_1')
    pass_the_gate_fallback_sequence_1_Check_Rem_time = py_trees.Behaviours.CustomConditional(topic_name = 'Rem_time',blackboard_bool = False)
    pass_the_gate_fallback_sequence_1_Deadfloat = py_trees.Behaviours.Action_node(publish_topic_name = 'DeadfloatAction',subscribe_topic_name = 'Deadfloatreply',publish_data =451461215120 ,blackboard_bool = False)
    curr_step_count_y = py_trees.blackboard.Blackboard().get('step_count_y')

    pass_the_gate_fallback_sequence_2 = py_trees.composites.sequence(memory = True, name='pass_the_gate_fallback_sequence_2')
    pass_the_gate_fallback_sequence_2_action = py_trees.Behaviours.Action_node(publish_topic_name = 'MovementAction_y',
                                                                                                      subscribe_topic_name = 'MovementAction_y_reply',
                                                                                                      publish_data = 8,
                                                                                                      blackboard_bool = True,
                                                                                                      var = 'step_count_y',
                                                                                                      blackboard_data_var = curr_step_count_y + 8
                                                                                                      )
    

    pass_the_gate_fallback_sequence_2_condition = py_trees.Behaviours.CustomConditional(topic_name = 'Gate_contact', blackboard_bool = True, Action_flag = 'Action_flag_pass', blackboard_data_flag = True)
    pass_the_gate_fallback_action = py_trees.Behaviours.Action_node(publish_topic_name = 'MovementAction_y',
                                                                                                      subscribe_topic_name = 'MovementAction_y_reply',
                                                                                                      publish_data = -3,
                                                                                                      blackboard_bool = True,
                                                                                                      flag = 'Action_flag_pass',
                                                                                                      blackboard_data_flag = False,
                                                                                                      var = 'step_count_y',
                                                                                                      blackboard_data_var = curr_step_count_y + 8
                                                                                                      )
    
    pass_the_gate_start_fallback.add_children([pass_the_gate_fallback_sequence_1 , pass_the_gate_fallback_sequence_2 , pass_the_gate_fallback_action])
    pass_the_gate_fallback_sequence_1.add_children([pass_the_gate_fallback_sequence_1_Check_Rem_time , pass_the_gate_fallback_sequence_1_Deadfloat])
    pass_the_gate_fallback_sequence_2.add_children([pass_the_gate_fallback_sequence_2_action , pass_the_gate_fallback_sequence_2_condition])

    return pass_the_gate_start_fallback


def move_right():
    move_right_start_fallback = py_trees.composites.selector(memory = True, name = 'move_right')
    move_right_fallback_sequence_1 = py_trees.composites.sequence(memory = True, name='move_right_fallback_sequence_1')
    move_right_fallback_sequence_1_Check_Rem_time = py_trees.Behaviours.CustomConditional(topic_name = 'Rem_time',blackboard_bool = False)
    move_right_fallback_sequence_1_Deadfloat = py_trees.Behaviours.Action_node(publish_topic_name = 'DeadfloatAction',subscribe_topic_name = 'Deadfloatreply',publish_data =451461215120 ,blackboard_bool = False)
    move_right_fallback_sequence_2 = py_trees.composites.sequence(memory = True, name='move_right_fallback_sequence_2')

    curr_step_count_x = py_trees.Blackboard.blackboard().get('step_count_x')

    if curr_step_count_x >0:
        move_right_fallback_sequence_2_condition = py_trees.Behaviours.AlwaysSuccess()
    else:
        move_right_fallback_sequence_2_condition = py_trees.Behaviours.AlwaysFailure()

    move_right_fallback_sequence_2_action = py_trees.Behaviours.Action_node(publish_topic_name = 'move_right',
                                                                                                      subscribe_topic_name = 'move_right_reply',
                                                                                                      publish_data = X_0 - curr_step_count_x,
                                                                                                      blackboard_bool = True,
                                                                                                      Action_flag = 'Action_flag_right',
                                                                                                      blackboard_data_flag = True
                                                                                                      )
    
    move_right_start_fallback.add_children([move_right_fallback_sequence_1 , move_right_fallback_sequence_2])
    move_right_fallback_sequence_1.add_children([move_right_fallback_sequence_1_Check_Rem_time , move_right_fallback_sequence_1_Deadfloat])
    move_right_fallback_sequence_2.add_children([move_right_fallback_sequence_2_condition , move_right_fallback_sequence_2_action])

    return move_right_start_fallback

def knockdown_ball(given_action_flag):

    ball_1_start_fallback = py_trees.composites.selector(memory = True, name = 'ball_2')
    ball_1_fallback_sequence_1 = py_trees.composites.sequence(memory = True, name='ball_2_fallback_sequence_1')
    ball_1_fallback_sequence_1_Check_Rem_time = py_trees.Behaviours.CustomConditional(topic_name = 'Rem_time',blackboard_bool = False)
    ball_1_fallback_sequence_1_Deadfloat = py_trees.Behaviours.Action_node(publish_topic_name = 'DeadfloatAction',subscribe_topic_name = 'Deadfloatreply',publish_data =451461215120 ,blackboard_bool = False)

    def condition_function_decorator_3():
        Rem_time = py_trees.blackboard.Blackboard().get('Rem_time')

        if Rem_time == 120:
            publisher = rospy.Publisher('DeadfloatAction', Float64, queue_size=10)
            publish_data = 451461215120
            publisher.publish(publish_data)
            exit()
        elif(given_action_flag):
            return False
        elif curr_step_count_x < 0 :
            return False
        

    curr_step_count_x = py_trees.blackboard.Blackboard.get('step_count_x')
    curr_step_count_y = py_trees.blackboard.Blackboard.get('step_count_y')

    ball_1_fallback_decorator = py_trees.decorators.ConditionalDecoratorLoop(name = 'ball_1_fallback_decorator',condition_function = condition_function_decorator_3)
    ball_1_fallback_decorator_sequence = py_trees.composites.sequence(memory = True, name='ball_1_fallback_decorator_sequence')
    ball_1_fallback_decorator_sequence_action_1 = py_trees.Behaviours.Action_node(publish_topic_name = 'MovementAction_x',
                                                                                                      subscribe_topic_name = 'MovementAction_x_reply',
                                                                                                      publish_data = -1,
                                                                                                      blackboard_bool = True,
                                                                                                      var = 'step_count_x',
                                                                                                      blackboard_data_var = curr_step_count_x-1
                                                                                                      )
    
    ball_1_fallback_decorator_sequence_Sequence = py_trees.composites.sequence(memory = True, name='ball_1_fallback_decorator_sequence_sequence')

    ball_1_fallback_decorator_sequence_Sequence_condition = py_trees.Behaviours.CustomConditional(topic_name = 'SightOfStick', blackboard_bool = False)
    ball_1_fallback_decorator_sequence_Sequence_action = py_trees.Behaviours.Action_node(publish_topic_name = 'MovementAction_y',
                                                                                                      subscribe_topic_name = 'MovementAction_y_reply',
                                                                                                      publish_data = 20,
                                                                                                      blackboard_bool = True,
                                                                                                      var = 'step_count_y',
                                                                                                      blackboard_data_var = curr_step_count_y + 20
                                                                                                      )
    

    ball_1_fallback_decorator_sequence_fallback = py_trees.composites.selector(memory = True, name = 'ball_1_fallback_decorator_sequence_fallback')
    ball_1_fallback_decorator_sequence_fallback_sequence = py_trees.composites.sequence(memory = True, name='ball_1_fallback_decorator_sequence_fallback_sequence')
    ball_1_fallback_decorator_sequence_fallback_sequence_Check_Rem_time = py_trees.Behaviours.CustomConditional(topic_name = 'Rem_time',blackboard_bool = False)
    ball_1_fallback_decorator_sequence_fallback_sequence_Deadfloat = py_trees.Behaviours.Action_node(publish_topic_name = 'DeadfloatAction',subscribe_topic_name = 'Deadfloatreply',publish_data =451461215120 ,blackboard_bool = False)

    ball_1_fallback_decorator_sequence_fallback_action = py_trees.Behaviours.Action_node(publish_topic_name = 'MovementAction_y',
                                                                                                      subscribe_topic_name = 'MovementAction_y_reply',
                                                                                                      publish_data = -20,
                                                                                                      blackboard_bool = True,
                                                                                                      flag = given_action_flag,
                                                                                                      blackboard_data_flag = True,
                                                                                                      var = 'step_count_y',
                                                                                                      blackboard_data_var = curr_step_count_y - 20
                                                                                                      )

    ball_1_start_fallback.add_children([ball_1_fallback_sequence_1 , ball_1_fallback_decorator])
    ball_1_fallback_sequence_1.add_children([ball_1_fallback_sequence_1_Check_Rem_time , ball_1_fallback_sequence_1_Deadfloat])
    ball_1_fallback_decorator.add_child(ball_1_fallback_decorator_sequence)
    ball_1_fallback_decorator_sequence.add_child([ball_1_fallback_decorator_sequence_action_1 , ball_1_fallback_decorator_sequence_Sequence , ball_1_fallback_decorator_sequence_fallback])
    ball_1_fallback_decorator_sequence_Sequence.add_children([ball_1_fallback_decorator_sequence_Sequence_condition , ball_1_fallback_decorator_sequence_Sequence_action])
    ball_1_fallback_decorator_sequence_fallback.add_children([ball_1_fallback_decorator_sequence_fallback_sequence , ball_1_fallback_decorator_sequence_fallback_action])
    ball_1_fallback_decorator_sequence_fallback_sequence.add_children([ball_1_fallback_decorator_sequence_fallback_sequence_Check_Rem_time , ball_1_fallback_decorator_sequence_fallback_sequence_Deadfloat])

    return ball_1_start_fallback



                                                #######CLASS FOR CONSTRUCTING A CONDITIONAL DECORATOR LOOP#######



# Define your custom conditional decorator loop class
class ConditionalDecoratorLoop(py_trees.decorators.Decorator):
    def __init__(self, name, condition_function):
        super(ConditionalDecoratorLoop, self).__init__(name=name)
        self.condition_function = condition_function

    def update(self):
        if self.condition_function():
            # If the condition is met, apply the loop to the child behavior
            for child in self.children:
                child.status = py_trees.common.Status.RUNNING
                child.tick()
            return py_trees.common.Status.RUNNING
        else:
            # If the condition is not met, return SUCCESS
            return py_trees.common.Status.SUCCESS


Root = create_root()
Behaviour_Tree = py_trees.trees.BehaviourTree(Root)
Behaviour_Tree.tick()