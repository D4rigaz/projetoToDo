import flet as ft
import json
import os

def main(page: ft.Page):
    # --- REVISOR: Configurações de Layout Kanban ---
    page.title = "quadro to do list Darigaz - KANBAN"
    page.bgcolor = "#0D1117"
    page.horizontal_alignment = "center"
    page.scroll = "adaptive"
    page.padding = 30
    page.theme_mode = "dark"

    data_file = "kanban_data.json"

    # --- LÓGICA DO QA (CRUD KANBAN) ---
    def save_data():
        data = []
        # Coleta tarefas de todas as colunas
        for col_name, col_view in zip(["todo", "doing", "done"], [todo_col, doing_col, done_col]):
            for task_card in col_view.controls:
                # O nome da tarefa está no primeiro controle (Text) do card
                task_name = task_card.controls[0].value
                data.append({"name": task_name, "status": col_name})
        
        with open(data_file, "w") as f:
            json.dump(data, f)
        page.update()

    def move_task(task_obj, current_status, direction):
        # Remove da coluna atual
        if current_status == "todo":
            todo_col.controls.remove(task_obj)
            new_status = "doing"
        elif current_status == "doing":
            doing_col.controls.remove(task_obj)
            new_status = "done" if direction == "forward" else "todo"
        elif current_status == "done":
            done_col.controls.remove(task_obj)
            new_status = "doing"

        # Adiciona na nova coluna
        create_task_ui(task_obj.controls[0].value, new_status)
        save_data()

    def delete_task(task_obj, status):
        if status == "todo": todo_col.controls.remove(task_obj)
        elif status == "doing": doing_col.controls.remove(task_obj)
        elif status == "done": done_col.controls.remove(task_obj)
        save_data()

    def create_task_ui(name, status="todo"):
        # QA: Criando o Card de Tarefa (Agnóstico e Sem Containers complexos)
        task_card = ft.Column(spacing=5, width=250)
        
        # Botões de ação baseados no status
        actions = ft.Row(alignment="spaceBetween")
        
        btn_delete = ft.IconButton(icon="delete", icon_color="#F85149", icon_size=18, on_click=lambda _: delete_task(task_card, status))
        
        move_buttons = []
        if status != "todo":
            move_buttons.append(ft.IconButton(icon="arrow_back", icon_color="white70", on_click=lambda _: move_task(task_card, status, "back")))
        if status != "done":
            move_buttons.append(ft.IconButton(icon="arrow_forward", icon_color="indigoaccent", on_click=lambda _: move_task(task_card, status, "forward")))

        actions.controls = [btn_delete, ft.Row(move_buttons)]

        task_card.controls = [
            ft.Text(name, weight="bold", size=16, color="white"),
            actions,
            ft.Divider(height=1, color="white10")
        ]

        if status == "todo": todo_col.controls.append(task_card)
        elif status == "doing": doing_col.controls.append(task_card)
        elif status == "done": done_col.controls.append(task_card)
        
        page.update()

    def on_add_click(e):
        if input_field.value:
            create_task_ui(input_field.value, "todo")
            input_field.value = ""
            save_data()

    # --- COMPONENTES DO QUADRO (Revisor: Estrutura Plana) ---
    title = ft.Text("quadro to do list Darigaz", size=40, weight="bold", color="indigoaccent")
    
    input_field = ft.TextField(hint_text="Nova tarefa para o quadro...", width=300, bgcolor="#161B22")
    add_btn = ft.ElevatedButton(content=ft.Text("ADICIONAR", weight="bold"), on_click=on_add_click, bgcolor="indigoaccent", color="white", height=45)

    # Colunas do Kanban
    todo_col = ft.Column(spacing=20, width=250)
    doing_col = ft.Column(spacing=20, width=250)
    done_col = ft.Column(spacing=20, width=250)

    # --- CARREGAR DADOS ---
    if os.path.exists(data_file):
        try:
            with open(data_file, "r") as f:
                for item in json.load(f):
                    create_task_ui(item["name"], item.get("status", "todo"))
        except: pass

    # --- MONTAGEM DA PÁGINA (Revisor: Sem containers aninhados) ---
    page.add(
        title,
        ft.Row([input_field, add_btn], alignment="center"),
        ft.Divider(height=30, color="indigoaccent"),
        ft.Row(
            alignment="start",
            vertical_alignment="start",
            spacing=30,
            controls=[
                ft.Column([ft.Text("PARA FAZER", size=18, weight="bold", color="white70"), ft.Divider(color="white10"), todo_col], width=250),
                ft.Column([ft.Text("FAZENDO", size=18, weight="bold", color="amber"), ft.Divider(color="amber"), doing_col], width=250),
                ft.Column([ft.Text("CONCLUÍDO", size=18, weight="bold", color="green"), ft.Divider(color="green"), done_col], width=250),
            ]
        )
    )

if __name__ == "__main__":
    ft.app(target=main, view="web_browser")
