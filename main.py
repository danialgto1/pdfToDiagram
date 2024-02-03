import base64
from PIL import Image
from create_diagram import create_requirement_diagrams
from pdf_reader import process_pdf
import io
import streamlit as st
from text_reader import process_text , divide_text
from dotenv import load_dotenv


def main():
    st.title("Text to Diagrams")
    menu = [ "PDF", "TEXT"]
    choice = st.sidebar.selectbox("Select File Type", menu)
    if choice == "PDF":
        handle_pdf()
    
    if choice == "TEXT":
        handle_text()

def handle_text():
    st.subheader("Text Input")
    # Allow the user to input text
    text_input = st.text_area("Enter Text:")
    if st.button("Process Text"):
        text_list = divide_text(text_input)
        st.write(f"your text is processing in {len(text_list)} stage(s); each stage longs about 1 minute ")
        # Process text and display the result
        json_result = process_text(st ,  text_list)
        show_diagram(st , json_result)
        

def handle_pdf():
  st.subheader("PDF")
  pdf_file = st.file_uploader("Upload PDF", type=["pdf"])
  if pdf_file is not None:
    # Allow the user to input page range
    page_range = st.text_input(
        "Enter Page Range (e.g., 1-5) it is contain maximum on section:")
    if page_range:
      try:
        start_page, end_page = map(int, page_range.split('-'))
      except ValueError:
        st.error(
            "Invalid page range format. Please use the format 'start-end'.")
        return
      st.write(f"Processing pages {start_page} to {end_page}...")

      # Process PDF and get a list of PNG base64-encoded images
      json_result = process_pdf(pdf_file, start_page, end_page)
      show_diagram(st , json_result)

def show_diagram(st , json_result):
    png_images_base64 = create_requirement_diagrams(json_result)

    # Display each PNG image using Markdown
    for idx, png_base64 in enumerate(png_images_base64):
        # Add padding if needed
        png_base64_padded = png_base64 + '=' * ((4 - len(png_base64) % 4) % 4)
        png_data = base64.b64decode(png_base64_padded)
        image = Image.open(io.BytesIO(png_data))
        st.image(image, caption=f"Diagram {idx + 1}", use_column_width=True)


if __name__ == "__main__":
    load_dotenv()
    main()