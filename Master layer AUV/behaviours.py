import py_trees
import roslibpy as  rospy
from std_msgs.msg import Float64, Bool

# Variables
##############
# action_list = ['ball_3','ball_2','ball_1','move_right','pass_the_gate','detect_the_gate','avoid_flare']
# Rem_time = 9000
# action = None
# Action_flag_AOF = False
# Action_flag_gate = False
# Action_flag_pass = False
# Action_flag_right = False
# Action_flag_ball_1 = False
# Action_flag_ball_2 = False
# Action_flag_ball_3 = False
# step_count_x = 0
# step_count_y = 0
# X_0 = 27
##############

lst_of_variables = ['action_list','Rem_time','action','Action_flag_AOF','Action_flag_gate','Action_flag_pass', 'Action_flag_right','Action_flag_ball_1','Action_flag_ball_2', 'Action_flag_ball_3', 'step_count_x','step_count_y','X_0']

# Initialize ROS node
rospy.init_node('bot_controller')

# Define your custom action class
class Action_node(py_trees.behaviour.Behaviour):
    def __init__(self, publish_topic_name, subscribe_topic_name, name = '',publish_data = None,Action_flag='', var = None,blackboard_bool = False, blackboard_data_flag = None , blackboard_var = None):
        self.publish_data = publish_data
        self.subscribe_topic_name = subscribe_topic_name
        self.topic_name = publish_topic_name
        self.name = f'{publish_topic_name}'
        self.Action_flag = Action_flag
        self.var = var
        self.blackboard_bool = blackboard_bool
        self.blackboard_data_flag = blackboard_data_flag
        self.blackboard_var = blackboard_var

        super(Action_node, self).__init__(name)



        # Initialize ROS publisher to send movement commands
        self.publisher = rospy.Publisher(publish_topic_name, Float64, queue_size=10)
        # Initialize ROS subscriber to receive movement success feedback
        self.success_subscriber = rospy.Subscriber(subscribe_topic_name, Bool, self.feedback_callback)
        # Flag to store movement success feedback
        self.Action_success = False

    def feedback_callback(self, feedback_msg):
        # Callback function to handle movement success feedback
        self.Action_success = feedback_msg.data

    def update(self):
        self.publisher.publish(self.publish_data)  # Publish the command
        
        # Wait for the bot to complete the movement (this duration depends on your bot's speed and movement capabilities)
        rospy.sleep(3)  # Assuming the bot takes 5 seconds to move 7 meters
        
        # Check the movement success feedback received from the subscribed topic
        if self.Action_success:
            if self.blackboard_bool == True:
                if self.blackboard_var != None:
                    py_trees.blackboard.Blackboard().set(self.var,self.blackboard__data_var)
                if self.blackboard_flag != None:
                    py_trees.blackboard.Blackboard().set(self.Action_flag, self.blackboard_data_flag)

            return py_trees.common.Status.SUCCESS
        else:
            # If the movement was not successful, return FAILURE status
            return py_trees.common.Status.FAILURE



# Initialize ROS node
rospy.init_node('condition_checker')

# Define your custom conditional class
class CustomConditional(py_trees.behaviour.Behaviour):
    def __init__(self,topic_name, name='',blackboard_bool = None, blackboard_data_flag = None,Action_flag = None):
        self.blackboard_data_flag = blackboard_data_flag
        self.Action_flag  = Action_flag
        self.topic_name = topic_name
        self.name = name=f"{self.topic_name}Conditional"
        self.blackboard_bool = blackboard_bool

        super(CustomConditional, self).__init__(name)
        # Initialize ROS subscriber to receive condition status
        self.condition_status = False
        self.subscriber = rospy.Subscriber(f'{topic_name}', Bool, self.condition_callback)

    def condition_callback(self, status_msg):
        # Callback function to handle condition status feedback
        self.condition_status = status_msg.data

    def update(self):
        # Check the condition status received from the subscribed topic
        if self.condition_status:
            # If the condition is met, return SUCCESS
            if self.blackboard_bool == True:
                py_trees.blackboard.Blackboard().set(self.Action_flag, self.blackboard_data_flag)
        
            return py_trees.common.Status.SUCCESS
        else:
            # If the condition is not met, return FAILURE
            return py_trees.common.Status.FAILURE


class AlwaysFailure(py_trees.behaviour.Behaviour):
    def __init__(self, name="Always_Failure"):
        super(AlwaysFailure, self).__init__(name)

    def update(self):
        # Always return FAILURE status
        return py_trees.common.Status.FAILURE
    

class AlwaysSuccess(py_trees.behaviour.Behaviour):
    def __init__(self, name="Always_Success"):
        super(AlwaysSuccess, self).__init__(name)

    def update(self):
        # Always return SUCCESS status
        return py_trees.common.Status.SUCCESS


