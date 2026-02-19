import flet as ft
import json
import os

class Task(ft.UserControl):
    def __init__(self, task_name, completed, task_status_change, task_delete):
        super().__init__()
        self.completed = completed
        self.task_name = task_name
        self.task_status_change = task_status_change
        self.task_delete = task_delete

    def build(self):
        self.display_task = ft.Checkbox(
            value=self.completed, 
            label=self.task_name, 
            on_change=self.status_changed,
            fill_color=ft.colors.INDIGO_ACCENT,
            check_color=ft.colors.WHITE,
        )
        self.edit_name = ft.TextField(expand=1, border_color=ft.colors.INDIGO_ACCENT, border_radius=8)

        self.display_view = ft.Container(
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    self.display_task,
                    ft.Row(
                        spacing=0,
                        controls=[
                            ft.IconButton(
                                icon=ft.icons.EDIT_ROUNDED,
                                tooltip="Editar",
                                on_click=self.edit_clicked,
                                icon_color=ft.colors.BLUE_GREY_200,
                                icon_size=20,
                            ),
                            ft.IconButton(
                                ft.icons.DELETE_OUTLINE_ROUNDED,
                                tooltip="Excluir",
                                on_click=self.delete_clicked,
                                icon_color=ft.colors.RED_300,
                                icon_size=20,
                            ),
                        ],
                    ),
                ],
            ),
            padding=ft.padding.all(10),
            bgcolor=ft.colors.with_opacity(0.05, ft.colors.WHITE),
            border_radius=12,
            margin=ft.margin.only(bottom=10),
        )

        self.edit_view = ft.Row(
            visible=False,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                self.edit_name,
                ft.IconButton(
                    icon=ft.icons.CHECK_CIRCLE_ROUNDED,
                    icon_color=ft.colors.GREEN_ACCENT_400,
                    on_click=self.save_clicked,
                ),
            ],
        )
        return ft.Column(controls=[self.display_view, self.edit_view])

    def edit_clicked(self, e):
        self.edit_name.value = self.display_task.label
        self.display_view.visible = False
        self.edit_view.visible = True
        self.update()

    def save_clicked(self, e):
        self.display_task.label = self.edit_name.value
        self.task_name = self.edit_name.value
        self.display_view.visible = True
        self.edit_view.visible = False
        self.update()
        self.task_status_change(self)

    def status_changed(self, e):
        self.completed = self.display_task.value
        self.task_status_change(self)

    def delete_clicked(self, e):
        self.task_delete(self)


class TodoApp(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.tasks = []
        self.data_file = "todo_data.json"
        self.load_data()

    def build(self):
        self.new_task = ft.TextField(
            hint_text="O que vamos realizar hoje?",
            on_submit=self.add_clicked,
            expand=True,
            border_radius=15,
            bgcolor=ft.colors.with_opacity(0.1, ft.colors.WHITE),
            border_color=ft.colors.TRANSPARENT,
            focused_border_color=ft.colors.INDIGO_ACCENT,
            content_padding=20,
        )
        
        self.tasks_view = ft.Column(scroll=ft.ScrollMode.ADAPTIVE, height=400)

        self.filter = ft.Tabs(
            selected_index=0,
            on_change=self.tabs_changed,
            tabs=[ft.Tab(text="Todas"), ft.Tab(text="Ativas"), ft.Tab(text="Finas")],
            indicator_color=ft.colors.INDIGO_ACCENT,
            label_color=ft.colors.WHITE,
            unselected_label_color=ft.colors.WHITE30,
        )

        self.items_left = ft.Text("0 tarefas restantes", color=ft.colors.WHITE30, size=12)
        
        # Barra de Progresso Moderna
        self.progress_bar = ft.ProgressBar(
            value=0, 
            width=600, 
            color=ft.colors.INDIGO_ACCENT, 
            bgcolor=ft.colors.WHITE10,
            border_radius=5
        )
        self.progress_text = ft.Text("0% concluído", size=12, color=ft.colors.INDIGO_ACCENT, weight=ft.FontWeight.BOLD)

        return ft.Container(
            content=ft.Column(
                controls=[
                    # Header
                    ft.Row(
                        [
                            ft.Icon(ft.icons.CHECKLIST_ROUNDED, color=ft.colors.INDIGO_ACCENT, size=40),
                            ft.Text(value="Check-It", size=32, weight=ft.FontWeight.BOLD),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    ft.Divider(height=20, color=ft.colors.TRANSPARENT),
                    
                    # Progress Section
                    ft.Column([
                        ft.Row([ft.Text("Seu Progresso", size=14, weight=ft.FontWeight.W_500), self.progress_text], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        self.progress_bar,
                    ], spacing=5),
                    
                    ft.Divider(height=20, color=ft.colors.TRANSPARENT),
                    
                    # Input Section
                    ft.Row(
                        controls=[
                            self.new_task,
                            ft.Container(
                                content=ft.IconButton(
                                    icon=ft.icons.ADD_ROUNDED, 
                                    on_click=self.add_clicked,
                                    icon_color=ft.colors.WHITE,
                                    icon_size=30,
                                ),
                                bgcolor=ft.colors.INDIGO_ACCENT,
                                border_radius=15,
                                padding=5,
                            ),
                        ],
                    ),
                    
                    # List Section
                    ft.Column(
                        spacing=15,
                        controls=[
                            self.filter,
                            self.tasks_view,
                            ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    self.items_left,
                                    ft.TextButton(
                                        text="Limpar Completas", 
                                        on_click=self.clear_clicked,
                                        style=ft.ButtonStyle(color=ft.colors.RED_ACCENT_200)
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
            padding=40,
            width=500,
            bgcolor=ft.colors.GREY_900,
            border_radius=30,
            border=ft.border.all(1, ft.colors.WHITE10),
        )

    def add_clicked(self, e):
        if self.new_task.value:
            task = Task(self.new_task.value, False, self.update_status, self.task_delete)
            self.tasks.append(task)
            self.tasks_view.controls.append(task)
            self.new_task.value = ""
            self.update_status()
            self.update()

    def task_delete(self, task):
        self.tasks.remove(task)
        self.tasks_view.controls.remove(task)
        self.update_status()
        self.update()

    def update_status(self, task=None):
        status = self.filter.tabs[self.filter.selected_index].text
        count_active = 0
        count_completed = 0
        
        for task in self.tasks:
            task.visible = (
                status == "Todas"
                or (status == "Ativas" and not task.completed)
                or (status == "Finas" and task.completed)
            )
            if not task.completed:
                count_active += 1
            else:
                count_completed += 1
        
        # Atualiza progresso
        total = len(self.tasks)
        progress = (count_completed / total) if total > 0 else 0
        self.progress_bar.value = progress
        self.progress_text.value = f"{int(progress * 100)}% concluído"
        
        self.items_left.value = f"{count_active} tarefa(s) restante(s)"
        self.save_data()
        self.update()

    def tabs_changed(self, e):
        self.update_status()

    def clear_clicked(self, e):
        for task in self.tasks[:]:
            if task.completed:
                self.task_delete(task)

    def save_data(self):
        data = [{"name": t.task_name, "completed": t.completed} for t in self.tasks]
        with open(self.data_file, "w") as f:
            json.dump(data, f)

    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, "r") as f:
                data = json.load(f)
                for item in data:
                    task = Task(item["name"], item["completed"], self.update_status, self.task_delete)
                    self.tasks.append(task)

    def did_mount(self):
        for task in self.tasks:
            self.tasks_view.controls.append(task)
        self.update_status()
        self.update()

def main(page: ft.Page):
    page.title = "Minha Lista To-Do"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK
    page.window_width = 650
    page.window_height = 800
    page.window_resizable = False
    
    # Adicionando app ao centro
    todo = TodoApp()
    page.add(todo)

if __name__ == "__main__":
    # Para rodar no navegador, usamos view=ft.AppView.WEB_BROWSER
    # Para rodar como app Windows, basta remover o parâmetro 'view'
    ft.app(target=main, view=ft.AppView.WEB_BROWSER)
