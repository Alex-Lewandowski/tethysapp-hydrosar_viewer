from django.shortcuts import render
from tethys_sdk.permissions import login_required
from tethys_sdk.gizmos import SelectInput, RangeSlider
from .utilities import new_id
from .app import HydrosarViewer as App

@login_required()
def home(request):
    """
    Controller for the app home page.
    """
    events = SelectInput(
        display_text='Select HydroSAR Event',
        name='events',
        multiple=False,
        original=True,
        options=(('2020 Bangladesh Flood', '2020_Bangladesh'),
                 ('2019 US Midwest Flood', '2019_Midwest'),
                 ('2017 Bangladesh Flood', '2017_Bangladesh'),),
    )

    variables = SelectInput(
        display_text='Select HydroSAR Product',
        name='variables',
        multiple=False,
        original=True,
        options=(('Surface Water Extent', 'S1_SWE'),
                 ('Flood Depth Proxy', 'S1_HAND_FD'),
                 ('Agriculture Extent', 'S1_AG')),
    )

    opacity = RangeSlider(
        display_text='HydroSAR Layer Opacity',
        name='opacity',
        min=0,
        max=1,
        step=.05,
        initial=1,
    )

    context = {
        'events': events,
        'variables': variables,
        'opacity': opacity,
        'instance_id': new_id(),
        'thredds_url': App.get_custom_setting('thredds_url'),
    }

    return render(request, 'hydrosar_viewer/home.html', context)