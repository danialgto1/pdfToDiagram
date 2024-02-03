
from openai import OpenAI
import os

def format_long_text(text, max_line_length=50):
  words = text.split()
  lines = []
  current_line = ""
  
  for word in words:
      if len(current_line + word) <= max_line_length:
          current_line += word + " "
      else:
          lines.append(current_line.strip())
          current_line = word + " "
  
  if current_line:
      lines.append(current_line.strip())
  
  return "\n".join(lines)

def GPT_result(detected_text):

    with open('prompt.txt' , 'r') as file:
        request = file.read()
        
    client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get('OPENAI_API_KEY'), )

    chat_completion = client.chat.completions.create(messages=[
        {
            "role": "system",
            "content": 'you are a helpfull assitant '
        },
        {
            "role": "user",
            "content": f"{request} the text is <{detected_text}>"
        },
    ],
                                                     model="gpt-4",
                                                     temperature=0)
    response_text = chat_completion.choices[0].message.content

    return response_text

