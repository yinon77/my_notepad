import tkinter as tk
from tkinter import filedialog, messagebox, colorchooser, font as tkfont, simpledialog
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
        
        # Dark mode state (False = light mode, True = dark mode)
        self.dark_mode = False
        
        # Default font settings
        self.current_font_family = "Consolas"
        self.current_font_size = 11
        self.current_font_color = "#000000"
        
        # Line numbers state
        self.show_line_numbers = True
        
        # Create menu bar
        self.create_menu()
        
        # Create text area with scrollbar and line numbers
        self.create_text_area()
        
    def create_menu(self):
        """Create the menu bar with File, Edit, Format, and Help menus"""
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
        edit_menu.add_separator()
        # NEW: Search and Replace functionality
        edit_menu.add_command(label="Find", command=self.find_text, accelerator="Ctrl+F")
        edit_menu.add_command(label="Replace", command=self.replace_text, accelerator="Ctrl+H")
        menu_bar.add_cascade(label="Edit", menu=edit_menu)
        
        # NEW: Format menu for font customization and dark mode
        format_menu = tk.Menu(menu_bar, tearoff=0)
        format_menu.add_command(label="Change Font Style", command=self.change_font_style)
        format_menu.add_command(label="Change Font Size", command=self.change_font_size)
        format_menu.add_command(label="Change Font Color", command=self.change_font_color)
        format_menu.add_separator()
        format_menu.add_checkbutton(label="Word Wrap", command=self.toggle_word_wrap, 
                                     variable=tk.BooleanVar(value=True))
        format_menu.add_checkbutton(label="Show Line Numbers", command=self.toggle_line_numbers,
                                     variable=tk.BooleanVar(value=True))
        format_menu.add_separator()
        format_menu.add_command(label="Toggle Dark Mode", command=self.toggle_dark_mode)
        menu_bar.add_cascade(label="Format", menu=format_menu)
        
        # Help menu
        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        menu_bar.add_cascade(label="Help", menu=help_menu)
        
        self.root.config(menu=menu_bar)
        
        # Bind keyboard shortcuts
        self.root.bind("<Control-n>", lambda e: self.new_file())
        self.root.bind("<Control-o>", lambda e: self.open_file())
        self.root.bind("<Control-s>", lambda e: self.save_file())
        self.root.bind("<Control-f>", lambda e: self.find_text())
        self.root.bind("<Control-h>", lambda e: self.replace_text())
        
    def create_text_area(self):
        """Create the main text area with scrollbar and line numbers"""
        # Create frame to hold line numbers and text area
        text_frame = tk.Frame(self.root)
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create line numbers widget (small text widget on the left)
        self.line_numbers = tk.Text(text_frame, width=4, padx=5, takefocus=0,
                                     border=0, background='lightgray', state='disabled',
                                     font=(self.current_font_family, self.current_font_size))
        self.line_numbers.pack(side=tk.LEFT, fill=tk.Y)
        
        # Create scrollbar
        scrollbar = tk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Create main text area with word wrap enabled by default
        self.text_area = tk.Text(text_frame, undo=True, wrap=tk.WORD, 
                                 yscrollcommand=scrollbar.set,
                                 font=(self.current_font_family, self.current_font_size),
                                 fg=self.current_font_color)
        self.text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Configure scrollbar to scroll both text area and line numbers
        scrollbar.config(command=self.sync_scroll)
        
        # Bind text area changes to update line numbers
        self.text_area.bind('<KeyRelease>', self.update_line_numbers)
        self.text_area.bind('<MouseWheel>', self.update_line_numbers)
        self.text_area.bind('<Button-1>', self.update_line_numbers)
        
        # Update line numbers initially
        self.update_line_numbers()
        
        # Focus on text area
        self.text_area.focus()
        
    def new_file(self):
        """Create a new file"""
        # Clear the text area
        self.text_area.delete(1.0, tk.END)
        self.file_path = None
        self.root.title("Untitled - Notepad")
        # Update line numbers
        self.update_line_numbers()
        
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
                
                # Update line numbers
                self.update_line_numbers()
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
    
    # ===== NEW FEATURES =====
    
    def update_line_numbers(self, event=None):
        """Update the line numbers display"""
        # Get the number of lines in the text area
        line_count = self.text_area.get('1.0', 'end-1c').count('\n') + 1
        
        # Generate line numbers text (1, 2, 3, ...)
        line_numbers_text = "\n".join(str(i) for i in range(1, line_count + 1))
        
        # Enable editing, update content, disable editing
        self.line_numbers.config(state='normal')
        self.line_numbers.delete('1.0', 'end')
        self.line_numbers.insert('1.0', line_numbers_text)
        self.line_numbers.config(state='disabled')
    
    def sync_scroll(self, *args):
        """Synchronize scrolling between line numbers and text area"""
        # Scroll both text widgets together
        self.text_area.yview(*args)
        self.line_numbers.yview(*args)
    
    def toggle_line_numbers(self):
        """Toggle line numbers display on/off"""
        if self.show_line_numbers:
            # Hide line numbers
            self.line_numbers.pack_forget()
            self.show_line_numbers = False
        else:
            # Show line numbers
            self.line_numbers.pack(side=tk.LEFT, fill=tk.Y, before=self.text_area)
            self.show_line_numbers = True
            self.update_line_numbers()
    
    def find_text(self):
        """Find text in the document"""
        # Ask user for text to find
        search_text = simpledialog.askstring("Find", "Enter text to find:")
        
        if search_text:
            # Remove previous highlights
            self.text_area.tag_remove('found', '1.0', tk.END)
            
            # Search for all occurrences
            start_pos = '1.0'
            count = 0
            while True:
                # Find next occurrence
                start_pos = self.text_area.search(search_text, start_pos, tk.END)
                if not start_pos:
                    break
                
                # Calculate end position
                end_pos = f"{start_pos}+{len(search_text)}c"
                
                # Highlight found text
                self.text_area.tag_add('found', start_pos, end_pos)
                count += 1
                
                # Move to next position
                start_pos = end_pos
            
            # Configure highlight color
            self.text_area.tag_config('found', background='yellow', foreground='black')
            
            # Show result message
            if count > 0:
                messagebox.showinfo("Find", f"Found {count} occurrence(s)")
            else:
                messagebox.showinfo("Find", "Text not found")
    
    def replace_text(self):
        """Replace text in the document"""
        # Ask user for text to find and replace
        find_text = simpledialog.askstring("Replace", "Enter text to find:")
        if not find_text:
            return
        
        replace_with = simpledialog.askstring("Replace", "Enter replacement text:")
        if replace_with is None:  # User clicked cancel
            return
        
        # Get all text content
        content = self.text_area.get('1.0', 'end-1c')
        
        # Count replacements
        count = content.count(find_text)
        
        if count > 0:
            # Replace all occurrences
            new_content = content.replace(find_text, replace_with)
            
            # Update text area
            self.text_area.delete('1.0', tk.END)
            self.text_area.insert('1.0', new_content)
            
            # Update line numbers
            self.update_line_numbers()
            
            # Show result message
            messagebox.showinfo("Replace", f"Replaced {count} occurrence(s)")
        else:
            messagebox.showinfo("Replace", "Text not found")
    
    def change_font_style(self):
        """Change the font family/style"""
        # List of common fonts
        available_fonts = ["Consolas", "Arial", "Times New Roman", "Courier New", 
                          "Georgia", "Verdana", "Comic Sans MS", "Calibri"]
        
        # Create a simple dialog to select font
        font_window = tk.Toplevel(self.root)
        font_window.title("Select Font")
        font_window.geometry("300x400")
        
        tk.Label(font_window, text="Choose a font:", font=("Arial", 12)).pack(pady=10)
        
        # Create listbox with fonts
        listbox = tk.Listbox(font_window, height=10)
        for font in available_fonts:
            listbox.insert(tk.END, font)
        listbox.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        def apply_font():
            """Apply selected font"""
            selection = listbox.curselection()
            if selection:
                # Update font family
                self.current_font_family = listbox.get(selection[0])
                self.text_area.config(font=(self.current_font_family, self.current_font_size))
                self.line_numbers.config(font=(self.current_font_family, self.current_font_size))
                self.update_line_numbers()
                font_window.destroy()
        
        tk.Button(font_window, text="Apply", command=apply_font, width=15).pack(pady=10)
    
    def change_font_size(self):
        """Change the font size"""
        # Ask user for new font size
        new_size = simpledialog.askinteger("Font Size", "Enter font size (8-72):",
                                          initialvalue=self.current_font_size,
                                          minvalue=8, maxvalue=72)
        
        if new_size:
            # Update font size
            self.current_font_size = new_size
            self.text_area.config(font=(self.current_font_family, self.current_font_size))
            self.line_numbers.config(font=(self.current_font_family, self.current_font_size))
            self.update_line_numbers()
    
    def change_font_color(self):
        """Change the font color"""
        # Open color chooser dialog
        color = colorchooser.askcolor(title="Choose Font Color", 
                                      initialcolor=self.current_font_color)
        
        if color[1]:  # color[1] contains the hex color code
            # Update font color
            self.current_font_color = color[1]
            self.text_area.config(fg=self.current_font_color)
    
    def toggle_word_wrap(self):
        """Toggle word wrap on/off"""
        # Check current wrap mode
        current_wrap = self.text_area.cget('wrap')
        
        if current_wrap == 'word':
            # Disable word wrap
            self.text_area.config(wrap='none')
        else:
            # Enable word wrap
            self.text_area.config(wrap='word')
    
    def toggle_dark_mode(self):
        """Toggle between light and dark mode"""
        if self.dark_mode:
            # Switch to light mode
            self.text_area.config(bg='white', fg=self.current_font_color, 
                                 insertbackground='black')
            self.line_numbers.config(bg='lightgray', fg='black')
            self.root.config(bg='white')
            self.dark_mode = False
        else:
            # Switch to dark mode
            self.text_area.config(bg='#2b2b2b', fg='#ffffff', 
                                 insertbackground='white')
            self.line_numbers.config(bg='#1e1e1e', fg='#858585')
            self.root.config(bg='#2b2b2b')
            self.dark_mode = True
        
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
