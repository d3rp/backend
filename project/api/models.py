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

from django.db import models
from colorfield.fields import ColorField

# Create your models here.
class TerritorialEntity(models.Model):
    """
    A 1-1 mapping between a https://www.wikidata.org/wiki/Q56061, and a PK in our db.
    Holds an additional color information.
    """

    wikidata_id = models.PositiveIntegerField(primary_key=True)  # Excluding the Q
    color = ColorField()
    admin_level = models.PositiveIntegerField()
    predecessors = models.ManyToManyField("self", blank=True, related_name="successors")
    relations = models.ManyToManyField(
        "self", blank=True, symmetrical=False, through=PoliticalRelation
    )


class PoliticalRelation(models.Model):
    """
    Stores various political relations
    """

    parents = models.ForeignKey(TerritorialEntity)
    children = models.ForeignKey(TerritorialEntity)

    start_date = models.DateField()
    end_date = models.DateField()

    DIRECT = 0
    INDIRECT = 1
    GROUP = 2
    CONTROL_TYPES = ((DIRECT, "direct"), (INDIRECT, "indirect"), (GROUP, "group"))
    control_type = models.PositiveIntegerField(choices=CONTROL_TYPES)
