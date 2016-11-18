# -*- coding: utf-8 -*-
# Copyright (c) 2015, MN Technique and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document

class ExcelusCustomerInquiry(Document):
	pass


@frappe.whitelist()
def calculate_fetch_item(req_items):
    final_items = []
    import json

    req_items_js = json.loads(req_items)





    for item in req_items_js:
        for x in xrange(1,10):
            print item
        if not item.get('bom'):
            frappe.throw(_("Please select BOM for all requirement Items"))
        bom_items = frappe.db.get_all("BOM Item", filters={"parent":item.get('bom')}, fields=["*"])
        for bom_item in bom_items:

            found_item = [x for x in final_items if x.item_code==bom_item.item_code]
            if len(found_item)==1:
                found_item[0].qty += bom_item.qty
            else:
                final_items.append(bom_item)

    return final_items