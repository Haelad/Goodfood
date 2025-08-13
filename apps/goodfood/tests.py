from django.test import TestCase


# Create your tests here.

# для того что бы воспользоваться тестом нужно запустить его через терминал 
# manage.py test "имя приложения"
class GoodfoodTest(TestCase):
  
  def test_index(self):
    res = self.client.get("/goodfood/")
    # сперва наш код, затем устанавливаем чему он должен быть равен"
    self.assertEqual(res.status_code, 200)
    
    
