import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import tensorflow as tf
from tensorflow.keras.preprocessing import image as keras_image
from tensorflow.keras.models import load_model

model = load_model('shirt_feature_extraction_inceptionv3_model.h5')  

def preprocess_image(image):
    
    img = keras_image.img_to_array(image)
    img = tf.image.resize(img, (299, 299))  
    img = img / 255.0  
    img = np.expand_dims(img, axis=0)  
    return img


st.title("Shirt Suitability Predictor")

st.divider()
st.write("Elevate your wardrobe with our Shirt Suitability Predictor. Input your body measurements, skin tone, and occasion. Our intelligent system will analyze your image and suggest the best shirt styles, ensuring you always look your best.")

st.divider()
col1, col2, col3 = st.columns(3)
col4, col5, col6 = st.columns(3)

with col1:
    body_type = st.selectbox('Select Body Type', ['Slim', 'Athletic', 'tall', 'short','broad','round'])
with col2:
    skin_tone = st.selectbox('Select Skin Tone', ['fair/light', 'medium/olive', 'darker/brown', 'deep/very dark'])
with col3:
    chest_waist_measurement = st.selectbox('Select Chest/Waist Measurement', ['slim chest & waist', 'athletic chest & slim waist', 'regular chest & waist', 'broad chest & narrow waist','full chest & waist','round waist'])
with col4:
    occasion = st.selectbox('Select Occasion', ['Casual', 'formal', 'Outing', 'Trip','Evening','Event','Sports'])
with col5:
    season = st.selectbox('Select Season', ['summer', 'winter', 'rainy', 'spring/fall'])
with col6:
    day_or_night = st.selectbox('Select Day or Night', ['Day', 'Night'])












reverse_shirt_t = {0: 'shirt', 1: 't'}
reverse_shirt_style = {
    0: 'formal', 1: 'Casual', 2: 'cargo', 3: 'Kurta', 4: 'plain', 5: 'Jersey', 6: 'Sweatshirt', 
    7: 'Polo', 8: 'logo', 9: 'Typography', 10: 'Sports', 11: 'graphic'
}
reverse_sleeves_type = {0: 'Full', 1: 'Half'}
reverse_fabric_type = {
    0: 'Cotton', 1: 'Polyester', 2: 'Silk', 3: 'Linen', 4: 'Cotton Blend'
}
reverse_color = {
    0: 'Blue', 1: 'Red', 2: 'Maroon', 3: 'Pink', 4: 'Lilac', 5: 'Navy', 6: 'Peach', 7: 'Green', 
    8: 'Olive', 9: 'White', 10: 'Black', 11: 'Brown', 12: 'Orange', 13: 'Purple', 14: 'Sky Blue', 
    15: 'Grey', 16: 'Beige', 17: 'Gold', 18: 'Yellow', 19: 'Lemon'
}
reverse_design = {
    0: 'Solid', 1: 'Graphic', 2: 'shiny', 3: 'Check', 4: 'Stripe', 5: 'Floral', 6: 'Paisley', 
    7: 'logo', 8: 'Typography'
}
reverse_collor_type = {
    0: 'point', 1: 'Spread', 2: 'Mandarin', 3: 'Button Down', 4: 'Round', 5: 'V-Neck', 
    6: 'Polo', 7: 'Henley', 8: 'Tutle'
}
reverse_pocket = {0: 'none', 1: 'one', 2: 'double'}

# # Example model prediction output (encoded numeric values)
# predicted_values = {
#     'shirt_t': 0,  # 'shirt'
#     'shirt_style': 1,  # 'Casual'
#     'sleeves_type': 0,  # 'Full'
#     'fabric_type': 0,  # 'Cotton'
#     'color': 7,  # 'Green'
#     'design': 1,  # 'Graphic'
#     'collor_type': 2,  # 'Mandarin'
#     'pocket': 1  # 'one'
# }

uploaded_image = st.file_uploader("Upload an Image", type=['jpg'])

if uploaded_image is not None:
    image = Image.open(uploaded_image)
    st.image(image, caption="Uploaded Image", use_column_width=True)


    processed_image = preprocess_image(image)

    
    prediction = model.predict(processed_image)
    print("Hello")


        # Reverse mapping function
    def decode_shirt_attributes(prediction):
        decoded_values = {
            'shirt_t': reverse_shirt_t[np.argmax(prediction[0])],
            'shirt_style': reverse_shirt_style[np.argmax(prediction[1])],
            'sleeves_type': reverse_sleeves_type[np.argmax(prediction[2])],
            'fabric_type': reverse_fabric_type[np.argmax(prediction[3])],
            'color': reverse_color[np.argmax(prediction[4])],
            'design': reverse_design[np.argmax(prediction[5])],
            'collor_type': reverse_collor_type[np.argmax(prediction[6])],
            'pocket': reverse_pocket[np.argmax(prediction[7])]
        }
        return decoded_values

    # Decode the predicted values
    decoded_shirt_attributes = decode_shirt_attributes(prediction)


    print(type(decoded_shirt_attributes))





    class ShirtSuitabilityChecker:
        def __init__(self):

            self.body_type_rules = {
                'slim': ['slim fit', 'athletic fit'],
                'athletic': ['athletic fit', 'slim fit', 'regular fit'],
                'tall': ['regular fit', 'slim fit'],
                'short': ['slim fit', 'regular fit'],
                'broad': ['regular fit', 'loose fit'],
                'round': ['loose fit', 'regular fit']  # corrected round waist mapping to loose/regular
            }


            self.chest_waist_fit = {
                'slim chest & waist': 'slim fit',
                'athletic chest & slim waist': 'athletic fit',
                'regular chest & waist': 'regular fit',
                'broad chest & narrow waist': 'regular fit',
                'full chest & waist': 'loose fit',
                'round waist': 'loose fit'  
            }

            # Skin tone to color mapping (specific to your provided colors)
            self.skin_tone_color_rules = {
                'fair/light': ['Blue', 'White', 'Navy','Purple','Orange','Black','Pink','Olive'],
                'medium/olive': ['Green', 'Olive', 'Blue', 'Navy','Maroon','Grey','White'],
                'darker/brown': ['Red', 'Blue', 'Maroon', 'Black', 'White','Beige','Brown','Navy','Purple'],
                'deep/very dark': ['White', 'Pink', 'sapphire', 'Orange','Grey','Black','Red','Yellow'],
            }

            # Fabric suitability based on season
            self.season_rules = {
                'summer': ['Cotton', 'Cotton Blend', 'Polo', 'Casual', 'Graphic', 'Half','Full'],
                'winter': ['Polyester', 'Silk', 'Sweatshirt','Cotton','Full'],
                'rainy': ['Polyester', 'Casual', 'Polo'],
                'spring/fall': ['Cotton', 'Polyester', 'Casual', 'Polo', 'Button Down', 'Half','Full', 'Cotton Blend'],
            }

            # Shirt design suitability for occasion
            self.shirt_design_rules = {
                'Solid': ['formal', 'Casual', 'Polo','Outing','Event'],
                'Graphic': ['Casual', 'Sports','Event','Evening','Trip'],
                'shiny': ['formal', 'Evening','Trip','Event'],
                'Check': ['formal', 'Casual','Evening','Trip','Event','Outing'],
                'Stripe': ['formal', 'Casual','Evening','Trip','Event','Outing','Sports', 'business'],
                'Floral': ['Casual', 'spring/summer','Trip'],
                'logo': ['Sports', 'Casual','Outing','Trip','Evening'],
                'Typography': ['Casual', 'Sports','Event','Evening','Trip', 'Graphic','graphic'],
            }

            # Collar types for shirt style and occasion
            self.shirt_collars_rules = {
                'point': ['formal', 'Casual', 'business','Outing','Event','shirt'],
                'Spread': ['formal', 'Casual', 'business','Outing','Event','shirt'],
                'Mandarin': ['Casual', 'formal','Event','Evning','Outing','shirt','t'],
                'Button Down': ['formal', 'business','Casual', 'formal','Event','Evening','Outing','shirt'],
                'Round': ['Casual', 't','Evening','Outing','Sports','Trip'],
                'V-Neck': ['Casual', 't','Evening','Outing','Sports','Trip'],
                'Polo': ['Casual', 't','Evening','Outing','Sports','Trip','formal'],
                'Tutle': ['formal', 'Casual', 'winter','Outing','Evening'],
            }

            # Pocket suitability based on shirt style
            self.pocket_rules = {
                'none': ['formal', 'Casual','Outing','Event','shirt','t','plain','Sweatshirt','Typography','graphic','Sports'],
                'one': ['Casual', 'formal','Polo','plain','Typography','graphic'],
                'double': [ 'Casual'],
            }

            # Day or night suitability
            self.time_of_day_rules = {
                'Day': ['Casual', 'Polo', 'graphic','Graphic','plain','Typography','Sports','formal','logo'],
                'Night': ['Casual','graphic','plain','Typography','Sports'], 
            }
    
        def get_shirt_fit(self, body_type, chest_waist_measurement):
            # Determine the fit based on body type and chest/waist measurement
            body_fit_rules = self.body_type_rules.get(body_type, [])
            chest_waist_fit = self.chest_waist_fit.get(chest_waist_measurement, 'regular fit')

            # If body type fit is more specific than chest/waist measurement fit, use body type fit
            if body_type in ['slim', 'athletic']:
                return body_fit_rules[0] 
            else:
                return chest_waist_fit

        def is_shirt_suitable(self, body_type, skin_tone, chest_waist_measurement, shirt_or_tshirt, shirt_style, fabric_type, color, sleeve_type, design, collar_type, pocket_type, occasion, season, day_or_night):
            # Get shirt fit based on body and chest/waist measurement
            shirt_fit = self.get_shirt_fit(body_type, chest_waist_measurement)

            # if color=='White' and fabric_type=='Cotton' and occasion=='Casual':
            #     return f"Suitable. Suggested Fit: {shirt_fit}"

            # Check Color Suitability for Skin Tone
            color_rules = self.skin_tone_color_rules.get(skin_tone, [])
            if color not in color_rules:
                
                return f"Not Suitable. Suggested Fit: {shirt_fit}"

            # Check Fabric Suitability for Season
            season_rules = self.season_rules.get(season, [])
            if fabric_type not in season_rules:
                
                return f"Not Suitable. Suggested Fit: {shirt_fit}"

            # Check Shirt Design Suitability for Occasion
            design_rules = self.shirt_design_rules.get(design, [])
            if occasion not in design_rules:
                
                return f"Not Suitable. Suggested Fit: {shirt_fit}"

            # Check Collar Type Suitability for Shirt Style and Occasion
            collar_rules = self.shirt_collars_rules.get(collar_type, [])
            if occasion not in collar_rules:
                
                return f"Not Suitable. Suggested Fit: {shirt_fit}"

            # Check Pocket Type Suitability for Shirt Style
            # pocket_rules = self.pocket_rules.get(pocket_type, [])
            # if shirt_style not in pocket_rules:
            #     print("hi")
            #     return f"Not Suitable. Suggested Fit: {shirt_fit}"

            # Check Time of Day Suitability
            time_of_day_rules = self.time_of_day_rules.get(day_or_night, [])
            if shirt_style not in time_of_day_rules:
                print("hi")
                return f"Not Suitable. Suggested Fit: {shirt_fit}"

            # Check Sleeve Type Suitability for Season
            if season == 'summer' and sleeve_type == 'full' and shirt_style == 'sweatshirt':
                return f"Not Suitable. Suggested Fit: {shirt_fit}"

            if season == 'winter' and shirt_style == 'polo' and sleeve_type == 'half':
                return f"Not Suitable. Suggested Fit: {shirt_fit}"

            # If all checks pass, return suitable with fit type
            return f"Suitable. Suggested Fit: {shirt_fit}"



    # Create the checker object
    checker = ShirtSuitabilityChecker()

    # Example input attributes
    body_type = body_type
    skin_tone = skin_tone
    chest_waist_measurement = chest_waist_measurement
    shirt_or_tshirt = decoded_shirt_attributes['shirt_t']
    shirt_style = decoded_shirt_attributes['shirt_style']
    fabric_type = decoded_shirt_attributes['fabric_type']
    color = decoded_shirt_attributes['color']
    sleeve_type = decoded_shirt_attributes['sleeves_type']
    design = decoded_shirt_attributes['design']
    collar_type = decoded_shirt_attributes['collor_type']
    pocket_type = decoded_shirt_attributes['pocket']
    occasion = occasion
    season = season
    day_or_night = day_or_night

    # Get shirt suitability and fit type
    result = checker.is_shirt_suitable(body_type, skin_tone, chest_waist_measurement, shirt_or_tshirt, shirt_style, fabric_type, color, sleeve_type, design, collar_type, pocket_type, occasion, season, day_or_night)
    # print(result)

    print(shirt_or_tshirt,shirt_style,fabric_type,color,sleeve_type,design,collar_type,pocket_type,occasion)

    if "Not Suitable" in result:
        st.error("The clothing is NOT suitable!")

    else:
        st.success(result)


else:
    st.warning("Please upload an image to proceed.")


