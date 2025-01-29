from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(value, arg):
    """
    Aggiunge una classe CSS ai widget del form.
    """
    return value.as_widget(attrs={'class': arg})

@register.filter(name='add_attrs')
def add_attrs(field, css):
    """
    Aggiungi attributi personalizzati ai widget dei form.
    Usa il formato: 'class:class-name placeholder:placeholder-text'.
    """
    attrs = {}
    try:
        definitions = css.split(',')
        for definition in definitions:
            key, value = definition.split(':')
            attrs[key.strip()] = value.strip()
    except ValueError:
        raise ValueError("Formato non valido per il filtro 'add_attrs'. Usa il formato: 'key:value, key:value'.")
    return field.as_widget(attrs=attrs)