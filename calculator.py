"""Sandbox Calculator - a small desktop calculator for basic arithmetic.

Run:  python calculator.py
"""

import tkinter as tk

APP_NAME = "Sandbox Calculator"
VERSION = "1.0.0"

# Theme (shared with the project's web page)
BG = "#16181d"
DISPLAY_BG = "#0f1115"
FG = "#e8eaed"
MUTED = "#8b93a3"
DIGIT_BG = "#262a33"
DIGIT_HOVER = "#323742"
FUNC_BG = "#343945"
FUNC_HOVER = "#414755"
OP_BG = "#33291d"
OP_HOVER = "#443524"
ACCENT = "#f0a04b"
ACCENT_HOVER = "#f5b370"


def format_number(value):
    """Render a float without float-noise or a pointless trailing zero."""
    if value != value or value in (float("inf"), float("-inf")):
        return "Error"
    if value == int(value) and abs(value) < 1e16:
        return str(int(value))
    return f"{value:.12g}"


class Calculator(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=BG)
        self.pack(fill="both", expand=True)

        self.current = "0"      # number currently being typed
        self.stored = None      # left-hand operand
        self.op = None          # pending operator
        self.fresh = True       # next digit starts a new number
        self.error = False

        self._build_display()
        self._build_keypad()
        self._bind_keys()

    # ---------- UI ----------

    def _build_display(self):
        wrap = tk.Frame(self, bg=DISPLAY_BG)
        wrap.pack(fill="x", padx=12, pady=(12, 8))

        self.history_var = tk.StringVar(value="")
        tk.Label(
            wrap, textvariable=self.history_var, anchor="e",
            bg=DISPLAY_BG, fg=MUTED, font=("Segoe UI", 11),
        ).pack(fill="x", padx=14, pady=(10, 0))

        self.display_var = tk.StringVar(value="0")
        tk.Label(
            wrap, textvariable=self.display_var, anchor="e",
            bg=DISPLAY_BG, fg=FG, font=("Segoe UI", 30, "bold"),
        ).pack(fill="x", padx=14, pady=(0, 12))

    def _button(self, parent, text, command, kind="digit"):
        palette = {
            "digit": (DIGIT_BG, DIGIT_HOVER, FG),
            "func": (FUNC_BG, FUNC_HOVER, FG),
            "op": (OP_BG, OP_HOVER, ACCENT),
            "eq": (ACCENT, ACCENT_HOVER, "#1b1400"),
        }[kind]
        bg, hover, fg = palette

        btn = tk.Button(
            parent, text=text, command=command,
            bg=bg, fg=fg, activebackground=hover, activeforeground=fg,
            font=("Segoe UI", 15, "bold" if kind == "eq" else "normal"),
            relief="flat", bd=0, highlightthickness=0, cursor="hand2",
        )
        btn.bind("<Enter>", lambda _e: btn.config(bg=hover))
        btn.bind("<Leave>", lambda _e: btn.config(bg=bg))
        return btn

    def _build_keypad(self):
        pad = tk.Frame(self, bg=BG)
        pad.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        layout = [
            [("C", self.clear, "func"), ("⌫", self.backspace, "func"),
             ("%", self.percent, "func"), ("÷", lambda: self.set_op("/"), "op")],
            [("7", lambda: self.digit("7"), "digit"), ("8", lambda: self.digit("8"), "digit"),
             ("9", lambda: self.digit("9"), "digit"), ("×", lambda: self.set_op("*"), "op")],
            [("4", lambda: self.digit("4"), "digit"), ("5", lambda: self.digit("5"), "digit"),
             ("6", lambda: self.digit("6"), "digit"), ("−", lambda: self.set_op("-"), "op")],
            [("1", lambda: self.digit("1"), "digit"), ("2", lambda: self.digit("2"), "digit"),
             ("3", lambda: self.digit("3"), "digit"), ("+", lambda: self.set_op("+"), "op")],
            [("±", self.negate, "func"), ("0", lambda: self.digit("0"), "digit"),
             (".", self.dot, "digit"), ("=", self.equals, "eq")],
        ]

        for r, row in enumerate(layout):
            pad.rowconfigure(r, weight=1, minsize=48)
            for c, (text, cmd, kind) in enumerate(row):
                pad.columnconfigure(c, weight=1, minsize=60)
                self._button(pad, text, cmd, kind).grid(
                    row=r, column=c, sticky="nsew", padx=4, pady=4
                )

    def _bind_keys(self):
        root = self.winfo_toplevel()
        for d in "0123456789":
            root.bind(d, lambda e, d=d: self.digit(d))
        for key, op in (("plus", "+"), ("minus", "-"), ("asterisk", "*"), ("slash", "/")):
            root.bind(f"<{key}>", lambda e, op=op: self.set_op(op))
        root.bind("<period>", lambda e: self.dot())
        root.bind("<Return>", lambda e: self.equals())
        root.bind("<KP_Enter>", lambda e: self.equals())
        root.bind("<equal>", lambda e: self.equals())
        root.bind("<BackSpace>", lambda e: self.backspace())
        root.bind("<Escape>", lambda e: self.clear())
        root.bind("<percent>", lambda e: self.percent())

    # ---------- state ----------

    def _refresh(self):
        self.display_var.set(self.current)
        if self.op and self.stored is not None:
            symbol = {"+": "+", "-": "−", "*": "×", "/": "÷"}[self.op]
            self.history_var.set(f"{format_number(self.stored)} {symbol}")
        else:
            self.history_var.set("")

    def _fail(self, message):
        self.current = message
        self.stored = None
        self.op = None
        self.fresh = True
        self.error = True
        self.display_var.set(message)
        self.history_var.set("")

    def _clear_error(self):
        if self.error:
            self.clear()

    def digit(self, d):
        self._clear_error()
        if self.fresh:
            self.current = "0"
            self.fresh = False
        self.current = d if self.current == "0" else self.current + d
        self._refresh()

    def dot(self):
        self._clear_error()
        if self.fresh:
            self.current = "0"
            self.fresh = False
        if "." not in self.current:
            self.current += "."
        self._refresh()

    def backspace(self):
        self._clear_error()
        if self.fresh:
            return
        self.current = self.current[:-1] or "0"
        if self.current == "-":
            self.current = "0"
        self._refresh()

    def negate(self):
        self._clear_error()
        if self.current.startswith("-"):
            self.current = self.current[1:]
        elif self.current != "0":
            self.current = "-" + self.current
        self._refresh()

    def percent(self):
        self._clear_error()
        self.current = format_number(float(self.current) / 100)
        self.fresh = False
        self._refresh()

    def clear(self):
        self.current = "0"
        self.stored = None
        self.op = None
        self.fresh = True
        self.error = False
        self._refresh()

    def _apply(self):
        """Fold the pending operation. Returns False if it could not be done."""
        a, b = self.stored, float(self.current)
        if self.op == "/" and b == 0:
            self._fail("Cannot divide by zero")
            return False
        result = {"+": lambda: a + b, "-": lambda: a - b,
                  "*": lambda: a * b, "/": lambda: a / b}[self.op]()
        if result != result or result in (float("inf"), float("-inf")):
            self._fail("Result too large")
            return False
        self.current = format_number(result)
        self.stored = result
        return True

    def set_op(self, op):
        self._clear_error()
        if self.op is not None and not self.fresh:
            if not self._apply():
                return
        else:
            self.stored = float(self.current)
        self.op = op
        self.fresh = True
        self._refresh()

    def equals(self):
        self._clear_error()
        if self.op is None:
            return
        if not self._apply():
            return
        self.stored = None
        self.op = None
        self.fresh = True
        self._refresh()


def main():
    root = tk.Tk()
    root.title(APP_NAME)
    root.configure(bg=BG)
    root.geometry("340x480")
    root.minsize(280, 400)
    Calculator(root)
    root.mainloop()


if __name__ == "__main__":
    main()
