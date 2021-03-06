from django.conf.urls import url

from bradmin.views.admin_error_log_view import AdminErrorLogView, AdminErrorLogsDetailsView
from bradmin.views.author.author_views import AdminAuthorListView, AdminAuthorCreateView, AdminBAuthorDetailsView, \
    AdminAuthorUpdateView, AdminAuthorUploadView, AdminAuthorDownloadView, AdminAuthorActivateView, \
    AdminAuthorDeactivateView, AdminAuthorDeleteView
from bradmin.views.book.book_views import AdminBooksListView, AdminBookUploadView, AdminBookDownloadView, \
    AdminBookActivateView, AdminBookDeactivateView, AdminBookDeleteView, AdminBookCreateView, AdminBookDetailsView
from bradmin.views.category.category_views import AdminCategoryUploadView, AdminCategoryListView, \
    AdminCategoryDownloadView, AdminCategoryActivateView, AdminCategoryDeactivateView, AdminCategoryDeleteView, \
    AdminCategoryDetailsView, AdminCategoryCreateView, AdminCategoryUpdateView
from bradmin.views.frontlist.front_palette_views import AdminFrontPaletteListView, AdminFrontPaletteCreateView, \
    AdminFrontPaletteUpdateView, AdminFrontPaletteActivateView, \
    AdminFrontPaletteDeactivateView, AdminFrontPaletteDeleteView, AdminFrontPaletteDetailsView
from bradmin.views.frontlist.frontlist_views import AdminFrontListListView, AdminFrontListCreateView, \
    AdminFrontListUpdateView, AdminFrontListActivateView, AdminFrontListDeactivateView, AdminFrontListDeleteView, \
    AdminFrontListDetailsView
from bradmin.views.inventory.inventory_views import AdminInventoryListView, AdminInventoryCreateView, \
    AdminInventoryUpdateView, AdminInventoryDetailsView, AdminInventoryActivateView, AdminInventoryDeactivateView, \
    AdminInventoryDeleteView, AdminInventoryUploadView, AdminInventoryDownloadView, AdminInventoryAlertListView
from bradmin.views.location.country_views import AdminCountryListView, AdminCountryCreateView, AdminCountryUpdateView, \
    AdminCountryActivateView, AdminCountryDeactivateView, AdminCountryDeleteView
from bradmin.views.productprices.currency_views import AdminCurrencyListView, AdminCurrencyCreateView, \
    AdminCurrencyUpdateView, AdminCurrencyActivateView, AdminCurrencyDeactivateView, AdminCurrencyDeleteView
from bradmin.views.productprices.product_price_views import AdminProductPriceListView, AdminProductPriceCreateView, \
    AdminProductPriceUpdateView, AdminProductPriceUploadView, AdminProductPriceDownloadView, \
    AdminProductPriceActivateView, AdminProductPriceDeactivateView, AdminProductPriceDeleteView
from bradmin.views.productprices.rent_plan_views import AdminRentPlanListView, AdminRentPlanCreateView, \
    AdminRentPlanUpdateView, AdminRentPlanActivateView, AdminRentPlanDeactivateView, AdminRentPlanDeleteView
from bradmin.views.promotion.promotion_views import AdminPromotionListView, AdminPromotionCreateView
from bradmin.views.publisher.publisher_views import AdminPublisherListView, AdminBookPublisherUploadView, \
    AdminBookPublisherDownloadView, AdminBookPublisherActivateView, AdminBookPublisherDeactivateView, \
    AdminBookPublisherDeleteView, AdminBookPublisherDetailsView, AdminBookPublisherCreateView, \
    AdminBookPublisherUpdateView
from bradmin.views.views import AdminHomeView, AdminLoginView, AdminLogoutView
from bradmin.views.warehouse.warehouse_views import AdminWarehouseListView, AdminWarehouseCreateView, \
    AdminWarehouseUpdateView, AdminWarehouseUploadView, AdminWarehouseDownloadView, AdminWarehouseActivateView, \
    AdminWarehouseDeactivateView, AdminWarehouseDeleteView, AdminWarehouseDetailsView

urlpatterns = [
    url(r'^$', AdminHomeView.as_view(), name='admin_home_view'),
    url(r'^login/', AdminLoginView.as_view(), name="admin_login_view"),
    url(r'^logout/', AdminLogoutView.as_view(), name="admin_logout_view"),
    #Category
    url(r'^category/', AdminCategoryListView.as_view(), name="admin_category_view"),
    url(r'^category-upload/', AdminCategoryUploadView.as_view(), name="admin_category_upload_view"),
    url(r'^category-download/', AdminCategoryDownloadView.as_view(), name="admin_category_download_view"),
    url(r'^category-activate/', AdminCategoryActivateView.as_view(), name="admin_category_activate_view"),
    url(r'^category-deactivate/', AdminCategoryDeactivateView.as_view(), name="admin_category_deactivate_view"),
    url(r'^category-delete/', AdminCategoryDeleteView.as_view(), name="admin_category_delete_view"),
    url(r'^category-details/(?P<pk>[0-9]+)/$', AdminCategoryDetailsView.as_view(), name="admin_category_details_view"),
    url(r'^category-create/$', AdminCategoryCreateView.as_view(), name="admin_category_create_view"),
    url(r'^category-edit/(?P<pk>[0-9]+)/$', AdminCategoryUpdateView.as_view(), name="admin_category_edit_link_view"),
    #Publisher
    url(r'^publishers/', AdminPublisherListView.as_view(), name="admin_publishers_view"),
    url(r'^publishers-upload/', AdminBookPublisherUploadView.as_view(), name="admin_book_publisher_upload_view"),
    url(r'^publishers-download/', AdminBookPublisherDownloadView.as_view(), name="admin_book_publisher_download_view"),
    url(r'^publishers-activate/', AdminBookPublisherActivateView.as_view(), name="admin_book_publisher_activate_view"),
    url(r'^publishers-deactivate/', AdminBookPublisherDeactivateView.as_view(), name="admin_book_publisher_deactivate_view"),
    url(r'^publishers-delete/', AdminBookPublisherDeleteView.as_view(), name="admin_book_publisher_delete_view"),
    url(r'^publishers-details/(?P<pk>[0-9]+)/$', AdminBookPublisherDetailsView.as_view(), name="admin_book_publisher_details_view"),
    url(r'^publishers-create/$', AdminBookPublisherCreateView.as_view(), name="admin_book_publisher_create_view"),
    url(r'^publishers-edit/(?P<pk>[0-9]+)/$', AdminBookPublisherUpdateView.as_view(), name="admin_book_publisher_edit_link_view"),
    #Author
    url(r'^authors/', AdminAuthorListView.as_view(), name="admin_author_list_view"),
    url(r'^author-upload/', AdminAuthorUploadView.as_view(), name="admin_author_upload_view"),
    url(r'^author-download/', AdminAuthorDownloadView.as_view(), name="admin_author_download_view"),
    url(r'^author-activate/', AdminAuthorActivateView.as_view(), name="admin_author_activate_view"),
    url(r'^author-deactivate/', AdminAuthorDeactivateView.as_view(), name="admin_author_deactivate_view"),
    url(r'^author-delete/', AdminAuthorDeleteView.as_view(), name="admin_author_delete_view"),
    url(r'^author-details/(?P<pk>[0-9]+)/$', AdminBAuthorDetailsView.as_view(), name="admin_author_details_view"),
    url(r'^author-create/$', AdminAuthorCreateView.as_view(), name="admin_author_create_view"),
    url(r'^author-edit/(?P<pk>[0-9]+)/$', AdminAuthorUpdateView.as_view(), name="admin_author_edit_link_view"),
    #Books
    url(r'^books/', AdminBooksListView.as_view(), name="admin_book_list_view"),
    url(r'^books-upload/', AdminBookUploadView.as_view(), name="admin_book_upload_view"),
    url(r'^books-download/', AdminBookDownloadView.as_view(), name="admin_book_download_view"),
    url(r'^books-activate/', AdminBookActivateView.as_view(), name="admin_book_activate_view"),
    url(r'^books-deactivate/', AdminBookDeactivateView.as_view(),name="admin_book_deactivate_view"),
    url(r'^books-delete/', AdminBookDeleteView.as_view(), name="admin_book_delete_view"),
    url(r'^book-details/(?P<pk>[0-9]+)/$', AdminBookDetailsView.as_view(), name="admin_book_details_view"),
    url(r'^books-create/$', AdminBookCreateView.as_view(), name="admin_book_create_view"),
    #Warehouse
    url(r'^warehouse/', AdminWarehouseListView.as_view(), name="admin_warehouse_list_view"),
    url(r'^warehouse-details/(?P<pk>[0-9]+)/$', AdminWarehouseDetailsView.as_view(), name="admin_warehouse_details_view"),
    url(r'^warehouse-upload/', AdminWarehouseUploadView.as_view(), name="admin_warehouse_upload_view"),
    url(r'^warehouse-download/', AdminWarehouseDownloadView.as_view(), name="admin_warehouse_download_view"),
    url(r'^warehouse-activate/', AdminWarehouseActivateView.as_view(), name="admin_warehouse_activate_view"),
    url(r'^warehouse-deactivate/', AdminWarehouseDeactivateView.as_view(),name="admin_warehouse_deactivate_view"),
    url(r'^warehouse-delete/', AdminWarehouseDeleteView.as_view(), name="admin_warehouse_delete_view"),
    url(r'^warehouse-create/$', AdminWarehouseCreateView.as_view(), name="admin_warehouse_create_view"),
    url(r'^warehouse-edit/(?P<pk>[0-9]+)/$', AdminWarehouseUpdateView.as_view(), name="admin_warehouse_edit_link_view"),
    #Inventory
    url(r'^inventory/$', AdminInventoryListView.as_view(), name="admin_inventory_list_view"),
    url(r'^inventory-alerts/$', AdminInventoryAlertListView.as_view(), name="admin_inventory_alert_list_view"),
    url(r'^inventory-details/(?P<pk>[0-9]+)/$', AdminInventoryDetailsView.as_view(), name="admin_inventory_details_view"),
    url(r'^inventory-upload/', AdminInventoryUploadView.as_view(), name="admin_inventory_upload_view"),
    url(r'^inventory-download/', AdminInventoryDownloadView.as_view(), name="admin_inventory_download_view"),
    url(r'^inventory-activate/', AdminInventoryActivateView.as_view(), name="admin_inventory_activate_view"),
    url(r'^inventory-deactivate/', AdminInventoryDeactivateView.as_view(),name="admin_inventory_deactivate_view"),
    url(r'^inventory-delete/', AdminInventoryDeleteView.as_view(), name="admin_inventory_delete_view"),
    url(r'^inventory-create/$', AdminInventoryCreateView.as_view(), name="admin_inventory_create_view"),
    url(r'^inventory-edit/(?P<pk>[0-9]+)/$', AdminInventoryUpdateView.as_view(), name="admin_inventory_edit_link_view"),
    #Promotion
    url(r'^promotions/$', AdminPromotionListView.as_view(), name="admin_promotion_list_view"),
    url(r'^promotion-create/$', AdminPromotionCreateView.as_view(), name="admin_promotion_create_view"),
    #Frontlist
    url(r'^front-list/$', AdminFrontListListView.as_view(), name="admin_frontlist_list_view"),
    url(r'^front-list-details/(?P<pk>[0-9]+)/$', AdminFrontListDetailsView.as_view(), name="admin_front_list_details_view"),
    url(r'^front-list-activate/', AdminFrontListActivateView.as_view(), name="admin_front_list_activate_view"),
    url(r'^front-list-deactivate/', AdminFrontListDeactivateView.as_view(),name="admin_front_list_deactivate_view"),
    url(r'^front-list-delete/', AdminFrontListDeleteView.as_view(), name="admin_front_list_delete_view"),
    url(r'^front-list-create/$', AdminFrontListCreateView.as_view(), name="admin_front_list_create_view"),
    url(r'^front-list-edit/(?P<pk>[0-9]+)/$', AdminFrontListUpdateView.as_view(), name="admin_front_list_edit_link_view"),
    url(r'^front-palette/$', AdminFrontPaletteListView.as_view(), name="admin_front_palette_list_view"),
    url(r'^front-palette-details/(?P<pk>[0-9]+)/$', AdminFrontPaletteDetailsView.as_view(), name="admin_front_palette_details_view"),
    url(r'^front-palette-activate/', AdminFrontPaletteActivateView.as_view(), name="admin_front_palette_activate_view"),
    url(r'^front-palette-deactivate/', AdminFrontPaletteDeactivateView.as_view(),name="admin_front_palette_deactivate_view"),
    url(r'^front-palette-delete/', AdminFrontPaletteDeleteView.as_view(), name="admin_front_palette_delete_view"),
    url(r'^front-palette-create/$', AdminFrontPaletteCreateView.as_view(), name="admin_front_palette_create_view"),
    url(r'^front-palette-edit/(?P<pk>[0-9]+)/$', AdminFrontPaletteUpdateView.as_view(), name="admin_front_palette_edit_link_view"),
    #Product Price
    url(r'^product-price-list/$', AdminProductPriceListView.as_view(), name="admin_product_price_list_view"),
    url(r'^product-price-upload/', AdminProductPriceUploadView.as_view(), name="admin_product_price_upload_view"),
    url(r'^product-price-download/', AdminProductPriceDownloadView.as_view(), name="admin_product_price_download_view"),
    url(r'^product-price-activate/', AdminProductPriceActivateView.as_view(), name="admin_product_price_activate_view"),
    url(r'^product-price-deactivate/', AdminProductPriceDeactivateView.as_view(),name="admin_product_price_deactivate_view"),
    url(r'^product-price-delete/', AdminProductPriceDeleteView.as_view(), name="admin_product_price_delete_view"),
    url(r'^product-price-create/$', AdminProductPriceCreateView.as_view(), name="admin_product_price_create_view"),
    url(r'^product-price-edit/(?P<pk>[0-9]+)/$', AdminProductPriceUpdateView.as_view(), name="admin_product_price_edit_link_view"),
    #Rent Plan
    url(r'^rent-plan-list/$', AdminRentPlanListView.as_view(), name="admin_rent_plan_list_view"),
    url(r'^rent-plan-create/$', AdminRentPlanCreateView.as_view(), name="admin_rent_plan_create_view"),
    url(r'^rent-plan-edit/(?P<pk>[0-9]+)/$', AdminRentPlanUpdateView.as_view(), name="admin_rent_plan_edit_link_view"),
    url(r'^rent-plan-activate/', AdminRentPlanActivateView.as_view(), name="admin_rent_plan_activate_view"),
    url(r'^rent-plan-deactivate/', AdminRentPlanDeactivateView.as_view(),name="admin_rent_plan_deactivate_view"),
    url(r'^rent-plan-delete/', AdminRentPlanDeleteView.as_view(), name="admin_rent_plan_delete_view"),
    #Currency
    url(r'^currency-list/$', AdminCurrencyListView.as_view(), name="admin_currency_list_view"),
    url(r'^currency-create/$', AdminCurrencyCreateView.as_view(), name="admin_currency_create_view"),
    url(r'^currency-edit/(?P<pk>[0-9]+)/$', AdminCurrencyUpdateView.as_view(), name="admin_currency_edit_link_view"),
    url(r'^currency-activate/', AdminCurrencyActivateView.as_view(), name="admin_currency_activate_view"),
    url(r'^currency-deactivate/', AdminCurrencyDeactivateView.as_view(),name="admin_currency_deactivate_view"),
    url(r'^currency-delete/', AdminCurrencyDeleteView.as_view(), name="admin_currency_delete_view"),
    #Country
    url(r'^country-list/$', AdminCountryListView.as_view(), name="admin_country_list_view"),
    url(r'^country-create/$', AdminCountryCreateView.as_view(), name="admin_country_create_view"),
    url(r'^country-edit/(?P<pk>[0-9]+)/$', AdminCountryUpdateView.as_view(), name="admin_country_edit_link_view"),
    url(r'^country-activate/', AdminCountryActivateView.as_view(), name="admin_country_activate_view"),
    url(r'^country-deactivate/', AdminCountryDeactivateView.as_view(),name="admin_country_deactivate_view"),
    url(r'^country-delete/', AdminCountryDeleteView.as_view(), name="admin_country_delete_view"),

    url(r'^error-logs/', AdminErrorLogView.as_view(), name="admin_error_logs_view"),
    url(r'^error-log/details/(?P<pk>[0-9]+)/$', AdminErrorLogsDetailsView.as_view(), name="admin_error_log_details_view"),
]
