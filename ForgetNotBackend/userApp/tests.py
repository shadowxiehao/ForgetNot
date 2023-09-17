from datetime import datetime, timedelta
import time

from django.test import Client, TestCase
from django.contrib.auth.hashers import make_password

from userApp.models import User, Label, Event, Event_User_Relation
from .views import authenticate


# Test for user
class UserTestCase(TestCase):
    def setUp(self):
        # Create a request factory for client test
        self.c = Client()
        # Setup two users
        self.user1 = User.objects.create(email="my@email.com", birthday="01012010",
                                         gender="male", firstName="joe", lastName="duo", is_active=True,
                                         password=make_password("random_password1"), is_visitor=False)
        self.user2 = User.objects.create(email="my@fakemail.com", birthday="01012000",
                                         gender="male", firstName="tim", lastName="Dickens", is_active=True,
                                         password=make_password("random_password2"), is_visitor=False)

        # Setup labels for test
        self.label1 = Label.objects.create(
            name="label1", owner=self.user1, color="green")
        Label.objects.create(name="label2", owner=self.user2, color="blue")

        # Create an event
        today = datetime.now()
        tomorrow = today + timedelta(days=1)
        self.event = Event.objects.create(title="event_title", notes="a test note",
                                          startDate=today, endDate=tomorrow)
        # Bind the relation between user and event
        Event_User_Relation.objects.create(event=self.event, user=self.user1,
                                           type=0, status=0, label=self.label1)

    def test_user_can_login(self):
        """Check if a registered user is able to login with correct credentials"""
        response = self.c.post(
            '/api/user/login/', {'email': 'my@email.com', 'password': 'random_password1'})
        self.assertEqual(response.status_code, 200)

    def test_event_list(self):
        """Test if user is able to get event list successfully"""
        # First, let user login
        self.c.post('/api/user/login/',
                    {'email': 'my@email.com', 'password': 'random_password1'})
        response = self.c.get('/api/event/get_list/', {"id": self.label1.id})
        events = response.json()
        self.assertGreater(len(events.get("data")), 0)

    def test_event_create(self):
        """Test if user is able to create a new event"""
        # First, let user login
        self.c.post('/api/user/login/',
                    {'email': 'my@email.com', 'password': 'random_password1'})
        post_data = {
            "title": "buy something to eat",
            "startDate": int(time.time() * 1000),
            "endDate": int(time.time() * 1000 + 86400),  # 86400 is one day
            "notes": "something to note here",
            "label_id": self.label1.id,
            "allDay": True,
            "rRule": ""  # Leave it blank
        }
        response = self.c.post('/api/event/create/', post_data)
        self.assertEqual(response.json().get("msg"), "Create successfully.")

    def test_update_an_event(self):
        """Test if user is able to update an event"""
        # First, let user login
        self.c.post('/api/user/login/',
                    {'email': 'my@email.com', 'password': 'random_password1'})
        # Try to update the event label from label1 to label1_edit
        label_data = {
            "label_id": self.label1.id,
            "name": "label1_edit",
            "color": "green"
        }
        label_change_response = self.c.post('/api/label/update/', label_data)
        self.assertEqual(label_change_response.status_code, 200)

    def test_delete_an_event(self):
        """Test if user is able to delete an event"""
        # First, let user login
        self.c.post('/api/user/login/',
                    {'email': 'my@email.com', 'password': 'random_password1'})
        # Delete the event that created in the test setUp
        event_data = {
            "event_id": self.event.id,
        }
        delete_response = self.c.post('/api/event/delete/', event_data)
        self.assertEqual(delete_response.status_code, 200)
        # Try to list all events and there should be no event now
        event_response = self.c.get(
            '/api/event/get_list/', {"id": self.label1.id})
        events = event_response.json()
        self.assertEqual(len(events.get("data")), 0)
