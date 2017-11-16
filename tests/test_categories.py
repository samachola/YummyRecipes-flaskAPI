from flask import json
from tests.base_testcase import BaseTestCase


class CategoriesTestCase(BaseTestCase):
    """Test for categories"""

    def test_category_creation(self):
        """Test API can create a category (POST request)"""

        req = self.authenticate()

        jwt_token = json.loads(req.data.decode())['jwt_token']

        # create a category by making a POST request
        req = self.client().post(
            'api/v1/category',
            headers=dict(Authorization="Bearer " + jwt_token),
            data=self.category)
        self.assertEqual(req.status_code, 201)

        # check if created category exists
        req = self.client().post('api/v1/category',
                                 headers=dict(Authorization="Bearer " + jwt_token),
                                 data=self.category)
        self.assertIn("Category already exists", str(req.data))
        self.assertEqual(req.status_code, 400)

        # check if fields are empty
        req = self.client().post('api/v1/category',
                                 headers=dict(Authorization="Bearer " + jwt_token),
                                 data={'name': '', 'desc': ''})
        self.assertIn("Name or description cannot be empty", str(req.data))
        self.assertEqual(req.status_code, 400)

    def test_if_user_can_retrieve_all_categories(self):
        """Test api can get all categories"""
        req = self.authenticate()

        jwt_token = json.loads(req.data.decode())['jwt_token']

        # create a category by making a POST request
        req = self.client().post(
            'api/v1/category',
            headers=dict(Authorization="Bearer " + jwt_token),
            data=self.category)
        self.assertEqual(req.status_code, 201)

        res = self.client().get(
            'api/v1/category',
            headers=dict(Authorization="Bearer " + jwt_token),
        )
        self.assertEqual(res.status_code, 200)
        # self.assertIn('description', str(res.data))

    def test_category_editing(self):
        """Test category can be updated"""

        req = self.authenticate()

        jwt_token = json.loads(req.data.decode())['jwt_token']

        # create a category by making a POST request
        req = self.client().post(
            'api/v1/category',
            headers=dict(Authorization="Bearer " + jwt_token),
            data=self.category)
        self.assertEqual(req.status_code, 201)

        # get the category in json
        results = json.loads(req.data.decode())

        # edit category
        req = self.client().put(
            'api/v1/category/1',
            headers=dict(Authorization="Bearer " + jwt_token),
            data=self.category)
        self.assertEqual(req.status_code, 200)

        # get edited category
        req = self.client().get(
            'api/v1/category/1',
            headers=dict(Authorization="Bearer " + jwt_token))
        self.assertIn('desc', str(req.data))

    def test_category_deletion(self):
        """Test category can be deleted"""

        req = self.authenticate()

        jwt_token = json.loads(req.data.decode())['jwt_token']

        # create a category by making a POST request
        req = self.client().post(
            'api/v1/category',
            headers=dict(Authorization="Bearer " + jwt_token),
            data=self.category)
        self.assertEqual(req.status_code, 201)

        # get the category in json
        req = json.loads(req.data.decode())

        # delete the category
        req = self.client().delete(
            'api/v1/category/1',
            headers=dict(Authorization="Bearer " + jwt_token), )
        self.assertEqual(req.status_code, 200)

        # Test to see if it exists
        req = self.client().get(
            'api/v1/category/1',
            headers=dict(Authorization="Bearer " + jwt_token))
        self.assertEqual(req.status_code, 401)

