# -*- coding: utf-8 -*-
import logging

from odoo import models
from odoo.http import request
from odoo.exceptions import AccessDenied
from werkzeug.exceptions import Unauthorized

_logger = logging.getLogger(__name__)


class IrHttp(models.AbstractModel):
    _inherit = "ir.http"

    @classmethod
    def _auth_method_fleetflow_api_key(cls):
        """Authenticate a request using a Bearer API key.

        The caller must provide an ``Authorization: Bearer <key>`` header.
        The key is validated against ``res.users.apikeys`` with the ``rpc``
        scope. On success ``request.uid`` is set to the owning user; on
        failure a 401 Unauthorized is raised.
        """
        authorization = request.httprequest.headers.get("Authorization", "")
        if not authorization or not authorization.startswith("Bearer "):
            _logger.warning(
                "FleetFlow API: missing or malformed Authorization header"
            )
            raise Unauthorized("Missing or invalid Authorization header")

        api_key = authorization[len("Bearer "):].strip()
        if not api_key:
            raise Unauthorized("Empty API key")

        try:
            user_id = request.env["res.users.apikeys"]._check_credentials(
                scope="rpc", key=api_key
            )
        except AccessDenied:
            user_id = False

        if not user_id:
            _logger.warning("FleetFlow API: invalid API key")
            raise Unauthorized("Invalid API key")

        request.uid = user_id
