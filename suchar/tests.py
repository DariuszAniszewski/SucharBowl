from django.test import TestCase
import simplejson
from suchar.models import Organisation

class TestOrganisations(TestCase):
    def setUp(self):
        pass

    def testAddNewOrganisationWithoutName(self):
        response = self.client.post("/api/organisations/add",{})
        self.assertEqual(response.status_code,400)
        json_response = simplejson.loads(response.content)
        self.assertTrue(json_response.has_key("error"))
        self.assertEqual(json_response["error"],"no name provided")

    def testAddNewOrganisationWithoutEmail(self):
        response = self.client.post("/api/organisations/add",{"name":"polidea"})
        self.assertEqual(response.status_code,400)
        json_response = simplejson.loads(response.content)
        self.assertTrue(json_response.has_key("error"))
        self.assertEqual(json_response["error"],"no email provided")

    def testAddNewOrganisationWithNameTaken(self):
        Organisation.objects.create(name="polidea",api_key="123")
        response = self.client.post("/api/organisations/add",{"name":"polidea","email":"dariusz@aniszewski.eu"})
        self.assertEqual(response.status_code,400)
        json_response = simplejson.loads(response.content)
        self.assertTrue(json_response.has_key("error"))
        self.assertEqual(json_response["error"],"Organisation already exists")

    def testAddNewOrganisationWithSuccess(self):
        response = self.client.post("/api/organisations/add",{"name":"polidea","email":"dariusz@aniszewski.eu"})
        self.assertEqual(response.status_code,200)
        json_response = simplejson.loads(response.content)
        self.assertFalse(json_response.has_key("error"))
        self.assertTrue(json_response.has_key("id"))
        self.assertTrue(json_response.has_key("name"))
        self.assertTrue(json_response.has_key("api_key"))

        organisation = Organisation.objects.get(pk=1)
        self.assertEqual(json_response["id"],organisation.id)
        self.assertEqual(json_response["name"],organisation.name)
        self.assertEqual(json_response["api_key"],organisation.api_key)
        print organisation.api_key