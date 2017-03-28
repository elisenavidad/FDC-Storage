from tethys_sdk.base import TethysAppBase, url_map_maker


class StorageCapacity(TethysAppBase):
    """
    Tethys app class for Storage Capacity.
    """

    name = 'FDC and Storage Capacity'
    index = 'storage_capacity:home'
    icon = 'storage_capacity/images/dam_icon.svg'
    package = 'storage_capacity'
    root_url = 'storage-capacity'
    color = 'blue'
    description = 'Calculate potential reservoir storage capacity and a flow duration curve at specific location in the DR given a dam height and curve number.'
    tags = 'StorageCapacity'
    enable_feedback = False
    feedback_emails = []

        
    def url_maps(self):
        """
        Add controllers
        """
        UrlMap = url_map_maker(self.root_url)

        url_maps = (UrlMap(name='home',
                           url='storage-capacity',
                           controller='storage_capacity.controllers.home'),
                    UrlMap(name='results',
                        url='results',
                        controller='storage_capacity.controllers.results'),
        )

        return url_maps