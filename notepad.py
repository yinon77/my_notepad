import tkinter as tk
from tkinter import filedialog, messagebox
import os

class Notepad:
    """A simple notepad application with basic text editing features"""
    
    def __init__(self, root):
        """Initialize the notepad application"""
        self.root = root
        self.root.title("Untitled - Notepad")
        self.root.geometry("800x600")
        
        # Variable to store current file path
        self.file_path = None
        
        # Create menu bar
        self.create_menu()
        
        # Create text area with scrollbar
        self.create_text_area()
        
    def create_menu(self):
        """Create the menu bar with File and Edit menus"""
        menu_bar = tk.Menu(self.root)
        
        # File menu
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="New", command=self.new_file, accelerator="Ctrl+N")
        file_menu.add_command(label="Open", command=self.open_file, accelerator="Ctrl+O")
        file_menu.add_command(label="Save", command=self.save_file, accelerator="Ctrl+S")
        file_menu.add_command(label="Save As", command=self.save_as_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.exit_app)
        menu_bar.add_cascade(label="File", menu=file_menu)
        
        # Edit menu
        edit_menu = tk.Menu(menu_bar, tearoff=0)
        edit_menu.add_command(label="Cut", command=self.cut_text, accelerator="Ctrl+X")
        edit_menu.add_command(label="Copy", command=self.copy_text, accelerator="Ctrl+C")
        edit_menu.add_command(label="Paste", command=self.paste_text, accelerator="Ctrl+V")
        edit_menu.add_separator()
        edit_menu.add_command(label="Select All", command=self.select_all, accelerator="Ctrl+A")
        menu_bar.add_cascade(label="Edit", menu=edit_menu)
        
        # Help menu
        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        menu_bar.add_cascade(label="Help", menu=help_menu)
        
        self.root.config(menu=menu_bar)
        
        # Bind keyboard shortcuts
        self.root.bind("<Control-n>", lambda e: self.new_file())
        self.root.bind("<Control-o>", lambda e: self.open_file())
        self.root.bind("<Control-s>", lambda e: self.save_file())
        
    def create_text_area(self):
        """Create the main text area with scrollbar"""
        # Create scrollbar
        scrollbar = tk.Scrollbar(self.root)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Create text area
        self.text_area = tk.Text(self.root, undo=True, wrap=tk.WORD, 
                                 yscrollcommand=scrollbar.set, font=("Consolas", 11))
        self.text_area.pack(fill=tk.BOTH, expand=True)
        
        # Configure scrollbar
        scrollbar.config(command=self.text_area.yview)
        
        # Focus on text area
        self.text_area.focus()
        
    def new_file(self):
        """Create a new file"""
        # Clear the text area
        self.text_area.delete(1.0, tk.END)
        self.file_path = None
        self.root.title("Untitled - Notepad")
        
    def open_file(self):
        """Open an existing file"""
        # Show file dialog to select file
        file_path = filedialog.askopenfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        
        # If a file was selected
        if file_path:
            try:
                # Read file contents
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                
                # Clear current text and insert file content
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(1.0, content)
                
                # Update file path and window title
                self.file_path = file_path
                self.root.title(f"{os.path.basename(file_path)} - Notepad")
            except Exception as e:
                messagebox.showerror("Error", f"Could not open file:\n{str(e)}")
                
    def save_file(self):
        """Save the current file"""
        # If file path exists, save to that path
        if self.file_path:
            try:
                # Get text content
                content = self.text_area.get(1.0, tk.END)
                
                # Write to file
                with open(self.file_path, 'w', encoding='utf-8') as file:
                    file.write(content)
            except Exception as e:
                messagebox.showerror("Error", f"Could not save file:\n{str(e)}")
        else:
            # If no file path, use save as
            self.save_as_file()
            
    def save_as_file(self):
        """Save the current file with a new name"""
        # Show save dialog
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        
        # If a file path was provided
        if file_path:
            try:
                # Get text content
                content = self.text_area.get(1.0, tk.END)
                
                # Write to file
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(content)
                
                # Update file path and window title
                self.file_path = file_path
                self.root.title(f"{os.path.basename(file_path)} - Notepad")
            except Exception as e:
                messagebox.showerror("Error", f"Could not save file:\n{str(e)}")
                
    def cut_text(self):
        """Cut selected text to clipboard"""
        self.text_area.event_generate("<<Cut>>")
        
    def copy_text(self):
        """Copy selected text to clipboard"""
        self.text_area.event_generate("<<Copy>>")
        
    def paste_text(self):
        """Paste text from clipboard"""
        self.text_area.event_generate("<<Paste>>")
        
    def select_all(self):
        """Select all text in the text area"""
        self.text_area.tag_add(tk.SEL, "1.0", tk.END)
        self.text_area.mark_set(tk.INSERT, "1.0")
        self.text_area.see(tk.INSERT)
        
    def show_about(self):
        """Show about dialog"""
        messagebox.showinfo("About Notepad", "Simple Notepad Application\nCreated with Python and Tkinter")
        
    def exit_app(self):
        """Exit the application"""
        self.root.quit()


def main():
    """Main function to run the notepad application"""
    # Create main window
    root = tk.Tk()
    
    # Create notepad instance
    notepad = Notepad(root)
    
    # Start the application
    root.mainloop()


if __name__ == "__main__":
    main()

