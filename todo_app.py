import flet as ft
import json
import os

def main(page: ft.Page):
    # --- REVISOR: Configurações de Segurança de Layout ---
    page.title = "CHECK-IT: Modern Flat"
    page.bgcolor = "#0D1117" # Fundo escuro premium
    page.horizontal_alignment = "center"
    page.padding = 40
    page.spacing = 15
    page.theme_mode = "dark"

    data_file = "todo_data.json"

    # --- LÓGICA DO QA ---
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
        # QA: Row simples, sem containers para evitar erro de renderização
        task_row = ft.Row(
            alignment="center",
            width=500,
            controls=[
                ft.Checkbox(
                    label=name, 
                    value=completed, 
                    on_change=lambda _: save_data(),
                    expand=True,
                    fill_color="#5865F2" # Cor Indigo/Blurple
                ),
                ft.TextButton(
                    "EXCLUIR", 
                    on_click=lambda _: delete_task(task_row),
                    font_color="#F85149"
                )
            ]
        )
        tasks_list.controls.append(task_row)
        page.update()

    def on_add_click(e):
        if input_field.value:
            add_task_ui(input_field.value)
            input_field.value = ""
            save_data()

    # --- COMPONENTES (Design Moderno com Estrutura Plana) ---
    title = ft.Text("CHECK-IT", size=60, weight="bold", color="#5865F2")
    
    subtitle = ft.Text("Organize sua rotina com estilo", color="#8B949E", size=16)

    input_field = ft.TextField(
        hint_text="Próxima tarefa...",
        width=300,
        bgcolor="#161B22",
        border_color="#30363D",
        focused_border_color="#5865F2",
        border_radius=10
    )

    # Botão Moderno (Usando ElevatedButton para estabilidade total)
    add_btn = ft.ElevatedButton(
        "ADICIONAR",
        on_click=on_add_click,
        bgcolor="#5865F2",
        color="white",
        height=50,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))
    )

    tasks_list = ft.Column(width=500, spacing=5, horizontal_alignment="center")

    # --- CARREGAR DADOS ---
    if os.path.exists(data_file):
        try:
            with open(data_file, "r") as f:
                for item in json.load(f):
                    add_task_ui(item["name"], item["completed"])
        except:
            pass

    # --- MONTAGEM (Revisor: Adição Direta e Sequencial) ---
    page.add(title)
    page.add(subtitle)
    page.add(ft.Divider(height=10, color="transparent"))
    page.add(ft.Row([input_field, add_btn], alignment="center", spacing=10))
    page.add(ft.Divider(height=20, color="#30363D"))
    page.add(tasks_list)

if __name__ == "__main__":
    ft.app(target=main, view="web_browser")
