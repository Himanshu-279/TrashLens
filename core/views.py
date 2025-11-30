from django.shortcuts import render, redirect
from PIL import Image
import base64
import io
from django.utils.safestring import mark_safe 
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

def download_app_page(request):
    apk_download_url = "https://github.com/anshikachaturavedibtechcs22-bit/My-Android-App-Releases/releases/download/v1.0.0/app-debug.apk"

    # Hero Section Stats
    stats = [
        { "value": "10K+", "label": "Active Users" },
        { "value": "50K+", "label": "Items Scanned" },
        { "value": "95%", "label": "Accuracy" }
    ]

    # Screenshots Section
    screenshots_data = [
        # image_url mein 'static/' ke baad wala path daalein
        { "id": 1, "title": "Home Screen", "color_class": "gradient-1", "image_url": "images/home.png" },
        { "id": 2, "title": "Scan Item", "color_class": "gradient-2", "image_url": "images/scan.png" },
        { "id": 3, "title": "Results", "color_class": "gradient-3", "image_url": "images/result.png" },
        { "id": 4, "title": "Map View", "color_class": "gradient-4", "image_url": "images/map.png" }
    ]
    screenshots = [
        {**data, "delay": i * 100} for i, data in enumerate(screenshots_data) # 0, 100, 200, 300
    ]

    # Features Section 
    features_data = [
        { "icon_svg": mark_safe("""<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="var(--trashlens-primary)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14.5 4h-5L7 7H4a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-3l-2.5-3z"></path><circle cx="12" cy="13" r="3"></circle></svg>"""), 
          "title": "AI Recognition", "description": "Instantly identify waste with camera" },
        
        { "icon_svg": mark_safe("""<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="var(--trashlens-primary)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path><circle cx="12" cy="10" r="3"></circle></svg>"""), 
          "title": "Find Centers", "description": "Locate nearest disposal centers" },
        
        # Leaf icon 
        { "icon_svg": mark_safe("""<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="var(--trashlens-primary)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 20A7 7 0 0 1 4 13c0-4.4 7-7.5 7-7.5s7 3.1 7 7.5c0 4.4-7 7.5-7 7.5Z"></path><path d="M12 18a2.5 2.5 0 0 0 0-5 2.5 2.5 0 0 1 0-5"></path></svg>"""), 
          "title": "Eco Impact", "description": "Track your recycling impact" }
    ]
    features = [
        {**data, "delay": i * 150} for i, data in enumerate(features_data) # 0, 150, 300
    ]

    # Benefits Section 
    benefits_data = [
        "AI-powered waste recognition with 95% accuracy",
        "Find nearest disposal centers with live navigation",
        "Track your environmental impact in real-time",
        "Learn proper disposal methods for any waste type",
        "Join a community of eco-conscious users",
        "Free to download and use, no hidden charges"
    ]
    benefits = [
        {"text": benefit, "delay": i * 100} for i, benefit in enumerate(benefits_data) # 0, 100, 200...
    ]
    
    context = {
        'apk_url': apk_download_url,
        'stats': stats,
        'screenshots': screenshots,
        'features': features,
        'benefits': benefits
    }
    
    return render(request, 'download_final.html', context)


def waste_types_view(request):
    """Renders the Waste Types page with new design, icons, and hover colors."""
    
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

    icons_and_colors["brown-glass"] = icons_and_colors["glass"]
    icons_and_colors["green-glass"] = icons_and_colors["glass"]
    icons_and_colors["white-glass"] = icons_and_colors["glass"]

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
            
            return redirect('result')

        except Exception as e:
            return render(request, 'classifier.html', {'error': f"An error occurred: {e}"})

    return render(request, 'classifier.html')

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
