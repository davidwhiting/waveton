import logging

from h2o_wave import Q, main, app, copy_expando, expando_to_dict, handle_on, on

from . import cards

logging.basicConfig(format='%(levelname)s:\t[%(asctime)s]\t%(message)s', level=logging.INFO)


@app('/')
async def serve(q: Q):
    """
    App function.
    """

    try:
        # initialize app
        if not q.app.app_initialized:
            await initialize_app(q)

        # initialize client
        if not q.client.client_initialized:
            await initialize_client(q)

        # set theme
        elif q.args.theme_dark is not None and q.args.theme_dark != q.client.theme_dark:
            await update_theme(q)

        # handle ons
        elif await handle_on(q):
            pass

        # dummy update for edge cases
        else:
            await update_dummy(q)

    except Exception as error:
        await handle_error(q, error=str(error))


async def initialize_app(q: Q):
    """
    Initializing app.
    """

    logging.info('Initializing app')

    q.app.app_initialized = True


async def initialize_client(q: Q):
    """
    Initializing client.
    """

    logging.info('Initializing client')

    q.page['meta'] = cards.meta()
    q.page['header'] = cards.header()
    q.page['home'] = cards.home()
    q.page['footer'] = cards.footer()

    q.page['dummy'] = cards.dummy()

    q.client.client_initialized = True

    await q.page.save()


async def update_theme(q: Q):
    """
    Update theme of app.
    """

    copy_expando(q.args, q.client)

    if q.client.theme_dark:
        logging.info('Updating theme to dark mode')

        q.page['meta'].theme = 'h2o-dark'
        q.page['header'].icon_color = 'black'
        q.page['home'].items[0].text.content = 'This is dark mode.'
    else:
        logging.info('Updating theme to light mode')

        q.page['meta'].theme = 'light'
        q.page['header'].icon_color = '#FEC924'
        q.page['home'].items[0].text.content = 'This is light mode.'

    q.page['header'].items[0].toggle.value = q.client.theme_dark

    await q.page.save()


async def drop_cards(q: Q, card_names: list):
    """
    Drop cards from Wave page.
    """

    for card_name in card_names:
        del q.page[card_name]


async def handle_error(q: Q, error: str):
    """
    Handle any app error.
    """

    logging.error(error)

    await drop_cards(q, cards.DROPPABLE_CARDS)

    q.page['error'] = cards.error(
        q_app=expando_to_dict(q.app),
        q_user=expando_to_dict(q.user),
        q_client=expando_to_dict(q.client),
        q_events=expando_to_dict(q.events),
        q_args=expando_to_dict(q.args)
    )

    await q.page.save()


@on('restart')
async def restart(q: Q):
    """
    Restart app.
    """

    logging.info('Restarting app')

    q.page['meta'].redirect = '#home'
    q.client.client_initialized = False

    await q.page.save()


@on('report')
async def report(q: Q):
    """
    Report error details.
    """

    q.page['error'].items[4].separator.visible = True
    q.page['error'].items[5].text.visible = True
    q.page['error'].items[6].text_l.visible = True
    q.page['error'].items[7].text.visible = True
    q.page['error'].items[8].text.visible = True
    q.page['error'].items[9].text.visible = True
    q.page['error'].items[10].text.visible = True
    q.page['error'].items[11].text.visible = True
    q.page['error'].items[12].text.visible = True

    await q.page.save()


async def update_dummy(q: Q):
    """
    Dummy update for edge cases.
    """

    q.page['dummy'].items = []

    await q.page.save()
