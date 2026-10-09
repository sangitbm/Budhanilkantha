with open('templates/includes/image_field.html', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('id="{{ field.name }}-clear_id"', 'id="id_{{ field.name }}-clear"')

with open('templates/includes/image_field.html', 'w', encoding='utf-8') as f:
    f.write(text)
print('Updated HTML')
