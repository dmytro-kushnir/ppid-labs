"""Tkinter GUI for mock USB mass-storage transfer (PPID lab 3)."""

from __future__ import annotations

import tempfile
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk
from typing import Any, Optional

from host.usb_scan import format_device_details, get_device_by_name, load_devices


class UsbGuiApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("PPID Lab 3 — Mock USB transfer")
        self.devices: list[dict[str, Any]] = []
        self.storage_dir = Path(tempfile.mkdtemp(prefix="ppid_usb_"))
        self._build()
        self._scan_devices()

    def _build(self) -> None:
        frame = ttk.Frame(self.root, padding=10)
        frame.grid(row=0, column=0, sticky="nsew")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        top_row = ttk.Frame(frame)
        top_row.grid(row=0, column=0, columnspan=3, sticky="ew", pady=(0, 4))
        ttk.Button(top_row, text="Сканувати", command=self._scan_devices).pack(side="left")

        ttk.Label(frame, text="Mock USB-пристрій:").grid(row=1, column=0, sticky="w")
        self.device_var = tk.StringVar()
        self.device_combo = ttk.Combobox(
            frame, textvariable=self.device_var, values=[], width=40, state="readonly"
        )
        self.device_combo.grid(row=1, column=1, columnspan=2, sticky="ew", pady=4)
        self.device_combo.bind("<<ComboboxSelected>>", lambda _e: self._show_device_details())

        ttk.Label(frame, text="Властивості:").grid(row=2, column=0, sticky="nw")
        self.details = tk.Text(frame, width=50, height=8, state="disabled")
        self.details.grid(row=2, column=1, columnspan=2, sticky="ew", pady=4)

        ttk.Button(frame, text="Відкрити файл", command=self._open_file).grid(
            row=3, column=0, pady=4, sticky="w"
        )
        ttk.Label(
            frame,
            text="Повідомлення (прізвище латиницею, літери A–Z) — введіть або відкрити .txt",
            wraplength=420,
        ).grid(row=3, column=1, columnspan=2, sticky="w", padx=(8, 0))
        self.text = tk.Text(frame, width=50, height=10)
        self.text.grid(row=4, column=0, columnspan=3, pady=4, sticky="nsew")

        ttk.Button(frame, text="Записати на mock-накопичувач", command=self._save).grid(
            row=5, column=0, columnspan=3, pady=4
        )

        ttk.Label(
            frame,
            text=f"Каталог накопичувача: {self.storage_dir}",
            wraplength=420,
        ).grid(row=6, column=0, columnspan=3, sticky="w")

        frame.columnconfigure(1, weight=1)
        frame.rowconfigure(4, weight=1)

    def _selected_device(self) -> Optional[dict[str, Any]]:
        name = self.device_var.get()
        if not name:
            return None
        return get_device_by_name(name) or next(
            (d for d in self.devices if d["name"] == name), None
        )

    def _set_details(self, text: str) -> None:
        self.details.configure(state="normal")
        self.details.delete("1.0", tk.END)
        self.details.insert(tk.END, text)
        self.details.configure(state="disabled")

    def _scan_devices(self) -> None:
        self.devices = load_devices()
        names = [d["name"] for d in self.devices]
        self.device_combo["values"] = names
        if names:
            current = self.device_var.get()
            self.device_var.set(current if current in names else names[0])
            self._show_device_details()
        else:
            self.device_var.set("")
            self._set_details("Пристрої не знайдено")

    def _show_device_details(self) -> None:
        dev = self._selected_device()
        if dev is None:
            self._set_details("")
            return
        self._set_details(format_device_details(dev))

    def _open_file(self) -> None:
        path = filedialog.askopenfilename(
            title="Відкрити текстовий файл",
            filetypes=[
                ("Текстові файли", "*.txt"),
                ("Markdown", "*.md"),
                ("Усі файли", "*.*"),
            ],
        )
        if not path:
            return
        raw = Path(path).read_bytes()
        if b"\x00" in raw[:8192]:
            messagebox.showerror(
                "Помилка",
                "Обрано бінарний файл (зображення, PDF тощо).\n"
                "Для лаб. 3 — текстовий .txt із прізвищем латиницею (напр. IVANOV).",
            )
            return
        content: str | None = None
        for encoding in ("utf-8", "cp1251"):
            try:
                content = raw.decode(encoding)
                break
            except UnicodeDecodeError:
                continue
        if content is None:
            messagebox.showerror(
                "Помилка",
                "Не вдалося прочитати файл як текст (UTF-8 або cp1251).",
            )
            return
        self.text.delete("1.0", tk.END)
        self.text.insert(tk.END, content)

    def _save(self) -> None:
        content = self.text.get("1.0", tk.END).strip()
        if not content:
            messagebox.showwarning("Увага", "Немає даних для запису")
            return
        dev = self._selected_device()
        label = dev["name"] if dev else "unknown"
        target = self.storage_dir / "message.txt"
        try:
            target.write_text(content, encoding="cp1251")
        except UnicodeEncodeError:
            messagebox.showerror(
                "Помилка",
                "Текст містить символи, яких немає в cp1251.\n"
                "Записуйте прізвище латиницею (літери A–Z), не PDF чи зображення.",
            )
            return
        messagebox.showinfo("Готово", f"Записано на {label}:\n{target}")


def main() -> None:
    root = tk.Tk()
    UsbGuiApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
