from tethys_sdk.base import TethysAppBase, url_map_maker


class StorageCapacity(TethysAppBase):
    """
    Tethys app class for Storage Capacity.
    """

    name = 'FDC and Storage Capacity'
    index = 'storage_capacity:home'
    icon = 'storage_capacity/images/app-logo2.png'
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
                    UrlMap(name='resultspage',
                        url='resultspage',
                        controller='storage_capacity.controllers.resultspage'),
        )

        return url_maps

    def persistent_stores(self):
        """
        Add one or more pesistent stores
        """

        stores=(PersistentStore(name='fdc_db',
                                initializer='storage_capacity.init_stores.init_fdc_db',
                                ),
        )
        return stores
