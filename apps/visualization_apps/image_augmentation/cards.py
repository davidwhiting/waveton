import sys
import traceback

from h2o_wave import Q, expando_to_dict, ui

# App name
app_name = 'Image Augmentation'

# Link to repo. Report bugs/features here :)
repo_url = 'https://github.com/vopani/waveton'
issue_url = f'{repo_url}/issues/new?assignees=vopani&labels=bug&template=error-report.md&title=%5BERROR%5D'

# A meta card to hold the app's title, layouts, dialogs, theme and other meta information
meta = ui.meta_card(
    box='',
    title='WaveTon',
    layouts=[
        ui.layout(
            breakpoint='xs',
            zones=[
                ui.zone(name='header'),
                ui.zone(
                    name='main',
                    size='calc(100vh - 130px)',
                    direction='row',
                    zones=[
                        ui.zone(name='augmentations', size='25%'),
                        ui.zone(name='images', size='75%')
                    ]
                ),
                ui.zone(name='footer')
            ]
        )
    ],
    theme='h2o-dark'
)

# The header shown on all the app's pages
header = ui.header_card(
    box='header',
    title='Image Augmentation',
    subtitle='Visualize image augmentations',
    icon='FieldChanged',
    icon_color='black',
    items=[ui.toggle(name='theme_dark', label='Dark Mode', value=True, trigger=True)]
)

# The footer shown on all the app's pages
footer = ui.footer_card(
    box='footer',
    caption=f'Learn more about <a href="{repo_url}" target="_blank"> WaveTon: 💯 Wave Applications</a>'
)

# Dialog for uploading new image
dialog_new_image = ui.dialog(
    name='dialog_new_image',
    title='Upload New Image',
    items=[ui.file_upload(name='upload', file_extensions=['jpg', 'jpeg', 'png'])],
    closable=True,
    events=['dismissed']
)

# A fallback card for handling bugs
fallback = ui.form_card(
    box='fallback',
    items=[ui.text('Uh-oh, something went wrong!')]
)


def augmentations(tab: str, augs: list) -> ui.FormCard:
    """
    Card for augmentations.
    """
    if tab == 'light':
        augmentations_list = [
            'CLAHE',
            'Defocus',
            'Equalize',
            'FancyPCA',
            'HorizontalFlip',
            'HueSaturationValue',
            'MultiplicativeNoise',
            'Normalize',
            'PixelDropout',
            'RandomBrightness',
            'RandomBrightnessContrast',
            'RandomContrast',
            'RandomCrop',
            'RandomCropFromBorders',
            'RandomGamma',
            'RandomRotate90',
            'RandomScale',
            'RandomShadow',
            'Rotate',
            'SafeRotate',
            'Spatter',
            'VerticalFlip'
        ]
    else:
        augmentations_list = [
            'AdvancedBlur',
            'Blur',
            'ChannelShuffle',
            'CoarseDropout',
            'ColorJitter',
            'Downscale',
            'GaussianBlur',
            'GlassBlur',
            'GaussNoise',
            'MedianBlur',
            'MotionBlur',
            'RandomGridShuffle',
            'RGBShift',
            'Sharpen',
            'ShiftScaleRotate',
            'ZoomBlur'
        ]

    aug_values = [ui.toggle(
        name=augmentation,
        label=augmentation,
        value=augmentation in augs,
        trigger=True
    ) for augmentation in augmentations_list]

    card = ui.form_card(
        box='augmentations',
        items=[
            ui.separator(label='Augmentations'),
            ui.tabs(
                name='tab',
                items=[
                    ui.tab(name='light', label='Light'),
                    ui.tab(name='heavy', label='Heavy')
                ],
                value=tab,
                link=True
            ),
            *aug_values
        ]
    )

    return card


def images(base_image_path: str, augmented_image_paths: list[str], n_images: int, augs: list) -> ui.FormCard:
    """
    Card for base and augmented images.
    """
    augs_visible = len(augs) > 0

    card = ui.form_card(
        box='images',
        items=[
            ui.separator(label='Base Image'),
            ui.inline(
                items=[
                    ui.image(title='', path=base_image_path, width='200px'),
                    ui.button(name='new_image', label='Upload New', primary=True)
                ],
                justify='around'
            ),
            ui.separator(label='Augmented Images'),
            ui.inline(
                items=[
                    ui.image(
                        title=f'augmented_image_{i}',
                        path=image_path,
                        width='25%'
                    ) for i, image_path in enumerate(augmented_image_paths)
                ],
                justify='center'
            ),
            ui.inline(
                items=[
                    ui.slider(name='images', label='Images', min=1, max=4, value=n_images, trigger=True, width='200px'),
                    ui.button(name='reset', label='Reset', primary=True)
                ],
                justify='center'
            ),
            ui.stats(
                items=[ui.stat(
                    label='Augmentations',
                    caption=', '.join(augs),
                    icon='PhotoCollection',
                    icon_color='#FEC924'
                )],
                justify='center',
                visible=augs_visible
            )
        ]
    )

    return card


def crash_report(q: Q) -> ui.FormCard:
    """
    Card for capturing the stack trace and current application state, for error reporting.
    This function is called by the main serve() loop on uncaught exceptions.
    """

    def code_block(content): return '\n'.join(['```', *content, '```'])

    type_, value_, traceback_ = sys.exc_info()
    stack_trace = traceback.format_exception(type_, value_, traceback_)

    dump = [
        '### Stack Trace',
        code_block(stack_trace),
    ]

    states = [
        ('q.app', q.app),
        ('q.user', q.user),
        ('q.client', q.client),
        ('q.events', q.events),
        ('q.args', q.args)
    ]
    for name, source in states:
        dump.append(f'### {name}')
        dump.append(code_block([f'{k}: {v}' for k, v in expando_to_dict(source).items()]))

    return ui.form_card(
        box='main',
        items=[
            ui.stats(
                items=[
                    ui.stat(
                        label='',
                        value='Oops!',
                        caption='Something went wrong',
                        icon='Error'
                    )
                ],
            ),
            ui.separator(),
            ui.text_l(content='Apologies for the inconvenience!'),
            ui.buttons(items=[ui.button(name='reload', label='Reload', primary=True)]),
            ui.expander(name='report', label='Error Details', items=[
                ui.text(
                    f'To report this issue, <a href="{issue_url}" target="_blank">please open an issue</a> with the details below:'),
                ui.text_l(content=f'Report Issue in App: **{app_name}**'),
                ui.text(content='\n'.join(dump)),
            ])
        ]
    )
