import unittest
from app import app, warehouse_store


class TestFlaskApp(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()
        warehouse_store["warehouses"].clear()
        warehouse_store["counter"] = 0

    def test_index_page_loads(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Kawaii Warehouse', response.data)

    def test_create_warehouse_page_loads(self):
        response = self.client.get('/warehouse/new')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Create New Warehouse', response.data)

    def test_create_warehouse_post(self):
        response = self.client.post('/warehouse/new', data={
            'name': 'Test Warehouse',
            'capacity': '100',
            'initial_balance': '50'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(warehouse_store["warehouses"]), 1)
        warehouse = warehouse_store["warehouses"][1]
        self.assertEqual(warehouse['name'], 'Test Warehouse')
        self.assertEqual(warehouse['varasto'].tilavuus, 100)
        self.assertEqual(warehouse['varasto'].saldo, 50)

    def test_view_warehouse(self):
        self.client.post('/warehouse/new', data={
            'name': 'Test Warehouse',
            'capacity': '100',
            'initial_balance': '0'
        })
        response = self.client.get('/warehouse/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Warehouse', response.data)

    def test_view_nonexistent_warehouse_redirects(self):
        response = self.client.get('/warehouse/999')
        self.assertEqual(response.status_code, 302)

    def test_edit_warehouse_page_loads(self):
        self.client.post('/warehouse/new', data={
            'name': 'Test Warehouse',
            'capacity': '100',
            'initial_balance': '0'
        })
        response = self.client.get('/warehouse/1/edit')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Edit Warehouse', response.data)

    def test_edit_warehouse_post(self):
        self.client.post('/warehouse/new', data={
            'name': 'Original Name',
            'capacity': '100',
            'initial_balance': '0'
        })
        response = self.client.post('/warehouse/1/edit', data={
            'name': 'New Name'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            warehouse_store["warehouses"][1]['name'],
            'New Name'
        )

    def test_add_content(self):
        self.client.post('/warehouse/new', data={
            'name': 'Test Warehouse',
            'capacity': '100',
            'initial_balance': '0'
        })
        response = self.client.post('/warehouse/1/add', data={
            'amount': '25'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(warehouse_store["warehouses"][1]['varasto'].saldo, 25)

    def test_remove_content(self):
        self.client.post('/warehouse/new', data={
            'name': 'Test Warehouse',
            'capacity': '100',
            'initial_balance': '50'
        })
        response = self.client.post('/warehouse/1/remove', data={
            'amount': '20'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(warehouse_store["warehouses"][1]['varasto'].saldo, 30)

    def test_delete_warehouse(self):
        self.client.post('/warehouse/new', data={
            'name': 'Test Warehouse',
            'capacity': '100',
            'initial_balance': '0'
        })
        self.assertEqual(len(warehouse_store["warehouses"]), 1)
        response = self.client.post(
            '/warehouse/1/delete',
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(warehouse_store["warehouses"]), 0)

    def test_create_warehouse_invalid_capacity(self):
        response = self.client.post('/warehouse/new', data={
            'name': 'Test Warehouse',
            'capacity': '-10',
            'initial_balance': '0'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(warehouse_store["warehouses"]), 0)

    def test_add_content_nonexistent_warehouse(self):
        response = self.client.post('/warehouse/999/add', data={
            'amount': '25'
        })
        self.assertEqual(response.status_code, 302)

    def test_remove_content_nonexistent_warehouse(self):
        response = self.client.post('/warehouse/999/remove', data={
            'amount': '25'
        })
        self.assertEqual(response.status_code, 302)

    def test_edit_nonexistent_warehouse(self):
        response = self.client.get('/warehouse/999/edit')
        self.assertEqual(response.status_code, 302)
