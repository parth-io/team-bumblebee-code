#!/usr/bin/env python
import rospy
from std_msgs.msg import Header, String
from assignment1.msg import Chat
from os import system
from collections import deque

class Messages:
    def __init__(self):
         self.stack = deque()
         
    def get_colour(self, author):
         last_three = author[-3] + author[-2] + author[-1]
         return ('38;5;' + last_three + 'm') if int(last_three) < 255 else '38;5;' + str(int(last_three) % 100) + 'm' #non-standard, only works for bash, https://chrisyeh96.github.io/2020/03/28/terminal-colors.html

    def get_stack(self):
        return ''.join(self.stack).strip() + '\033[0m'
      
    def add_to_stack(self, x, author):
        if len(self.stack) > 9:
            self.stack.popleft()
        self.stack.append('\033[{}{}'.format(self.get_colour(author), author + ': ' + x + '\n'))


def clear():
    system('clear')


def talker():
    messages = Messages()
    pub = rospy.Publisher('chatter', Chat, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(10)
    
    def callback(data):
        clear()
        messages.add_to_stack(data.message.data, data.author.data)
        print messages.get_stack()
    
    rospy.Subscriber('chatter', Chat, callback)

    while not rospy.is_shutdown():
        hello_str = raw_input()
        if hello_str:
            header = Header()
            header.stamp = rospy.Time.now()
            source_id = String(rospy.get_name())
            message = String(hello_str)
            c = Chat(header, source_id, message)
            pub.publish(c)
        
        rate.sleep()


if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
