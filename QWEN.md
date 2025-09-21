# HEIC to JPG Converter - Project Context

## Project Overview

This is a simple Windows desktop application for batch converting HEIC images to JPG format. It's built with Python using Tkinter for the GUI and leverages the `pillow-heif` library to handle HEIC format conversion.

### Key Features
- GUI-based file selection for HEIC images
- Batch conversion of multiple HEIC files to JPG
- Output directory selection
- Error handling for conversion failures
- Standalone executable available via PyInstaller

## Project Structure

```
heic2jpg/
├── heic_to_jpg_converter.py     # Main application code
├── requirements.txt             # Python dependencies
├── heic_to_jpg_converter.spec   # PyInstaller build specification
├── README.md                    # Usage instructions
├── .env                         # Configuration (contains API keys/secrets)
├── build/                       # PyInstaller build artifacts
│   └── heic_to_jpg_converter/   # Build directory
└── dist/                        # Packaged executable
    └── heic_to_jpg_converter.exe # Standalone Windows executable
```

## Technologies Used

- **Python 3.x**: Core programming language
- **Tkinter**: GUI framework for desktop application
- **Pillow**: Python Imaging Library for image processing
- **pillow-heif**: Extension for handling HEIC format images
- **PyInstaller**: Tool for packaging Python applications as standalone executables

## Installation and Setup

1. Install Python 3.x if not already installed
2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

Dependencies include:
- `pillow-heif`: For HEIC image reading
- `Pillow`: For general image processing

## Running the Application

### Development Mode
```bash
python heic_to_jpg_converter.py
```

### From Executable
Simply run the packaged executable:
```
dist/heic_to_jpg_converter.exe
```

## How to Use

1. Run the application (either Python script or executable)
2. Click "Select Files" to choose HEIC images for conversion
3. Click "Select Directory" to choose output location for JPG files
4. Click "Convert" to start the conversion process
5. A success message will appear when conversion is complete

## Building the Executable

The application can be packaged as a standalone Windows executable using PyInstaller:

```bash
pyinstaller heic_to_jpg_converter.spec
```

This will create the executable in the `dist/` directory.

## Development Notes

- The main application logic is in `heic_to_jpg_converter.py`
- The GUI is built with Tkinter
- HEIC to JPG conversion uses the `pillow_heif` library
- Error handling is implemented for failed conversions
- The `.spec` file contains PyInstaller configuration for proper packaging

## Security Note

The `.env` file contains API keys and secrets that should not be committed to version control in a production environment.