# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "excelus_erpnext"
app_title = "Excelus ERPNext"
app_publisher = "MN Technique"
app_description = "Excelus Customizations for ERPNext"
app_icon = "octicon octicon-diff-modified"
app_color = "scarlet"
app_email = "support@mntechnique.com"
app_license = "GPL v3"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/excelus_erpnext/css/excelus_erpnext.css"
# app_include_js = "/assets/excelus_erpnext/js/excelus_erpnext.js"

# include js, css files in header of web template
# web_include_css = "/assets/excelus_erpnext/css/excelus_erpnext.css"
# web_include_js = "/assets/excelus_erpnext/js/excelus_erpnext.js"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "excelus_erpnext.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "excelus_erpnext.install.before_install"
# after_install = "excelus_erpnext.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "excelus_erpnext.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"excelus_erpnext.tasks.all"
# 	],
# 	"daily": [
# 		"excelus_erpnext.tasks.daily"
# 	],
# 	"hourly": [
# 		"excelus_erpnext.tasks.hourly"
# 	],
# 	"weekly": [
# 		"excelus_erpnext.tasks.weekly"
# 	]
# 	"monthly": [
# 		"excelus_erpnext.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "excelus_erpnext.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "excelus_erpnext.event.get_events"
# }

fixtures = [{"dt": "Custom Field", "filters":[["name", "in", ['Item-excelus_pack_weight', 'Item-excelus_packs_per_carton','Item-excelus_pack_length','Item-excelus_pack_width','Item-excelus_film_wastage','Item-excelus_film_thickness','Item-excelus_carton_width','Item-excelus_tape_required_per_carton','Item-excelus_sticker_cost_per_no'
												 ]]]},
             {"dt": "Custom Script", "filters":[["name", "in", ['Item-client']]]}]