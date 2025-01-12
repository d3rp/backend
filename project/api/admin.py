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

from django.contrib import admin

from .models import (
    TerritorialEntity,
    PoliticalRelation,
    SpacetimeVolume,
    CachedData,
    Narration,
    Narrative,
    MapSettings,
    City,
    Profile,
    NarrativeVote,
)

# Register your models here.
admin.site.register(TerritorialEntity)
admin.site.register(PoliticalRelation)
admin.site.register(SpacetimeVolume)
admin.site.register(CachedData)
admin.site.register(Narration)
admin.site.register(Narrative)
admin.site.register(MapSettings)
admin.site.register(City)
admin.site.register(Profile)
admin.site.register(NarrativeVote)
