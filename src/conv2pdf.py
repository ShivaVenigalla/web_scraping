import pdfkit
import os
import hashlib
import json

# Function to generate a unique filename from a URL and return the filename and URL hash
def generate_filename(url):
    max_length = 255  # Maximum allowed filename length
    hash_length = 16  # Length of the hash value

    # Generate a hash from the URL
    url_hash = hashlib.sha256(url.encode()).hexdigest()[:hash_length]

    # Generate a sanitized version of the URL to avoid special characters
    sanitized_url = url.replace('https://', '').replace('/', '_')[:max_length - hash_length - 5]

    # Combine the sanitized URL and hash to create a filename
    filename = sanitized_url + "_" + url_hash + ".pdf"

    return filename, url_hash  # Return the filename and URL hash

# Rest of your code remains the same
# ...

# Function to convert a URL to PDF
def convert_url_to_pdf(url, output_dir):
    try:
        output_filename, url_hash = generate_filename(url)
        output_fullpath = os.path.join(output_dir, output_filename)  # Full path to the PDF in the "pdf" directory
        pdfkit.from_url(url, output_fullpath)
        print(f"Converted {url} to {output_fullpath}")
        # Store the mapping of hash value to URL in a dictionary
        url_mapping[url_hash] = url
        # Save the mapping to a file
        save_url_mapping(output_dir, url_mapping)
    except Exception as e:
        print(f"Error converting {url} to PDF: {str(e)}")
        not_reachable_filename = os.path.join(output_dir, f"{output_filename}_not_reachable.txt")
        with open(not_reachable_filename, 'w') as not_reachable_file:
            not_reachable_file.write(f"URL not reachable: {url}")


# Function to save the URL-to-hash mapping to a file
def save_url_mapping(output_dir, mapping):
    mapping_filename = os.path.join(output_dir, "url_mapping.json")
    with open(mapping_filename, 'w') as mapping_file:
        json.dump(mapping, mapping_file)

# Function to load the URL-to-hash mapping from a file
def load_url_mapping(output_dir):
    mapping_filename = os.path.join(output_dir, "url_mapping.json")
    if os.path.exists(mapping_filename):
        with open(mapping_filename, 'r') as mapping_file:
            return json.load(mapping_file)
    return {}

# Main function
def main(input_file, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    global url_mapping
    url_mapping = load_url_mapping(output_dir)

    with open(input_file, 'r') as urls_file:
        urls = urls_file.read().splitlines()

    for url in urls:
        convert_url_to_pdf(url, output_dir)

if __name__ == "__main__":
    input_file = "ftouch2.txt"  # Change this to the path of your input file
    output_directory = "pdf"  # Change this to the desired output directory
    main(input_file, output_directory)

