import flet as ft
import json
import os

def main(page: ft.Page):
    # --- REVISOR: Configuração de Blindagem de Layout ---
    page.title = "Quadro Kanban Darigaz"
    page.bgcolor = "#000000"
    page.theme_mode = "dark"
    page.padding = 40
    page.window_width = 1100
    page.window_height = 850
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

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

    # --- SISTEMA DE NOTIFICAÇÕES ---
    def show_notification(message, color="white"):
        page.snack_bar = ft.SnackBar(
            content=ft.Text(message, color="black", weight="bold"),
            bgcolor=color,
            duration=2000
        )
        page.snack_bar.open = True
        page.update()

    # --- LÓGICA DE ARRASTE (Drag & Drop Estabilizada) ---
    def drag_accept(e):
        # Tenta obter o índice do dado do evento ou do controle de origem
        src_idx_str = e.data if e.data else page.get_control(e.src_id).data
        
        if src_idx_str is not None:
            src_idx = int(src_idx_str)
            dest_status = e.control.data
            
            # Sincronização de Dados antes da Renderização
            tasks_data[src_idx]["status"] = dest_status
            save_db()
            render_board()
            show_notification(f"Tarefa movida para {dest_status.upper()}", "#3498db")

    def render_board():
        # Limpeza total das listas
        todo_list.controls.clear()
        doing_list.controls.clear()
        done_list.controls.clear()

        for index, task in enumerate(tasks_data):
            cat_color = task.get("color", "#95a5a6")
            priority = task.get("priority", "Média")
            
            # Ícone de Prioridade
            prio_icon = "⭐" if priority == "Alta" else ("⚪" if priority == "Média" else "🔽")
            prio_color = "#e74c3c" if priority == "Alta" else ("#f1c40f" if priority == "Média" else "#2ecc71")

            task_card = ft.Draggable(
                group="kanban",
                data=str(index),
                content=ft.Container(
                    content=ft.Stack([
                        # Indicador de Categoria (Topo)
                        ft.Container(
                            height=6, 
                            bgcolor=cat_color, 
                            border_radius=3, 
                            width=30,
                            top=8,
                            left=5
                        ),
                        # Prioridade (Topo Direita)
                        ft.Container(
                            content=ft.Text(prio_icon, size=9, color=prio_color),
                            top=5,
                            right=25
                        ),
                        # Texto da Tarefa (Centro)
                        ft.Container(
                            content=ft.Text(
                                value=task["name"],
                                size=11,
                                weight="bold",
                                color="white",
                                text_align=ft.TextAlign.CENTER,
                            ),
                            alignment=ft.Alignment(0, 0),
                            expand=True,
                            padding=ft.padding.only(top=10, left=5, right=5, bottom=15)
                        ),
                        # Tags e Deadline (Rodapé)
                        ft.Row([
                            ft.Text(task.get("deadline", ""), size=8, color="#AAAAAA", italic=True),
                            ft.Text(task.get("tags", ""), size=8, color="#3498db", weight="bold"),
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, bottom=2, left=5, right=5),
                        
                        # Botão Excluir (Canto Superior Direito) - Estilo Container para evitar erros de Ícone
                        ft.Container(
                            content=ft.Text("X", color="#FF5555", weight="bold", size=10),
                            on_click=lambda e, idx=index: delete_task(idx),
                            width=20,
                            height=20,
                            top=2,
                            right=2,
                            alignment=ft.Alignment(0, 0),
                            border_radius=10,
                        ),
                    ]),
                    bgcolor="#1A1A1A",
                    border_radius=8,
                    border=ft.border.all(1, "#333333"),
                    width=115,  # ~3cm
                    height=75,  # ~2cm
                    shadow=ft.BoxShadow(blur_radius=5, color="black")
                )
            )

            if task["status"] == "todo": todo_list.controls.append(task_card)
            elif task["status"] == "doing": doing_list.controls.append(task_card)
            elif task["status"] == "done": done_list.controls.append(task_card)
        
        page.update()

    def add_task(e):
        if input_field.value:
            cat_name = selected_category.value
            cat_color = categories.get(cat_name, "#95a5a6")
            
            tasks_data.append({
                "name": input_field.value, 
                "status": "todo",
                "category": cat_name,
                "color": cat_color,
                "deadline": deadline_field.value if deadline_field.value else "",
                "priority": priority_dropdown.value,
                "tags": tags_field.value if tags_field.value else ""
            })
            input_field.value = ""
            deadline_field.value = ""
            tags_field.value = ""
            save_db()
            render_board()
            
            notif_color = "#e74c3c" if cat_name == "Urgente" or priority_dropdown.value == "Alta" else "#2ecc71"
            show_notification(f"Tarefa '{cat_name}' adicionada!", notif_color)

    def delete_task(idx):
        tasks_data.pop(idx)
        save_db()
        render_board()
        show_notification("Tarefa excluída!", "#e74c3c")

    # --- COMPONENTES DA UI ---
    title = ft.Text("Quadro Kanban Darigaz", size=40, weight="bold", color="#5865F2")

    categories = {
        "Trabalho": "#3498db",  # Azul
        "Pessoal": "#e67e22",   # Laranja
        "Urgente": "#e74c3c",   # Vermelho
        "Outros": "#95a5a6"     # Cinza
    }

    selected_category = ft.Dropdown(
        options=[ft.dropdown.Option(k) for k in categories.keys()],
        width=120,
        value="Outros",
        text_size=12,
        bgcolor="#111111",
        border_color="#333333",
        color="white",
        content_padding=10
    )
    
    input_field = ft.TextField(
        hint_text="Tarefa...", 
        width=200,
        bgcolor="#111111",
        on_submit=add_task,
        text_size=14
    )

    deadline_field = ft.TextField(
        hint_text="Data (ex: 25/12)", 
        width=100,
        bgcolor="#111111",
        on_submit=add_task,
        text_size=12
    )

    priority_dropdown = ft.Dropdown(
        options=[
            ft.dropdown.Option("Alta"),
            ft.dropdown.Option("Média"),
            ft.dropdown.Option("Baixa")
        ],
        width=100,
        value="Média",
        text_size=12,
        bgcolor="#111111",
        border_color="#333333",
        color="white",
        content_padding=10
    )

    tags_field = ft.TextField(
        hint_text="Tags...", 
        width=100,
        bgcolor="#111111",
        on_submit=add_task,
        text_size=12
    )

    todo_list = ft.Row(wrap=True, spacing=10, width=240, alignment=ft.MainAxisAlignment.CENTER)
    doing_list = ft.Row(wrap=True, spacing=10, width=240, alignment=ft.MainAxisAlignment.CENTER)
    done_list = ft.Row(wrap=True, spacing=10, width=240, alignment=ft.MainAxisAlignment.CENTER)

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
                    ft.Column([target_list], scroll="auto", height=480)
                ], spacing=15, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                width=260,
                height=550, # Altura fixa para estabilidade visual
                padding=12,
                bgcolor="#0D1117",
                border_radius=15,
                border=ft.border.all(1, "#1E1E1E")
            )
        )

    # Montagem da Página
    page.add(
        title,
        ft.Row([
            selected_category,
            input_field, 
            deadline_field,
            priority_dropdown,
            tags_field,
            ft.ElevatedButton(
                content=ft.Text("ADICIONAR", color="white", weight="bold"),
                on_click=add_task, 
                bgcolor="#5865F2",
                height=45
            )
        ], alignment=ft.MainAxisAlignment.CENTER),
        ft.Divider(height=20, color="transparent"),
        ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.START,
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
    ft.app(target=main, view="web_browser", port=8550)
