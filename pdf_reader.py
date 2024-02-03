import PyPDF2
from openai import OpenAI
from utils import GPT_result
import json
import re


def process_pdf(pdf_file, start_page, end_page):
  reader = PyPDF2.PdfReader(pdf_file)
  # Please upload you pdf file and change the name of the file
  num_pages = len(reader.pages)
  if end_page > num_pages:
    end_page = num_pages
  if start_page >= end_page:
    start_page = end_page - 1
  if start_page < 0:
    start_page = 0
  response = []


  for page_num in range(start_page, end_page):
    page_obj = reader.pages[page_num]
    detected_text = page_obj.extract_text() + '\n\n'
    response_text = GPT_result(detected_text)
    with open (f'{page_num}.txt' , 'w') as file:
      file.writelines(response_text)

    try:
      # clear_output()
      print(f'processing page{page_num+1} of {num_pages} ...')

        # if AI can find sequense added it dictionary
      if "```" in response_text:
        response_text=re.findall(r"(?<=```)[\s,\S]+(?=```)",response_text)[0].replace('\n',"")
      jason_object = json.loads(response_text)
      print(f'founded sequence = {jason_object}')
      for obj in jason_object:
        if len(obj.get("section").split("."))>2:
          for res in response:
            if res["section"][0]==obj["section"][0] and res["section"] in obj["section"]:
              res["spec"]["requirements"] += obj["spec"]["requirements"]
              break
        else:
          response.append(obj)

    except Exception as e:
      print('we Couldn\'t find any sequence in that page')
      print(response_text)
      print(str(e))
      pass

  return response