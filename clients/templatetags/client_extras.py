from django import template

#va a recibir los campos de dicho modelo
def list_fields(model):
    return [ field.name for field in model._meta.get_fields() if not field.is_relation and field.name != 'id']

def get_value(model, value):
    return getattr(model, value)
#nos va a permitir trabajar con nuestras funciones dentro de nuestro template
register = template.Library()

#filter nos va a permitir trabajar con nuestra funcion title_say_hello
#el primer parametro es como quiero que se llame dentro de nuestro html
#el segundo parametro es mi funcion
register.filter('list_fields', list_fields)
register.filter('get_value', get_value)
