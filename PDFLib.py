import PyPDF2
from PyPDF2 import PdfReader, PdfWriter, PdfMerger
import os
import traceback
from PIL import Image

version = "0.0.2"
debugMode = False


def set_debugMode(mode: bool = False):
  """This function sets the debugMode to True or False.
  
     Args:
         mode(bool): debugMode (default False).
  
      Returns:
          nothing:
  """
  global debugMode
  if mode == True:
    debugMode = mode
  else:
    debugMode = False


def info():
  """This function provides information about the entire library."""
  print("""
  \033[32mPDFLib by Rosario Moscato (rosario.moscato@outlook.com)
  PDFLib version: {} (relies on PyPDF2 >= 3.0.1)\033[0m
  PyPDF current version:  {}
  Pillow current version: {}
  \033[31mLicense: MIT\033[0m""".format(version, PyPDF2.__version__, Image.__version__))


def get_metadata(pdf_file):
  """This function gets all metadata from a pdf file.
     It's possible to print them one by one with '.author', '.title', etc.
  
      Args:
          pdf_file(str): pdf file name (with path if needed).
  
      Returns:
          info(dict): dictionay of pdf metadata (author, title, etc.)
  """
  try:
    with open(pdf_file, 'rb') as f:
      reader = PdfReader(f)
      info = reader.metadata
      return info
  except Exception:
    print("ERROR: Unable to load pdf file")
    if debugMode:
      print(traceback.format_exc())


def extract_text(pdf_file):
  """This function extracts all the text from a pdf file.
  
     Args:
         pdf_file(str): pdf file name (with path if needed).
  
     Returns:
         text(str): all text contained in the pdf file.
  """
  try:
    with open(pdf_file, 'rb') as f:
      reader = PdfReader(f)
      results = []
      for i in range (0, len(reader.pages)):
        selected_page = reader.pages[i]
        text = selected_page.extract_text()
        results.append(text)
      return ' '.join(results)
  except Exception:
    print("ERROR: Unable to load pdf file")
    if debugMode:
      print(traceback.format_exc())


def pages_splitter(pdf_file):
  """This function splits a pdf file into many different files,
      each of them from a single page.
      
     Args:
         pdf_file(str): pdf file name (with path if needed).
  
     Returns:
         nothing: this function creates a different pdf file for each starting page.    
      
  """
  try:
    with open(pdf_file, 'rb') as f:
      reader = PdfReader(f)
      #get all pages
      for page_num in range (0, len(reader.pages)):
        selected_page = reader.pages[page_num]
        writer = PdfWriter()
        writer.add_page(selected_page)
        filename = os.path.splitext(pdf_file)[0]
        output_filename = f"{filename}_page_{page_num + 1}.pdf"
        #save and compile to pdf
        with open(output_filename, 'wb') as out:
          writer.write(out)
  except Exception:
    print("ERROR: Unable to load pdf file")
    if debugMode:
      print(traceback.format_exc())


def fromto_splitter(pdf_file, start_page: int = 0, stop_page: int = 0):
  """This function puts all the pages from selected starting and ending page
     into a unique new pdf file.
     
     Args:
         pdf_file(str): pdf file name (with path if needed).
         start_page(int): starting page of the splitting.
         stop_page(int): ending page of the splitting.
  
     Returns:
         nothing: this function creates a pdf file from starting to ending page.      
  """
  try:
    with open(pdf_file, 'rb') as f:
      reader = PdfReader(f)
      writer = PdfWriter()
      for page_num in range (start_page-1, stop_page):
        selected_page = reader.pages[page_num]
        writer.add_page(selected_page)
        filename = os.path.splitext(pdf_file)[0]
        output_filename = f"{filename}_from_{start_page}_to_{stop_page}.pdf"
      with open(output_filename, 'wb') as out:
        writer.write(out)
  except Exception:
    print("ERROR: pls check your arguments")
    if debugMode:
      print(traceback.format_exc())


def last_page(pdf_file):
  """This function gets the last page of a pdf file.
  
     Args:
         pdf_file(str): pdf file name (with path if needed).
  
     Returns:
         nothing: this function creates a pdf containing only last page of original document.  
  """
  try:
    with open(pdf_file, 'rb') as f:
      reader = PdfReader(f)
      writer = PdfWriter()
      selected_page = reader.pages[len(reader.pages)-1]
      writer.add_page(selected_page)
      filename = os.path.splitext(pdf_file)[0]
      output_filename = f"{filename}_last_page.pdf"
      with open(output_filename, 'wb') as out:
        writer.write(out)
  except Exception:
    print("ERROR: Unable to load pdf file")
    if debugMode:
      print(traceback.format_exc())


def pdf_files_collector(parent_folder: str):
  """This function gets all pdf files in a defined folder.
  
     Args:
         parent_folder(str): folder name (with path if needed).
  
     Returns:
         target_files(list): a list of all pdf files in the specified folder.
  """
  try:
    target_files = []
    for path, subdirs, files in os.walk(parent_folder):
      for name in files:
        if name.endswith(".pdf"):
          target_files.append(os.path.join(path, name))
    return target_files
  except Exception:
    print("ERROR: pls check your arguments")
    if debugMode:
      print(traceback.format_exc())


def pdf_list_merger(pdfs_list, output_filename = "merged_file.pdf"):
  """This function merges all pdf files from a list into a unique final pfd file.
  
     Args:
         pdfs_list(list): a list of pdf files to be merged.
         output_filename(str): the name of the output file (default="merged_file.pdf").
  
     Returns:
         nothing: this function merges all the starting files into a unique final pdf.  
  """
  try:
    merger = PdfMerger()
    with open(output_filename, 'wb') as f:
      for file in pdfs_list:
        merger.append(file)
      merger.write(f)
  except Exception:
    print("ERROR: pls check your arguments")
    if debugMode:
      print(traceback.format_exc())


def pdf_folder_merger(parent_folder, output_filename = "merged_file.pdf"):
  """This function merges all pdf files contained in a folder into a unique final pfd file.
  
     Args:
         parent_folder(str): folder name (with path if needed).
         output_filename(str): the name of the output file (default="merged_file.pdf").
  
     Returns:
         nothing: this function merges all the starting files into a unique final pdf.  
  """
  try:
    pdfs_list = pdf_files_collector(parent_folder)
    merger = PdfMerger()
    with open(output_filename, 'wb') as f:
      for file in pdfs_list:
        merger.append(file)
      merger.write(f)
  except Exception:
    print("ERROR: pls check your arguments")
    if debugMode:
      print(traceback.format_exc())    


def pdf_rotate(pdf_file, page_num: int, rotation: int = 90):
  """This function rotate a specific page of a pdf file with a specific angle.
  
     Args:
         pdf_file(str): pdf file name (with path if needed).
         page_num(int): number of the page to be rotated.
         rotation(int): degrees of rotation.
  
     Returns:
         nothing: this function creates a pdf file with the selected page rotated.     
  """
  try:
    with open(pdf_file, 'rb') as f:
      reader = PdfReader(f)
      writer = PdfWriter()
      #rotate
      writer.add_page(reader.pages[page_num-1].rotate(rotation))
      filename = os.path.splitext(pdf_file)[0]
      output_filename = f"{filename}_{rotation}_rotated_page.pdf"
      with open(output_filename, 'wb') as out:
        writer.write(out)
  except Exception:
    print("ERROR: pls check your arguments")
    if debugMode:
      print(traceback.format_exc())    


def pdf_images_extractor(pdf_file):
  """This function gets all images contained in a pdf file.
  
     Args:
         pdf_file(str): pdf file name (with path if needed).
  
     Returns:
         nothing: this function creates a jpg file for each image contained in the pdf.  
  """
  try:
    with open(pdf_file, 'rb') as f:
      reader = PdfReader(f)
      for page_num in range (0, len(reader.pages)):
        selected_page = reader.pages[page_num]
        for img_file_obj in selected_page.images:
          with open(img_file_obj.name, 'wb') as out:
            out.write(img_file_obj.data)
  except Exception:
    print("ERROR: Unable to load pdf file")
    if debugMode:
      print(traceback.format_exc())


def img2pdf(image_file):
  """This function converts an image into a pdf file.
  
     Args:
         image_file(str): image file name (with path if needed).
  
     Returns:
         nothing: this function creates a pdf file of the specified image.  
  """
  try:
    img = Image.open(image_file)
    img = img.convert("RGB")
    filename = f"{os.path.splitext(image_file)[0]}.pdf"
    img.save(filename)
  except Exception:
    print("ERROR: Unable to load image file")
    if debugMode:
      print(traceback.format_exc())

