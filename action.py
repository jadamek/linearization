from numpy import inf
from message import Message

#================================================================================
class ActionSend:
#================================================================================
# Represents the guarded command *send*
#================================================================================
# Methods
    #----------------------------------------------------------------------------
    # - Check Guard
    #----------------------------------------------------------------------------
    # * process : process to evaluate the action's guard against
    #----------------------------------------------------------------------------
    def guard(self, process):
        return (process.left > -inf or process.right < inf) and len(process.outgoing) == 0
    
    #----------------------------------------------------------------------------
    # - Execute Command
    #----------------------------------------------------------------------------
    # * process : process to execute the action's commands on
    #----------------------------------------------------------------------------
    def command(self, process):
        if process.left > -inf:
            process.send(process.left, Message(process.id))
        if process.right < inf:
            process.send(process.right, Message(process.id))            

# Members
    name = "send"
#================================================================================

#================================================================================
class ActionReceive:
#================================================================================
# Represents the guarded command *receive*
#================================================================================
# Methods    
    #----------------------------------------------------------------------------
    # - Check Guard
    #----------------------------------------------------------------------------
    # * process : process to evaluate the action's guard against
    #----------------------------------------------------------------------------
    def guard(self, process):
        return len(process.channel) > 0
    
    #----------------------------------------------------------------------------
    # - Execute Command
    #----------------------------------------------------------------------------
    # * process : process to execute the action's commands on
    #----------------------------------------------------------------------------
    def command(self, process):
        message = process.receive()
        
        if message.content > process.id:
            if message.content < process.right:
                if process.right < inf:
                    process.send(message.content, Message(process.right))
                process.right = message.content
            else:
                process.send(process.right, message)
        elif message.content < process.id:
            if message.content > process.left:
                if process.left > -inf:
                    process.send(message.content, Message(process.left))
                process.left = message.content
            else:
                process.send(process.left, message)

# Members
    name = "receive"
#================================================================================

ACTIONS = [ActionSend(), ActionReceive()]