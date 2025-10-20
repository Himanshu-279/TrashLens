from django.shortcuts import render, redirect
from PIL import Image
import base64
import io
import pandas as pd 
from django.conf import settings
from . import utils

def home_view(request):
    """Renders the home page."""
    return render(request, 'home.html')

def how_it_works_view(request):
    """Renders the 'How It Works' page."""
    return render(request, 'how_it_works.html')

def about_view(request):
    """Renders the 'About' page which contains 'The Challenge'."""
    return render(request, 'about.html')

# views.py mein PURANE waste_types_view ko isse BADAL do

# views.py mein PURANE waste_types_view ko isse BADAL do

def waste_types_view(request):
    """Renders the Waste Types page with new design, icons, and hover colors."""
    
    # Har category ke liye icon aur color theme define karo
    # Yeh React code se milte-julte hain
    icons_and_colors = {
        "plastic": {"icon": "fa-box", "color_theme": "blue"},
        "biological": {"icon": "fa-leaf", "color_theme": "green"},
        "paper": {"icon": "fa-newspaper", "color_theme": "orange"},
        "cardboard": {"icon": "fa-box-open", "color_theme": "yellow"},
        "glass": {"icon": "fa-wine-bottle", "color_theme": "purple"},
        "metal": {"icon": "fa-bolt", "color_theme": "slate"}, # Icon changed to fa-bolt
        "battery": {"icon": "fa-car-battery", "color_theme": "red"}, # Represents E-Waste
        "clothes": {"icon": "fa-shirt", "color_theme": "pink"}, # Represents Textile Waste
        "shoes": {"icon": "fa-shoe-prints", "color_theme": "amber"},
        "trash": {"icon": "fa-trash-alt", "color_theme": "zinc"}, # Represents General Waste
    }

    # Glass ki sabhi categories ke liye same style
    icons_and_colors["brown-glass"] = icons_and_colors["glass"]
    icons_and_colors["green-glass"] = icons_and_colors["glass"]
    icons_and_colors["white-glass"] = icons_and_colors["glass"]

    # Final data taiyar karo template ke liye
    waste_types_data = {}
    for key, details in utils.waste_info_details.items():
        theme = icons_and_colors.get(key, {"icon": "fa-question-circle", "color_theme": "gray"})
        waste_types_data[key] = {
            "title": details["title"],
            "info": details["info"],
            "icon": theme["icon"],
            "color_theme": theme["color_theme"]
        }

    context = {'waste_types': waste_types_data}
    return render(request, 'waste_types.html', context)

# views.py mein PURANE dos_and_donts_view ko isse BADAL do

def dos_and_donts_view(request):
    """Renders the Do's and Don'ts page with new design data."""
    
    dos_data = [
        { "title": "Separate at Source", "description": "Always separate wet and dry waste at home before disposal" },
        { "title": "Clean Before Recycling", "description": "Rinse containers and remove labels before recycling" },
        { "title": "Use Reusable Bags", "description": "Carry cloth or jute bags for shopping instead of plastic" },
        { "title": "Compost Organic Waste", "description": "Convert kitchen waste into nutrient-rich compost" },
        { "title": "Donate Usable Items", "description": "Give away clothes, books, and electronics that still work" },
        { "title": "Use Proper Bins", "description": "Always dispose waste in designated color-coded bins" }
    ]

    donts_data = [
        { "title": "Don't Mix Waste Types", "description": "Never mix recyclable and non-recyclable waste together" },
        { "title": "Don't Litter", "description": "Never throw waste on streets, beaches, or public spaces" },
        { "title": "Don't Burn Plastic", "description": "Burning plastic releases toxic fumes harmful to health" },
        { "title": "Don't Flush Non-Biodegradables", "description": "Avoid flushing plastic, sanitary products, or wet wipes" },
        { "title": "Don't Use Single-Use Plastics", "description": "Minimize use of straws, cups, and disposable cutlery" },
        { "title": "Don't Ignore E-Waste", "description": "Never throw electronics in regular bins, use e-waste centers" }
    ]

    context = {
        'dos': dos_data,
        'donts': donts_data
    }
    return render(request, 'dos_and_donts.html', context)

def classifier_view(request):
    if request.method == 'POST' and request.FILES.get('image_file'):
        uploaded_file = request.FILES['image_file']
        try:
            img = Image.open(uploaded_file).convert('RGB')
            pred_class, conf, preds = utils.classify_image(img)
            
            buffered = io.BytesIO()
            img.save(buffered, format="JPEG")
            uploaded_image_b64 = base64.b64encode(buffered.getvalue()).decode()
            
            request.session['prediction'] = pred_class
            request.session['confidence'] = float(conf)
            request.session['uploaded_image_b64'] = uploaded_image_b64
            request.session['feedback_submitted'] = False
            request.session.modified = True
            
            # NAYE RESULT PAGE PAR BHEJ DO
            return redirect('result')

        except Exception as e:
            return render(request, 'classifier.html', {'error': f"An error occurred: {e}"})

    # Agar GET request hai, to sirf upload form dikhao
    return render(request, 'classifier.html')


# NEW Result Page View
def result_view(request):
    prediction = request.session.get('prediction')
    if not prediction:
        return redirect('classifier')
        
    confidence = request.session.get('confidence')
    uploaded_image_b64 = request.session.get('uploaded_image_b64')
    
    info = utils.recycling_info.get(prediction, {})
    
    context = {
        'prediction': prediction,
        'confidence': confidence,
        'uploaded_image_b64': uploaded_image_b64,
        'recyclable': info.get('recyclable', False),
        'steps': info.get('steps', [])
    }
    return render(request, 'result.html', context)

def map_feedback_view(request):
    prediction = request.session.get('prediction')
    uploaded_image_b64 = request.session.get('uploaded_image_b64')
    
    if not prediction:
        return redirect('classifier')

    feedback_submitted = request.session.get('feedback_submitted', False)

    if request.method == 'POST':
        correct_status = request.POST.get('correct')
        new_class = request.POST.get('new_class')
        user_comment = request.POST.get('user_comment')
        
        img_data = base64.b64decode(uploaded_image_b64)
        pil_img = Image.open(io.BytesIO(img_data))
        
        utils.save_feedback(prediction, correct_status, new_class, pil_img, user_comment)
        
        request.session['feedback_submitted'] = True
        request.session.modified = True
        return redirect('map_feedback')
    
    # MAP KE LIYE DATA BHEJNE KA LOGIC
    try:
        centers_df = pd.read_csv("centers.csv")
        centers_json = centers_df.to_json(orient='records')
    except FileNotFoundError:
        centers_json = "[]"
        print("WARNING: centers.csv file not found.")

    context = {
        'prediction': prediction,
        'uploaded_image_b64': uploaded_image_b64,
        'class_names': utils.class_names,
        'feedback_submitted': feedback_submitted,
        'centers_json': centers_json, # Centers ka data bheja
        'google_api_key': getattr(settings, 'GOOGLE_MAPS_API_KEY', None) # API key bheji
    }
    return render(request, 'map_feedback.html', context)
