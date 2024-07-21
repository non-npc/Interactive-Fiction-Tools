import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import xml.etree.ElementTree as ET
from xml.dom import minidom

class StoryXMLEditor:
    def __init__(self, master):
        self.master = master
        self.master.title("Interactive Fiction Editor")
        self.master.geometry("800x600")

        self.tree = ET.Element("story")
        self.current_page = None

        self.create_widgets()

    def create_widgets(self):
        # Menu
        menubar = tk.Menu(self.master)
        self.master.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)

        # Notebook for different sections
        self.notebook = ttk.Notebook(self.master)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)

        # Intro tab
        self.intro_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.intro_frame, text="Intro")
        self.create_intro_widgets()

        # Pages tab
        self.pages_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.pages_frame, text="Pages")
        self.create_pages_widgets()

    def create_intro_widgets(self):
        # Title (required)
        ttk.Label(self.intro_frame, text="Title (required):").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.title_entry = ttk.Entry(self.intro_frame, width=50)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)

        # Author (required)
        ttk.Label(self.intro_frame, text="Author (required):").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.author_entry = ttk.Entry(self.intro_frame, width=50)
        self.author_entry.grid(row=1, column=1, padx=5, pady=5)

        # Image
        ttk.Label(self.intro_frame, text="Image:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.image_entry = ttk.Entry(self.intro_frame, width=50)
        self.image_entry.grid(row=2, column=1, padx=5, pady=5)

        # Audio
        ttk.Label(self.intro_frame, text="Audio:").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.audio_entry = ttk.Entry(self.intro_frame, width=50)
        self.audio_entry.grid(row=3, column=1, padx=5, pady=5)

        # Audio Autoplay
        self.audio_autoplay_var = tk.BooleanVar()
        self.audio_autoplay_check = ttk.Checkbutton(self.intro_frame, text="Audio Autoplay", variable=self.audio_autoplay_var)
        self.audio_autoplay_check.grid(row=4, column=1, sticky="w", padx=5, pady=5)

        # Note about fixed choices
        ttk.Label(self.intro_frame, text="Note: The intro has fixed choices 'Start Story' and 'Exit'").grid(row=5, column=0, columnspan=2, sticky="w", padx=5, pady=5)

    def create_pages_widgets(self):
        # Pages list
        self.pages_list = tk.Listbox(self.pages_frame, width=30, height=20)
        self.pages_list.grid(row=0, column=0, rowspan=6, padx=5, pady=5)
        self.pages_list.bind('<<ListboxSelect>>', self.on_page_select)

        # Add and Remove buttons
        ttk.Button(self.pages_frame, text="Add Page", command=self.add_page).grid(row=6, column=0, sticky="w", padx=5, pady=5)
        ttk.Button(self.pages_frame, text="Remove Page", command=self.remove_page).grid(row=6, column=0, sticky="e", padx=5, pady=5)

        # Page details
        ttk.Label(self.pages_frame, text="ID:").grid(row=0, column=1, sticky="w", padx=5, pady=5)
        self.page_id_entry = ttk.Entry(self.pages_frame, width=50, state="readonly")
        self.page_id_entry.grid(row=0, column=2, padx=5, pady=5)

        ttk.Label(self.pages_frame, text="Text:").grid(row=1, column=1, sticky="w", padx=5, pady=5)
        self.page_text_entry = tk.Text(self.pages_frame, width=50, height=5)
        self.page_text_entry.grid(row=1, column=2, padx=5, pady=5)

        ttk.Label(self.pages_frame, text="Image:").grid(row=2, column=1, sticky="w", padx=5, pady=5)
        self.page_image_entry = ttk.Entry(self.pages_frame, width=50)
        self.page_image_entry.grid(row=2, column=2, padx=5, pady=5)

        ttk.Label(self.pages_frame, text="Audio:").grid(row=3, column=1, sticky="w", padx=5, pady=5)
        self.page_audio_entry = ttk.Entry(self.pages_frame, width=50)
        self.page_audio_entry.grid(row=3, column=2, padx=5, pady=5)

        ttk.Label(self.pages_frame, text="Video:").grid(row=4, column=1, sticky="w", padx=5, pady=5)
        self.page_video_entry = ttk.Entry(self.pages_frame, width=50)
        self.page_video_entry.grid(row=4, column=2, padx=5, pady=5)

        self.page_video_autoplay_var = tk.BooleanVar()
        self.page_video_autoplay_check = ttk.Checkbutton(self.pages_frame, text="Video Autoplay", variable=self.page_video_autoplay_var)
        self.page_video_autoplay_check.grid(row=5, column=2, sticky="w", padx=5, pady=5)

        # Choices
        ttk.Label(self.pages_frame, text="Choices:").grid(row=6, column=1, sticky="w", padx=5, pady=5)
        self.page_choices_frame = ttk.Frame(self.pages_frame)
        self.page_choices_frame.grid(row=6, column=2, sticky="w", padx=5, pady=5)

        self.page_choices = []
        self.add_page_choice()

        # Add Choice button
        ttk.Button(self.pages_frame, text="Add Choice", command=self.add_page_choice).grid(row=7, column=2, sticky="w", padx=5, pady=5)

        # Save Page button
        ttk.Button(self.pages_frame, text="Save Page", command=self.save_page).grid(row=8, column=2, sticky="e", padx=5, pady=5)


    def add_page_choice(self):
        choice_frame = ttk.Frame(self.page_choices_frame)
        choice_frame.pack(fill="x", pady=2)

        text_entry = ttk.Entry(choice_frame, width=30)
        text_entry.pack(side="left", padx=2)

        next_entry = ttk.Entry(choice_frame, width=20)
        next_entry.pack(side="left", padx=2)

        remove_btn = ttk.Button(choice_frame, text="Remove", command=lambda: self.remove_page_choice(choice_frame))
        remove_btn.pack(side="left", padx=2)

        self.page_choices.append((text_entry, next_entry))

    def remove_page_choice(self, choice_frame):
        for i, (text_entry, next_entry) in enumerate(self.page_choices):
            if text_entry.master == choice_frame:
                del self.page_choices[i]
                break
        choice_frame.destroy()

    def new_file(self):
        self.tree = ET.Element("story")
        self.clear_all_fields()
        self.pages_list.delete(0, tk.END)

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Interactive Fiction Game", "*.ifg")])
        if file_path:
            try:
                self.tree = ET.parse(file_path).getroot()
                self.load_story()
            except ET.ParseError:
                messagebox.showerror("Error", "Invalid IFG file")

    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".ifg", filetypes=[("Interactive Fiction Game", "*.ifg")])
        if file_path:
            self.save_intro()
            xml_str = minidom.parseString(ET.tostring(self.tree)).toprettyxml(indent="    ")
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(xml_str)
            messagebox.showinfo("Success", "Story saved successfully!")

    def load_story(self):
        self.clear_all_fields()

        # Load intro
        intro = self.tree.find("intro")
        if intro is not None:
            self.title_entry.insert(0, intro.findtext("title", ""))
            self.author_entry.insert(0, intro.findtext("author", ""))
            self.image_entry.insert(0, intro.findtext("image", ""))
            audio = intro.find("audio")
            if audio is not None:
                self.audio_entry.insert(0, audio.text)
                self.audio_autoplay_var.set(audio.get("autoplay", "false").lower() == "true")

        # Load pages
        for page in self.tree.findall("part"):
            self.pages_list.insert(tk.END, page.get("id", ""))

    def on_page_select(self, event):
        selection = self.pages_list.curselection()
        if selection:
            page_id = self.pages_list.get(selection[0])
            self.current_page = self.tree.find(f".//part[@id='{page_id}']")
            self.load_page()

    def add_page(self):
        page_id = f"page_{len(self.tree.findall('part')) + 1}"
        new_page = ET.SubElement(self.tree, "part", id=page_id)
        ET.SubElement(new_page, "text").text = ""
        self.pages_list.insert(tk.END, page_id)
        self.pages_list.selection_clear(0, tk.END)
        self.pages_list.selection_set(tk.END)
        self.on_page_select(None)
        
    def remove_page(self):
        selection = self.pages_list.curselection()
        if selection:
            page_id = self.pages_list.get(selection[0])
            page = self.tree.find(f".//part[@id='{page_id}']")
            if page is not None:
                self.tree.remove(page)
            self.pages_list.delete(selection[0])
            self.clear_page_fields()

    def load_page(self):
        if self.current_page is not None:
            self.clear_page_fields()
            self.page_id_entry.config(state="normal")
            self.page_id_entry.delete(0, tk.END)
            self.page_id_entry.insert(0, self.current_page.get("id", ""))
            self.page_id_entry.config(state="readonly")
            
            self.page_text_entry.insert("1.0", self.current_page.findtext("text", ""))
            self.page_image_entry.insert(0, self.current_page.findtext("image", ""))
            self.page_audio_entry.insert(0, self.current_page.findtext("audio", ""))
            video = self.current_page.find("video")
            if video is not None:
                self.page_video_entry.insert(0, video.text)
                self.page_video_autoplay_var.set(video.get("autoplay", "false").lower() == "true")

            for choice in self.current_page.findall("choice"):
                self.add_page_choice()
                self.page_choices[-1][0].insert(0, choice.get("text", ""))
                self.page_choices[-1][1].insert(0, choice.get("next", ""))


    def save_intro(self):
        intro = self.tree.find("intro")
        if intro is None:
            intro = ET.SubElement(self.tree, "intro")
        else:
            intro.clear()

        title = self.title_entry.get().strip()
        if not title:
            title = "Untitled Story"
        ET.SubElement(intro, "title").text = title

        author = self.author_entry.get().strip()
        if not author:
            author = "Anonymous"
        ET.SubElement(intro, "author").text = author

        image = self.image_entry.get().strip()
        if image:
            ET.SubElement(intro, "image").text = image
        
        audio = self.audio_entry.get().strip()
        if audio:
            audio_elem = ET.SubElement(intro, "audio")
            audio_elem.text = audio
            if self.audio_autoplay_var.get():
                audio_elem.set("autoplay", "true")

        # Add fixed choices
        start_choice = ET.SubElement(intro, "choice")
        start_choice.set("text", "Start Story")
        start_choice.set("action", "start")

        exit_choice = ET.SubElement(intro, "choice")
        exit_choice.set("text", "Exit")
        exit_choice.set("action", "exit")

    def save_page(self):
        if self.current_page is None:
            messagebox.showerror("Error", "No page selected.")
            return

        # We don't need to update the ID as it's now read-only
        self.current_page.clear()
        self.current_page.set("id", self.page_id_entry.get())

        text = self.page_text_entry.get("1.0", tk.END).strip()
        if text:
            ET.SubElement(self.current_page, "text").text = text
        
        image = self.page_image_entry.get().strip()
        if image:
            ET.SubElement(self.current_page, "image").text = image

        audio = self.page_audio_entry.get().strip()
        if audio:
            ET.SubElement(self.current_page, "audio").text = audio

        video = self.page_video_entry.get().strip()
        if video:
            video_elem = ET.SubElement(self.current_page, "video")
            video_elem.text = video
            if self.page_video_autoplay_var.get():
                video_elem.set("autoplay", "true")

        for text_entry, next_entry in self.page_choices:
            text = text_entry.get().strip()
            next_id = next_entry.get().strip()
            if text and next_id:
                choice = ET.SubElement(self.current_page, "choice")
                choice.set("text", text)
                choice.set("next", next_id)

        messagebox.showinfo("Success", f"Page {self.page_id_entry.get()} saved successfully!")

    def clear_all_fields(self):
        # Clear intro fields
        self.title_entry.delete(0, tk.END)
        self.author_entry.delete(0, tk.END)
        self.image_entry.delete(0, tk.END)
        self.audio_entry.delete(0, tk.END)
        self.audio_autoplay_var.set(False)

        # Clear pages list
        self.pages_list.delete(0, tk.END)

        # Clear page fields
        self.clear_page_fields()

    def clear_page_fields(self):
        self.page_id_entry.config(state="normal")
        self.page_id_entry.delete(0, tk.END)
        self.page_id_entry.config(state="readonly")
        self.page_text_entry.delete("1.0", tk.END)
        self.page_image_entry.delete(0, tk.END)
        self.page_audio_entry.delete(0, tk.END)
        self.page_video_entry.delete(0, tk.END)
        self.page_video_autoplay_var.set(False)

        for text_entry, next_entry in self.page_choices:
            text_entry.master.destroy()
        self.page_choices.clear()

if __name__ == "__main__":
    root = tk.Tk()
    app = StoryXMLEditor(root)
    root.mainloop()
