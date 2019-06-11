"""
Chron.
Copyright (C) 2018 Alisa Belyaeva, Ata Ali Kilicli, Amaury Martiny,
Daniil Mordasov, Liam O’Flynn, Mikhail Orlov.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from math import ceil
from django.core.exceptions import ValidationError
from django.contrib.gis.geos import Point, Polygon
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from jdcal import gcal2jd

from .factories import (
    TerritorialEntityFactory,
    PoliticalRelationFactory,
    CachedDataFactory,
    SpacetimeVolumeFactory,
    NarrativeFactory,
    MapSettingsFactory,
    NarrationFactory,
    CityFactory,
)
from .models import (
    PoliticalRelation,
    TerritorialEntity,
    SpacetimeVolume,
    Narrative,
    MapSettings,
    Narration,
    CachedData,
    City,
)

# Constants
JD_0001 = ceil(sum(gcal2jd(1, 1, 1))) + 0.0
JD_0002 = ceil(sum(gcal2jd(2, 1, 1))) + 0.0
JD_0003 = ceil(sum(gcal2jd(3, 1, 1))) + 0.0
JD_0004 = ceil(sum(gcal2jd(4, 1, 1))) + 0.0
JD_0005 = ceil(sum(gcal2jd(5, 1, 1))) + 0.0

# Tests
class ModelTest(TestCase):
    """
    Tests model constraints directly
    """

    @classmethod
    def setUpTestData(cls):
        """
        Create basic model instances
        """

        cls.european_union = TerritorialEntityFactory(
            wikidata_id=10,
            label="European Union",
            color=1,
            admin_level=1,
            inception_date=0,
            dissolution_date=1,
        )
        cls.nato = TerritorialEntityFactory(
            wikidata_id=11,
            label="NATO",
            color=1,
            admin_level=1,
            inception_date=0,
            dissolution_date=1,
        )

        cls.germany = TerritorialEntityFactory(
            wikidata_id=20,
            label="Germany",
            color=1,
            admin_level=2,
            inception_date=0,
            dissolution_date=1,
        )
        cls.france = TerritorialEntityFactory(
            wikidata_id=21,
            label="France",
            color=1,
            admin_level=2,
            inception_date=0,
            dissolution_date=1,
        )
        cls.spain = TerritorialEntityFactory(
            wikidata_id=22,
            label="Spain",
            color=1,
            admin_level=2,
            inception_date=0,
            dissolution_date=1,
        )
        cls.italy = TerritorialEntityFactory(
            wikidata_id=23,
            label="Italy",
            color=1,
            admin_level=2,
            inception_date=0,
            dissolution_date=1,
        )
        cls.british_empire = TerritorialEntityFactory(
            wikidata_id=24,
            label="British Empire",
            color=1,
            admin_level=2,
            inception_date=0,
            dissolution_date=1,
        )
        cls.british_hk = TerritorialEntityFactory(
            wikidata_id=25,
            label="British HK",
            color=1,
            admin_level=2,
            inception_date=0,
            dissolution_date=1,
        )

        cls.alsace = TerritorialEntityFactory(
            wikidata_id=30,
            label="Alsace",
            color=1,
            admin_level=3,
            inception_date=0,
            dissolution_date=1,
        )
        cls.lorraine = TerritorialEntityFactory(
            wikidata_id=31,
            label="Lorraine",
            color=1,
            admin_level=3,
            inception_date=0,
            dissolution_date=1,
        )

    def test_model_can_create_te(self):
        """
        Ensure that we can create TerritorialEntity
        """

        test_te = TerritorialEntity.objects.create(
            wikidata_id=9,
            label="test TE",
            color=2,
            admin_level=4,
            inception_date=0,
            dissolution_date=1,
        )
        test_te.save()
        test_te.predecessor.add(self.alsace)
        self.assertTrue(TerritorialEntity.objects.filter(wikidata_id=9).exists())

    def test_model_can_create_pr(self):
        """
        Ensure that we can create PoliticalRelations of types GROUP and DIRECT
        Tests get_children() and get_parents() methods
        """

        # GROUP
        PoliticalRelation.objects.create(
            start_date=JD_0001,
            end_date=JD_0002,
            parent=self.european_union,
            child=self.france,
            control_type=PoliticalRelation.GROUP,
        )
        PoliticalRelation.objects.create(
            start_date=JD_0001,
            end_date=JD_0002,
            parent=self.european_union,
            child=self.germany,
            control_type=PoliticalRelation.GROUP,
        )
        PoliticalRelation.objects.create(
            start_date=JD_0001,
            end_date=JD_0002,
            parent=self.nato,
            child=self.france,
            control_type=PoliticalRelation.GROUP,
        )
        self.assertEqual(
            PoliticalRelation.objects.filter(parent=self.european_union).count(), 2
        )
        self.assertEqual(PoliticalRelation.objects.filter(parent=self.nato).count(), 1)

        # DIRECT
        PoliticalRelation.objects.create(
            start_date=JD_0001,
            end_date=JD_0002,
            parent=self.france,
            child=self.alsace,
            control_type=PoliticalRelation.DIRECT,
        )
        PoliticalRelation.objects.create(
            start_date=JD_0001,
            end_date=JD_0002,
            parent=self.france,
            child=self.lorraine,
            control_type=PoliticalRelation.DIRECT,
        )
        self.assertEqual(
            PoliticalRelation.objects.filter(parent=self.france).count(), 2
        )

        # get_parents()
        self.assertEqual(self.lorraine.get_parents().count(), 1)
        self.assertEqual(self.lorraine.get_parents().first(), self.france)
        self.assertEqual(self.france.get_parents().count(), 2)  # euopean_union and nato
        self.assertFalse(self.european_union.get_parents().exists())

        # get_children()
        self.assertEqual(
            self.european_union.get_children().count(), 2
        )  # france and germany
        self.assertEqual(self.france.get_children().count(), 2)  # alsace and lorraine
        self.assertFalse(self.lorraine.get_children().exists())

    def test_model_can_not_create_pr(self):
        """
        Ensure PoliticalRelation validations work
        """

        with self.assertRaises(ValidationError):
            PoliticalRelation.objects.create(
                start_date=JD_0005,
                end_date=JD_0002,
                parent=self.european_union,
                child=self.germany,
                control_type=PoliticalRelation.GROUP,
            )

        with self.assertRaises(ValidationError):
            PoliticalRelation.objects.create(
                start_date=JD_0001,
                end_date=JD_0002,
                parent=self.germany,
                child=self.european_union,
                control_type=PoliticalRelation.DIRECT,
            )

    def test_model_can_create_stv(self):
        """
        Ensure we can create SpacetimeVolumes
        """

        SpacetimeVolume.objects.create(
            start_date=JD_0001,
            end_date=JD_0002,
            entity=self.france,
            references=["ref"],
            visual_center=Point(1.2, 1.8),
            territory=Polygon(((1, 1), (1, 2), (2, 2), (1, 1))),
        )

        self.assertTrue(
            SpacetimeVolume.objects.filter(
                territory=Polygon(((1, 1), (1, 2), (2, 2), (1, 1)))
            ).exists()
        )

        self.assertEqual(
            str(
                SpacetimeVolume.objects.filter(
                    territory=Polygon(((1, 1), (1, 2), (2, 2), (1, 1)))
                )[0].visual_center
            ),
            "SRID=4326;POINT (1.2 1.8)",
        )

    def test_model_can_not_create_stv(self):
        """
        Ensure non overlapping timeframe and territory constraints works
        """
        # Timeframe
        with self.assertRaises(ValidationError):
            SpacetimeVolume.objects.create(
                start_date=JD_0001,
                end_date=JD_0003,
                entity=self.france,
                references=["ref"],
                visual_center=Point(2, 2),
                territory=Polygon(((1, 1), (1, 2), (2, 2), (1, 1))),
            )
            SpacetimeVolume.objects.create(
                start_date=JD_0002,
                end_date=JD_0004,
                entity=self.france,
                references=["ref"],
                visual_center=Point(1, 1),
                territory=Polygon(((3, 3), (3, 4), (4, 4), (3, 3))),
            )

        # Territory
        with self.assertRaises(ValidationError):
            SpacetimeVolume.objects.create(
                start_date=JD_0003,
                end_date=JD_0004,
                entity=self.british_empire,
                references=["ref"],
                visual_center=Point(2, 2),
                territory=Polygon(((6, 6), (6, 7), (7, 7), (6, 6))),
            )
            SpacetimeVolume.objects.create(
                start_date=JD_0002,
                end_date=JD_0004,
                entity=self.italy,
                references=["ref"],
                visual_center=Point(1, 1),
                territory=Polygon(((6, 6), (6, 7), (7, 7), (6, 6))),
            )

        # Geom type
        with self.assertRaises(ValidationError):
            SpacetimeVolume.objects.create(
                start_date=JD_0001,
                end_date=JD_0003,
                entity=self.france,
                references=["ref"],
                visual_center=Point(2, 2),
                territory=Point(1, 1),
            )

    def test_model_can_create_narrative(self):
        """
        Ensure that we can create a narrative and the ordering plugin works.
        """
        test_narrative = Narrative.objects.create(
            author="Test Author",
            title="Test Narrative",
            url="test",
            description="This is a test narrative for automated testing.",
            tags=["test", "tags"],
        )

        test_settings = MapSettings.objects.create(zoom_min=1, zoom_max=12)

        hastings = CachedData.objects.create(
            wikidata_id=1,
            location=Point(0, 0),
            date=JD_0001,
            event_type=CachedData.BATTLE,
        )

        balaclava = CachedData.objects.create(
            wikidata_id=2,
            location=Point(0, 0),
            date=JD_0002,
            event_type=CachedData.BATTLE,
        )

        narration1 = Narration.objects.create(
            narrative=test_narrative,
            title="Test Narration",
            description="This is a narration point",
            date_label="test",
            map_datetime=JD_0002,
            settings=test_settings,
            location=Point(0, 0),
        )

        narration1.attached_events.add(hastings)

        test_settings2 = MapSettings.objects.create(zoom_min=1, zoom_max=12)

        narration2 = Narration.objects.create(
            narrative=test_narrative,
            title="Test Narration2",
            description="This is another narration point",
            date_label="test2",
            map_datetime=JD_0002,
            settings=test_settings2,
            location=Point(0, 0),
        )

        narration2.attached_events.add(balaclava)

        narration1.swap(narration2)

        self.assertEqual(Narrative.objects.filter().count(), 1)
        self.assertEqual(Narration.objects.filter().count(), 2)
        self.assertEqual(narration2.next().title, "Test Narration")

    def test_model_can_not_create_ms(self):
        """
        Ensure that the constraints on mapsettings work.
        """

        with self.assertRaises(ValidationError):
            MapSettings.objects.create(zoom_min=-0.1, zoom_max=2)

        with self.assertRaises(ValidationError):
            MapSettings.objects.create(zoom_min=1, zoom_max=22.1)

        with self.assertRaises(ValidationError):
            MapSettings.objects.create(zoom_min=5, zoom_max=3)

    def test_model_can_create_cd(self):
        """
        Ensure CachedData can be created
        """

        hastings = CachedData.objects.create(
            wikidata_id=1,
            location=Point(0, 0),
            date=JD_0001,
            event_type=CachedData.BATTLE,
        )

        self.assertTrue(hastings.rank >= 0)
        self.assertEqual(hastings.date, JD_0001)
        self.assertEqual(CachedData.objects.count(), 1)

    def test_model_can_create_city(self):
        """
        Ensure Cities can be created
        """

        paris = City.objects.create(
            wikidata_id=1, label="Paris", location=Point(0, 0), inception_date=JD_0001
        )

        self.assertEqual(paris.label, "Paris")
        self.assertEqual(City.objects.count(), 1)


class APITest(APITestCase):
    """
    Tests operations through the API
    """

    @classmethod
    def setUpTestData(cls):
        """
        Create basic model instances
        """

        # TerritorialEntities
        cls.european_union = TerritorialEntityFactory(
            wikidata_id=10,
            label="European Union",
            color=1,
            admin_level=1,
            inception_date=0,
            dissolution_date=1,
        )
        cls.nato = TerritorialEntityFactory(
            wikidata_id=11,
            label="NATO",
            color=1,
            admin_level=1,
            inception_date=0,
            dissolution_date=1,
        )

        cls.germany = TerritorialEntityFactory(
            wikidata_id=20,
            label="Germany",
            color=1,
            admin_level=2,
            inception_date=0,
            dissolution_date=1,
        )
        cls.france = TerritorialEntityFactory(
            wikidata_id=21,
            label="France",
            color=1,
            admin_level=2,
            inception_date=0,
            dissolution_date=1,
        )
        cls.spain = TerritorialEntityFactory(
            wikidata_id=22,
            label="Spain",
            color=1,
            admin_level=2,
            inception_date=0,
            dissolution_date=1,
        )
        cls.italy = TerritorialEntityFactory(
            wikidata_id=23,
            label="Italy",
            color=1,
            admin_level=2,
            inception_date=0,
            dissolution_date=1,
        )
        cls.british_empire = TerritorialEntityFactory(
            wikidata_id=24,
            label="British Empire",
            color=1,
            admin_level=2,
            inception_date=0,
            dissolution_date=1,
        )
        cls.british_hk = TerritorialEntityFactory(
            wikidata_id=25,
            label="British HK",
            color=1,
            admin_level=2,
            inception_date=0,
            dissolution_date=1,
        )

        cls.alsace = TerritorialEntityFactory(
            wikidata_id=30,
            label="Alsace",
            color=1,
            admin_level=3,
            inception_date=0,
            dissolution_date=1,
        )
        cls.lorraine = TerritorialEntityFactory(
            wikidata_id=31,
            label="Lorraine",
            color=1,
            admin_level=3,
            inception_date=0,
            dissolution_date=1,
        )

        # PoliticalRelations
        cls.EU_germany = PoliticalRelationFactory(
            parent=cls.european_union,
            child=cls.germany,
            start_date=JD_0001,
            end_date=JD_0002,
            control_type=PoliticalRelation.INDIRECT,
        )

        # CachedData
        cls.hastings = CachedDataFactory(
            wikidata_id=1,
            location=Point(0, 0),
            date=JD_0001,
            event_type=CachedData.BATTLE,
        )

        # SpacetimeVolumes
        cls.alsace_stv = SpacetimeVolumeFactory(
            start_date=JD_0001,
            end_date=JD_0002,
            entity=cls.france,
            references=["ref"],
            visual_center=Point(1.2, 1.8),
            territory=Polygon(((1, 1), (1, 2), (2, 2), (1, 1))),
        )

        # Narratives
        cls.norman_conquest = NarrativeFactory(
            author="Test Author",
            title="Test Narrative",
            url="test",
            description="This is a test narrative for automated testing.",
            tags=["test", "tags"],
        )

        # MapSettings
        cls.norman_conquest_settings = MapSettingsFactory(zoom_min=1, zoom_max=12)

        # Narrations
        cls.hastings_narration = NarrationFactory(
            narrative=cls.norman_conquest,
            title="Test Narration",
            description="This is a narration point",
            date_label="test",
            map_datetime=JD_0002,
            settings=cls.norman_conquest_settings,
            location=Point(0, 0),
        )

        # Cities
        cls.paris = CityFactory(
            wikidata_id=1, label="Paris", location=Point(0, 0), inception_date=JD_0001
        )

    def test_api_can_create_te(self):
        """
        Ensure we can create TerritorialEntities
        """

        url = reverse("territorialentity-list")
        data = {
            "wikidata_id": 9,
            "label": "Test TE",
            "color": "#fff",
            "admin_level": 4,
            "inception_date": 0,
            "dissolution_date": 1,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TerritorialEntity.objects.count(), 11)
        self.assertEqual(TerritorialEntity.objects.last().admin_level, 4)

    def test_api_can_update_te(self):
        """
        Ensure we can update TerritorialEntities
        """

        url = reverse("territorialentity-detail", args=[self.european_union.pk])
        data = {
            "wikidata_id": 10,
            "label": "Update",
            "color": "#fff",
            "admin_level": 5,
            "inception_date": 0,
            "dissolution_date": 1,
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["admin_level"], 5)

    def test_api_can_query_tes(self):
        """
        Ensure we can query for all TerritorialEntities
        """

        url = reverse("territorialentity-list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["id"], self.european_union.pk)
        self.assertEqual(response.data[3]["stv_count"], 1)

    def test_api_can_query_te(self):
        """
        Ensure we can query for individual TerritorialEntities
        """

        url = reverse("territorialentity-detail", args=[self.european_union.pk])
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["admin_level"], 1)

    def test_api_can_create_pr(self):
        """
        Ensure we can create PoliticalRelations
        """

        url = reverse("politicalrelation-list")
        data = {
            "start_date": JD_0001,
            "end_date": JD_0002,
            "parent": self.european_union.pk,
            "child": self.france.pk,
            "control_type": PoliticalRelation.GROUP,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PoliticalRelation.objects.count(), 2)
        self.assertEqual(
            PoliticalRelation.objects.last().control_type, PoliticalRelation.GROUP
        )

    def test_api_can_update_pr(self):
        """
        Ensure we can update PoliticalRelations
        """

        url = reverse("politicalrelation-detail", args=[self.EU_germany.pk])
        data = {
            "start_date": JD_0001,
            "end_date": JD_0002,
            "parent": self.european_union.pk,
            "child": self.france.pk,
            "control_type": PoliticalRelation.GROUP,
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["control_type"], PoliticalRelation.GROUP)

    def test_api_can_query_prs(self):
        """
        Ensure we can query for all PoliticalRelations
        """

        url = reverse("politicalrelation-list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["control_type"], PoliticalRelation.INDIRECT)

    def test_api_can_query_pr(self):
        """
        Ensure we can query for individual PoliticalRelations
        """

        url = reverse("politicalrelation-detail", args=[self.EU_germany.pk])
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["control_type"], PoliticalRelation.INDIRECT)

    def test_api_can_create_cd(self):
        """
        Ensure we can create CachedData
        """

        url = reverse("cacheddata-list")
        data = {
            "wikidata_id": 2,
            "location": "Point(0 1)",
            "date": JD_0001,
            "event_type": CachedData.DOCUMENT,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CachedData.objects.count(), 2)
        self.assertEqual(CachedData.objects.last().event_type, CachedData.DOCUMENT)

    def test_api_can_create_cd_othertype(self):
        """
        Ensure we can create CachedData with an event_type not in the choices
        """

        url = reverse("cacheddata-list")
        data = {
            "wikidata_id": 2,
            "location": "Point(0 1)",
            "date": JD_0001,
            "event_type": 555,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CachedData.objects.count(), 2)
        self.assertEqual(CachedData.objects.last().event_type, 555)

    def test_api_can_update_cd(self):
        """
        Ensure we can update CachedData
        """

        url = reverse("cacheddata-detail", args=[self.hastings.pk])
        data = {
            "wikidata_id": 1,
            "location": "Point(0 0)",
            "date": JD_0001,
            "event_type": CachedData.DOCUMENT,
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["event_type"], CachedData.DOCUMENT)

    def test_api_can_query_cds(self):
        """
        Ensure we can query for all CachedDatas
        """

        url = reverse("cacheddata-list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["event_type"], CachedData.BATTLE)

    def test_api_can_query_cd(self):
        """
        Ensure we can query for individual CachedDatas
        """

        url = reverse("cacheddata-detail", args=[self.hastings.pk])
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["event_type"], CachedData.BATTLE)

    def test_api_can_create_stv(self):
        """
        Ensure we can create SpacetimeVolumes
        """

        url = reverse("spacetimevolume-list")
        data = {
            "start_date": JD_0001,
            "end_date": JD_0002,
            "entity": self.germany.pk,
            "references": ["ref"],
            "territory": "POLYGON((3 3, 3 4, 4 4, 3 3))",
            "visual_center": "POINT(1.2 1.8)",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(SpacetimeVolume.objects.count(), 2)
        self.assertEqual(SpacetimeVolume.objects.last().references, ["ref"])

    def test_api_can_update_stv(self):
        """
        Ensure we can update SpacetimeVolumes
        """

        url = reverse("spacetimevolume-detail", args=[self.alsace_stv.pk])
        data = {
            "start_date": JD_0001,
            "end_date": JD_0005,
            "entity": self.france.pk,
            "references": ["ref"],
            "territory": "POLYGON((1 1, 1 2, 2 2, 1 1))",
            "visual_center": "POINT (0.7 0.7)",
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["end_date"], str(JD_0005))

    def test_api_can_query_stv(self):
        """
        Ensure we can query for individual SpacetimeVolumes
        """

        url = reverse("spacetimevolume-detail", args=[self.alsace_stv.pk])
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["end_date"], str(JD_0002))

    def test_api_can_create_narrative(self):
        """
        Ensure we can create Narratives
        """

        url = reverse("narrative-list")
        data = {
            "author": "Test Author 2",
            "title": "Test Narrative",
            "url": "test2",
            "description": "This is a test narrative for automated testing.",
            "tags": ["test", "tags"],
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Narrative.objects.count(), 2)
        self.assertEqual(Narrative.objects.last().author, "Test Author 2")

    def test_api_can_update_narrative(self):
        """
        Ensure we can update Narratives
        """

        url = reverse("narrative-detail", args=[self.norman_conquest.pk])
        data = {
            "author": "Other Test Author",
            "title": "Test Narrative",
            "url": "test2",
            "description": "This is a test narrative for automated testing.",
            "tags": ["test", "tags"],
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["author"], "Other Test Author")

    def test_api_can_query_narratives(self):
        """
        Ensure we can query for all Narratives
        """

        url = reverse("narrative-list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["author"], "Test Author")

    def test_api_can_query_narrative(self):
        """
        Ensure we can query for individual Narratives
        """

        url = reverse("narrative-detail", args=[self.norman_conquest.pk])
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["author"], "Test Author")

    def test_api_can_create_ms(self):
        """
        Ensure we can create MapSettings
        """

        url = reverse("mapsettings-list")
        data = {"zoom_min": 1, "zoom_max": 13}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(MapSettings.objects.count(), 2)
        self.assertEqual(MapSettings.objects.last().zoom_min, 1.0)

    def test_api_can_update_ms(self):
        """
        Ensure we can update MapSettings
        """

        url = reverse("mapsettings-detail", args=[self.norman_conquest_settings.pk])
        data = {"zoom_min": 5, "zoom_max": 13}
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["zoom_min"], 5)

    def test_api_can_query_mss(self):
        """
        Ensure we can query for all MapSettings
        """

        url = reverse("mapsettings-list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["zoom_min"], 1)

    def test_api_can_query_ms(self):
        """
        Ensure we can query for individual MapSettings
        """

        url = reverse("mapsettings-detail", args=[self.norman_conquest_settings.pk])
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["zoom_min"], 1)

    def test_api_can_create_narration(self):
        """
        Ensure we can create Narrations
        """

        url = reverse("narration-list")
        data = {
            "narrative": self.norman_conquest.pk,
            "title": "Test Narration",
            "description": "This is a narration point",
            "date_label": "test",
            "map_datetime": JD_0002,
            "settings": self.norman_conquest_settings.pk,
            "attached_events_ids": [self.hastings.pk],
            "location": "POINT (0 0)",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Narration.objects.count(), 2)
        self.assertEqual(Narration.objects.last().title, "Test Narration")

    def test_api_can_update_narration(self):
        """
        Ensure we can update Narrations
        """

        url = reverse("narration-detail", args=[self.hastings_narration.pk])
        data = {
            "narrative": self.norman_conquest.pk,
            "title": "Test Narration 2",
            "description": "This is a narration point",
            "date_label": "test",
            "map_datetime": JD_0002,
            "settings": self.norman_conquest_settings.pk,
            "attached_events_ids": [self.hastings.pk],
            "location": "POINT (0 0)",
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Test Narration 2")

    def test_api_can_query_narrations(self):
        """
        Ensure we can query for all Narrations
        """

        url = reverse("narration-list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["title"], "Test Narration")

    def test_api_can_query_narration(self):
        """
        Ensure we can query for individual Narrations
        """

        url = reverse("narration-detail", args=[self.hastings_narration.pk])
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Test Narration")

    def test_api_can_create_city(self):
        """
        Ensure we can create Cities
        """

        url = reverse("city-list")
        data = {
            "wikidata_id": 2,
            "label": "London",
            "location": "POINT (10 10)",
            "inception_date": JD_0001,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(City.objects.count(), 2)
        self.assertEqual(City.objects.last().label, "London")

    def test_api_can_update_city(self):
        """
        Ensure we can update Cities
        """

        url = reverse("city-detail", args=[self.paris.pk])
        data = {
            "wikidata_id": 2,
            "label": "London",
            "location": "POINT (10 10)",
            "inception_date": JD_0001,
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["label"], "London")

    def test_api_can_query_cities(self):
        """
        Ensure we can query for all Cities
        """

        url = reverse("city-list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["label"], "Paris")

    def test_api_can_query_city(self):
        """
        Ensure we can query for individual Cities
        """

        url = reverse("city-detail", args=[self.paris.pk])
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["label"], "Paris")
