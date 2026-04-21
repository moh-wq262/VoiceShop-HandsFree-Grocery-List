from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse, Gather

app = Flask(__name__)

# Sample personal grocery list
my_list = ["Milk", "Eggs", "Whole Wheat Bread", "Apples", "Coffee"]

@app.route("/voice", methods=['GET', 'POST'])
def voice_entry():
    """Initial entry point for the voice call"""
    response = VoiceResponse()
    
    if not my_list:
        response.say("Your shopping list is empty. Have a great day!")
        return str(response)

    response.say("Welcome to VoiceShop. Let's start your shopping list.")
    return redirect_to_item(0)

def redirect_to_item(index):
    response = VoiceResponse()
    item = my_list[index]
    
    # Using Gather to capture user keypad input
    gather = Gather(num_digits=1, action=f"/handle-key?index={index}")
    gather.say(f"Item {index + 1}: {item}. Press 1 for next item, or 2 to repeat.")
    response.append(gather)
    
    return str(response)

@app.route("/handle-key", methods=['GET', 'POST'])
def handle_key():
    """Handles keypad input from the user"""
    digit = request.values.get('Digits')
    index = int(request.args.get('index'))
    
    if digit == '1': # Move to next
        if index + 1 < len(my_list):
            return redirect_to_item(index + 1)
        else:
            res = VoiceResponse()
            res.say("That was the last item. Shopping complete. Goodbye!")
            return str(res)
    elif digit == '2': # Repeat current
        return redirect_to_item(index)
    
    return voice_entry() # Default restart

if __name__ == "__main__":
    app.run(debug=True)
