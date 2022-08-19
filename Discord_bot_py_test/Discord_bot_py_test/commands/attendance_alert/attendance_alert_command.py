import interactions
from datetime import datetime

alert_ctx: interactions.CommandContext = ''
alert_on = False

async def attendance_alert_start_func(ctx: interactions.CommandContext):
    alert_ctx = ctx
    alert_on = True
    await ctx.send('명령어가 실행되었습니다!')

async def attendance_alert_func():
    for i in range(10):
        await alert_ctx.send('test')