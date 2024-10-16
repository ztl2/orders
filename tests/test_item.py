######################################################################
# Copyright 2016, 2024 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
######################################################################

"""
Test cases for Item Model
"""

# pylint: disable=duplicate-code
import os
import logging
from unittest import TestCase
from wsgi import app
from service.models import Order, Item, db
from .factories import OrderFactory, ItemFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql+psycopg://postgres:postgres@localhost:5432/testdb"
)


######################################################################
#  I T E M   M O D E L   T E S T   C A S E S
######################################################################
# pylint: disable=too-many-public-methods
class TestItem(TestCase):
    """Test Cases for Item Model"""

    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        app.app_context().push()

    @classmethod
    def tearDownClass(cls):
        """This runs once after the entire test suite"""
        db.session.close()

    def setUp(self):
        """This runs before each test"""
        db.session.query(Order).delete()  # clean up the last tests
        db.session.query(Item).delete()  # clean up the last tests
        db.session.commit()

    def tearDown(self):
        """This runs after each test"""
        db.session.remove()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_create_item(self):
        """It should create an Item associate with an Order and add it to the database"""
        orders = Order.all()
        self.assertEqual(orders, [])
        order = OrderFactory()
        item = ItemFactory(order=order)
        order.amount = order.amount + item.amount()
        order.create()
        self.assertIsNotNone(order.id)
        orders = Order.all()
        self.assertEqual(len(orders), 1)

        new_order = Order.find(order.id)
        self.assertEqual(new_order.id, item.order_id)

        new_item = ItemFactory(order=order)
        order.amount += new_item.amount()
        order.update()

        new_order = Order.find(order.id)
        self.assertEqual(new_order.id, new_item.order_id)
        self.assertEqual(
            new_order.amount,
            item.amount() + new_item.amount(),
        )

    # Todo: Add your test cases here...
