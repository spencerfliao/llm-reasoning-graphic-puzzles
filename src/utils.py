import json
import os
import shutil
import numpy as np
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.patches as patches


def load_json(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)


def add_margin(pil_img, top, right, bottom, left, color):
    width, height = pil_img.size
    new_width = width + right + left
    new_height = height + top + bottom
    result = Image.new(pil_img.mode, (new_width, new_height), color)
    result.paste(pil_img, (left, top))
    return result


def delete_directory(path):
    try:
        shutil.rmtree(path)
    except Exception as e:
        print(f"Error: {e}")


def generate_image(array, file_path, title):
    color_map = {
        0: '#000000',  # White
        1: '#0000FF',  # Blue
        2: '#FF0000',  # Red
        3: '#00FF00',  # Green
        4: '#FFFF00',  # Yellow
        5: '#808080',  # Gray
        6: '#FF00FF',  # Magenta
        7: '#e3a77a',  # Orange
        8: '#aacce0',  # Cyan
        9: '#a57279',  # Maroon
    }
    array = np.array(array)
    n_rows, n_cols = array.shape
    fig, ax = plt.subplots(figsize=(n_cols, n_rows))
    ax.set_xlim(0, n_cols)
    ax.set_ylim(0, n_rows)
    plt.gca().invert_yaxis()
    ax.axis('off')
    plt.title(title, pad=20, fontsize=40)
    for i in range(n_rows):
        for j in range(n_cols):
            color = color_map[array[i, j]]
            rect = patches.Rectangle((j, i), 1, 1, linewidth=1, edgecolor='w', facecolor=color)
            ax.add_patch(rect)
    plt.savefig(file_path, format='png', bbox_inches='tight', pad_inches=1)
    plt.close()


def generate_and_combine_images(data, output_dir, filename, temp_dir='./temp'):
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    combined_images = []
    margin = 70
    background_color = '#808080'
    for dataset in ['train', 'test']:
        dataset_images = []
        count = 0
        for idx, example in enumerate(data[dataset]):
            input_file_path = os.path.join(temp_dir, f"{dataset}_input_{idx}.png")
            output_file_path = os.path.join(temp_dir, f"{dataset}_output_{idx}.png")

            # Generate images
            generate_image(example['input'], input_file_path, f"{dataset.capitalize()} Input {count}")
            generate_image(example['output'], output_file_path, f"{dataset.capitalize()} Output {count}")
            input_image = Image.open(input_file_path)
            output_image = Image.open(output_file_path)


            # Add margin around images
            input_image_with_margin = add_margin(input_image, margin, margin, margin, margin, background_color)
            output_image_with_margin = add_margin(output_image, margin, margin, margin, margin, background_color)

            # Combine the input and output images horizontally
            total_width = input_image_with_margin.width + output_image_with_margin.width + margin
            combined_height = max(input_image_with_margin.height, output_image_with_margin.height)
            combined_io = Image.new('RGB', (total_width, combined_height), background_color)
            combined_io.paste(input_image_with_margin, (0, 0))
            combined_io.paste(output_image_with_margin, (input_image_with_margin.width + margin, 0))

            dataset_images.append(combined_io)
            count += 1

        # Combine all images for the dataset vertically
        total_height = sum(image.height for image in dataset_images) + (margin * (len(dataset_images) - 1))
        max_width = max(image.width for image in dataset_images)
        combined_dataset_image = Image.new('RGB', (max_width, total_height), background_color)
        y_offset = 0
        for image in dataset_images:
            combined_dataset_image.paste(image, (0, y_offset))
            y_offset += image.height + margin

        combined_images.append(combined_dataset_image)

    # Combine train and test images vertically
    total_height = sum(image.height for image in combined_images) + margin
    max_width = max(image.width for image in combined_images)
    final_image = Image.new('RGB', (max_width, total_height), background_color)
    y_offset = 0
    for image in combined_images:
        final_image.paste(image, (0, y_offset))
        y_offset += image.height + margin

    # Save the final combined image
    final_image_path = os.path.join(output_dir, f'{filename}.png')
    final_image.save(final_image_path)

    delete_directory(temp_dir)
    return final_image_path


def get_metadata(input_data):
    metadata = {
        "input_n_rows": len(input_data['train'][0]['input']),
        "input_n_cols": len(input_data['train'][0]['input'][0]),
        "output_n_rows": len(input_data['train'][0]['output']),
        "output_n_cols": len(input_data['train'][0]['output'][0]),
    }
    return metadata

if __name__ == '__main__':
    output_dir = './data/images'
    training_dir = './data/training'
    evaluation_dir = './data/evaluation'
    # Read all the files in the training directory
    training_metadata = {}
    evaluation_metadata = {}
    count = 0
    for filename in os.listdir(training_dir):
        print(f"Processing file {count}/{len(os.listdir(training_dir))}")
        if filename.endswith('.json'):
            file_path = os.path.join(training_dir, filename)
            data = load_json(file_path)
            generate_and_combine_images(data, f"{output_dir}/training", filename.split('.')[0])
            training_metadata[filename.split('.')[0]] = get_metadata(data)
        count += 1
    
    # Read all the files in the evaluation directory
    count = 0
    for filename in os.listdir(evaluation_dir):
        print(f"Processing file {count}/{len(os.listdir(evaluation_dir))}")
        if filename.endswith('.json'):
            file_path = os.path.join(evaluation_dir, filename)
            data = load_json(file_path)
            generate_and_combine_images(data, f"{output_dir}/evaluation", filename.split('.')[0])
            evaluation_metadata[filename.split('.')[0]] = get_metadata(data)
        count += 1
    # Save metadata as pandas dataframe
    training_metadata_df = pd.DataFrame(training_metadata).T
    evaluation_metadata_df = pd.DataFrame(evaluation_metadata).T
    training_metadata_df.to_csv(f"{output_dir}/training_metadata.csv")
    evaluation_metadata_df.to_csv(f"{output_dir}/evaluation_metadata.csv")
