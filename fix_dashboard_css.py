import re

file_path = r'c:\Users\sangi\Desktop\budhanilkantha_school\core\templates\core\dashboard_settings.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

missing_css = """
    /* Form Styles */
    .form-field {
        margin-bottom: 20px;
    }
    .form-field label {
        display: block;
        font-weight: 600;
        margin-bottom: 8px;
        color: var(--text-dark);
        font-size: 0.95rem;
    }
    .form-field input[type="text"],
    .form-field input[type="url"],
    .form-field input[type="email"],
    .form-field input[type="number"],
    .form-field input[type="date"],
    .form-field input[type="file"],
    .form-field textarea {
        width: 100%;
        padding: 12px 16px;
        border: 1px solid var(--gray-light);
        border-radius: var(--radius-sm);
        font-family: inherit;
        font-size: 1rem;
        transition: all 0.2s;
        background-color: #f9fbfc;
    }
    .form-field input:focus,
    .form-field textarea:focus {
        outline: none;
        border-color: var(--primary);
        background-color: white;
        box-shadow: 0 0 0 3px rgba(30,58,138,0.1);
    }
    .settings-section {
        background: #f9fbfc;
        padding: 24px;
        border-radius: var(--radius-md);
        border: 1px solid var(--gray-light);
        margin-bottom: 24px;
    }
    .settings-card {
        background: white;
        padding: 20px;
        border-radius: var(--radius-md);
        border: 1px solid var(--gray-light);
        margin-bottom: 16px;
        position: relative;
    }
"""

if ".form-field {" not in content:
    content = content.replace("<style>", "<style>\n" + missing_css)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("CSS for forms added.")
else:
    print("CSS already present.")
