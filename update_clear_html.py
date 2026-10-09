with open('templates/includes/image_field.html', 'r', encoding='utf-8') as f:
    text = f.read()

old_label = '''<label class="st-img-clear">
        <input type="checkbox" name="{{ field.name }}-clear" id="{{ field.name }}-clear_id" class="st-clear-checkbox">
        Remove current image
      </label>'''

new_label = '''<label class="st-clear-row">
        <input type="checkbox" name="{{ field.name }}-clear" id="{{ field.name }}-clear_id">
        <span>Remove current image</span>
      </label>'''

text = text.replace(old_label, new_label)

with open('templates/includes/image_field.html', 'w', encoding='utf-8') as f:
    f.write(text)

print('Updated HTML')
