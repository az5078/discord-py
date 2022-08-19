import interactions

async def create_alert_role_func(ctx: interactions.CommandContext):
    role_list = await ctx.guild.get_all_roles()
    role_name_list = []
    for role in role_list:
        role_name_list.append(role.name)

    day_list = ['월', '화', '수', '목', '금']
    role_color_list = {'월' : 0xFFCED1, '화' : 0xFBE3A7, '수' : 0xD0ECBB, '목' : 0xD4ECF8, '금' : 0xCFB0E1}
    
    for day in day_list:
        if (day == '월' or day == '화'):
            for i in range(9):
                role_name = '{}.{}'.format(day, i+1)
                if role_name not in role_name_list:
                    await ctx.guild.create_role(role_name, color = role_color_list[day])
        else:
            for i in range(7):
                role_name = '{}.{}'.format(day, i+1)
                if role_name not in role_name_list:
                    await ctx.guild.create_role(role_name, color = role_color_list[day])

    role_create_complete_embed = interactions.Embed(title = '**역할 생성이 완료되었습니다!**')

    await ctx.send(embeds = role_create_complete_embed)


            

