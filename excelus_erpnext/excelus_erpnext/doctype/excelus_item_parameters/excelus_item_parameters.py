# -*- coding: utf-8 -*-
# Copyright (c) 2017, MN Technique and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class ExcelusItemParameters(Document):
	def validate(self):
		self.set_item_parameters()

	def set_item_parameters(self):
		item = frappe.get_doc("Item", self.item)
		item.excelus_pm_length = self.excelus_pm_length
		item.excelus_pm_length_uom = self.excelus_pm_length_uom
		item.excelus_pm_width = self.excelus_pm_width
		item.excelus_pm_width_uom = self.excelus_pm_width_uom
		item.excelus_pm_height = self.excelus_pm_height
		item.excelus_pm_height_uom = self.excelus_pm_height_uom
		item.excelus_pm_thickness = self.excelus_pm_thickness
		item.excelus_pm_thickness_uom = self.excelus_pm_thickness_uom
		item.excelus_pm_fold_bleed = self.excelus_pm_fold_bleed
		item.excelus_pm_fold_bleed_uom = self.excelus_pm_fold_bleed_uom
		item.excelus_pm_flap_bleed = self.excelus_pm_flap_bleed
		item.excelus_pm_flap_bleed_uom = self.excelus_pm_flap_bleed_uom
		item.excelus_tape_bleed_uom = self.excelus_tape_bleed_uom
		item.excelus_tape_bleed = self.excelus_tape_bleed
		item.excelus_packs_per_carton = self.excelus_packs_per_carton
		item.excelus_conversion_cost = self.excelus_conversion_cost
		item.excelus_pm_wastage = self.excelus_pm_wastage
		item.hsm_code = self.hsm_code
		item.abetment_rate = self.abatement_rate
		item.mrp_rate = self.mrp_rate

		# Save and commit Item
		item.save()
		frappe.db.commit()
