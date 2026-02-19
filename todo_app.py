import flet as ft
import json
import os

def main(page: ft.Page):
    # --- REVISOR: Alinhamento Direto na Página ---
    page.title = "CHECK-IT"
    page.bgcolor = "#000000"
    page.horizontal_alignment = "center" # Alinha tudo ao centro horizontalmente
    page.padding = 50
    page.spacing = 20 # Espaço entre cada item adicionado

    data_file = "todo_data.json"

    # --- LÓGICA DO QA ---
    def save_data():
        data = []
        for ctrl in tasks_list.controls:
            # Estrutura plana: Checkbox + Botão
            cb = ctrl.controls[0]
            data.append({"name": cb.label, "completed": cb.value})
        with open(data_file, "w") as f:
            json.dump(data, f)
        page.update()

    def delete_task(row_obj):
        tasks_list.controls.remove(row_obj)
        save_data()

    def add_task_ui(name, completed=False):
        # QA: Linha de tarefa simplificada
        task_row = ft.Row(
            alignment="center",
            width=500,
            controls=[
                ft.Checkbox(
                    label=name, 
                    value=completed, 
                    on_change=lambda _: save_data(),
                    expand=True
                ),
                ft.TextButton(
                    "EXCLUIR", 
                    on_click=lambda _: delete_task(task_row),
                    font_color="red"
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

    # --- COMPONENTES (Revisor: Sem Containers, apenas componentes puros) ---
    title = ft.Text("CHECK-IT", size=60, weight="bold", color="blue")
    
    input_field = ft.TextField(
        hint_text="O que fazer hoje?",
        width=300,
        bgcolor="#1a1a1a"
    )

    add_btn = ft.ElevatedButton(
        "ADICIONAR TAREFA",
        on_click=on_add_click,
        bgcolor="blue",
        color="white",
        height=50
    )

    tasks_list = ft.Column(width=500, horizontal_alignment="center")

    # --- CARREGAR DADOS ---
    if os.path.exists(data_file):
        try:
            with open(data_file, "r") as f:
                for item in json.load(f):
                    add_task_ui(item["name"], item["completed"])
        except:
            pass

    # --- MONTAGEM (Revisor: Adição Direta na Página) ---
    page.add(title)
    page.add(ft.Text("Sua lista de tarefas profissional", color="white70"))
    page.add(ft.Row([input_field, add_btn], alignment="center"))
    page.add(ft.Divider(height=20, color="blue"))
    page.add(tasks_list)

if __name__ == "__main__":
    ft.app(target=main, view="web_browser")
