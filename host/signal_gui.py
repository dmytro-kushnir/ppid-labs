"""Reference tkinter GUI for UART and NRZI signal visualization (PPID labs 1–2)."""

from __future__ import annotations

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from typing import Optional

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from encoding.uart_plot import (
    char_to_frame_bits_from_format,
    message_to_frames,
    plot_to_figure,
    transmission_time,
)
from encoding.usb_nrzi import (
    char_nrzi_bits,
    nrzi_bits_string,
    nrzi_encode_with_stuffing,
    plot_nrzi_char_to_figure,
    plot_nrzi_to_figure,
)
from host.uart_host import open_port, send_message

BAUD_VALUES = (50, 75, 100, 150, 300, 600, 1200, 2400, 4800, 9600, 19200, 38400)
FORMAT_VALUES = ("8N1", "7E1", "8N2")
ALL_CHARS_LABEL = "Усе повідомлення"


class SignalGuiApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("PPID Lab 1–2 — Signal visualization (reference)")
        self._canvas: Optional[FigureCanvasTkAgg] = None
        self._current_figure: Optional[Figure] = None
        self._build()

    def _build(self) -> None:
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True, padx=8, pady=8)

        self.uart_tab = ttk.Frame(notebook, padding=8)
        self.nrzi_tab = ttk.Frame(notebook, padding=8)
        notebook.add(self.uart_tab, text="UART")
        notebook.add(self.nrzi_tab, text="NRZI")

        self._build_uart_tab()
        self._build_nrzi_tab()
        self._build_plot_area()

    def _build_plot_area(self) -> None:
        plot_frame = ttk.LabelFrame(self.root, text="Графік", padding=8)
        plot_frame.pack(fill="both", expand=True, padx=8, pady=(0, 8))
        self.plot_container = ttk.Frame(plot_frame)
        self.plot_container.pack(fill="both", expand=True)

    def _set_figure(self, fig: Figure) -> None:
        if self._canvas is not None:
            self._canvas.get_tk_widget().destroy()
        if self._current_figure is not None:
            plt.close(self._current_figure)
        self._current_figure = fig
        self._canvas = FigureCanvasTkAgg(fig, master=self.plot_container)
        self._canvas.draw()
        self._canvas.get_tk_widget().pack(fill="both", expand=True)

    def _save_figure_png(self) -> None:
        if self._current_figure is None:
            messagebox.showwarning("Увага", "Спочатку побудуйте графік")
            return
        path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG", "*.png")],
        )
        if path:
            self._current_figure.savefig(path, dpi=150, bbox_inches="tight")
            messagebox.showinfo("Готово", f"Збережено: {path}")

    def _message(self, entry: tk.Entry) -> str:
        return entry.get().strip()

    def _char_index_from_combo(self, message: str, combo: ttk.Combobox) -> Optional[int]:
        value = combo.get()
        if value == ALL_CHARS_LABEL:
            return None
        return int(value)

    def _refresh_char_combo(self, message: str, combo: ttk.Combobox) -> None:
        values = [ALL_CHARS_LABEL] + [str(i) for i in range(len(message))]
        combo["values"] = values
        if combo.get() not in values:
            combo.set(ALL_CHARS_LABEL)

    def _build_uart_tab(self) -> None:
        frame = self.uart_tab

        ttk.Label(frame, text="Повідомлення:").grid(row=0, column=0, sticky="w")
        self.uart_message = tk.Entry(frame, width=40)
        self.uart_message.insert(0, "IVANOV")
        self.uart_message.grid(row=0, column=1, columnspan=2, sticky="ew", pady=2)
        self.uart_message.bind("<KeyRelease>", lambda _e: self._on_uart_message_change())

        ttk.Label(frame, text="Baud:").grid(row=1, column=0, sticky="w")
        self.uart_baud = ttk.Combobox(frame, values=[str(b) for b in BAUD_VALUES], width=10)
        self.uart_baud.set("9600")
        self.uart_baud.grid(row=1, column=1, sticky="w", pady=2)

        ttk.Label(frame, text="Формат:").grid(row=2, column=0, sticky="w")
        self.uart_format = ttk.Combobox(frame, values=list(FORMAT_VALUES), width=10)
        self.uart_format.set("8N1")
        self.uart_format.grid(row=2, column=1, sticky="w", pady=2)

        ttk.Label(frame, text="Символ:").grid(row=3, column=0, sticky="w")
        self.uart_char = ttk.Combobox(frame, width=20)
        self.uart_char.grid(row=3, column=1, sticky="w", pady=2)
        self.uart_char.bind("<<ComboboxSelected>>", lambda _e: self._update_uart_fields())
        self._refresh_char_combo(self._message(self.uart_message), self.uart_char)
        self.uart_char.set(ALL_CHARS_LABEL)

        ttk.Label(frame, text="Кадр (біти):").grid(row=4, column=0, sticky="nw")
        self.uart_frame_bits = tk.Text(frame, width=50, height=2, state="disabled")
        self.uart_frame_bits.grid(row=4, column=1, columnspan=2, sticky="ew", pady=2)

        ttk.Label(frame, text="Hex:").grid(row=5, column=0, sticky="w")
        self.uart_hex = tk.Entry(frame, width=20, state="readonly")
        self.uart_hex.grid(row=5, column=1, sticky="w", pady=2)

        ttk.Label(frame, text="Час, с:").grid(row=6, column=0, sticky="w")
        self.uart_time = tk.Entry(frame, width=20, state="readonly")
        self.uart_time.grid(row=6, column=1, sticky="w", pady=2)

        btn_row = ttk.Frame(frame)
        btn_row.grid(row=7, column=0, columnspan=3, pady=8, sticky="w")
        ttk.Button(btn_row, text="Графік UART", command=self._plot_uart).pack(side="left", padx=(0, 4))
        ttk.Button(btn_row, text="Зберегти PNG", command=self._save_figure_png).pack(side="left", padx=4)
        ttk.Button(btn_row, text="Надіслати (loop://)", command=self._send_loopback).pack(side="left", padx=4)

        frame.columnconfigure(1, weight=1)
        self._update_uart_fields()

    def _build_nrzi_tab(self) -> None:
        frame = self.nrzi_tab

        ttk.Label(frame, text="Повідомлення:").grid(row=0, column=0, sticky="w")
        self.nrzi_message = tk.Entry(frame, width=40)
        self.nrzi_message.insert(0, "IVANOV")
        self.nrzi_message.grid(row=0, column=1, columnspan=2, sticky="ew", pady=2)
        self.nrzi_message.bind("<KeyRelease>", lambda _e: self._on_nrzi_message_change())

        ttk.Label(frame, text="Символ:").grid(row=1, column=0, sticky="w")
        self.nrzi_char = ttk.Combobox(frame, width=20)
        self.nrzi_char.grid(row=1, column=1, sticky="w", pady=2)
        self.nrzi_char.bind("<<ComboboxSelected>>", lambda _e: self._update_nrzi_fields())
        self._refresh_char_combo(self._message(self.nrzi_message), self.nrzi_char)
        if self._message(self.nrzi_message):
            self.nrzi_char.set("0")
        else:
            self.nrzi_char.set(ALL_CHARS_LABEL)

        for row, label, attr in (
            (2, "Raw (8 біт):", "nrzi_raw"),
            (3, "Після bit stuffing:", "nrzi_stuffed"),
            (4, "NRZI (рядок):", "nrzi_levels"),
        ):
            ttk.Label(frame, text=label).grid(row=row, column=0, sticky="nw")
            widget = tk.Text(frame, width=50, height=2, state="disabled")
            widget.grid(row=row, column=1, columnspan=2, sticky="ew", pady=2)
            setattr(self, attr, widget)

        btn_row = ttk.Frame(frame)
        btn_row.grid(row=5, column=0, columnspan=3, pady=8, sticky="w")
        ttk.Button(btn_row, text="Графік NRZI (символ)", command=self._plot_nrzi_char).pack(
            side="left", padx=(0, 4)
        )
        ttk.Button(btn_row, text="Графік NRZI (усі)", command=self._plot_nrzi_all).pack(
            side="left", padx=4
        )
        ttk.Button(btn_row, text="Зберегти PNG", command=self._save_figure_png).pack(side="left", padx=4)

        frame.columnconfigure(1, weight=1)
        self._update_nrzi_fields()

    def _set_text(self, widget: tk.Text, value: str) -> None:
        widget.configure(state="normal")
        widget.delete("1.0", tk.END)
        widget.insert(tk.END, value)
        widget.configure(state="disabled")

    def _set_readonly_entry(self, widget: tk.Entry, value: str) -> None:
        widget.configure(state="normal")
        widget.delete(0, tk.END)
        widget.insert(0, value)
        widget.configure(state="readonly")

    def _on_uart_message_change(self) -> None:
        message = self._message(self.uart_message)
        self._refresh_char_combo(message, self.uart_char)
        self._update_uart_fields()

    def _on_nrzi_message_change(self) -> None:
        message = self._message(self.nrzi_message)
        self._refresh_char_combo(message, self.nrzi_char)
        if message and self.nrzi_char.get() == ALL_CHARS_LABEL:
            self.nrzi_char.set("0")
        self._update_nrzi_fields()

    def _update_uart_fields(self) -> None:
        message = self._message(self.uart_message)
        fmt = self.uart_format.get()
        if not message:
            self._set_text(self.uart_frame_bits, "")
            self._set_readonly_entry(self.uart_hex, "")
            self._set_readonly_entry(self.uart_time, "")
            return

        idx = self._char_index_from_combo(message, self.uart_char)
        if idx is None:
            frames = message_to_frames(message, fmt)
            frame_bits = " | ".join(frames)
            hex_vals = " ".join(f"0x{ord(c):02X}" for c in message)
        else:
            target = message[idx]
            frame_bits = char_to_frame_bits_from_format(target, fmt)
            hex_vals = f"0x{ord(target):02X}"
        self._set_text(self.uart_frame_bits, frame_bits)
        self._set_readonly_entry(self.uart_hex, hex_vals)

        baud = int(self.uart_baud.get())
        duration = transmission_time(message, baud, fmt)
        self._set_readonly_entry(self.uart_time, f"{duration:.6f}")

    def _update_nrzi_fields(self) -> None:
        message = self._message(self.nrzi_message)
        if not message:
            for widget in (self.nrzi_raw, self.nrzi_stuffed, self.nrzi_levels):
                self._set_text(widget, "")
            return

        value = self.nrzi_char.get()
        if value == ALL_CHARS_LABEL:
            raw, stuffed, _levels = nrzi_encode_with_stuffing(message)
            nrzi_str = nrzi_bits_string(stuffed)
        else:
            raw, stuffed, _levels = char_nrzi_bits(message[int(value)])
            nrzi_str = nrzi_bits_string(stuffed)

        self._set_text(self.nrzi_raw, raw)
        self._set_text(self.nrzi_stuffed, stuffed)
        self._set_text(self.nrzi_levels, nrzi_str)

    def _plot_uart(self) -> None:
        message = self._message(self.uart_message)
        if not message:
            messagebox.showwarning("Увага", "Введіть повідомлення")
            return
        try:
            baud = int(self.uart_baud.get())
            fmt = self.uart_format.get()
            idx = self._char_index_from_combo(message, self.uart_char)
            fig, duration = plot_to_figure(message, baud, fmt, idx)
            self._set_figure(fig)
            self._set_readonly_entry(self.uart_time, f"{duration:.6f}")
        except (ValueError, IndexError) as exc:
            messagebox.showerror("Помилка", str(exc))

    def _plot_nrzi_char(self) -> None:
        message = self._message(self.nrzi_message)
        if not message:
            messagebox.showwarning("Увага", "Введіть повідомлення")
            return
        value = self.nrzi_char.get()
        if value == ALL_CHARS_LABEL:
            messagebox.showinfo("Підказка", "Оберіть індекс символу (0, 1, …) для посимвольного графіка")
            return
        try:
            fig, _, _, _ = plot_nrzi_char_to_figure(message, int(value))
            self._set_figure(fig)
            self._update_nrzi_fields()
        except (ValueError, IndexError) as exc:
            messagebox.showerror("Помилка", str(exc))

    def _plot_nrzi_all(self) -> None:
        message = self._message(self.nrzi_message)
        if not message:
            messagebox.showwarning("Увага", "Введіть повідомлення")
            return
        fig, _, _, _ = plot_nrzi_to_figure(message)
        self._set_figure(fig)

    def _send_loopback(self) -> None:
        message = self._message(self.uart_message)
        if not message:
            messagebox.showwarning("Увага", "Введіть повідомлення")
            return
        try:
            baud = int(self.uart_baud.get())
            with open_port("loop://", baud, timeout=2) as ser:
                nbytes = send_message(ser, message)
            messagebox.showinfo("Готово", f"Надіслано {nbytes} байт на loop:// @ {baud} бод")
        except Exception as exc:
            messagebox.showerror("Помилка", str(exc))


def main() -> None:
    root = tk.Tk()
    SignalGuiApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
