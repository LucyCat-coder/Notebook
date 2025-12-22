import os
from datetime import datetime
import json
from tkinter import *
from tkinter import Button, Label, Text, Scrollbar
from tkinter import messagebox
from tkinter import simpledialog


def new_note():
    text_fild.delete("1.0", END)


def save_note():
    content = text_fild.get("1.0", END).strip()

    if not content:
        messagebox.showwarning("Внимание", "Заметка не должна быть пустой!")
        return

    # Подготовка данных
    date_str = datetime.now().strftime("%d.%m.%Y %H:%M")
    note_data = {
        "date": date_str,
        "text": content
    }

    try:
        # Получаем абсолютный путь к файлу notes.json
        script_dir = os.path.dirname(os.path.abspath(__file__))
        notes_file = os.path.join(script_dir, "notes.json")

        # Читаем существующие данные
        notes_list = []
        if os.path.exists(notes_file):
            with open(notes_file, "r", encoding="utf-8") as f:
                notes_list = json.load(f)

        # Добавляем новую заметку
        notes_list.append(note_data)

        # Сохраняем обратно
        with open(notes_file, "w", encoding="utf-8") as f:
            json.dump(notes_list, f, ensure_ascii=False, indent=4)

        messagebox.showinfo("Готово", "Заметка сохранена!")

    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибка при сохранении: {e}")

def show_note():
    try:
        # Получаем абсолютный путь к файлу notes.json
        script_dir = os.path.dirname(os.path.abspath(__file__))
        notes_file = os.path.join(script_dir, "notes.json")

        if not os.path.exists(notes_file):
            messagebox.showinfo("Информация", "Нет сохранённых заметок")
            return

        with open(notes_file, "r", encoding="utf-8") as f:
            notes_list = json.load(f)

            if not notes_list:
                messagebox.showinfo("Информация", "Нет сохранённых заметок")
                return


        for i, note in enumerate(notes_list, 1):
            text_fild.insert(END, f"{i}. {note['date']}\n")
            text_fild.insert(END, f"{note['text']}\n")
            text_fild.insert(END, "-" * 20 + "\n")



    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибка при чтении заметок: {e}")


def delete_note():
    try:
        # Получаем абсолютный путь к файлу notes.json
        script_dir = os.path.dirname(os.path.abspath(__file__))
        notes_file = os.path.join(script_dir, "notes.json")

        if not os.path.exists(notes_file):
            messagebox.showinfo("Информация", "Нет сохранённых заметок")
            return

        with open(notes_file, "r", encoding="utf-8") as f:
            notes_list = json.load(f)

        if not notes_list:
            messagebox.showinfo("Информация", "Нет сохранённых заметок")
            return

        # Очищаем текстовое поле
        text_fild.delete("1.0", END)

        # Выводим все заметки с нумерацией
        text_fild.insert(END, "=== ВЫБЕРИТЕ НОМЕР ЗАМЕТКИ ДЛЯ УДАЛЕНИЯ ===\n\n")
        for i, note in enumerate(notes_list, 1):
            text_fild.insert(END, f"{i}. {note['date']}\n")
            text_fild.insert(END, f"{note['text'][:100]}{'...' if len(note['text']) > 100 else ''}\n")
            text_fild.insert(END, "-" * 40 + "\n\n")

        # Запрашиваем номер заметки для удаления
        note_number = simpledialog.askinteger(
            "Удаление заметки",
            f"Введите номер заметки для удаления (1-{len(notes_list)}):",
            minvalue=1,
            maxvalue=len(notes_list)
        )

        if note_number is None:  # Пользователь нажал "Отмена"
            return

        # Подтверждение удаления
        note_to_delete = notes_list[note_number - 1]
        confirm = messagebox.askyesno(
            "Подтверждение",
            f"Вы уверены, что хотите удалить заметку №{note_number}?\n"
            f"Дата: {note_to_delete['date']}\n"
            f"Текст: {note_to_delete['text'][:50]}..."
        )

        if not confirm:
            return

        # Удаляем заметку из списка
        notes_list.pop(note_number - 1)

        # Сохраняем обновленный список
        with open(notes_file, "w", encoding="utf-8") as f:
            json.dump(notes_list, f, ensure_ascii=False, indent=4)

        # Очищаем текстовое поле и выводим результат
        text_fild.delete("1.0", END)
        text_fild.insert(END, f"Заметка №{note_number} успешно удалена!\n")
        text_fild.insert(END, f"Осталось заметок: {len(notes_list)}\n\n")

        if notes_list:
            text_fild.insert(END, "Оставшиеся заметки:\n")
            for i, note in enumerate(notes_list, 1):
                text_fild.insert(END, f"{i}. {note['date']}\n")
                text_fild.insert(END, f"{note['text'][:50]}...\n")
                text_fild.insert(END, "-" * 30 + "\n")
        else:
            text_fild.insert(END, "Больше нет сохранённых заметок.\n")

        messagebox.showinfo("Успех", f"Заметка №{note_number} удалена!")

    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибка при удалении заметки: {e}")

root = Tk()
root.title('Мои заметки')
root.geometry('300x500')
root.iconbitmap('icon/-romb.ico')


# Верхний фрейм с кнопками
frame_top = Frame(root)
frame_top.pack(pady=10, padx=10)

'''image = None - это защита от ошибок и четкое указание
начального состояния переменной
перед попыткой загрузки изображения.'''
# Первая кнопка - Новая заметка
image = None

try:
    image = PhotoImage(file="./icon/page.png")
except Exception as e:
    print(f"Ошибка загрузки изображения: {e}")
    image = None

if image is not None:
    button = Button(
        frame_top,
        image=image,
        padx=20,
        pady=10,
        command=new_note
    )
else:
    button = Button(
        frame_top,
        text="📝",
        font=("Arial", 24),
        padx=20,
        pady=10,
        command=new_note
    )
button.pack(side=LEFT, padx=5)

# Вторая кнопка - Сохранить
image2 = None

try:
    image2 = PhotoImage(file="./icon/cabinet.png")
except Exception as e:
    print(f"Ошибка загрузки изображения: {e}")
    image2 = None

if image2 is not None:
    button2 = Button(
        frame_top,
        image=image2,
        font=("Arial", 12),
        padx=20,
        pady=10,
        command=save_note
    )
else:
    button2 = Button(
        frame_top,
        text="💾",
        font=("Arial", 24),
        padx=20,
        pady=10,
        command=save_note
    )
button2.pack(side=LEFT, padx=5)

# Третья кнопка - Показать все заметки (вместо удаления)
image4 = None

try:
    image4 = PhotoImage(file="./icon/openbook.png")
except Exception as e:
    print(f"Ошибка загрузки изображения: {e}")
    image4 = None

if image4 is not None:
    button4 = Button(
        frame_top,
        image=image4,
        font=("Arial", 12),
        padx=20,
        pady=10,
        command=show_note
    )
else:
    button4 = Button(
        frame_top,
        text="📋",
        font=("Arial", 24),
        padx=20,
        pady=10,
        command=show_note
    )
button4.pack(side=LEFT, padx=5)

# Четвёртая кнопка - Удалить
image3 = None

try:
    image3 = PhotoImage(file="./icon/delete.png")
except Exception as e:
    print(f"Ошибка загрузки изображения: {e}")
    image3 = None

if image3 is not None:
    button3 = Button(
        frame_top,
        image=image3,
        font=("Arial", 12),
        padx=20,
        pady=10,
        command=delete_note
    )
else:
    button3 = Button(
        frame_top,
        text="🗑️",
        font=("Arial", 24),
        padx=20,
        pady=10,
        command=delete_note
    )
button3.pack(side=LEFT, padx=5)

frame_bottom = Frame(root)
frame_bottom.pack(pady=10)

try:
    image5 = PhotoImage(file="./icon/razdelitel.png")
    separator = Label(frame_bottom, image=image5)
    separator.pack()
    separator.image = image5
except:
    # Разделитель из Label
    separator = Label(frame_bottom, text="────────────",
                      font=("Arial", 14), fg="gray")
    separator.pack()

f_text = Frame(root)
f_text.pack(fill="both", expand=1)

text_fild = Text(f_text, bg='Lavender',
                 fg='black',
                 font=('Times New Roman', 12),
                 padx=10,
                 pady=10,
                 wrap=WORD,
                 insertbackground='DarkSlateGrey',
                 selectbackground='DarkSlateGrey',
                 spacing3=10,
                 width=30,
                 )
text_fild.pack(expand=1, fill="both", side=LEFT)

scroll = Scrollbar(f_text, command=text_fild.yview)
scroll.pack(side="right", fill="y")
text_fild.config(yscrollcommand=scroll.set)


root.mainloop()
