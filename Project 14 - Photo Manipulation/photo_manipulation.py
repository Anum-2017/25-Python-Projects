from PIL import Image, ImageEnhance, ImageFilter
import os

# Input images list
image_paths = [
    r"C:\Users\anumk\Desktop\25 Python Projects\Project 14 - Photo Manipulation\input\city.jpg",
    r"C:\Users\anumk\Desktop\25 Python Projects\Project 14 - Photo Manipulation\input\lake.jpeg"
]

# Output directory
output_dir = r"C:\Users\anumk\Desktop\25 Python Projects\Project 14 - Photo Manipulation\output"
os.makedirs(output_dir, exist_ok=True)

# User inputs
brightness_factor = float(input("Enter the brightness factor (e.g., 1.5 for brighter, 0.5 for darker): "))
contrast_factor = float(input("Enter the contrast factor (e.g., 2 for higher contrast, 0.5 for lower contrast): "))
blur_radius = float(input("Enter the blur radius (e.g., 3 for strong blur, 1 for light blur): "))

# Define functions
def adjust_brightness(image, factor):
    enhancer = ImageEnhance.Brightness(image)
    return enhancer.enhance(factor)

def adjust_contrast(image, factor):
    enhancer = ImageEnhance.Contrast(image)
    return enhancer.enhance(factor)

def apply_blur(image, radius):
    return image.filter(ImageFilter.GaussianBlur(radius=radius))

# Process each image
for img_path in image_paths:
    image = Image.open(img_path)
    base_name = os.path.splitext(os.path.basename(img_path))[0]  # Get name without extension

    # Apply transformations
    image_bright = adjust_brightness(image, brightness_factor)
    image_contrast = adjust_contrast(image, contrast_factor)
    image_blur = apply_blur(image, blur_radius)

    # Combined version
    image_combined = adjust_brightness(image, brightness_factor)
    image_combined = adjust_contrast(image_combined, contrast_factor)

    # Save results
    image_bright.save(os.path.join(output_dir, f'{base_name}_bright.jpg'))
    image_contrast.save(os.path.join(output_dir, f'{base_name}_contrast.jpg'))
    image_blur.save(os.path.join(output_dir, f'{base_name}_blur.jpg'))
    image_combined.save(os.path.join(output_dir, f'{base_name}_combined.jpg'))

    # Optional: Show images
    image_combined.show()

print("✅ All images processed and saved successfully!")
