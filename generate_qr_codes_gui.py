import qrcode
import svgwrite
import math
import tkinter as tk
from tkinter import messagebox, filedialog

def parse_ranges(input_str):
    number = []
    for part in input_str.split(','):
        part = part.strip()
        if '-' in part:
            start,end = map(int, part.split('-'))
            number.extend(range(start,end+1))
        else:
            number.append(int(part))
    return sorted(set(number))

def generate_qr_codes():
    try:
        range_str = entry_first.get().strip()

        if not range_str:
            messagebox.showerror("Ошибка", "Введите диапазон или номера.")
            return

        numbers = parse_ranges(range_str)

        if not numbers:
            messagebox.showerror("Ошибка", "Неверный формат ввода.")
            return
        if min(numbers) <= 0:
            messagebox.showerror("Ошибка", "Номер не может быть меньше 1.")
            return

        num_qr_codes = len(numbers)
        cols = math.ceil(math.sqrt(num_qr_codes))
        rows = math.ceil(num_qr_codes / cols)
        qr_size = 100
        margin = 30
        spacing = 90
        page_width = margin * 2 + cols * qr_size + (cols - 1) * spacing
        page_height = margin * 2 + rows * qr_size + (rows - 1) * spacing
        box_size = qr_size // 25
        border = 4

        dwg = svgwrite.Drawing(filename="temp.svg", size=(f"{page_width}px", f"{page_height}px"),
                               viewBox=f"0 0 {page_width} {page_height}", fill="none")

        for index, i in enumerate(numbers):
            data = f"https://t.me/StartcolorSupport_bot?start=p_{i}"
            qr = qrcode.QRCode(version=5, error_correction=qrcode.constants.ERROR_CORRECT_H,
                              box_size=1, border=border)
            qr.add_data(data)
            qr.make(fit=True)
            matrix = qr.get_matrix()

            col = index % cols
            row = index // cols
            x_offset = margin + col * (qr_size + spacing)
            y_offset = margin + row * (qr_size + spacing)
            g = dwg.g(transform=f"translate({x_offset}, {y_offset})")

            # Рисуем QR-код как прямоугольники
            for r in range(len(matrix)):
                for c in range(len(matrix[r])):
                    if matrix[r][c]:
                        x = c * box_size
                        y = r * box_size
                        g.add(dwg.rect((x, y), (box_size, box_size), fill="#000000", fill_rule="nonzero"))

            # Текст с фоном
            text_size = max(26, qr_size // 4)
            text_width = len(str(i)) * text_size * 0.6
            text_height = text_size * 1.5

            if i < 10:
                g.add(dwg.rect(((2*text_height-7) ,
                                (2*text_height-9)),
                               (text_height, text_height), fill="white", opacity="1", stroke="black", stroke_width="2"))

                g.add(dwg.text(str(i),
                               insert=((qr_size + spacing - 10) / 2, (qr_size + spacing + 5) / 2),
                               font_size=f"{text_size+3}px", text_anchor="middle",
                               dominant_baseline="middle", fill="black", font_weight="bold",
                               font_family="Arial", stroke="black", stroke_width="0"))
                dwg.add(g)
            elif 10 <= i < 100:
                g.add(dwg.rect(((qr_size + spacing - text_width - 3) / 2,
                                (qr_size + spacing - text_height + 5) / 2),
                               (text_height + 1, text_height), fill="white", opacity="1", stroke="black", stroke_width="2"))

                g.add(dwg.text(str(i),
                               insert=((qr_size + spacing + 6) / 2, (qr_size + spacing + 27.5) / 2),
                               font_size=f"{text_size+5}px", text_anchor="middle",
                               dominant_baseline="middle", fill="black", font_weight="bold",
                               font_family="Arial", stroke="black", stroke_width="0"))
                dwg.add(g)
            elif 100 <= i < 1000:
                g.add(dwg.rect(((qr_size + spacing - text_width - 5.5) / 2,
                                (qr_size + spacing - text_height + 5) / 2),
                               (text_height + text_height/2, text_height), fill="white", opacity="1", stroke="black", stroke_width="2"))

                g.add(dwg.text(str(i),
                               insert=((qr_size + spacing + 6) / 2, (qr_size + spacing + 27.5) / 2),
                               font_size=f"{text_size+5}px", text_anchor="middle",
                               dominant_baseline="middle", fill="black", font_weight="bold",
                               font_family="Arial", stroke="black", stroke_width="0"))
                dwg.add(g)
            else:
                g.add(dwg.rect(((qr_size + spacing - text_width) / 2 - 4 ,
                                (qr_size + spacing - text_height + 5) / 2),
                               (text_height + text_height, text_height), fill="white", opacity="1", stroke="black", stroke_width="2"))

                g.add(dwg.text(str(i),
                               insert=((qr_size + spacing + 8) / 2, (qr_size + spacing + 27.5) / 2),
                               font_size=f"{text_size+5}px", text_anchor="middle",
                               dominant_baseline="middle", fill="black", font_weight="bold",
                               font_family="Arial", stroke="black", stroke_width="0"))
                dwg.add(g)


        save_path = filedialog.asksaveasfilename(defaultextension=".svg",
                                                filetypes=[("SVG files", "*.svg")])
        if save_path:
            xml_declaration = '<?xml version="1.0" encoding="utf-8"?>\n' \
                             '<!-- Uploaded to: SVG Repo, www.svgrepo.com, Generator: SVG Repo Mixer Tools -->\n'
            dwg.saveas(save_path)
            with open(save_path, "r", encoding="utf-8") as f:
                svg_content = f.read()
            with open(save_path, "w", encoding="utf-8") as f:
                f.write(xml_declaration + svg_content)
            messagebox.showinfo("Успех", f"QR-коды сохранены в {save_path}")
    except ValueError:
        messagebox.showerror("Ошибка", "Введите корректные числовые значения.")

root = tk.Tk()
root.title("Генератор QR-кодов")
root.geometry("300x150")
tk.Label(root, text="Диапазон или номера клиентов:").pack(pady=5)
entry_first = tk.Entry(root)
entry_first.pack()
tk.Button(root, text="Сгенерировать QR-коды", command=generate_qr_codes).pack(pady=10)
root.mainloop()