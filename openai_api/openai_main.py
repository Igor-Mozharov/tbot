import google.generativeai as genai
from credentials import credentialss

def gemini_speaker(text):
    """
    Generate text response for use questions with Gemini
    :param text: USer text
    :return Gemini response text
    """
    genai.configure(api_key='AIzaSyBluTIHu_s-0PkrMtpLKm3bsJsFSxOmC9s')
    model = genai.GenerativeModel('models/gemini-2.0-flash')
    response = model.generate_content(text)
    return response.text