from dotenv import load_dotenv
from openai import OpenAI
from pypdf import PdfReader
import gradio as gr
import os
load_dotenv(override=True)

openapi_api_key = os.getenv("OPENAI_API_KEY")
if openapi_api_key:
    print("OpenAI API key loaded successfully.")
else:
    print("Failed to load OpenAI API key. Please check your .env file.")
    raise ValueError("OpenAI API key not found in environment variables.")  

openai = OpenAI()

reader = PdfReader("Profile.pdf")
linkedin_text = ""
for page in reader.pages:
    if page.extract_text():
        linkedin_text += page.extract_text()

with open("summary.txt", "r", encoding="utf-8") as f:
    summary = f.read()

name = "Mohamed Zayed"

system_prompt = f"You are acting as {name}. You are answering questions on {name}'s website, \
particularly questions related to {name}'s career, background, skills and experience. \
Your responsibility is to represent {name} for interactions on the website as faithfully as possible. \
You are given a summary of {name}'s background and LinkedIn profile which you can use to answer questions. \
Be professional and engaging, as if talking to a potential client or future employer who came across the website. \
If you don't know the answer, say so."

system_prompt += f"\n\n## Summary:\n{summary}\n\n## LinkedIn Profile:\n{linkedin_text}\n\n"
system_prompt += f"With this context, please chat with the user, always staying in character as {name}."

def chat(message, history):
    messages = [{"role": "system", "content": system_prompt}] + history + [{"role": "user", "content": message}]
    response = openai.chat.completions.create(model="gpt-4o-mini", messages=messages)
    return response.choices[0].message.content
if __name__ == "__main__":
    gr.ChatInterface(chat, type="messages").launch(share=True)
