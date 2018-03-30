__author__ = "auto generated"

from bradmin.views.author.author_views import AdminAuthorListView, AdminAuthorUploadView, AdminAuthorDownloadView, AdminAuthorActivateView, AdminAuthorDeactivateView, AdminAuthorDeleteView, AdminBAuthorDetailsView, AdminAuthorCreateView, AdminAuthorUpdateView
from bradmin.views.book.book_views import AdminBooksListView, AdminBookUploadView, AdminBookDownloadView, AdminBookActivateView, AdminBookDeactivateView, AdminBookDeleteView, AdminBookDetailsView, AdminBookCreateView
from bradmin.views.category.category_views import AdminCategoryView, AdminCategoryListView, AdminCategoryUploadView, AdminCategoryDownloadView, AdminCategoryActivateView, AdminCategoryDeactivateView, AdminCategoryDeleteView, AdminCategoryDetailsView, AdminCategoryCreateView, AdminCategoryUpdateView
from bradmin.views.frontlist.frontlist_views import AdminFrontListListView, AdminFrontListDetailsView, AdminFrontListActivateView, AdminFrontListDeactivateView, AdminFrontListDeleteView, AdminFrontListCreateView, AdminFrontListUpdateView
from bradmin.views.frontlist.front_palette_views import AdminFrontPaletteListView, AdminFrontPaletteDetailsView, AdminFrontPaletteActivateView, AdminFrontPaletteDeactivateView, AdminFrontPaletteDeleteView, AdminFrontPaletteCreateView, AdminFrontPaletteUpdateView
from bradmin.views.inventory.inventory_views import AdminInventoryListView, AdminInventoryAlertListView, AdminInventoryUploadView, AdminInventoryDownloadView, AdminInventoryActivateView, AdminInventoryDeactivateView, AdminInventoryDeleteView, AdminInventoryDetailsView, AdminInventoryCreateView, AdminInventoryUpdateView
from bradmin.views.location.country_views import AdminCountryListView, AdminCountryActivateView, AdminCountryDeactivateView, AdminCountryDeleteView, AdminCountryCreateView, AdminCountryUpdateView
from bradmin.views.productprices.currency_views import AdminCurrencyListView, AdminCurrencyActivateView, AdminCurrencyDeactivateView, AdminCurrencyDeleteView, AdminCurrencyCreateView, AdminCurrencyUpdateView
from bradmin.views.productprices.product_price_views import AdminProductPriceListView, AdminProductPriceUploadView, AdminProductPriceDownloadView, AdminProductPriceActivateView, AdminProductPriceDeactivateView, AdminProductPriceDeleteView, AdminProductPriceCreateView, AdminProductPriceUpdateView
from bradmin.views.productprices.rent_plan_views import AdminRentPlanListView, AdminRentPlanActivateView, AdminRentPlanDeactivateView, AdminRentPlanDeleteView, AdminRentPlanCreateView, AdminRentPlanUpdateView
from bradmin.views.promotion.promotion_views import AdminPromotionListView, AdminPromotionCreateView, AdminPromotionUpdateView
from bradmin.views.publisher.publisher_views import AdminPublisherListView, AdminBookPublisherUploadView, AdminBookPublisherDownloadView, AdminBookPublisherActivateView, AdminBookPublisherDeactivateView, AdminBookPublisherDeleteView, AdminBookPublisherDetailsView, AdminBookPublisherCreateView, AdminBookPublisherUpdateView
from bradmin.views.warehouse.warehouse_views import AdminWarehouseListView, AdminWarehouseUploadView, AdminWarehouseDownloadView, AdminWarehouseActivateView, AdminWarehouseDeactivateView, AdminWarehouseDeleteView, AdminWarehouseDetailsView, AdminWarehouseCreateView, AdminWarehouseUpdateView
from bradmin.views.activate_base_view import ActivateBaseView
from bradmin.views.admin_base_template_view import AdminBaseTemplateView
from bradmin.views.admin_error_log_view import AdminErrorLogView, AdminErrorLogsDetailsView
from bradmin.views.admin_logs_view import AdminLogView
from bradmin.views.base_approve_view import BaseApproveView
from bradmin.views.base_create_view import BRBaseCreateView
from bradmin.views.base_detail_view import BaseDetailView
from bradmin.views.base_form_view import BaseFormView
from bradmin.views.base_reject_view import BaseRejectView
from bradmin.views.base_update_view import BRBaseUpdateView
from bradmin.views.books_views import AdminBooksView, AdminBooksUploadView
from bradmin.views.deactivate_base_view import DeactivateBaseView
from bradmin.views.delete_base_view import DeleteBaseView
from bradmin.views.download_base_view import DownloadBaseView
from bradmin.views.upload_base_view import UploadBaseView
from bradmin.views.views import AdminLoginView, AdminHomeView, AdminLogoutView


__all__ = ['AdminAuthorListView']
__all__ = ['AdminAuthorUploadView']
__all__ = ['AdminAuthorDownloadView']
__all__ = ['AdminAuthorActivateView']
__all__ = ['AdminAuthorDeactivateView']
__all__ = ['AdminAuthorDeleteView']
__all__ = ['AdminBAuthorDetailsView']
__all__ = ['AdminAuthorCreateView']
__all__ = ['AdminAuthorUpdateView']
__all__ += ['AdminBooksListView']
__all__ += ['AdminBookUploadView']
__all__ += ['AdminBookDownloadView']
__all__ += ['AdminBookActivateView']
__all__ += ['AdminBookDeactivateView']
__all__ += ['AdminBookDeleteView']
__all__ += ['AdminBookDetailsView']
__all__ += ['AdminBookCreateView']
__all__ += ['AdminCategoryView']
__all__ += ['AdminCategoryListView']
__all__ += ['AdminCategoryUploadView']
__all__ += ['AdminCategoryDownloadView']
__all__ += ['AdminCategoryActivateView']
__all__ += ['AdminCategoryDeactivateView']
__all__ += ['AdminCategoryDeleteView']
__all__ += ['AdminCategoryDetailsView']
__all__ += ['AdminCategoryCreateView']
__all__ += ['AdminCategoryUpdateView']
__all__ += ['AdminFrontListListView']
__all__ += ['AdminFrontListDetailsView']
__all__ += ['AdminFrontListActivateView']
__all__ += ['AdminFrontListDeactivateView']
__all__ += ['AdminFrontListDeleteView']
__all__ += ['AdminFrontListCreateView']
__all__ += ['AdminFrontListUpdateView']
__all__ += ['AdminFrontPaletteListView']
__all__ += ['AdminFrontPaletteDetailsView']
__all__ += ['AdminFrontPaletteActivateView']
__all__ += ['AdminFrontPaletteDeactivateView']
__all__ += ['AdminFrontPaletteDeleteView']
__all__ += ['AdminFrontPaletteCreateView']
__all__ += ['AdminFrontPaletteUpdateView']
__all__ += ['AdminInventoryListView']
__all__ += ['AdminInventoryAlertListView']
__all__ += ['AdminInventoryUploadView']
__all__ += ['AdminInventoryDownloadView']
__all__ += ['AdminInventoryActivateView']
__all__ += ['AdminInventoryDeactivateView']
__all__ += ['AdminInventoryDeleteView']
__all__ += ['AdminInventoryDetailsView']
__all__ += ['AdminInventoryCreateView']
__all__ += ['AdminInventoryUpdateView']
__all__ += ['AdminCountryListView']
__all__ += ['AdminCountryActivateView']
__all__ += ['AdminCountryDeactivateView']
__all__ += ['AdminCountryDeleteView']
__all__ += ['AdminCountryCreateView']
__all__ += ['AdminCountryUpdateView']
__all__ += ['AdminCurrencyListView']
__all__ += ['AdminCurrencyActivateView']
__all__ += ['AdminCurrencyDeactivateView']
__all__ += ['AdminCurrencyDeleteView']
__all__ += ['AdminCurrencyCreateView']
__all__ += ['AdminCurrencyUpdateView']
__all__ += ['AdminProductPriceListView']
__all__ += ['AdminProductPriceUploadView']
__all__ += ['AdminProductPriceDownloadView']
__all__ += ['AdminProductPriceActivateView']
__all__ += ['AdminProductPriceDeactivateView']
__all__ += ['AdminProductPriceDeleteView']
__all__ += ['AdminProductPriceCreateView']
__all__ += ['AdminProductPriceUpdateView']
__all__ += ['AdminRentPlanListView']
__all__ += ['AdminRentPlanActivateView']
__all__ += ['AdminRentPlanDeactivateView']
__all__ += ['AdminRentPlanDeleteView']
__all__ += ['AdminRentPlanCreateView']
__all__ += ['AdminRentPlanUpdateView']
__all__ += ['AdminPromotionListView']
__all__ += ['AdminPromotionCreateView']
__all__ += ['AdminPromotionUpdateView']
__all__ += ['AdminPublisherListView']
__all__ += ['AdminBookPublisherUploadView']
__all__ += ['AdminBookPublisherDownloadView']
__all__ += ['AdminBookPublisherActivateView']
__all__ += ['AdminBookPublisherDeactivateView']
__all__ += ['AdminBookPublisherDeleteView']
__all__ += ['AdminBookPublisherDetailsView']
__all__ += ['AdminBookPublisherCreateView']
__all__ += ['AdminBookPublisherUpdateView']
__all__ += ['AdminWarehouseListView']
__all__ += ['AdminWarehouseUploadView']
__all__ += ['AdminWarehouseDownloadView']
__all__ += ['AdminWarehouseActivateView']
__all__ += ['AdminWarehouseDeactivateView']
__all__ += ['AdminWarehouseDeleteView']
__all__ += ['AdminWarehouseDetailsView']
__all__ += ['AdminWarehouseCreateView']
__all__ += ['AdminWarehouseUpdateView']
__all__ += ['ActivateBaseView']
__all__ += ['AdminBaseTemplateView']
__all__ += ['AdminErrorLogView']
__all__ += ['AdminErrorLogsDetailsView']
__all__ += ['AdminLogView']
__all__ += ['BaseApproveView']
__all__ += ['BRBaseCreateView']
__all__ += ['BaseDetailView']
__all__ += ['BaseFormView']
__all__ += ['BaseRejectView']
__all__ += ['BRBaseUpdateView']
__all__ += ['AdminBooksView']
__all__ += ['AdminBooksUploadView']
__all__ += ['DeactivateBaseView']
__all__ += ['DeleteBaseView']
__all__ += ['DownloadBaseView']
__all__ += ['UploadBaseView']
__all__ += ['AdminLoginView']
__all__ += ['AdminHomeView']
__all__ += ['AdminLogoutView']
