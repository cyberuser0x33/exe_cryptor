import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os

class SteganographyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image File Steganography")
        self.root.geometry("600x400")
        self.root.resizable(False, False)
        
        # Create main container with padding
        main_frame = ttk.Frame(root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Embedding section
        embed_frame = ttk.LabelFrame(main_frame, text="Embed File", padding="10")
        embed_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(embed_frame, text="Image File:").grid(row=0, column=0, sticky=tk.W)
        self.image_path = tk.StringVar()
        ttk.Entry(embed_frame, textvariable=self.image_path, width=50).grid(row=0, column=1, padx=5)
        ttk.Button(embed_frame, text="Browse", command=self.browse_image).grid(row=0, column=2)
        
        ttk.Label(embed_frame, text="File to Hide:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.file_to_hide_path = tk.StringVar()
        ttk.Entry(embed_frame, textvariable=self.file_to_hide_path, width=50).grid(row=1, column=1, padx=5)
        ttk.Button(embed_frame, text="Browse", command=self.browse_file_to_hide).grid(row=1, column=2)
        
        ttk.Button(embed_frame, text="Embed File", command=self.embed_file).grid(row=2, column=1, pady=10)
        
        # Extraction section
        extract_frame = ttk.LabelFrame(main_frame, text="Extract File", padding="10")
        extract_frame.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        ttk.Label(extract_frame, text="Combined Image:").grid(row=0, column=0, sticky=tk.W)
        self.combined_path = tk.StringVar()
        ttk.Entry(extract_frame, textvariable=self.combined_path, width=50).grid(row=0, column=1, padx=5)
        ttk.Button(extract_frame, text="Browse", command=self.browse_combined).grid(row=0, column=2)
        
        ttk.Button(extract_frame, text="Extract File", command=self.extract_file).grid(row=1, column=1, pady=10)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(10, 0))

    def browse_image(self):
        filename = filedialog.askopenfilename(
            filetypes=[("JPEG files", "*.jpg *.jpeg")]
        )
        if filename:
            self.image_path.set(filename)

    def browse_file_to_hide(self):
        filename = filedialog.askopenfilename(
            filetypes=[("All files", "*.*")]
        )
        if filename:
            self.file_to_hide_path.set(filename)

    def browse_combined(self):
        filename = filedialog.askopenfilename(
            filetypes=[("JPEG files", "*.jpg *.jpeg")]
        )
        if filename:
            self.combined_path.set(filename)

    def embed_file(self):
        if not self.image_path.get() or not self.file_to_hide_path.get():
            messagebox.showerror("Error", "Please select both an image and a file to hide")
            return
            
        try:
            # Read the image file
            with open(self.image_path.get(), 'rb') as img_file:
                img_data = img_file.read()
            
            # Find the end of the JPEG
            end_marker = b'\xff\xd9'
            img_end = img_data.index(end_marker) + len(end_marker)
            
            # Read the file to hide
            with open(self.file_to_hide_path.get(), 'rb') as file_to_hide:
                hide_data = file_to_hide.read()
            
            # Create the combined data
            combined_data = img_data[:img_end] + hide_data
            
            # Get output filename
            output_path = filedialog.asksaveasfilename(
                defaultextension=".jpg",
                filetypes=[("JPEG files", "*.jpg *.jpeg")]
            )
            
            if output_path:
                # Write the combined file
                with open(output_path, 'wb') as output_file:
                    output_file.write(combined_data)
                
                self.status_var.set(f"File successfully embedded in {os.path.basename(output_path)}")
                messagebox.showinfo("Success", "File has been successfully embedded in the image")
        
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            self.status_var.set("Error occurred while embedding file")

    def extract_file(self):
        if not self.combined_path.get():
            messagebox.showerror("Error", "Please select a combined image file")
            return
            
        try:
            # Read the combined file
            with open(self.combined_path.get(), 'rb') as combined_file:
                combined_data = combined_file.read()
            
            # Find the end of the JPEG
            end_marker = b'\xff\xd9'
            img_end = combined_data.index(end_marker) + len(end_marker)
            
            # Extract the hidden file data
            hidden_data = combined_data[img_end:]
            
            # Get output filename
            output_path = filedialog.asksaveasfilename(
                filetypes=[("All files", "*.*")]
            )
            
            if output_path:
                # Write the extracted file
                with open(output_path, 'wb') as output_file:
                    output_file.write(hidden_data)
                
                self.status_var.set(f"File successfully extracted to {os.path.basename(output_path)}")
                messagebox.showinfo("Success", "File has been successfully extracted")
        
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            self.status_var.set("Error occurred while extracting file")

if __name__ == "__main__":
    root = tk.Tk()
    app = SteganographyApp(root)
    root.mainloop()