import openai

# Replace with your key
openai.api_key = ""
	
completion = openai.Completion()


prompt_text = "StreetGuard is a chat Bot created by the team Jugaadu Coders who gives precautions to the users of their app named StreetGuardian. StreetGuard is smart, intelligent, polite, caring and can give precautions based on the description and the fault at that place which is given by the user by using openai intelligence. StreetGuard is created using gpt 3 ai model. \nFriend: At avenue 3 two motorcycle riders clashed each other due to the fault in the street mirror on that blind corner.\nnothingDUDE: Be careful rider! Here are some precautions you can take for this place: 1. Kindly ride slow on this road as some other rider may be coming at super fast speed beside you. 2. Be careful while riding on this road as there be someone coming at a very fast speed from the adjacent lane \nFriend: At Surajkund the road had a sudden invisible hole which led to the accident of bike. \nnothingDUDE: Ayo rider keep these points in mind while driving around Surajkund: 1. Be careful while travelling on this road, keep a thorough check on the road as there might be another road faults in the day. 2. "


def ask(question, chat_log=None):
    
    prompt=prompt_text+question+"\nnothingDUDE:"
    print(prompt)
    response = openai.Completion.create(
        model="text-davinci-003",
        temperature=0.9,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0 ,
        presence_penalty=0.6,   
        prompt=prompt,
        stop=[" Friend:", " nothingDUDE:"],
        suffix=""
    )
    print(response)
    if response["choices"][0]["text"]=="":
        return "Didnt get you!";
    return response["choices"][0]["text"]
