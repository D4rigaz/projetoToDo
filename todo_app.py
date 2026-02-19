import flet as ft
import json
import os

def main(page: ft.Page):
    # --- REVISOR (DevOps): Configuração de Blindagem Total ---
    page.title = "Quadro Kanban Darigaz"
    page.bgcolor = "#000000"
    page.theme_mode = "dark"
    page.padding = 30
    page.window_width = 1100
    page.window_height = 800
    page.horizontal_alignment = "center"

    data_file = "kanban_data.json"
    tasks_data = []

    def load_db():
        nonlocal tasks_data
        if os.path.exists(data_file):
            try:
                with open(data_file, "r") as f:
                    tasks_data = json.load(f)
            except: tasks_data = []
        else: tasks_data = []

    def save_db():
        with open(data_file, "w") as f:
            json.dump(tasks_data, f)

    # --- LÓGICA DE ARRASTE (Drag & Drop) ---
    def drag_accept(e):
        src_idx = int(e.src_data)
        dest_status = e.control.data
        tasks_data[src_idx]["status"] = dest_status
        save_db()
        render_board()

    def render_board():
        # Limpando as listas de controles
        todo_list.controls.clear()
        doing_list.controls.clear()
        done_list.controls.clear()

        for index, task in enumerate(tasks_data):
            # QA: Usando TextButton com Content para evitar erros de IconButton
            btn_delete = ft.TextButton(
                content=ft.Icon("delete", color="#FF5555", size=18),
                on_click=lambda e, idx=index: delete_task(idx)
            )

            # Card Arrastável (Draggable)
            task_card = ft.Draggable(
                group="kanban",
                data=str(index),
                content=ft.Container(
                    content=ft.Column([
                        ft.Text(task["name"], weight="bold", size=14, color="white"),
                        ft.Row([
                            ft.Text("ARRASTE", size=10, color="white30"),
                            btn_delete
                        ], alignment="spaceBetween")
                    ], spacing=5),
                    bgcolor="#1A1A1A",
                    padding=10,
                    border_radius=10,
                    border=ft.border.all(1, "#333333"),
                    width=230,
                )
            )

            if task["status"] == "todo": todo_list.controls.append(task_card)
            elif task["status"] == "doing": doing_list.controls.append(task_card)
            elif task["status"] == "done": done_list.controls.append(task_card)
        
        page.update()

    def add_task(e):
        if input_field.value:
            tasks_data.append({"name": input_field.value, "status": "todo"})
            input_field.value = ""
            save_db()
            render_board()

    def delete_task(idx):
        tasks_data.pop(idx)
        save_db()
        render_board()

    # --- COMPONENTES DA UI ---
    title = ft.Text("Quadro Kanban Darigaz", size=40, weight="bold", color="#5865F2")
    
    # QA: TextField simplificado para garantir digitação limpa
    input_field = ft.TextField(
        hint_text="Próxima tarefa...", 
        width=300,
        bgcolor="#111111",
        on_submit=add_task
    )

    todo_list = ft.Column(spacing=10)
    doing_list = ft.Column(spacing=10)
    done_list = ft.Column(spacing=10)

    # Função para criar colunas alvo (DragTarget) - REVISOR: Altura Fixa
    def create_kanban_column(name, status_key, color):
        target_list = todo_list if status_key == "todo" else (doing_list if status_key == "doing" else done_list)
        
        return ft.DragTarget(
            group="kanban",
            data=status_key,
            on_accept=drag_accept,
            content=ft.Container(
                content=ft.Column([
                    ft.Text(name, weight="bold", size=16, color=color),
                    ft.Divider(color=color, height=2),
                    target_list
                ], spacing=15),
                width=280,
                height=550, # Altura fixa para evitar colapso (quadrado cinza)
                padding=15,
                bgcolor="#0D1117",
                border_radius=15,
                border=ft.border.all(1, "#1E1E1E")
            )
        )

    # Montagem Final da Página
    page.add(
        title,
        ft.Row([
            input_field, 
            ft.ElevatedButton(
                content=ft.Text("ADICIONAR", color="white", weight="bold"),
                on_click=add_task, 
                bgcolor="#5865F2"
            )
        ], alignment="center"),
        ft.Divider(height=20, color="transparent"),
        ft.Row(
            alignment="center",
            vertical_alignment="start",
            spacing=20,
            controls=[
                create_kanban_column("PARA FAZER", "todo", "white"),
                create_kanban_column("FAZENDO", "doing", "amber"),
                create_kanban_column("CONCLUÍDO", "done", "green"),
            ]
        )
    )

    load_db()
    render_board()

if __name__ == "__main__":
    ft.app(target=main, view="web_browser")
