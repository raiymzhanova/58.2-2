import flet as ft 
from db import main_db
import datetime


def main(page: ft.Page):
    page.title = 'ToDo list'
    page.theme_mode = ft.ThemeMode.LIGHT

    task_list = ft.Column(spacing=10)
    
    filter_type = 'all'

    def load_task(filter_type=None):
        task_list.controls.clear()
        for task_id, task_text, completed in main_db.get_tasks(filter_type):
            task_list.controls.append(create_task_row(task_id, task_text, completed))
        page.update()

    def create_task_row(task_id, task_text, completed = None):
        task_field = ft.TextField(value=task_text, read_only=True, expand=True)
        now = datetime.datetime.now()
        time = now.strftime("%Y-%m-%d %H:%M:%S")
        task_time = ft.Text(value=time)

        checkbox = ft.Checkbox(value=bool(completed), on_change=lambda e: toggle_task(task_id, e.control.value))

        def enable_edit(_):
            task_field.read_only = False
            task_field.update()

        edit_button = ft.IconButton(icon=ft.Icons.EDIT, tooltip="Редактировать", on_click=enable_edit, icon_color=ft.Colors.ORANGE_700)

        def save_task(_):
            main_db.update_task(task_id=task_id, new_task=task_field.value)
            task_field.read_only = True
            task_field.update()
            page.update()

        save_button = ft.IconButton(icon=ft.Icons.SAVE_ALT_ROUNDED, on_click=save_task)

        def delete_task(_):
            main_db.delete_task(task_id=task_id)
            load_task()
            
        delete_button = ft.IconButton(icon=ft.Icons.DELETE, tooltip="Удалить", on_click=delete_task, icon_color=ft.Colors.RED_700)

        return ft.Row([task_time, task_field, edit_button, save_button, delete_button, checkbox ])

    def add_task(_):
        if task_input.value:
            task = task_input.value
            task_id = main_db.add_task(task)
            task_list.controls.append(create_task_row(task_id=task_id, task_text=task))
            task_input.value = ''
            page.update()

    def delete_all_tasks(_):
        main_db.delete_all_tasks()
        load_task()

   
    def clear_completed(_):
        main_db.delete_completed_tasks() 
        load_task()
    
    def toggle_task(task_id, is_completed):
        main_db.update_task(task_id, completed=int(is_completed))
        load_task()

    warning_text = ft.Text(
        value="Длина задачи не должна превышать 100 символов!", 
        color=ft.Colors.RED, 
        visible=False,
        size=12
    )
    
    def check_length(e):
        if len(e.control.value) >= 100:
           warning_text.visible = True
        else:
           warning_text.visible = False
        page.update()

    task_input = ft.TextField(label='Введите новую задачу', expand=True,max_length=100, on_change=check_length) 
    add_button = ft.IconButton(icon=ft.Icons.ADD, tooltip='Добавить задачу', on_click=add_task)
    clear_completed_button = ft.ElevatedButton("Очистить выполненные", icon=ft.Icons.DELETE_SWEEP_OUTLINED, on_click=clear_completed,icon_color=ft.Colors.RED_400)
    delete_all_button = ft.ElevatedButton("Удалить все задачи", on_click=delete_all_tasks)
    
    filter_buttons = ft.Row([
        ft.ElevatedButton('Все задачи', on_click=lambda e: load_task()),
        ft.ElevatedButton('К выполнению', on_click=lambda e: load_task("uncompleted")),
        ft.ElevatedButton('Выполнено ✅', on_click=lambda e: load_task("completed"))
    ], alignment=ft.MainAxisAlignment.SPACE_EVENLY)

    page.add(ft.Row([task_input,add_button,delete_all_button,clear_completed_button]),warning_text,filter_buttons,task_list)
    
    load_task()


if __name__ == '__main__':
    main_db.init_db()
    ft.app(target=main)