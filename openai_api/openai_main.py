import google.generativeai as genai
from credentials import credentialss

def gemini_speaker(text):
    """
    Generate text response for use questions with Gemini
    :param text: USer text
    :return Gemini response text
    """
    genai.configure(api_key='AIzaSyDCVlZCAR2e0sgFbDogUa2YeFaO39-MXUI')
    model = genai.GenerativeModel('models/gemini-2.0-flash')
    response = model.generate_content(text)
    return response.text