import io
import os
from PIL import Image

def process_rrb_signature(input_path, output_path, target_kb=45):
    with Image.open(input_path) as img:
        img = img.convert("RGB")
        
        resized_img = img.resize((140, 60), Image.Resampling.LANCZOS)
        
        buffer = io.BytesIO()
        resized_img.save(buffer, format="JPEG", quality=100)
        jpeg_bytes = buffer.getvalue()

    target_bytes = target_kb * 1024

    if len(jpeg_bytes) < target_bytes:
        padding_needed = target_bytes - len(jpeg_bytes)
        final_bytes = jpeg_bytes + (b"\x00" * padding_needed)
    else:
        final_bytes = jpeg_bytes

    with open(output_path, "wb") as f:
        f.write(final_bytes)

    actual_kb = os.path.getsize(output_path) / 1024
    with Image.open(output_path) as check_img:
        width, height = check_img.size

    print(f"File saved: {output_path}")
    print(f"Dimensions: {width}px x {height}px")
    print(f"File Size : {actual_kb:.2f} KB")

if __name__ == "__main__":
    input_file = input("Enter input file name(with extension) : ")
    output_file = input("Enter output file name (with extension): ")
    tar_kb=input("Enter target size in kb : ")
    process_rrb_signature(input_file, output_file, target_kb=tar_kb)