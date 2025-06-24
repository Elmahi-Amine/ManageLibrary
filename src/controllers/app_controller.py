from views.main_view import MainView 
from views.home_view import HomeView

class AppController:
    def __init__(self, root):
        self.root = root
        self.menu_visible = False

        # View
        self.view = MainView(root, self)

        # Bind events
        root.bind("<Button-1>", self.on_click_outside)
        root.bind("<Configure>", self.on_window_resize)

    def show_Home_view(self):
        self.clear_content()
        home_view = HomeView(self.view.content_area)
        home_view.pack(fill="both", expand=True)
        self.hide_menu()

    def clear_content(self):
        for widget in self.view.content_area.winfo_children():
            widget.destroy()

    def toggle_menu(self):
        if self.menu_visible:
            self.hide_menu()
        else:
            self.show_menu()

    def show_menu(self):
        self.update_menu_height()
        self.animate_menu(-self.view.menu_width, 0)
        self.menu_visible = True

    def hide_menu(self):
        self.animate_menu(0, -self.view.menu_width)
        self.menu_visible = False

    def animate_menu(self, start_x, end_x):
        delta = 10 if end_x > start_x else -10
        for x in range(start_x, end_x, delta):
            self.view.menu_frame.place(x=x, y=0)
            self.root.update()
        self.view.menu_frame.place(x=end_x, y=0)

    def on_click_outside(self, event):
        if self.menu_visible:
            x, y = event.x_root, event.y_root
            menu_x1 = self.view.menu_frame.winfo_rootx()
            menu_y1 = self.view.menu_frame.winfo_rooty()
            menu_x2 = menu_x1 + self.view.menu_frame.winfo_width()
            menu_y2 = menu_y1 + self.view.menu_frame.winfo_height()
            if not (menu_x1 <= x <= menu_x2 and menu_y1 <= y <= menu_y2):
                self.hide_menu()

    def on_window_resize(self, event):
        self.update_menu_height()

    def update_menu_height(self):
        height = self.root.winfo_height()
        self.view.menu_frame.config(height=height)
        self.view.menu_frame.place(y=0)