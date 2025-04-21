import os
import shutil

def bulk_rename_and_copy(src_folder, dest_folder, prefix="", suffix="", start_index=1, rename_type="default"):
    try:
        # Create destination folder if it doesn't exist
        if not os.path.exists(dest_folder):
            os.makedirs(dest_folder)

        files = os.listdir(src_folder)
        files.sort() 

        count = start_index
        for file in files:
            src_path = os.path.join(src_folder, file)

            if os.path.isfile(src_path):
                file_name, file_ext = os.path.splitext(file)

                if rename_type == "default":
                    new_name = f"{prefix}{count}{suffix}{file_ext}"
                elif rename_type == "uppercase":
                    new_name = f"{prefix}{file_name.upper()}{suffix}{file_ext}"
                elif rename_type == "lowercase":
                    new_name = f"{prefix}{file_name.lower()}{suffix}{file_ext}"
                else:
                    new_name = f"{prefix}{count}{suffix}{file_ext}"

                dest_path = os.path.join(dest_folder, new_name)
                shutil.copy2(src_path, dest_path)  
                print(f"Copied & Renamed: {file} ➝ {new_name}")
                count += 1

        print("\n✅ All files renamed and copied successfully!")

    except Exception as e:
        print(f"❌ Error: {e}")

source_folder = "image_folder"
destination_folder = "test_folder"
bulk_rename_and_copy(src_folder=source_folder, dest_folder=destination_folder, prefix="Renamed_", start_index=1, rename_type="default")
