import json

from telegram import Update

from recept_menu import application


# application = Application.builder().token(TELEGRAM_API_KEY).build()


async def handler(event, context):
    return await main(event, context)


async def main(event, context):
    # Add conversation, command, and any other handlers

    try:
        print(f'{application._initialized=}')

        await application.initialize()
        await application.process_update(
            Update.de_json(json.loads(event["body"]), application.bot)
        )

        return {
            'statusCode': 200,
            'body': 'Success'
        }

    except Exception as exc:
        return {
            'statusCode': 500,
            'body': 'Failure'
        }