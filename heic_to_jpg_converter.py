
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import pillow_heif
import os
import logging

# Set up logging
logging.basicConfig(filename='heic_conversion.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def is_valid_heic(file_path):
    """
    Check if a file is a valid HEIC file by examining its header.
    HEIC files should start with a 'ftyp' box.
    """
    try:
        # Check if file exists and is readable
        if not os.path.exists(file_path):
            logging.warning(f"File does not exist: {file_path}")
            return False
            
        # Check file size (HEIC files are typically not empty)
        file_size = os.path.getsize(file_path)
        if file_size < 12:
            logging.warning(f"File is too small to be HEIC: {file_path} ({file_size} bytes)")
            return False
            
        with open(file_path, 'rb') as f:
            # Read the first 12 bytes to check for the 'ftyp' box
            header = f.read(12)
            if len(header) < 12:
                logging.warning(f"Could not read enough bytes from file: {file_path}")
                return False
            
            # Check if it contains the 'ftyp' signature
            # The format is: [4-byte length][4-byte type='ftyp'][4-byte brand]
            if header[4:8] == b'ftyp':
                logging.info(f"Valid HEIC header found in: {file_path}")
                return True
            else:
                logging.warning(f"Invalid HEIC header in: {file_path}")
                return False
    except Exception as e:
        logging.error(f"Error validating HEIC file {file_path}: {str(e)}")
        return False


def is_jpeg_file(file_path):
    """
    Check if a file is a JPEG file by examining its header.
    """
    try:
        if not os.path.exists(file_path):
            return False
            
        with open(file_path, 'rb') as f:
            header = f.read(10)
            return header.startswith(b'\xFF\xD8\xFF')
    except:
        return False

def get_file_format_info(file_path):
    """
    Get information about the file format for better error reporting.
    """
    try:
        if not os.path.exists(file_path):
            return "File does not exist"
            
        file_size = os.path.getsize(file_path)
        if file_size == 0:
            return "File is empty (0 bytes)"
            
        with open(file_path, 'rb') as f:
            # Read first 20 bytes to determine file type
            header = f.read(20)
            
            # Check for common file signatures
            if header.startswith(b'\xFF\xD8\xFF'):
                # Check for more specific JPEG markers
                if header[6:10] == b'JFIF':
                    return "File is JPEG format (JFIF), not HEIC - File extension may be incorrect"
                elif header[6:10] == b'Exif':
                    return "File is JPEG format (EXIF), not HEIC - File extension may be incorrect"
                else:
                    return "File is JPEG format, not HEIC - File extension may be incorrect"
            elif header.startswith(b'\x89PNG\r\n\x1a\n'):
                return "File is PNG format, not HEIC - File extension may be incorrect"
            elif header.startswith(b'RIFF') and b'WEBP' in header:
                return "File is WebP format, not HEIC - File extension may be incorrect"
            elif header[4:8] == b'ftyp':
                # This looks like a valid HEIC file
                brand = header[8:12].decode('ascii', errors='ignore')
                return f"Valid HEIC file (brand: {brand})"
            elif b'ftyp' in header:
                # 'ftyp' is somewhere in the header but not at the right position
                return "File contains 'ftyp' but may be corrupted or not a valid HEIC"
            else:
                # Try to identify what it might be
                if header.startswith(b'<?xml'):
                    return "File appears to be XML format"
                elif header.startswith(b'{') or header.startswith(b'['):
                    return "File appears to be JSON format"
                elif header.startswith(b'%PDF'):
                    return "File is PDF format"
                else:
                    # Check if it's mostly text
                    try:
                        header.decode('utf-8')
                        return "File appears to be text format"
                    except UnicodeDecodeError:
                        return "File is not a recognized format"
    except Exception as e:
        return f"Error reading file: {str(e)}"

def convert_heic_to_jpg(heic_path, jpg_path):
    # Log the conversion attempt
    logging.info(f"Attempting to convert: {heic_path} -> {jpg_path}")
    
    # First check if the file is a valid HEIC file
    if not is_valid_heic(heic_path):
        # Get more detailed information about why the file is invalid
        format_info = get_file_format_info(heic_path)
        logging.warning(f"Invalid HEIC file {heic_path}: {format_info}")
        
        # Special handling for JPEG files with wrong extension
        filename = os.path.basename(heic_path)
        if "not HEIC" in format_info and "JPEG" in format_info:
            try:
                # If it's actually a JPEG file, just copy it with the correct extension
                with open(heic_path, 'rb') as src, open(jpg_path, 'wb') as dst:
                    dst.write(src.read())
                logging.info(f"File was already JPEG format, copied with correct extension: {heic_path} -> {jpg_path}")
                messagebox.showinfo("Already JPEG", 
                                   f"The file {filename} was already in JPEG format.\n"
                                   f"It has been copied to {os.path.basename(jpg_path)} with the correct extension.")
                return True
            except Exception as copy_error:
                logging.error(f"Failed to copy JPEG file {heic_path}: {str(copy_error)}")
                messagebox.showerror("Copy Error", 
                                   f"Failed to copy {filename}:\n\n"
                                   f"The file is already in JPEG format but could not be copied.\n"
                                   f"Error: {str(copy_error)}")
                return False
        elif "not HEIC" in format_info:
            messagebox.showerror("Format Mismatch", 
                               f"Failed to convert {filename}:\n\n"
                               f"The selected file is actually {format_info}.\n"
                               f"If this is the format you want, you don't need conversion.\n"
                               f"If you intended to convert a HEIC file, please check the file.")
        else:
            messagebox.showerror("Invalid File", 
                               f"Failed to convert {filename}:\n\n"
                               f"{format_info}.\n\n"
                               f"Please ensure you've selected a valid HEIC file for conversion.")
        return False
        
    try:
        heif_file = pillow_heif.read_heif(heic_path)
        image = Image.frombytes(
            heif_file.mode,
            heif_file.size,
            heif_file.data,
            "raw",
            heif_file.mode,
            heif_file.stride,
        )
        image.save(jpg_path, "JPEG")
        logging.info(f"Successfully converted: {heic_path} -> {jpg_path}")
        return True
    except Exception as e:
        # Try fallback method using Pillow directly
        try:
            logging.warning(f"Primary conversion failed for {heic_path}, trying fallback method: {str(e)}")
            # Attempt to open with Pillow directly (newer versions may support HEIC)
            image = Image.open(heic_path)
            image.save(jpg_path, "JPEG")
            logging.info(f"Successfully converted using fallback method: {heic_path} -> {jpg_path}")
            return True
        except Exception as fallback_e:
            # Provide more detailed error information
            format_info = get_file_format_info(heic_path)
            logging.error(f"Both conversion methods failed for {heic_path}: {format_info} - Primary: {str(e)}, Fallback: {str(fallback_e)}")
            
            # Create a more user-friendly error message
            filename = os.path.basename(heic_path)
            error_msg = f"Failed to convert {filename}:\n\n"
            
            if "not HEIC" in format_info:
                error_msg += f"The selected file is actually {format_info}.\n"
                error_msg += f"If this is the format you want, you don't need conversion.\n\n"
            else:
                error_msg += f"File format issue: {format_info}\n\n"
                
            error_msg += f"Technical details:\n"
            error_msg += f"- Primary error: {str(e)}\n"
            error_msg += f"- Fallback error: {str(fallback_e)}\n\n"
            error_msg += "Please check the file and try again."
            
            messagebox.showerror("Conversion Error", error_msg)
            return False

def select_files():
    files = filedialog.askopenfilenames(
        title="Select HEIC files", 
        filetypes=[("HEIC files", "*.heic *.HEIC")]
    )
    entry_files.delete(0, tk.END)
    entry_files.insert(0, ";".join(files))

def select_output_dir():
    output_dir = filedialog.askdirectory(title="Select Output Directory")
    entry_output_dir.delete(0, tk.END)
    entry_output_dir.insert(0, output_dir)

def start_conversion():
    heic_files = entry_files.get().split(";")
    output_dir = entry_output_dir.get()

    if not heic_files or not output_dir:
        logging.warning("Conversion attempted without selecting files or output directory")
        messagebox.showwarning("Warning", "Please select HEIC files and an output directory.")
        return

    # Filter out empty strings
    heic_files = [f for f in heic_files if f]
    
    if not heic_files:
        logging.warning("No files selected for conversion")
        messagebox.showwarning("Warning", "Please select at least one HEIC file for conversion.")
        return

    # Track conversion results
    successful_conversions = 0
    failed_conversions = 0
    failed_files = []
    format_mismatch_files = []
    
    logging.info(f"Starting conversion of {len(heic_files)} files to {output_dir}")

    for heic_file in heic_files:
        if heic_file:
            base_name = os.path.basename(heic_file)
            jpg_name = os.path.splitext(base_name)[0] + ".jpg"
            jpg_path = os.path.join(output_dir, jpg_name)
            
            if convert_heic_to_jpg(heic_file, jpg_path):
                successful_conversions += 1
            else:
                failed_conversions += 1
                failed_files.append(base_name)
                
                # Check if this is a format mismatch to provide better feedback
                format_info = get_file_format_info(heic_file)
                if "not HEIC" in format_info:
                    format_mismatch_files.append(base_name)

    # Show results summary
    logging.info(f"Conversion completed: {successful_conversions} successful, {failed_conversions} failed")
    
    # Prepare a more detailed summary
    if failed_conversions == 0:
        messagebox.showinfo("Success", f"Conversion complete!\n{successful_conversions} file(s) converted successfully.")
    else:
        error_message = f"Conversion completed with errors:\n"
        error_message += f"- {successful_conversions} file(s) converted successfully\n"
        error_message += f"- {failed_conversions} file(s) failed to convert\n\n"
        
        if format_mismatch_files:
            error_message += f"Format mismatch issues: {len(format_mismatch_files)} file(s)\n"
            error_message += "These files have the wrong extension but are already in the target format.\n\n"
        
        if failed_files:
            error_message += "Failed files:\n" + "\n".join(failed_files[:5])  # Show first 5 failed files
            if len(failed_files) > 5:
                error_message += f"\n... and {len(failed_files) - 5} more"
        
        if failed_conversions == len(heic_files):
            logging.error(f"All files failed to convert. Failed files: {', '.join(failed_files)}")
            if len(heic_files) == 1:
                # For a single file, we might want to be more specific
                messagebox.showerror("Conversion Failed", error_message)
            else:
                messagebox.showerror("Conversion Failed", error_message)
        else:
            logging.warning(f"Some files failed to convert. Failed files: {', '.join(failed_files)}")
            messagebox.showwarning("Conversion Completed with Errors", error_message)

# Create the main window
root = tk.Tk()
root.title("HEIC to JPG Converter")

# Create and pack the widgets
frame = tk.Frame(root, padx=10, pady=10)
frame.pack()

label_files = tk.Label(frame, text="HEIC Files:")
label_files.grid(row=0, column=0, sticky="w")

entry_files = tk.Entry(frame, width=50)
entry_files.grid(row=0, column=1, padx=5)

btn_select_files = tk.Button(frame, text="Select Files", command=select_files)
btn_select_files.grid(row=0, column=2)

label_output_dir = tk.Label(frame, text="Output Directory:")
label_output_dir.grid(row=1, column=0, sticky="w")

entry_output_dir = tk.Entry(frame, width=50)
entry_output_dir.grid(row=1, column=1, padx=5)

btn_select_output_dir = tk.Button(frame, text="Select Directory", command=select_output_dir)
btn_select_output_dir.grid(row=1, column=2)

btn_convert = tk.Button(root, text="Convert", command=start_conversion)
btn_convert.pack(pady=10)

root.mainloop()
