import google.generativeai as genai

genai.configure(api_key="AIzaSyDXXcKZuzn9T56QR8Tt6jDQfhKHEspRdDc")

model = genai.GenerativeModel("gemini-pro")
res = model.generate_content("Halo")
print(res.text)
