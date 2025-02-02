# Генератор PDF не используется, данный файл - наработка на случай необходимости реализовать функционал генерации отчетов PDF

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

pdfmetrics.registerFont(
    TTFont('DejaVuSansCondensed', 'DejaVuSansCondensed.ttf'))
# Создание PDF-документа
doc = SimpleDocTemplate("table_example.pdf", pagesize=A4)

styles = getSampleStyleSheet()
paragraph_style = [styles['Normal']]


# Данные для таблицы
data = [
    ['№', Paragraph('Описание уязвимости', style=paragraph_style), 'Путь до файла',
     'Номер строки', 'Пояснение'],
    [1, 'Алексей', 30],
    [2, '', 22],
    [3, 'Иван', 19],
    [1, 'Алексей', 30],
    [2, '', 22],
    [3, 'Иван', 19],
    [1, 'Алексей', 30],
    [2, '', 22],
    [3, 'Иван', 19],
    [1, 'Алексей', 30],
    [2, '', 22],
    [3, 'Иван', 19],
    [1, 'Алексей', 30],
    [2, '', 22],
    [3, 'Иван', 19],
    [1, 'Алексей', 30],
    [2, '', 22],
    [3, 'Иван', 19],
    [1, 'Алексей', 30],
    [2, '', 22],
    [3, 'Иван', 19],
    [1, 'Алексей', 30],
    [2, '', 22],
    [3, 'Иван', 19],
    [1, 'Алексей', 30],
    [2, '', 22],
    [3, 'Иван', 19],
    [1, 'Алексей', 30],
    [2, '', 22],
    [3, 'Иван', 19],

]

colWidths = [50, 100, 50, 200, 100]  # Ширина столбцов в пунктах
rowHeights = [20, 20, 20, 20]  # Высота строк в пунктах


# Создание объекта таблицы
table = Table(data, colWidths=colWidths)
table2 = Table(data)


# Стилизация таблицы
style = TableStyle([
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, -1), 'DejaVuSansCondensed'),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ('GRID', (0, 0), (-1, -1), 1, "#000000"),

])


table.setStyle(style)
table2.setStyle(style)

# Добавление таблицы в список элементов документа
elements = [table, Spacer(1, 12), table2]
elements.append(Paragraph("Это пример абзаца.", paragraph_style))

# Построение документа
doc.build(elements)
