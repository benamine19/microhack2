import base64
import json
from openai import OpenAI
from dotenv import load_dotenv
import os

# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

def TaskEvaluation(task,ImagePath):
    relativeimagepath = ImagePath[1:]
    load_dotenv()
    client = OpenAI(api_key=os.environ.get("API_KEY"))
    # Getting the base64 string
    base64_image = encode_image(relativeimagepath)
    
    response = client.chat.completions.create(
    model="gpt-4-turbo",
    response_format={ "type": "json_object" },
    messages=[
        {
        "role": "user",
        "content": [
            {"type": "text", "text": "give me the percentage from 0 to 100 of this task : " + task + " in json for example : {\"percentage\": number}"},
            {
                "type": "image_url",
                "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image}"
            }
        }

        ],
        }
    ],
    max_tokens=300,
    )

    json_data = json.loads(response.choices[0].message.content)

    return json_data