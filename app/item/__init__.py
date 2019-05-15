# -*- coding: utf-8 -*-
from flask import Blueprint

item = Blueprint('item', __name__)

from . import views
from ..models import Permission

@item.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)