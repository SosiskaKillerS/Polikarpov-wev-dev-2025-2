import unittest
from app import app, User, validate_login, validate_password, validate_name, validate_middle_name, validate_second_name
from flask import url_for
import json

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_validate_login(self):
        # Тест пустого логина
        self.assertFalse(validate_login('')[0])
        
        # Тест короткого логина
        self.assertFalse(validate_login('user')[0])
        
        # Тест логина с недопустимыми символами
        self.assertFalse(validate_login('user@123')[0])
        
        # Тест корректного логина
        self.assertTrue(validate_login('user123')[0])

    def test_validate_password(self):
        # Тест пустого пароля
        self.assertFalse(validate_password('')[0])
        
        # Тест короткого пароля
        self.assertFalse(validate_password('Pass1')[0])
        
        # Тест пароля без заглавных букв
        self.assertFalse(validate_password('password123')[0])
        
        # Тест пароля без цифр
        self.assertFalse(validate_password('Password')[0])
        
        # Тест пароля с пробелами
        self.assertFalse(validate_password('Pass word123')[0])
        
        # Тест корректного пароля
        self.assertTrue(validate_password('Password123')[0])

    def test_validate_name_fields(self):
        # Тест пустого имени
        self.assertFalse(validate_name('')[0])
        
        # Тест корректного имени
        self.assertTrue(validate_name('Иван')[0])
        
        # Тест пустого отчества
        self.assertFalse(validate_middle_name('')[0])
        
        # Тест корректного отчества
        self.assertTrue(validate_middle_name('Иванович')[0])
        
        # Тест пустой фамилии
        self.assertFalse(validate_second_name('')[0])
        
        # Тест корректной фамилии
        self.assertTrue(validate_second_name('Иванов')[0])

    def test_add_user(self):
        # Тест добавления пользователя с корректными данными
        response = self.app.post('/add_user', data={
            'name': 'Иван',
            'middle_name': 'Иванович',
            'second_name': 'Иванов',
            'login': 'ivanov123',
            'password': 'Password123',
            'role': 'user'
        })
        self.assertEqual(response.status_code, 302)  # Редирект после успешного добавления

        # Тест добавления пользователя с существующим логином
        response = self.app.post('/add_user', data={
            'name': 'Петр',
            'middle_name': 'Петрович',
            'second_name': 'Петров',
            'login': 'ivanov123',  # Тот же логин
            'password': 'Password123',
            'role': 'user'
        })
        self.assertEqual(response.status_code, 302)

    def test_edit_user(self):
        # Тест редактирования пользователя
        response = self.app.post('/edit_user/1', data={
            'name': 'Иван',
            'middle_name': 'Иванович',
            'second_name': 'Иванов',
            'role': 'admin'
        })
        self.assertEqual(response.status_code, 302)

    def test_change_password(self):
        # Тест изменения пароля с неверным текущим паролем
        response = self.app.post('/change_password/1', data={
            'current_password': 'WrongPassword',
            'new_password': 'NewPassword123',
            'confirm_password': 'NewPassword123'
        })
        self.assertEqual(response.status_code, 302)

        # Тест изменения пароля с несовпадающими новыми паролями
        response = self.app.post('/change_password/1', data={
            'current_password': 'Password123',
            'new_password': 'NewPassword123',
            'confirm_password': 'DifferentPassword123'
        })
        self.assertEqual(response.status_code, 302)

    def test_delete_user(self):
        # Тест удаления пользователя
        response = self.app.post('/delete_user/1')
        self.assertEqual(response.status_code, 302)

    def test_user_details(self):
        # Тест просмотра деталей пользователя
        response = self.app.get('/user/1')
        self.assertEqual(response.status_code, 200)

    def test_users_list(self):
        # Тест получения списка пользователей
        response = self.app.get('/users')
        self.assertEqual(response.status_code, 200)

    def test_invalid_user_id(self):
        # Тест запроса несуществующего пользователя
        response = self.app.get('/user/999')
        self.assertEqual(response.status_code, 302)  # Редирект на список пользователей

    def test_edit_nonexistent_user(self):
        # Тест редактирования несуществующего пользователя
        response = self.app.post('/edit_user/999', data={
            'name': 'Иван',
            'middle_name': 'Иванович',
            'second_name': 'Иванов',
            'role': 'user'
        })
        self.assertEqual(response.status_code, 302)

    def test_delete_nonexistent_user(self):
        # Тест удаления несуществующего пользователя
        response = self.app.post('/delete_user/999')
        self.assertEqual(response.status_code, 302)

    def test_change_password_nonexistent_user(self):
        # Тест изменения пароля несуществующего пользователя
        response = self.app.post('/change_password/999', data={
            'current_password': 'Password123',
            'new_password': 'NewPassword123',
            'confirm_password': 'NewPassword123'
        })
        self.assertEqual(response.status_code, 302)

    def test_add_user_validation(self):
        # Тест добавления пользователя с некорректными данными
        response = self.app.post('/add_user', data={
            'name': '',  # Пустое имя
            'middle_name': '',  # Пустое отчество
            'second_name': '',  # Пустая фамилия
            'login': 'user',  # Короткий логин
            'password': 'pass',  # Некорректный пароль
            'role': 'user'
        })
        self.assertEqual(response.status_code, 200)  # Возврат на форму с ошибками

if __name__ == '__main__':
    unittest.main() 