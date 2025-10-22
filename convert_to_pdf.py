"""
Convert Markdown documentation to PDF format
Requires: pip install markdown pdfkit wkhtmltopdf
"""

import markdown
from pathlib import Path
import os

try:
    import pdfkit
    PDFKIT_AVAILABLE = True
except ImportError:
    PDFKIT_AVAILABLE = False

def convert_md_to_pdf(md_file_path, output_pdf_path=None):
    """Convert markdown file to PDF"""
    
    try:
        # Read markdown file
        with open(md_file_path, 'r', encoding='utf-8') as f:
            md_content = f.read()
        
        # Convert markdown to HTML
        html_content = markdown.markdown(
            md_content, 
            extensions=['codehilite', 'fenced_code', 'tables', 'toc']
        )
        
        # Add CSS styling for better PDF appearance
        css_style = """
        <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 40px;
            color: #333;
        }
        h1, h2, h3, h4, h5, h6 {
            color: #2c3e50;
            margin-top: 2em;
            margin-bottom: 1em;
        }
        h1 {
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }
        h2 {
            border-bottom: 2px solid #95a5a6;
            padding-bottom: 5px;
        }
        code {
            background-color: #f8f9fa;
            padding: 2px 4px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
        }
        pre {
            background-color: #f8f9fa;
            border: 1px solid #e9ecef;
            border-radius: 5px;
            padding: 15px;
            overflow-x: auto;
            font-family: 'Courier New', monospace;
        }
        table {
            border-collapse: collapse;
            width: 100%;
            margin: 1em 0;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 8px 12px;
            text-align: left;
        }
        th {
            background-color: #f2f2f2;
            font-weight: bold;
        }
        blockquote {
            border-left: 4px solid #3498db;
            margin-left: 0;
            padding-left: 20px;
            font-style: italic;
        }
        .page-break {
            page-break-before: always;
        }
        </style>
        """
        
        # Complete HTML document
        full_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>ImageNet Pre-trained Models Guide</title>
            {css_style}
        </head>
        <body>
            {html_content}
        </body>
        </html>
        """
        
        # Set output path
        if output_pdf_path is None:
            output_pdf_path = md_file_path.replace('.md', '.pdf')
        
        # PDF options
        options = {
            'page-size': 'A4',
            'margin-top': '0.75in',
            'margin-right': '0.75in',
            'margin-bottom': '0.75in',
            'margin-left': '0.75in',
            'encoding': "UTF-8",
            'no-outline': None,
            'enable-local-file-access': None,
            'print-media-type': None
        }
        
        # Try to convert to PDF
        try:
            pdfkit.from_string(full_html, output_pdf_path, options=options)
            print(f"✅ PDF created successfully: {output_pdf_path}")
            return True
            
        except OSError as e:
            if "wkhtmltopdf" in str(e):
                print("❌ wkhtmltopdf not found. Please install it:")
                print("   1. Download from: https://wkhtmltopdf.org/downloads.html")
                print("   2. Install the executable")
                print("   3. Add to system PATH")
                print("\n   Alternative: Use the manual conversion method below")
                return False
            else:
                raise e
                
    except Exception as e:
        print(f"❌ Error converting to PDF: {str(e)}")
        return False

def manual_html_conversion(md_file_path):
    """Create HTML file for manual PDF conversion"""
    
    try:
        # Read markdown file
        with open(md_file_path, 'r', encoding='utf-8') as f:
            md_content = f.read()
        
        # Convert markdown to HTML
        html_content = markdown.markdown(
            md_content, 
            extensions=['codehilite', 'fenced_code', 'tables', 'toc']
        )
        
        # Add comprehensive CSS for better appearance
        css_style = """
        <style>
        @media print {
            body { margin: 0.5in; }
            .page-break { page-break-before: always; }
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            margin: 40px;
            color: #333;
            max-width: none;
        }
        
        h1, h2, h3, h4, h5, h6 {
            color: #2c3e50;
            margin-top: 2.5em;
            margin-bottom: 1em;
            font-weight: 600;
        }
        
        h1 {
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
            font-size: 2.5em;
            margin-top: 0;
        }
        
        h2 {
            border-bottom: 2px solid #95a5a6;
            padding-bottom: 8px;
            font-size: 2em;
        }
        
        h3 {
            color: #34495e;
            font-size: 1.5em;
        }
        
        code {
            background-color: #f8f9fa;
            padding: 3px 6px;
            border-radius: 4px;
            font-family: 'SF Mono', Monaco, 'Cascadia Code', 'Roboto Mono', Consolas, 'Courier New', monospace;
            font-size: 0.9em;
            border: 1px solid #e1e4e8;
        }
        
        pre {
            background-color: #f6f8fa;
            border: 1px solid #d1d5da;
            border-radius: 6px;
            padding: 16px;
            overflow-x: auto;
            font-family: 'SF Mono', Monaco, 'Cascadia Code', 'Roboto Mono', Consolas, 'Courier New', monospace;
            font-size: 0.85em;
            line-height: 1.45;
        }
        
        pre code {
            background: none;
            padding: 0;
            border: none;
            font-size: inherit;
        }
        
        table {
            border-collapse: collapse;
            width: 100%;
            margin: 1.5em 0;
            border: 1px solid #d0d7de;
            border-radius: 6px;
        }
        
        th, td {
            border: 1px solid #d0d7de;
            padding: 12px 16px;
            text-align: left;
        }
        
        th {
            background-color: #f6f8fa;
            font-weight: 600;
            color: #24292f;
        }
        
        tr:nth-child(even) {
            background-color: #f6f8fa;
        }
        
        blockquote {
            border-left: 4px solid #3498db;
            margin-left: 0;
            padding-left: 20px;
            font-style: italic;
            color: #555;
        }
        
        ul, ol {
            padding-left: 2em;
        }
        
        li {
            margin-bottom: 0.5em;
        }
        
        strong {
            color: #24292f;
            font-weight: 600;
        }
        
        hr {
            border: none;
            border-top: 2px solid #e1e4e8;
            margin: 2em 0;
        }
        
        .toc {
            background-color: #f6f8fa;
            border: 1px solid #d0d7de;
            border-radius: 6px;
            padding: 20px;
            margin: 2em 0;
        }
        
        .toc ul {
            list-style-type: none;
            padding-left: 1em;
        }
        
        .page-break {
            page-break-before: always;
        }
        </style>
        """
        
        # Complete HTML document with title page
        title_page = f"""
        <div style="text-align: center; margin-top: 25%; margin-bottom: 25%; page-break-after: always;">
            <h1 style="font-size: 3em; color: #2c3e50; border: none; margin-bottom: 0.5em;">
                SwasthVedha Backend
            </h1>
            <h2 style="font-size: 2em; color: #34495e; border: none; font-weight: 400;">
                Comprehensive Technical Analysis
            </h2>
            <h3 style="font-size: 1.5em; color: #7f8c8d; border: none; font-weight: 300; margin-top: 2em;">
                AI-Powered Ayurvedic Healthcare Platform
            </h3>
            <hr style="width: 50%; margin: 2em auto;">
            <p style="font-size: 1.2em; color: #95a5a6; margin-top: 3em;">
                FastAPI • Google Flan-T5 Large • ImageNet ResNet<br>
                Computer Vision • Traditional Medicine Integration
            </p>
            <p style="font-size: 1em; color: #bdc3c7; margin-top: 4em;">
                Generated: October 15, 2024<br>
                Status: ✅ Production Ready
            </p>
        </div>
        """
        
        full_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>ImageNet Pre-trained Models - Complete Guide</title>
            {css_style}
        </head>
        <body>
            {title_page}
            {html_content}
        </body>
        </html>
        """
        
        # Save HTML file
        html_file_path = md_file_path.replace('.md', '.html')
        with open(html_file_path, 'w', encoding='utf-8') as f:
            f.write(full_html)
        
        print(f"✅ HTML file created: {html_file_path}")
        print("\n📄 To convert to PDF:")
        print(f"   1. Open {html_file_path} in your web browser")
        print("   2. Press Ctrl+P (or Cmd+P on Mac)")
        print("   3. Select 'Save as PDF' as destination")
        print("   4. Choose 'More settings' and enable 'Background graphics'")
        print("   5. Save as: ImageNet_PreTrained_Models_Guide.pdf")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating HTML file: {str(e)}")
        return False

def main():
    """Main conversion function"""
    print("📄 PDF Converter for SwasthVedha Backend Analysis")
    print("=" * 60)
    
    # File paths
    md_file = "SwasthVedha_Backend_Analysis_Report.md"
    pdf_file = "SwasthVedha_Backend_Analysis_Report.pdf"
    
    # Check if markdown file exists
    if not os.path.exists(md_file):
        print(f"❌ Markdown file not found: {md_file}")
        return
    
    print(f"📖 Converting: {md_file}")
    print(f"📄 Target: {pdf_file}")
    
    # Try automatic PDF conversion first
    print("\n🔄 Attempting automatic PDF conversion...")
    
    if PDFKIT_AVAILABLE:
        success = convert_md_to_pdf(md_file, pdf_file)
        if success:
            print(f"\n🎉 SUCCESS! PDF saved as: {pdf_file}")
            print(f"📁 Location: {os.path.abspath(pdf_file)}")
            return
    else:
        print("📦 pdfkit not installed. Trying alternative method...")
    
    # Fallback to manual HTML conversion
    print("\n🔄 Creating HTML for manual conversion...")
    success = manual_html_conversion(md_file)
    
    if success:
        print("\n✅ HTML file created successfully!")
        print("🔧 Follow the instructions above to create PDF manually.")
    else:
        print("\n❌ Conversion failed. Please check the error messages above.")

if __name__ == "__main__":
    # Install required packages if not present
    try:
        import markdown
    except ImportError:
        print("Installing required packages...")
        os.system("pip install markdown")
    
    main()