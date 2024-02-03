import json
from utils import GPT_result
import re

def divide_text(text, max_words=3000):
    words = text.split()
    chunks = []
    current_chunk = []

    for word in words:
        if len(' '.join(current_chunk + [word])) <= max_words:
            current_chunk.append(word)
        else:
            chunks.append(' '.join(current_chunk))
            current_chunk = [word]

    if current_chunk:
        chunks.append(' '.join(current_chunk))

    return chunks


def process_text( st , text_list):
    response = []
    for detected_text in text_list:
        response_text = GPT_result(detected_text)
        try:
            # if AI can find sequense added it dictionary
            if "```" in response_text:
                response_text=re.findall(r"(?<=```)[\s,\S]+(?=```)",response_text)[0].replace('\n',"")
            jason_object = json.loads(response_text)
            st.write(f'founded sequence = {len(jason_object)}')
            for obj in jason_object:
                if len(obj.get("section").split("."))>2:
                    for res in response:
                        if res["section"][0]==obj["section"][0] and res["section"] in obj["section"]:
                            res["spec"]["requirements"] += obj["spec"]["requirements"]
                        break
                else:
                    response.append(obj)

        except Exception as e:
            st.write('we Couldn\'t find any sequence in that page')
            st.write(response_text)
            st.write(str(e))
            pass

    return response 

