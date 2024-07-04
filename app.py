from flask import Flask, request, render_template, redirect
from PIL import Image
import colorsys
import os
import random

app = Flask(__name__)

def generate_aesthetic_palette(num_colors=5):
    palette = []
    for _ in range(num_colors):
        h = random.random()  # Random hue
        s = random.uniform(0.4, 0.7)  # Saturation between 40% and 70%
        l = random.uniform(0.5, 0.8)  # Lightness between 50% and 80%
        r, g, b = colorsys.hls_to_rgb(h, l, s)
        palette.append((int(r * 255), int(g * 255), int(b * 255)))
    return palette

def classify_skin_tone(r, g, b):
    # Determine warm or cool based on saturation
    _, s, _ = colorsys.rgb_to_hls(r / 255.0, g / 255.0, b / 255.0)
    tone = "Warm" if s > 0.5 else "Cool"
    
    # Determine season
    season = "Spring"
    if tone == "Warm":
        if r > g and r > b:
            season = "Autumn"
        else:
            season = "Spring"
    else:
        if b > r and b > g:
            season = "Winter"
        else:
            season = "Summer"
    return tone, season

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            print("No file part")
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            print("No selected file")
            return redirect(request.url)
        if file:
            try:
                image = Image.open(file.stream)
                colors = image.getcolors(image.size[0] * image.size[1])
                most_frequent_color = max(colors, key=lambda t: t[0])[1]
                palette = generate_aesthetic_palette()
                tone, season = classify_skin_tone(*most_frequent_color)
                return render_template('index.html', palette=palette, tone=tone, season=season)
            except Exception as e:
                print(f"Error processing file: {e}")
                return redirect(request.url)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

