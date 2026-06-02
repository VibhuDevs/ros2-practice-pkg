#!/usr/bin/env python3
import rclpy
import time
from rclpy.node import Node
from rclpy.action import ActionServer
from my_robot_interfaces.action import BatteryLevel
from rclpy.action import CancelResponse
from rclpy.executors import MultiThreadedExecutor
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.action.server import ServerGoalHandle, GoalResponse

class BatteryLevelServer(Node):
    def __init__(self):
        super().__init__('battery_node')
        self.action_server = ActionServer(self, BatteryLevel, 'battery_level',
                goal_callback = self.battery_goal_callback, execute_callback = self.execution_callback,
                cancel_callback  = self.cancel_callback)
        self.battery_percent = 10
        
    def battery_goal_callback(self, goal_request: BatteryLevel.Goal):
        self.get_logger().info('Got a goal!')
        if goal_request.target_percent < 0:
            self.get_logger().info("Battery percentage can't be negative")
            return GoalResponse.REJECT
        elif goal_request.target_percent <= self.battery_percent:
            self.get_logger().info("You can't discharge the battery")
            return GoalResponse.REJECT
        else:
            self.get_logger().info("Accepting the goal")
            return GoalResponse.ACCEPT
        
    def execution_callback(self, goal_handle: ServerGoalHandle):
        target_percent = goal_handle.request.target_percent
        result = BatteryLevel.Result()
        
        while self.battery_percent < target_percent:
            self.get_logger().info(f"Charging. Current charge: {self.battery_percent}" + '%')
            self.battery_percent += 5.0
            time.sleep(1.0)
            
            if goal_handle.is_cancel_requested:
                self.get_logger().info(f'Cancelling charging at {self.battery_percent}'+'%')
                goal_handle.canceled()
                result.final_percent = self.battery_percent
                result.success = 'Cancelled'
                return result
        goal_handle.succeed()
        result.final_percent = self.battery_percent
        result.success = 'Goal achieved'
        return result


    
    def cancel_callback(self, goal_handle: ServerGoalHandle):
        self.get_logger().info('Receiving a cancel charging request')
        return CancelResponse.ACCEPT
        
    
def main(args = None):
    rclpy.init(args = args)
    node = BatteryLevelServer()
    rclpy.spin(node, MultiThreadedExecutor())
    rclpy.shutdown()

if __name__ == '__main__':
    main()


        


