from  .models import Conversation,Message


def add_messages(con):
    messages=Message.objects.all().distinct()
    for msg in messages:
        if(( msg.from_user == con.from_user) and ( msg.to_user == con.to_user)) or(( msg.from_user == con.to_user) and ( msg.to_user == con.from_user)):
            Conversation.objects.message_add(msg,con)
def create_conversation(from_user,to_user):
    try:
        conversation = Conversation.objects.get(from_user=from_user,to_user=to_user)
        if conversation:
            add_messages(conversation)
            return conversation
    except :
        pass
    try:
        conversation = Conversation.objects.get(from_user=to_user,to_user=from_user)
        if conversation:
            add_messages(conversation)
            return conversation
    except :
        pass
 
    conversation,created = Conversation.objects.get_or_create(from_user=from_user,to_user=to_user)
    if created:
        add_messages(conversation)
    return conversation    
