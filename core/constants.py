ALLOWED_TABS = ['school', 'about', 'programs', 'contact', 'social', 'admissions', 'advanced']
ALL_GRADES = [
    'ECD', 'Nursery', 'LKG', 'UKG', 'Grade 1', 'Grade 2', 'Grade 3', 'Grade 4', 
    'Grade 5', 'Grade 6', 'Grade 7', 'Grade 8', 'Grade 9', 'Grade 10', 'Grade 11', 'Grade 12'
]
FIELD_TO_TAB = {
    'school_name': 'school', 'school_short_name': 'school', 'marquee_text': 'school', 'ticker_enabled': 'school', 'tagline': 'school',
    'established_year': 'school', 'principal_name': 'school', 'principal_photo': 'school', 'principal_message': 'school',
    'about_short': 'school', 'logo': 'school', 'favicon': 'school',
    'about_image': 'about', 'about_text': 'about', 'curriculum_text': 'about',
    'value_1': 'about', 'value_2': 'about', 'value_3': 'about',
    'stat_students': 'about', 'stat_faculty': 'about', 'stat_support': 'about',
    'phone_primary': 'contact', 'phone_secondary': 'contact', 'email_general': 'contact', 'email_admissions': 'contact',
    'address': 'contact', 'google_maps_url': 'contact', 'office_hours': 'contact',
    'facebook_url': 'social', 'youtube_url': 'social', 'twitter_url': 'social', 'instagram_url': 'social', 'whatsapp_url': 'social',
    'admissions_open': 'admissions', 'admissions_btn_label': 'admissions', 'admissions_btn_link': 'admissions',
    'admissions_badge': 'admissions', 'admissions_start': 'admissions', 'admissions_end': 'admissions', 'admissions_message': 'admissions',
    'meta_description': 'advanced', 'og_title': 'advanced', 'og_image': 'advanced', 'maintenance_mode': 'advanced',
    'hero_images': 'school', 'open_grades': 'admissions',
}
GROUPED_GRADES = [
    ("Early Childhood", [g for g in ALL_GRADES if g in ['ECD', 'Nursery', 'LKG', 'UKG']]),
    ("Primary", [g for g in ALL_GRADES if g in ['Grade 1', 'Grade 2', 'Grade 3', 'Grade 4', 'Grade 5']]),
    ("Lower Secondary", [g for g in ALL_GRADES if g in ['Grade 6', 'Grade 7', 'Grade 8']]),
    ("Secondary", [g for g in ALL_GRADES if g in ['Grade 9', 'Grade 10']]),
    ("+2", [g for g in ALL_GRADES if g in ['Grade 11', 'Grade 12']]),
]
