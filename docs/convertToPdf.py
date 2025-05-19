import pdfkit
import os

def process_directory(directory):
    # Walk through directory and subdirectories
    for root, dirs, files in os.walk(directory):
        for file in files:
            # Check if file has .adoc extension
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                out_file = file.replace('.html', '.pdf')
                convert_html_to_pdf(file_path, out_file)

def convert_html_to_pdf(html_path, pdf_path):
    try:
        pdfkit.from_file(html_path, pdf_path)
        print(f"PDF creato con successo: {pdf_path}")
    except Exception as e:
        print(f"Errore durante la conversione di {pdf_path}: {str(e)}")


def move_pdfs_to_directory(target_dir):
    # Create target directory if it doesn't exist
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    
    # Walk through current directory and subdirectories
    for root, dirs, files in os.walk(os.getcwd()):
        for file in files:
            if file.endswith('.pdf'):
                source_path = os.path.join(root, file)
                target_path = os.path.join(target_dir, file)
                try:
                    os.rename(source_path, target_path)
                    print(f"Moved {file} to {target_dir}")
                except Exception as e:
                    print(f"Error moving {file}: {str(e)}")

if __name__ == "__main__":
    current_dir = os.getcwd()
    process_directory(current_dir)
    move_pdfs_to_directory(os.path.join(current_dir, 'pdfdocs'))