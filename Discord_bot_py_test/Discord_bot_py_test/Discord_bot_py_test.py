import interactions
from commands.PUBG.PUBG_command import 배그전적
from commands.poll_command import poll_command
from commands.attendance_alert.attendance_role_create_command import create_alert_role_func
from commands.attendance_alert.attendance_role_delete_command import delete_alert_role_func
from commands.attendance_alert.attendance_alert_command import attendance_alert_start_func
import asyncio
import os

#토큰 파일 열기
token_path = os.path.dirname(os.path.abspath(__file__)) + '\Token.token'
with open(token_path, 'r', encoding='utf-8') as t:
    token = t.readlines()

bot = interactions.Client(
    token = token[0],
    default_scope = 652553915123892245,
    intents = interactions.Intents.DEFAULT,
    presence = interactions.ClientPresence(
        activities = [
            interactions.PresenceActivity(
                name="이제 거의 파이썬으로 구동됩니다! (출첵 기능 미구현)",
                type=interactions.PresenceActivityType.GAME
                )
            ]
        )
    )

bot.load('interactions.ext.files')

@bot.event
async def on_start():
    print('봇이 시작되었습니다.')


@bot.command(
    name = 'hello',
    description = '인사 명령어입니다.',
    )
async def hello(ctx: interactions.CommandContext):
    await ctx.send('반갑습니다.')
    print('명령어 [안녕]이 실행되었습니다.')

@bot.command(
    name="say_something",
    description="say something!",
    options = [
        interactions.Option(
            name="text",
            description="What you want to say",
            type=interactions.OptionType.STRING,
            required=True,
        ),
    ],
)
async def my_first_command(ctx: interactions.CommandContext, text: str):
    await ctx.send(f"You said '{text}'!")

@bot.command(
    name = 'pubg',
    )
async def pubg(ctx : interactions.CommandContext):
    await ctx.defer()

@pubg.subcommand(
    name = 'stat',
    description = '배틀그라운드 전적을 확인하고 입력한 변째의 매치 정보를 가져옵니다.',
    options = [
        interactions.Option(
            name="match_no",
            description="몇번째 매치를 검색하시겠습니까? 가장 최근 매치부터 1로 시작합니다. (최대 59)",
            type=interactions.OptionType.INTEGER,
            required=True,
        ),
        interactions.Option(
            name="user_name",
            description="검색할 유저의 닉네임을 입력하세요.",
            type=interactions.OptionType.STRING,
            required=True,
        ),
    ],
)
async def stat(ctx: interactions.CommandContext, match_no: int, user_name: str):
    print('명령어 [전적확인]이 실행되었습니다.')
    await 배그전적(ctx, match_no, user_name)

@bot.command(
    name = 'poll',
    description = '투표 명령어 입니다.',
    options = [
        interactions.Option(
            name="duration",
            description="투표를 진행할 시간을 정하세요. 초단위 입니다.",
            type=interactions.OptionType.INTEGER,
            required=True,
        ),
        interactions.Option(
            name="emoji",
            description="투표 보기로 사용될 이모지를 입력하세요.",
            type=interactions.OptionType.STRING,
            required=True,
        ),
    ],
)
async def poll(ctx: interactions.CommandContext, duration: int, emoji: str):
    print('명령어 [투표]가 실행되었습니다.')
    await ctx.defer()
    args_list = emoji.split(" ")
    args_tuple = tuple(args_list)
    await poll_command(ctx, duration, args_tuple)

@bot.command(
    name = 'role'
    )
async def role(ctx: interactions.CommandContext):
    pass

@role.group(
    name = 'test'
    )
async def test(ctx: interactions.CommandContext):
    pass

@test.subcommand(
    name = 'create'
    )
async def create(ctx: interactions.CommandContext):
    await ctx.defer()
    test_role = await ctx.guild.create_role('test role')
    print('test role 역할이 생성되었습니다.')
    
    await asyncio.sleep(5)

    await ctx.guild.delete_role(test_role.id)
    print('test role 역할이 제거되었습니다.')

@bot.command(
    name = 'attendance'
    )
async def attendance(ctx: interactions.CommandContext):
    pass

@attendance.group(
    name = 'alert'
    )
async def alert(ctx: interactions.CommandContext):
    pass

@alert.subcommand(
    name = 'create_role'
    )
async def create_role(ctx: interactions.CommandContext):
    await ctx.defer()
    await create_alert_role_func(ctx)

@alert.subcommand(
    name = 'delete_role'
    )
async def delete_role(ctx: interactions.CommandContext):
    await ctx.defer()
    await delete_alert_role_func(ctx)
    
@alert.subcommand(
    name = 'alert_start'
    )
async def alert_start(ctx: interactions.CommandContext):
    await ctx.defer()
    await attendance_alert_start_func(ctx)

#@alert.subcommand(
#    name ='test'
#    )
#async def test(ctx: interactions.CommandContext):
#    await ctx.send('test')

bot.start()