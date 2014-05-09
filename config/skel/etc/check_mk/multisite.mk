# Confguration for Check_MK Multisite

# Users with unrestricted permissions
# admin
admin_users = [ "omdadmin", "admin_a", "admin_b" ]
admin_users_pass = [ "omd", "admin_a@123", "admin_b@123"]
# end-admin

# Users seeing all data but cannot do any action
# guest
guest_users = [ "viewer_a","viewer_b","viewer_c","viewer_d" ]
guest_users_pass = [ "viewer_a@123","viewer_b@123","viewer_c@123","viewer_d@123" ]
# end-guest


# A lists of all normal operational users allowed to use
# Multisite. If this variable is not set, then everybody with a correct
# HTTP login may use Multisite and gets the role "user"
# user
users = [ "operator_a","operator_b","operator_c","operator_d" ]
users_pass = [ "operator_a@123","operator_b@123","operator_c@123","operator_d@123" ]
# end-user

# Users not explicitely being listed in admin_users or guest_users
# get the role "user" if they have a valid login. You can change this
# to "guest", "admin" or None by setting the following variable:
# default_user_role = "guest"

# Sites to connect to. If this variable is unset, a single
# connection to the local host is done.
# sites = {
#    # connect to local Nagios
#    "local" : {
#         "alias" : "Munich"
#    },
# 
#    # connect to remote site
#    "paris": {
#         "alias":          "Paris",
#         "socket":         "tcp:10.0.0.2:6557",
#         "nagios_url":     "/paris/nagios",
#         "nagios_cgi_url": "/paris/nagios/cgi-bin",
#         "pnp_url":        "/paris/pnp4nagios/",
#     },
# }

# 
# NagVis
#
# The NagVis-Snapin needs to know the URL to nagvis.
# This is not always /nagvis/ - especially not for OMD
nagvis_base_url = "/###SITE###/nagvis"


# Restrict number of datasets queries via Livestatus.
# This prevents you from consuming too much ressources
# in case of insensible queries.
# soft_query_limit = 1000
# hard_query_limit = 5000

# Views allow to play alarm sounds according to the
# "worst" state of the show items. Configure here
# which sounds to play. Possible events: critical,
# warning, unknown, ok, up, down, unreachable,
# pending. Sounds are expected in the sounds subdirectory
# of htdocs (Default is /usr/share/check_mk/web/htdocs/sounds)
# sounds = [
#  ( "down", "down.wav" ),
#  ( "critical", "critical.wav" ),
#  ( "unknown", "unknown.wav" ),
#  ( "warning", "warning.wav" ),
#  ( None,      "ok", ), 
# ]
# Note: this example has not sound for unreachable hosts. 
# set sound_url to another url, if you place your sound
# files elsewhere:
# sound_url = "http://otherhost/path/to/sound/"
# or
# sound_url = "/nagios/alarms/"

# Tabs for choosing number of columns refresh
# view_option_refreshes = [ 30, 60, 90, 0 ]
# view_option_columns   = [ 1, 2, 3, 4, 5, 6, 8 ]

# Custom links for "Custom Links" Snapin. Feel free to add your
# own links here. The boolean values True and False determine
# wether the sections are open or closed by default.

# Links for everyone
custom_links['guest'] = [
  ( "Classical Nagios GUI", "../nagios/", "link_home.gif" ),
  ( "Addons", True, [
        ( "PNP4Nagios", "../pnp4nagios/",       "link_reporting.gif" ),
        ( "NagVis", False, [
            ( "Automap",    "../nagvis/index.php?map=__automap", "link_map.gif"),
            ( "Demo map",   "../nagvis/index.php?map=demo-map",  "link_map.gif"),
            ( "Demo Map 2", "../nagvis/index.php?map=demo2",     "link_map.gif"),
        ]),
  ]),
]

# The members of the role 'user' get the same links as the guests
# but some in addition
custom_links['user'] = custom_links['guest'] + [
  ( "Open Source Components", False, [
        ( "Multisite",     "http://mathias-kettner.de/checkmk_multisite.html" ),
        ( "MK Livestatus", "http://mathias-kettner.de/checkmk_livestatus.html" ),
        ( "Check_MK",      "http://mathias-kettner.de/check_mk.html" ),
        ( "Nagios",        "http://www.nagios.org/" ), 
        ( "PNP4Nagios",    "http://pnp4nagios.org/" ),
        ( "NagVis",        "http://nagvis.org/" ),
        ( "RRDTool",       "http://oss.oetiker.ch/rrdtool/" ),
   ])
]

# The admins yet get further links
custom_links['admin'] = custom_links['user'] + [
  ( "Support", False, [
      ( "Mathias Kettner",              "http://mathias-kettner.de/" ),
      ( "Check_MK Mailinglists",        "http://mathias-kettner.de/check_mk_lists.html" ),
      ( "Check_MK Portal (inofficial)", "http://check-mk-portal.org/"),
      ( "Nagios Portal (German)",       "http://nagios-portal.org"),
  ])
]

# Show error messages from unreachable sites in views. Set this
# to False in order to hide those messages.
show_livestatus_errors = True

# Hide certain views from the sidebar
# hidden_views = [ "hosttiles", "allhosts_mini" ]
# Vice versa: hide all views except these (be carefull, this

# will also exclude custom views)
# visible_views = [ "allhosts", "searchsvc" ]

# Load custom style sheet which can override styles defined in check_mk.css
# Put your style sheet into web/htdocs/
# custom_style_sheet = "my_styles.css"

# URL to show as welcome page (in the 'main' frame).
# You can use relative URL or absolute URLs like 'http://server/url'
# Default is 'main.py'
# start_url = 'view.py?view_name=hostgroups'


# Quicksearch: Limit the number of hits to shop in dropdown.
# Default is to show at most 80 items.
# quicksearch_dropdown_limit = 80
