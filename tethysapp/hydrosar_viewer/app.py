from tethys_sdk.base import TethysAppBase, url_map_maker
from tethys_sdk.app_settings import CustomSetting

class HydrosarViewer(TethysAppBase):
    """
    Tethys app class for Hydrosar Viewer.
    """

    name = 'HydroSAR Viewer'
    index = 'hydrosar_viewer:home'
    icon = 'hydrosar_viewer/images/floodlogo.JPG'
    package = 'hydrosar_viewer'
    root_url = 'hydrosar-viewer'
    color = '#1F618D'
    description = 'HydroSAR Viewer'
    tags = ''
    enable_feedback = False
    feedback_emails = []

    def url_maps(self):
        """
        Add controllers
        """
        UrlMap = url_map_maker(self.root_url)

        url_maps = (
            UrlMap(
                name='home',
                url='hydrosar-viewer',
                controller='hydrosar_viewer.controllers.home'
            ),
            UrlMap(
                name='uploadShapefile',
                url='hydrosar-viewer/ajax/uploadShapefile',
                controller='hydrosar_viewer.ajax.uploadshapefile',
            ),
            UrlMap(
                name='uploadGeoJSON',
                url='hydrosar-viewer/ajax/uploadGeoJSON',
                controller='hydrosar_viewer.ajax.uploadgeojson',
            ),
            UrlMap(
                name='requestTimeSeries',
                url='hydrosar-viewer/ajax/requestTimeSeries',
                controller='hydrosar_viewer.ajax.requestTimeSeries',
            ),
        )

        return url_maps


    def custom_settings(self):
        return (
            CustomSetting(
                name='thredds_path',
                type=CustomSetting.TYPE_STRING,
                description="Local file path to datasets (same as used by Thredds) (e.g. /data/thredds/)",
                required=True,
            ),
            CustomSetting(
                name='thredds_url',
                type=CustomSetting.TYPE_STRING,
                description="URL to the GLDAS folder served by THREDDS with trailing / (e.g. http://127.0.0.1:7000/thredds/)",
                required=True,
            )
        )


