from string import ascii_letters, digits

from django.forms import ValidationError
from django.utils.deconstruct import deconstructible

@deconstructible
class GoodfoodValidator():
  
  ALLOWED_CHARACTERS = ascii_letters + digits + "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабвгдеёжзийклмнопрстуфхцчшщбыъэюя " + "-,.;:!?"
  
  def __init__(self, massage=None):
    
    self.massage = massage if massage else "input should be ascii_letters, digits or russian"
    
  def __call__(self, value):

    if not (set(value) <= set(self.ALLOWED_CHARACTERS)):
      raise ValidationError(self.massage, params={"value": value})
  