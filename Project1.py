import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
import hashlib

FILE_NAME = Path(__file__).with_name('loginData.txt')


def hash_password(p: str) -> str:
    return hashlib.sha256(p.encode('utf-8')).hexdigest()


def load_users():
    users = {}
    if not FILE_NAME.exists():
        return users
    for line in FILE_NAME.read_text(encoding='utf-8').splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if '*' in line:
            parts = line.split('*')
        elif ':' in line:
            parts = line.split(':')
        elif ',' in line:
            parts = line.split(',')
        else:
            parts = line.split()
        if len(parts) >= 3:
            user, email, pw = parts[0].strip(), parts[1].strip(), parts[2].strip()
        elif len(parts) == 2:
            user, pw = parts[0].strip(), parts[1].strip()
            email = ''
        else:
            continue
        users[user] = (email, pw)
    return users


def save_user(username: str, email: str, password_hash: str):
    FILE_NAME.parent.mkdir(parents=True, exist_ok=True)
    with FILE_NAME.open('a', encoding='utf-8') as f:
        f.write(f"{username}*{email}*{password_hash}\n")


def _hex_to_rgb(h: str):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))


def _rgb_to_hex(c):
    return '#%02x%02x%02x' % c


def draw_linear_gradient(canvas, x1, y1, x2, y2, color1, color2, steps=100):
    r1, g1, b1 = _hex_to_rgb(color1)
    r2, g2, b2 = _hex_to_rgb(color2)
    height = y2 - y1
    for i in range(steps):
        frac = i / (steps - 1)
        r = int(r1 + (r2 - r1) * frac)
        g = int(g1 + (g2 - g1) * frac)
        b = int(b1 + (b2 - b1) * frac)
        y = int(y1 + (height * i / steps))
        canvas.create_rectangle(x1, y, x2, y + (height / steps) + 1, outline='', fill=_rgb_to_hex((r, g, b)))


class GradientButton(tk.Canvas):
    def __init__(self, parent, text, colors, command=None, width=140, height=40, radius=8, **kwargs):
        super().__init__(parent, width=width, height=height, highlightthickness=0, bd=0, cursor='hand2', **kwargs)
        # avoid clobbering tkinter internals (_w is used internally), use explicit names
        self.width_px = width
        self.height_px = height
        self._text = text
        self._colors = colors
        self._command = command
        self.radius = radius
        self._draw(False)
        self.bind('<Enter>', self._on_enter)
        self.bind('<Leave>', self._on_leave)
        self.bind('<Button-1>', self._on_click)

    def _draw(self, hover: bool):
        self.delete('all')
        c1, c2 = self._colors
        if hover:
            # slightly darken
            c1 = _rgb_to_hex(tuple(max(0, v-20) for v in _hex_to_rgb(c1)))
            c2 = _rgb_to_hex(tuple(max(0, v-20) for v in _hex_to_rgb(c2)))
        draw_linear_gradient(self, 0, 0, self.width_px, self.height_px, c1, c2, steps=60)
        self.create_text(self.width_px/2, self.height_px/2, text=self._text, fill='white', font=('Segoe UI', 10, 'bold'))

    def _on_enter(self, _):
        self._draw(True)

    def _on_leave(self, _):
        self._draw(False)

    def _on_click(self, _):
        if callable(self._command):
            self._command()


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Secure Login')
        self.geometry('820x520')
        self.minsize(720, 460)
        
        # dark/light mode
        self.dark_mode = False
        self.colors_light = {
            'bg': '#F3F6FB', 'card_bg': '#FFFFFF', 'card_border': '#E6EDF3',
            'text': '#0f172a', 'label': '#475569', 'accent': '#5B8DEF',
            'focus': '#5B8DEF', 'border': '#E6EDF3', 'error': '#EF4444'
        }
        self.colors_dark = {
            'bg': '#0f172a', 'card_bg': '#1E293B', 'card_border': '#334155',
            'text': '#F1F5F9', 'label': '#CBD5E1', 'accent': '#60A5FA',
            'focus': '#60A5FA', 'border': '#334155', 'error': '#FF6B6B'
        }
        self.colors = self.colors_light
        self.configure(bg=self.colors['bg'])
        
        try:
            self.style = ttk.Style(self)
            self.style.theme_use('clam')
        except Exception:
            self.style = None
        
        self.bind('<Configure>', self._on_resize)
        self._build()

    def _build(self):
        # main container for responsiveness
        self.main_frame = tk.Frame(self, bg=self.colors['bg'])
        self.main_frame.pack(fill='both', expand=True)
        
        # left panel with gradient
        self.left = tk.Canvas(self.main_frame, highlightthickness=0, bg=self.colors['bg'])
        self.left.pack(side='left', fill='y')
        
        # redraw gradient on initial build
        self._redraw_left_panel()

        # right panel with login form
        self.right = tk.Frame(self.main_frame, bg=self.colors['bg'])
        self.right.pack(side='right', expand=True, fill='both', padx=30, pady=30)
        
        # theme toggle button (top-left of card)
        self.theme_btn = tk.Button(self.right, text='🌙 Dark', bg=self.colors['card_bg'], fg=self.colors['text'], 
                                    relief='flat', cursor='hand2', command=self._toggle_theme, font=('Segoe UI', 9))
        self.theme_btn.pack(anchor='ne', padx=0, pady=(0, 12))

        # outlined login card (subtle border)
        self.card_border = tk.Frame(self.right, bg=self.colors['card_border'])
        self.card_border.pack(anchor='center', expand=True)
        self.card = tk.Frame(self.card_border, bg=self.colors['card_bg'])
        self.card.pack(padx=2, pady=2)

        tk.Label(self.card, text='Sign in or create account', bg=self.colors['card_bg'], fg=self.colors['text'], 
                font=('Segoe UI', 18, 'bold')).grid(row=0, column=0, columnspan=3, pady=(0, 12), sticky='w', padx=(12,0))

        # username field
        tk.Label(self.card, text='Username', bg=self.colors['card_bg'], fg=self.colors['label'], 
                font=('Segoe UI', 10)).grid(row=1, column=0, sticky='w', padx=(12,0))
        self.frame_user = tk.Frame(self.card, bg=self.colors['border'])
        self.frame_user.grid(row=2, column=0, columnspan=3, sticky='we', pady=(0, 8), padx=12)
        self.entry_user = tk.Entry(self.frame_user, width=36, bg=self.colors['card_bg'], fg=self.colors['text'], 
                                  relief='flat', font=('Segoe UI', 11), insertbackground=self.colors['text'])
        self.entry_user.pack(fill='x', padx=6, pady=6)
        self.entry_user.bind('<FocusIn>', lambda e: self._focus_in_frame(self.frame_user))
        self.entry_user.bind('<FocusOut>', lambda e: self._focus_out_frame(self.frame_user))

        # email field
        tk.Label(self.card, text='Email', bg=self.colors['card_bg'], fg=self.colors['label'], 
                font=('Segoe UI', 10)).grid(row=3, column=0, sticky='w', padx=(12,0))
        self.frame_email = tk.Frame(self.card, bg=self.colors['border'])
        self.frame_email.grid(row=4, column=0, columnspan=3, sticky='we', pady=(0, 8), padx=12)
        self.entry_email = tk.Entry(self.frame_email, width=36, bg=self.colors['card_bg'], fg=self.colors['text'], 
                                   relief='flat', font=('Segoe UI', 11), insertbackground=self.colors['text'])
        self.entry_email.pack(fill='x', padx=6, pady=6)
        self.entry_email.bind('<FocusIn>', lambda e: self._focus_in_frame(self.frame_email))
        self.entry_email.bind('<FocusOut>', lambda e: self._focus_out_frame(self.frame_email))

        # password field (fixed - same box structure as username/email)
        tk.Label(self.card, text='Password', bg=self.colors['card_bg'], fg=self.colors['label'], 
                font=('Segoe UI', 10)).grid(row=5, column=0, sticky='w', padx=(12,0))
        self.frame_pass = tk.Frame(self.card, bg=self.colors['border'])
        self.frame_pass.grid(row=6, column=0, columnspan=3, sticky='we', pady=(0, 8), padx=12)
        pass_inner = tk.Frame(self.frame_pass, bg=self.colors['card_bg'])
        pass_inner.pack(fill='x', padx=6, pady=6)
        self.entry_pass = tk.Entry(pass_inner, width=28, bg=self.colors['card_bg'], fg=self.colors['text'], 
                                  relief='flat', show='*', font=('Segoe UI', 11), insertbackground=self.colors['text'])
        self.entry_pass.pack(side='left', fill='x', expand=True)
        self.eye_btn = tk.Button(pass_inner, text='SHOW', bg=self.colors['card_bg'], fg=self.colors['text'], 
                                relief='flat', command=self._toggle_password, cursor='hand2', font=('Segoe UI', 9))
        self.eye_btn.pack(side='right', padx=(6, 0))
        self.entry_pass.bind('<FocusIn>', lambda e: self._focus_in_frame(self.frame_pass))
        self.entry_pass.bind('<FocusOut>', lambda e: self._focus_out_frame(self.frame_pass))

        # error message
        self.msg = tk.Label(self.card, text='', bg=self.colors['card_bg'], fg=self.colors['error'])
        self.msg.grid(row=7, column=0, columnspan=3, sticky='w', padx=12)

        # gradient buttons
        self.btn_frame = tk.Frame(self.card, bg=self.colors['card_bg'])
        self.btn_frame.grid(row=8, column=0, columnspan=3, pady=16, sticky='we', padx=12)

        self.btn_sign = GradientButton(self.btn_frame, 'Create account', ('#7B61FF', '#5B8DEF'), 
                                      command=self._on_signup, width=180, height=44)
        self.btn_sign.pack(side='left', padx=(0, 12))

        self.btn_login = GradientButton(self.btn_frame, 'Sign In', ('#2DD4BF', '#06B6D4'), 
                                       command=self._on_login, width=140, height=44)
        self.btn_login.pack(side='left')

        for i in range(3):
            self.card.grid_columnconfigure(i, weight=1)

    def _redraw_left_panel(self):
        self.left.delete('all')
        self.left.config(width=320, bg=self.colors['bg'])
        # gradient mix: purple -> blue -> teal
        draw_linear_gradient(self.left, 0, 0, 320, 520, '#7B61FF', '#5B8DEF', steps=120)
        draw_linear_gradient(self.left, 0, 0, 320, 520, '#5B8DEF', '#2DD4BF', steps=120)
        self.left.create_text(160, 160, text='App Login', fill='white', font=('Segoe UI', 34, 'bold'))

    def _on_resize(self, event):
        # responsive behavior: adapt left panel width on window resize
        if event.widget == self:
            self.left.config(width=max(200, int(self.winfo_width() * 0.35)))

    def _toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.colors = self.colors_dark if self.dark_mode else self.colors_light
        self.configure(bg=self.colors['bg'])
        self.main_frame.config(bg=self.colors['bg'])
        self.right.config(bg=self.colors['bg'])
        
        self._redraw_left_panel()
        self.theme_btn.config(text='☀️ Light' if self.dark_mode else '🌙 Dark', 
                             bg=self.colors['card_bg'], fg=self.colors['text'])
        self.card_border.config(bg=self.colors['card_border'])
        self.card.config(bg=self.colors['card_bg'])
        
        # update all labels and entry fields
        for widget in self.card.winfo_children():
            if isinstance(widget, tk.Label):
                widget.config(bg=self.colors['card_bg'], fg=self.colors['label'] if widget.cget('text') != 'Sign in or create account' else self.colors['text'])
        
        self.frame_user.config(bg=self.colors['border'])
        self.entry_user.config(bg=self.colors['card_bg'], fg=self.colors['text'], insertbackground=self.colors['text'])
        
        self.frame_email.config(bg=self.colors['border'])
        self.entry_email.config(bg=self.colors['card_bg'], fg=self.colors['text'], insertbackground=self.colors['text'])
        
        self.frame_pass.config(bg=self.colors['border'])
        self.entry_pass.config(bg=self.colors['card_bg'], fg=self.colors['text'], insertbackground=self.colors['text'])
        self.eye_btn.config(bg=self.colors['card_bg'], fg=self.colors['text'])
        
        self.msg.config(bg=self.colors['card_bg'], fg=self.colors['error'])
        self.btn_frame.config(bg=self.colors['card_bg'])


    def _focus_in_frame(self, frame):
        frame.config(bg=self.colors['focus'])

    def _focus_out_frame(self, frame):
        frame.config(bg=self.colors['border'])


    def _toggle_password(self):
        if self.entry_pass.cget('show') == '*':
            self.entry_pass.config(show='')
            self.eye_btn.config(text='HIDE')
        else:
            self.entry_pass.config(show='*')
            self.eye_btn.config(text='SHOW')

    def _on_signup(self):
        u = self.entry_user.get().strip()
        e = self.entry_email.get().strip()
        p = self.entry_pass.get()
        if not u or not e or not p:
            self.msg.config(text='Enter username, email and password')
            return
        users = load_users()
        if u in users:
            self.msg.config(text='Username already exists')
            return
        save_user(u, e, hash_password(p))
        messagebox.showinfo('Account created', 'Account created successfully — you can now sign in')
        self._clear()

    def _on_login(self):
        u = self.entry_user.get().strip()
        p = self.entry_pass.get()
        if not u or not p:
            self.msg.config(text='Please enter username and password')
            return
        users = load_users()
        stored = users.get(u)
        if stored is None:
            self.msg.config(text='User not found — try Create account')
            return
        email, stored_pw = stored
        if stored_pw == hash_password(p) or stored_pw == p:
            messagebox.showinfo('Welcome', f'Hello, {u}!\n{email}')
            self.msg.config(text='')
            self._clear()
        else:
            self.msg.config(text='Incorrect password')

    def _clear(self):
        self.entry_user.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)
        self.entry_pass.delete(0, tk.END)


if __name__ == '__main__':
    app = App()
    app.mainloop()
