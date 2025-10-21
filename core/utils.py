import os
from django.conf import settings
import numpy as np
import requests
import huggingface_hub
import cloudinary
import cloudinary.uploader
from supabase import create_client, Client
import io
import base64
from PIL import Image

# ==========================
# Data Dictionaries for Pages
# ==========================

# Defines the list of class names our model can predict.
class_names = ['battery', 'biological', 'brown-glass', 'cardboard', 'clothes', 'green-glass', 'metal', 'paper', 'plastic', 'shoes', 'trash', 'white-glass']

# Contains details for the "Waste Types" page.
waste_info_details = {
    "battery": {"image_url": "https://i.ibb.co/L5rK5z7/battery.jpg", "title": "Battery", "info": "Includes AA, AAA, and car batteries. Requires special disposal."},
    "biological": {"image_url": "https://i.ibb.co/d7sC5t4/biological.jpg", "title": "Biological", "info": "Food scraps, fruit peels, yard waste. Can be composted."},
    "brown-glass": {"image_url": "https://i.ibb.co/3Wf20z7/brown-glass.jpg", "title": "Brown Glass", "info": "Beer bottles, medicine bottles. 100% recyclable."},
    "cardboard": {"image_url": "https://i.ibb.co/gR3yg7C/cardboard.jpg", "title": "Cardboard", "info": "Packaging boxes, cartons. Should be flattened and dry."},
    "clothes": {"image_url": "https://i.ibb.co/GvxYh7G/clothes.jpg", "title": "Clothes", "info": "Unwanted garments. Can be donated or recycled."},
    "green-glass": {"image_url": "https://i.ibb.co/gJF7vB2/green-glass.jpg", "title": "Green Glass", "info": "Wine bottles, juice bottles. Fully recyclable."},
    "metal": {"image_url": "https://i.ibb.co/G03gKJV/metal.jpg", "title": "Metal", "info": "Aluminum cans, steel food cans. Highly recyclable."},
    "paper": {"image_url": "https://i.ibb.co/ZcDmcsy/paper.jpg", "title": "Paper", "info": "Newspapers, magazines, office paper. Must be clean and dry."},
    "plastic": {"image_url": "https://i.ibb.co/fDbMmjm/plastic.jpg", "title": "Plastic", "info": "Bottles, containers, bags. Check the recycling symbol (1-7)."},
    "shoes": {"image_url": "https://i.ibb.co/YyVhhx9/shoes.jpg", "title": "Shoes", "info": "All types of footwear. Can be donated if wearable."},
    "trash": {"image_url": "https://i.ibb.co/Lz0J1xK/trash.jpg", "title": "Trash", "info": "General, non-recyclable waste like chip bags, styrofoam."},
    "white-glass": {"image_url": "https://i.ibb.co/KjJz1Wz/white-glass.jpg", "title": "White Glass", "info": "Clear glass jars (jam, pickles), beverage bottles. Fully recyclable."}
}

# Contains details for the "Do's and Don'ts" page.
dos_list = [
    "Rinse containers before recycling to remove food residue.",
    "Flatten cardboard boxes to save space in bins and trucks.",
    "Check local recycling guidelines as rules can vary by city.",
    "Separate different types of waste like paper, plastic, and glass.",
    "Donate usable items like clothes and shoes to charities.",
    "Compost your organic waste like fruit peels and vegetable scraps.",
]

donts_list = [
    "Don't put recyclables in a plastic bag; it jams sorting machines.",
    "Don't recycle greasy or food-soiled items like pizza boxes.",
    "Don't 'Wish-cycle' - hoping something is recyclable when it's not.",
    "Don't throw electronics or batteries in the regular trash.",
    "Don't recycle small items like straws or bottle caps individually.",
    "Don't forget to empty and rinse liquids from bottles and containers.",
]

# Contains detailed recycling steps for each waste category.
recycling_info = {
    'battery': { "recyclable": True, "steps": [
        "Do Not Put in Regular Trash: Batteries contain heavy metals that can contaminate soil and water.",
        "Find an E-waste Collection Point: Search online for 'e-waste collection near me' for special drop-off locations.",
        "Tape the Terminals: Put a small piece of non-conductive tape over the ends of lithium-ion batteries to prevent fire risk.",
        "Check with Retailers: Many electronic stores have take-back programs for old batteries.",
        "Store Safely: Keep used batteries in a cool, dry place in a non-conductive container.",
        "Never Burn Batteries: Burning batteries releases toxic fumes and can cause explosions."
    ]},
    'plastic': { "recyclable": True, "steps": [
        "Check the Number: Look for the recycling symbol (1-7) and check if your local facility accepts that type.",
        "Empty and Rinse: Make sure the container is completely empty and give it a quick rinse to remove residue.",
        "Lids On or Off?: Rules vary. When in doubt, it's often safer to throw small plastic lids in the trash.",
        "Remove Non-Plastic Parts: Take off any paper labels or metal rings if possible.",
        "Keep them Dry: Shake out excess water. Wet items can damage paper products in a mixed recycling bin.",
        "Don't Bag Recyclables: Place plastic items loose in the recycling bin, not inside a plastic bag."
    ]},
    'cardboard': { "recyclable": True, "steps": [
        "Flatten the Box: Break down and flatten all cardboard boxes to save space.",
        "Remove Packing Materials: Take out all plastic bags, bubble wrap, and styrofoam from inside the box.",
        "Keep it Dry: Wet or damp cardboard has damaged fibers and cannot be recycled.",
        "No Food Contamination: Greasy or food-stained cardboard (like a pizza box bottom) cannot be recycled.",
        "Remove Tape: Peel off as much plastic tape as you can before recycling.",
        "Bundle or Bin: Place flattened cardboard in your recycling bin or bundle it according to local rules."
    ]},
    'glass': { "recyclable": True, "steps": [
        "Empty and Rinse: Ensure the glass bottle or jar is completely empty and clean.",
        "Remove Lids: Metal or plastic lids should be removed and recycled separately if possible.",
        "Don't Break the Glass: It's safer for sanitation workers if the glass is intact.",
        "Check Colors: Some facilities require you to separate glass by color (brown, green, clear).",
        "Labels are OK: You usually don't need to remove the paper labels.",
        "No Other Glass Types: Do not recycle window panes, light bulbs, or mirrors with glass bottles."
    ]},
    'metal': { "recyclable": True, "steps": [
        "Empty and Rinse: For food cans (steel, aluminum), make sure they are empty and rinsed.",
        "Crush if Possible: Crushing aluminum cans saves a lot of space in recycling bins.",
        "Aerosol Cans: Ensure aerosol cans are completely empty before recycling. Do not puncture them.",
        "Labels are OK: You usually don't need to remove the paper labels from cans.",
        "Sharp Edges: Be careful with sharp lids. You can tuck them inside the can.",
        "No Hazardous Containers: Containers that held hazardous materials like paint should not be recycled."
    ]},
    'biological': { "recyclable": False, "steps": [
        "Separate Organic Waste: Keep a separate bin in your kitchen for food scraps, peels, and leftovers.",
        "Find a Compost Method: You can create a compost pile in your backyard or use a compost bin.",
        "No Meat or Dairy in Home Compost: Avoid adding meat, bones, or dairy as they can attract pests.",
        "Balance Greens and Browns: Mix 'greens' (kitchen scraps) with 'browns' (dried leaves, twigs) for good compost.",
        "Use Community Programs: If you can't compost at home, check for local community composting programs.",
        "General Bin as Last Resort: If composting is not an option, dispose of it in the general waste bin."
    ]},
    'paper': { "recyclable": True, "steps": [
        "Keep it Clean and Dry: Only clean, dry paper can be recycled. Stained paper should be thrown away.",
        "Remove Attachments: Remove plastic wrappers, spiral bindings, and large metal clips.",
        "No Shredded Paper in Bins: Loose shredded paper can jam machinery. Put it in a sealed paper bag first.",
        "Don't Crumple: Keep paper as flat as possible.",
        "Includes Junk Mail: Envelopes (even with plastic windows), magazines, and newspapers are recyclable.",
        "No Laminated Paper: Paper with a glossy plastic coating cannot be recycled."
    ]},
    'shoes': { "recyclable": True, "steps": [
        "Donate First: If the shoes are still wearable, donation to a charity is the best option.",
        "Find a Recycling Program: Many brands (like Nike) have take-back programs to recycle old shoes.",
        "Separate Parts (If Possible): For some programs, separating the rubber sole from the fabric can be helpful.",
        "Clean Before Donating: If donating, please give them a quick clean first.",
        "Community Drop-offs: Look for shoe and textile recycling bins in your local area.",
        "Last Resort: If they are completely unusable, they go in the general trash."
    ]},
    'clothes': { "recyclable": True, "steps": [
        "Donate First: If clothes are in good condition, donate them to a local charity or thrift store.",
        "Textile Recycling Bins: Look for textile recycling bins for clothes that are too worn to be donated.",
        "Repurpose at Home: Old t-shirts and towels make excellent cleaning rags.",
        "Check with Animal Shelters: Many shelters accept old towels and blankets for animal bedding.",
        "Retailer Programs: Some clothing stores have in-store collection programs for old clothes.",
        "Never in Recycling Bin: Do not put clothes in your regular mixed recycling bin."
    ]},
    'trash': { "recyclable": False, "steps": [
        "Confirm it's Trash: This is for items that cannot be recycled, like chip bags, diapers, and broken ceramics.",
        "Bag it Securely: Place all trash into a sealed trash bag to keep bins clean and prevent litter.",
        "General Waste Bin: Dispose of the bag in your designated general waste or landfill bin.",
        "Hazardous Waste is Different: Do not put items like paint or chemicals in the regular trash.",
        "Reduce First: The best way to manage trash is to create less of it. Opt for reusable items.",
        "Check for Special Instructions: Some items like styrofoam may have special drop-off locations."
    ]},
}
# Assign the same recycling info for all glass types.
for cat in ['brown-glass', 'green-glass', 'white-glass']:
    recycling_info[cat] = recycling_info['glass']


# ==========================
# Core Application Logic
# ==========================

def classify_image(img):
    """
    Sends an image to the backend Model API for classification.
    """
    print("Preparing to call the Model API...")
    
    # Retrieve the Model API URL from Django settings.
    MODEL_API_URL = getattr(settings, 'MODEL_API_URL')
    
    if not MODEL_API_URL:
        print("CRITICAL ERROR: MODEL_API_URL is not configured in settings.py or environment variables!")
        raise Exception("MODEL_API_URL is not set in settings.py!")

    # Convert the Pillow Image object to bytes for the API request.
    byte_arr = io.BytesIO()
    img.save(byte_arr, format='PNG')
    image_bytes = byte_arr.getvalue()

    try:
        # Send a POST request to the prediction endpoint of the API.
        response = requests.post(
            f"{MODEL_API_URL.rstrip('/')}/predict", 
            files={"file": ("image.png", image_bytes, "image/png")},
            timeout=120 # Wait up to 120 seconds for a response.
        )
        response.raise_for_status() # Raise an exception for HTTP error codes (4xx or 5xx).

        # Parse the JSON response from the API.
        data = response.json()
        pred_class_name = data.get("prediction", "error")
        confidence = data.get("confidence", 0.0)

        print(f"API returned: {pred_class_name} with {confidence:.2f}% confidence.")

        # Return the results. A dummy list is returned for the 'preds' array as it's not needed.
        return pred_class_name, confidence, []

    except requests.exceptions.RequestException as e:
        print("!!!!!!!!!!!!!! API CALL FAILED !!!!!!!!!!!!!!")
        print(f"Error calling model API: {e}")
        # Return a default error result if the API call fails, to prevent the app from crashing.
        return "error", 0.0, []

def save_feedback(predicted, correct, new_class, pil_img, user_comment):
    """
    Saves user feedback by uploading the image to Cloudinary and the record to Supabase.
    """
    try:
        # Step 1: Configure Cloudinary using keys from settings.
        print("Configuring Cloudinary...")
        cloudinary.config(
            cloud_name = settings.CLOUDINARY_CLOUD_NAME,
            api_key = settings.CLOUDINARY_API_KEY,
            api_secret = settings.CLOUDINARY_API_SECRET,
            secure=True
        )

        # Step 2: Convert the image to bytes and upload to Cloudinary.
        byte_arr = io.BytesIO()
        pil_img.save(byte_arr, format='PNG')
        byte_arr = byte_arr.getvalue()
        
        print("Uploading image to Cloudinary...")
        upload_result = cloudinary.uploader.upload(byte_arr)
        image_url = upload_result.get("secure_url")

        if not image_url:
            print("ERROR: Image upload to Cloudinary failed.")
            return

        print(f"Image uploaded successfully: {image_url}")

        # Step 3: Configure the Supabase client.
        print("Connecting to Supabase...")
        supabase_client: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
        
        # Step 4: Prepare and insert the feedback record into the Supabase table.
        record = {
            "predicted_class": predicted,
            "is_correct": correct == "Yes",
            "actual_class": new_class if correct == "No" else None,
            "image_url": image_url,
            "comment": user_comment
        }
        
        print(f"Saving record to Supabase: {record}")
        supabase_client.table('feedback').insert(record).execute()
        print("Feedback saved successfully to Supabase.")

    except Exception as e:
        # Log any errors that occur during the process.
        print(f"!!!!!!!!!!!!!! AN ERROR OCCURRED WHILE SAVING FEEDBACK !!!!!!!!!!!!!!")
        print(f"Error details: {e}")

def get_image_as_base64(path, max_size=(400, 400)):
    """
    A utility function to open an image, resize it, and encode it as a Base64 string.
    This is not currently used in the main application flow but can be useful.
    """
    try:
        img = Image.open(path)
        img.thumbnail(max_size)
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode()
    except Exception as e:
        print(f"Error processing image {path}: {e}")
        return None

