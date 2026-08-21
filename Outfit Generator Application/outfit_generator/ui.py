from __future__ import annotations

import shutil
import uuid
from datetime import datetime
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from PIL import Image, ImageTk

from .constants import CLOTHING_TYPES, COLORS, STYLES, WEATHERS
from .generator import generate_outfit
from .storage import JsonStore

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
IMAGE_DIR = DATA_DIR / "images"


def thumbnail(path: str, size=(96, 96)):
    try:
        image = Image.open(path)
        image.thumbnail(size)
        return ImageTk.PhotoImage(image)
    except (OSError, ValueError):
        return None


class OutfitGeneratorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Outfit Generator Application")
        self.geometry("950x700")
        self.minsize(760, 560)
        IMAGE_DIR.mkdir(parents=True, exist_ok=True)
        self.store = JsonStore(DATA_DIR)
        self.wardrobe = self.store.load_wardrobe()
        self.saved_outfits = self.store.load_outfits()
        self.current_outfit: list[dict] = []
        self.preview_images = []
        self._build()

    def _build(self):
        header = ttk.Frame(self, padding=16)
        header.pack(fill="x")
        ttk.Label(header, text="Outfit Generator", font=("Segoe UI", 24, "bold")).pack(side="left")
        ttk.Button(header, text="Upload Clothes", command=self.open_upload_popup).pack(side="right", padx=4)
        ttk.Button(header, text="Manage Wardrobe", command=self.open_wardrobe_manager).pack(side="right", padx=4)
        filters = ttk.LabelFrame(self, text="Outfit filters", padding=12)
        filters.pack(fill="x", padx=16, pady=(0, 10))
        self.style_var = tk.StringVar(value="Any")
        self.weather_var = tk.StringVar(value="Any")
        ttk.Label(filters, text="Style").pack(side="left")
        ttk.Combobox(filters, textvariable=self.style_var, values=STYLES, state="readonly", width=20).pack(side="left", padx=8)
        ttk.Label(filters, text="Weather").pack(side="left", padx=(12, 0))
        ttk.Combobox(filters, textvariable=self.weather_var, values=WEATHERS, state="readonly", width=12).pack(side="left", padx=8)
        ttk.Button(filters, text="Generate Random Outfit", command=self.generate).pack(side="left", padx=12)
        ttk.Button(filters, text="Save Outfit", command=self.save_current_outfit).pack(side="left")
        ttk.Button(filters, text="Saved Outfits", command=self.open_saved_outfits).pack(side="right")
        self.status_var = tk.StringVar(value=f"{len(self.wardrobe)} wardrobe item(s) • {len(self.saved_outfits)} saved outfit(s)")
        ttk.Label(self, textvariable=self.status_var, padding=(16, 0)).pack(anchor="w")
        self.preview = ttk.Frame(self, padding=16)
        self.preview.pack(fill="both", expand=True)
        self._render_message("Add wardrobe items, then generate an outfit.")

    def _render_message(self, text):
        for child in self.preview.winfo_children(): child.destroy()
        ttk.Label(self.preview, text=text, font=("Segoe UI", 13)).pack(pady=40)

    def refresh_status(self):
        self.status_var.set(f"{len(self.wardrobe)} wardrobe item(s) • {len(self.saved_outfits)} saved outfit(s)")

    def open_upload_popup(self):
        UploadPopup(self)

    def open_wardrobe_manager(self):
        WardrobeManager(self)

    def generate(self):
        self.current_outfit = generate_outfit(self.wardrobe, self.style_var.get(), self.weather_var.get())
        if not self.current_outfit:
            self._render_message("No wardrobe items match these filters.")
            return
        for child in self.preview.winfo_children(): child.destroy()
        self.preview_images = []
        for index, item in enumerate(self.current_outfit):
            card = ttk.Frame(self.preview, padding=8, relief="ridge")
            card.grid(row=index // 4, column=index % 4, padx=7, pady=7, sticky="nsew")
            pic = thumbnail(item.get("image", ""))
            if pic:
                self.preview_images.append(pic)
                ttk.Label(card, image=pic).pack()
            ttk.Label(card, text=item.get("name", "Unnamed"), font=("Segoe UI", 10, "bold")).pack()
            ttk.Label(card, text=f"{item.get('type')} • {item.get('style')}").pack()

    def save_current_outfit(self):
        if not self.current_outfit:
            messagebox.showinfo("Save Outfit", "Generate an outfit first.", parent=self)
            return
        self.saved_outfits.append({"id": uuid.uuid4().hex, "created_at": datetime.now().isoformat(timespec="seconds"), "style": self.style_var.get(), "weather": self.weather_var.get(), "items": [i["id"] for i in self.current_outfit]})
        self.store.save_outfits(self.saved_outfits)
        self.refresh_status()
        messagebox.showinfo("Saved", "This outfit was saved permanently.", parent=self)

    def open_saved_outfits(self):
        SavedOutfitsWindow(self)


class ItemForm(tk.Toplevel):
    def __init__(self, app: OutfitGeneratorApp, title: str, item=None, on_saved=None):
        super().__init__(app)
        self.app, self.item, self.on_saved = app, item, on_saved
        self.title(title); self.resizable(False, False); self.transient(app); self.grab_set()
        self.image_path = tk.StringVar(value=(item or {}).get("image", ""))
        self.name_var = tk.StringVar(value=(item or {}).get("name", ""))
        self.type_var = tk.StringVar(value=(item or {}).get("type", CLOTHING_TYPES[0]))
        self.main_color_var = tk.StringVar(value=(item or {}).get("main_color", COLORS[0]))
        self.secondary_var = tk.StringVar(value=(item or {}).get("secondary_color", ""))
        self.style_var = tk.StringVar(value=(item or {}).get("style", STYLES[1]))
        self.weather_var = tk.StringVar(value=(item or {}).get("weather", "Any"))
        form = ttk.Frame(self, padding=18); form.pack(fill="both", expand=True)
        ttk.Button(form, text="Upload Photo", command=self.choose_photo).grid(row=0, column=0, sticky="w")
        self.photo_label = ttk.Label(form, text=Path(self.image_path.get()).name or "No photo selected")
        self.photo_label.grid(row=0, column=1, sticky="w", padx=8)
        fields = [("Write name of cloth", ttk.Entry(form, textvariable=self.name_var)), ("Select Type", ttk.Combobox(form, textvariable=self.type_var, values=CLOTHING_TYPES, state="readonly")), ("Main Color", ttk.Combobox(form, textvariable=self.main_color_var, values=COLORS, state="readonly")), ("Secondary Color (Optional)", ttk.Combobox(form, textvariable=self.secondary_var, values=("",)+COLORS, state="readonly")), ("Select Style", ttk.Combobox(form, textvariable=self.style_var, values=STYLES[1:], state="readonly")), ("Weather", ttk.Combobox(form, textvariable=self.weather_var, values=WEATHERS, state="readonly"))]
        for row, (label, widget) in enumerate(fields, 1):
            ttk.Label(form, text=label).grid(row=row, column=0, sticky="w", pady=6)
            widget.grid(row=row, column=1, sticky="ew", pady=6)
        buttons = ttk.Frame(form); buttons.grid(row=8, column=0, columnspan=2, pady=(14,0), sticky="e")
        ttk.Button(buttons, text="Save", command=self.save).pack(side="left", padx=4)
        ttk.Button(buttons, text="Cancel", command=self.destroy).pack(side="left")
        form.columnconfigure(1, weight=1)

    def choose_photo(self):
        selected = filedialog.askopenfilename(parent=self, title="Select clothing photo", filetypes=[("Images", "*.png *.jpg *.jpeg *.webp *.bmp"), ("All files", "*.*")])
        if selected:
            self.image_path.set(selected); self.photo_label.config(text=Path(selected).name)

    def save(self):
        name = self.name_var.get().strip()
        if not name:
            messagebox.showerror("Missing name", "Please write a name for the clothing item.", parent=self); return
        saved_image = self.image_path.get()
        if saved_image and Path(saved_image).exists() and Path(saved_image).parent != IMAGE_DIR:
            destination = IMAGE_DIR / f"{uuid.uuid4().hex}{Path(saved_image).suffix.lower()}"
            shutil.copy2(saved_image, destination); saved_image = str(destination)
        record = {"id": (self.item or {}).get("id", uuid.uuid4().hex), "name": name, "type": self.type_var.get(), "main_color": self.main_color_var.get(), "secondary_color": self.secondary_var.get(), "style": self.style_var.get(), "weather": self.weather_var.get(), "image": saved_image}
        if self.item:
            index = next(i for i, old in enumerate(self.app.wardrobe) if old.get("id") == self.item.get("id")); self.app.wardrobe[index] = record
        else: self.app.wardrobe.append(record)
        self.app.store.save_wardrobe(self.app.wardrobe); self.app.refresh_status()
        if self.on_saved: self.on_saved()
        self.destroy()


class UploadPopup(ItemForm):
    def __init__(self, app, on_saved=None):
        super().__init__(app, "Add a New Cloth to Your Wardrobe", on_saved=on_saved)


class EditPopup(ItemForm):
    def __init__(self, app, item, on_saved=None):
        super().__init__(app, "Edit Wardrobe Item", item=item, on_saved=on_saved)


class WardrobeManager(tk.Toplevel):
    def __init__(self, app: OutfitGeneratorApp):
        super().__init__(app); self.app = app; self.title("Manage Wardrobe"); self.geometry("760x500"); self.transient(app)
        bar = ttk.Frame(self, padding=10); bar.pack(fill="x")
        ttk.Button(bar, text="Add New Cloth", command=lambda: UploadPopup(app, self.refresh)).pack(side="left")
        ttk.Button(bar, text="Close", command=self.destroy).pack(side="right")
        columns = ("name", "type", "colors", "style", "weather")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", selectmode="browse")
        for col, title in zip(columns, ("Name", "Type", "Colors", "Style", "Weather")):
            self.tree.heading(col, text=title); self.tree.column(col, width=130)
        self.tree.pack(fill="both", expand=True, padx=10)
        actions = ttk.Frame(self, padding=10); actions.pack(fill="x")
        ttk.Button(actions, text="Edit Selected", command=self.edit).pack(side="left", padx=4)
        ttk.Button(actions, text="Delete Selected", command=self.delete).pack(side="left")
        self.refresh()

    def refresh(self):
        self.tree.delete(*self.tree.get_children())
        for item in self.app.wardrobe:
            colors = item.get("main_color", "") + ((" / " + item["secondary_color"]) if item.get("secondary_color") else "")
            self.tree.insert("", "end", iid=item["id"], values=(item.get("name"), item.get("type"), colors, item.get("style"), item.get("weather", "Any")))

    def selected(self):
        selection = self.tree.selection()
        return next((i for i in self.app.wardrobe if selection and i.get("id") == selection[0]), None)

    def edit(self):
        item = self.selected()
        if item: EditPopup(self.app, item, self.refresh)
        else: messagebox.showinfo("Select an item", "Choose an item to edit.", parent=self)

    def delete(self):
        item = self.selected()
        if not item: messagebox.showinfo("Select an item", "Choose an item to delete.", parent=self); return
        if messagebox.askyesno("Delete item", f"Delete {item.get('name')}?", parent=self):
            self.app.wardrobe[:] = [i for i in self.app.wardrobe if i.get("id") != item.get("id")]
            self.app.store.save_wardrobe(self.app.wardrobe); self.app.refresh_status(); self.refresh()


class SavedOutfitsWindow(tk.Toplevel):
    def __init__(self, app: OutfitGeneratorApp):
        super().__init__(app); self.title("Saved Outfits"); self.geometry("700x450"); self.transient(app)
        tree = ttk.Treeview(self, columns=("date", "style", "weather", "items"), show="headings")
        for col, title in zip(("date", "style", "weather", "items"), ("Saved", "Style", "Weather", "Items")): tree.heading(col, text=title)
        tree.column("date", width=160); tree.column("items", width=280)
        by_id = {i.get("id"): i.get("name", "Unknown") for i in app.wardrobe}
        for outfit in reversed(app.saved_outfits):
            names = ", ".join(by_id.get(i, "Missing item") for i in outfit.get("items", []))
            tree.insert("", "end", values=(outfit.get("created_at", ""), outfit.get("style", "Any"), outfit.get("weather", "Any"), names))
        tree.pack(fill="both", expand=True, padx=10, pady=10)
        ttk.Button(self, text="Close", command=self.destroy).pack(pady=(0,10))
