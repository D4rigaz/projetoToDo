import flet as ft
import json
import os

def main(page: ft.Page):
    # --- REVISOR: Configurações de Segurança de Layout ---
    page.title = "quadro to do list Darigaz"
    page.bgcolor = "#000000"
    page.horizontal_alignment = "center"
    page.padding = 50
    page.spacing = 20
    page.theme_mode = "dark"

    data_file = "todo_data.json"

    # --- LÓGICA DO QA (CRUD) ---
    def save_data():
        data = []
        for ctrl in tasks_list.controls:
            # Estrutura: Row -> Checkbox
            cb = ctrl.controls[0]
            data.append({"name": cb.label, "completed": cb.value})
        with open(data_file, "w") as f:
            json.dump(data, f)
        page.update()

    def delete_task(row_obj):
        tasks_list.controls.remove(row_obj)
        save_data()

    def add_task_ui(name, completed=False):
        # QA: Usando 'content' em vez de 'text' para garantir compatibilidade
        btn_delete = ft.TextButton(
            content=ft.Text("EXCLUIR", color="#FF5555"),
            on_click=lambda _: delete_task(task_row)
        )

        task_row = ft.Row(
            alignment="center",
            width=550,
            controls=[
                ft.Checkbox(
                    label=name, 
                    value=completed, 
                    on_change=lambda _: save_data(),
                    expand=True,
                    fill_color="#5865F2"
                ),
                btn_delete
            ]
        )
        tasks_list.controls.append(task_row)
        page.update()

    def on_add_click(e):
        if input_field.value:
            add_task_ui(input_field.value)
            input_field.value = ""
            save_data()

    # --- COMPONENTES (UI/UX: Novo Título Personalizado) ---
    title = ft.Text("quadro to do list Darigaz", size=45, weight="bold", color="#5865F2", text_align="center")
    
    subtitle = ft.Text("Seu gerenciador de tarefas personalizado", color="white70")

    input_field = ft.TextField(
        hint_text="Próxima tarefa...",
        width=300,
        bgcolor="#1a1a1a",
        border_color="#5865F2",
        on_submit=on_add_click
    )

    # QA: Botão de adicionar sem o argumento 'text'
    add_btn = ft.ElevatedButton(
        content=ft.Text("ADICIONAR TAREFA", color="white", weight="bold"),
        on_click=on_add_click,
        bgcolor="#5865F2",
        height=50
    )

    tasks_list = ft.Column(width=550, horizontal_alignment="center")

    # --- CARREGAR DADOS ---
    if os.path.exists(data_file):
        try:
            with open(data_file, "r") as f:
                for item in json.load(f):
                    add_task_ui(item["name"], item["completed"])
        except:
            pass

    # --- MONTAGEM ---
    page.add(title)
    page.add(subtitle)
    page.add(ft.Row([input_field, add_btn], alignment="center", spacing=10))
    page.add(ft.Divider(height=20, color="#5865F2"))
    page.add(tasks_list)

if __name__ == "__main__":
    ft.app(target=main, view="web_browser")
