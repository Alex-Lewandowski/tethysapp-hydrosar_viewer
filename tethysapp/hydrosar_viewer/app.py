from tethys_sdk.base import TethysAppBase, url_map_maker


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
        )

        return url_maps


