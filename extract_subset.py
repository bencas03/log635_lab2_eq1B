import os
import shutil
import random
from pathlib import Path

def split_stratified_dataset(source_dir, subset_dir, remaining_dir, fraction=1/6):
    """
    Extracts a stratified random subset from a nested folder structure 
    by splitting all files into two separate destination folders (subset and remaining),
    preserving category proportions and folder hierarchy.
    """
    source_path = Path(source_dir)
    subset_path = Path(subset_dir)
    remaining_path = Path(remaining_dir)
    
    image_extensions = {'.jpg'}
    
    if not source_path.exists():
        print(f"Error: Source directory '{source_dir}' does not exist.")
        return

    total_subset = 0
    total_remaining = 0
    total_images = 0

    print("Starting dataset split...")
    
    # Iterate through the Type folders
    for type_dir in source_path.iterdir():
        if type_dir.is_dir():
            # Iterate through the Sub-type folders inside each Type folder
            for subtype_dir in type_dir.iterdir():
                if subtype_dir.is_dir():
                    # Collect all valid image files in the sub-type folder
                    images = [f for f in subtype_dir.iterdir() if f.is_file() and f.suffix.lower() in image_extensions]
                    
                    if not images:
                        continue
                        
                    num_total = len(images)
                    total_images += num_total
                    
                    # Calculate sample size
                    sample_size = max(1, round(num_total * fraction))
                    
                    # Randomly sample images without replacement for the subset
                    selected_subset_images = set(random.sample(images, min(sample_size, num_total)))
                    
                    # Create matching output directory structures for both folders
                    dest_subset_subtype = subset_path / type_dir.name / subtype_dir.name
                    dest_remaining_subtype = remaining_path / type_dir.name / subtype_dir.name
                    
                    dest_subset_subtype.mkdir(parents=True, exist_ok=True)
                    dest_remaining_subtype.mkdir(parents=True, exist_ok=True)
                    
                    # Move images into either subset or remaining folder
                    for img in images:
                        if img in selected_subset_images:
                            shutil.move(str(img), str(dest_subset_subtype / img.name))
                            total_subset += 1
                        else:
                            shutil.move(str(img), str(dest_remaining_subtype / img.name))
                            total_remaining += 1
                            
                    num_subset_moved = len(selected_subset_images)
                    num_remaining_moved = num_total - num_subset_moved
                    print(f"[{type_dir.name} / {subtype_dir.name}] Subset: {num_subset_moved} | Remaining: {num_remaining_moved}")

    print("\n--- Split Complete ---")
    print(f"Total processed images: {total_images}")
    print(f"Total subset images: {total_subset}")
    print(f"Total remaining images: {total_remaining}")
    print(f"Subset folder: {subset_path.absolute()}")
    print(f"Remaining folder: {remaining_path.absolute()}")

if __name__ == "__main__":
    print("=== Dataset Stratified Splitter (Two Folders) ===")
    source = "EnsembleA_H2020"
    subset_out = "Ensemble_B"
    remaining_out = "Ensemble_entrainement"
    
    fraction_input = input("Enter the fraction of images for the subset (default is 1/5 or 20%): ").strip()
    fraction = float(fraction_input) if fraction_input else 1/5
    
    split_stratified_dataset(source, subset_out, remaining_out, fraction)