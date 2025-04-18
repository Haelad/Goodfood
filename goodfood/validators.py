from string import ascii_letters, digits

from django.forms import ValidationError
from django.utils.deconstruct import deconstructible

@deconstructible
class GoodfoodValidator():
  
  ALLOWED_CHARACTERS = (
    ascii_letters +
    digits +
    "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯ" +
    "абвгдеёжзийклмнопрстуфхцчшщьыъэюя" +
    " -,.;:!?"
    )
  
  
  def __init__(self, message=None):
    
    self.massage = message if message else "input should be ascii_letters, digits or russian"
    
  def __call__(self, value):

    if not (set(value) <= set(self.ALLOWED_CHARACTERS)):
      raise ValidationError(self.message, params={"value": value})
  