import discord
from discord.ext import commands
from discord.ui import Button, View
import random


TOKEN = "MTUzMjM4ODUxMTg1OTA4MTQ2Ng.GF43m6.kLN2_ZGtsKAU00TOdbli6uXvxVB9uaoyrlP3OI"


intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)


# -----------------------------
# POINT STORAGE
# -----------------------------

points = {}


# -----------------------------
# PRESCRIPTS
# -----------------------------

prescripts = [

"Prescript 001:\nEnter Archived and defeat 1 opponent in PvP.",

"Prescript 002:\nWin a duel without using your strongest equipment.",

"Prescript 003:\nDefeat 2 opponents while remaining alive.",

"Prescript 004:\nMercy obstructs efficiency. Eliminate 3 players. Leave no unfinished task.",

"Prescript 005:\nComplete a Impuritas Civitatis (Buffed) Library run using only blood setup. Solo or Not.",

"Prescript 006:\nThe Index demands harmony. Match your opponent's playstyle exactly for the first minute of battle (if they use range, use range; if they rush, rush) before delivering the execution.",

"Prescript 007:\nAssist another protected player/Edict user(s) in defeating an enemy.",

"Prescript 008:\nSurvive three battles consecutively.",

"Prescript 009:\nDefeat an opponent while using an unusual build.",

"Prescript 010:\nSilent observer. Follow a Initiate or higher-ranking Edict member during an encounter and assist them in ganking five times.",

"Prescript 011:\nFlawless execution. Win a 1v1 duel without missing a single heavy attack or key skill. A single miss counts as a failed Prescript.",

"Prescript 012:\nEnter combat against a random for no reason.",

"Prescript 013:\nThe Edict's shadow. Defeat an opponent without allowing them to hit you more than three times in total.",

"Prescript 014:\nDefeat 5 opponents in PD before returning.",

"Prescript 015:\nComplete the Philosophy Floor with only one page of your choice successfully.",

"Prescript 016:\nUse a different strategy than your normal approach.",

"Prescript 017:\nProtect another player during a dangerous encounter.",

"Prescript 018:\nAccept your next combat encounter without inspecting the opponent's build, rank, or equipment. Walk in blind.",

"Prescript 019:\nComplete 10 objectives in one session.",

"Prescript 020:\nTarget the weakest player currently present in the district/server. Eliminate them three times consecutively, regardless of their pleas or surrender.",

"Prescript 021:\nDefeat a player with only your weapon.",

"Prescript 022:\nAttempt a challenge without your usual advantages.",

"Prescript 023:\nAchieve victory against a random assignment.",

"Prescript 024:\nComplete a run selected by another player.",

"Prescript 025:\nThe Edict watches. Demonstrate discipline."

"Prescript 026:\nForce feed the 17th person you see with Cinnamon-infused raw meat skewers until they die."

"Prescript 027:\nDrink The Darink mid-fight with the Mimicry E.G.O popped and parry-bait them by drinking it so it makes the 'Goodbye' sound."

"Prescript 028:\nUse Wheel's Industry but Recolor it to Vanta Pink, and yourself aswell, while using a chromatic kit, and then use it to kill a player in PvP. After Prescript, return to the Standard Edict Outfit/Weapon"

"Prescript 029:\nCreate a build that uses your HP, regardless of how low your pages are and play with it for a week."

"Prescript 030:\nJoin a random gank-office, use the Smile Outfit with Fell Bullet E.G.O in mid-PD gank and kill your entire office (THIS DOES NOT INCLUDE THE EDICT), and repeat this process on three offices. You may gain 50+ points with proof."

"Prescript 031:\nBeat Impuritas Civitatis Kether Floor with Flaming Bat.",

"Prescript 032:\nThe first person you see, Dismember them from existence in PD.",

"Prescript 033:\nWin against Impuritas Civitatis Language Floor with Fixer Battleaxe, no pages.",

"Prescript 034:\nGo on a rampage in PD and kill 10 players in a row without dying. You may gain 100 points with proof.",

"Prescript 035:\nWhen meeting with h̸̺̅e͈͛͘r̛̥ͬ, accept her help.",

"Prescript 036:\nIf you die from any user, you MUST drink 2 litres of Pepsi and the HamHamPangPang-Special-Weekly-Sandwich"

]


# -----------------------------
# ROLE UPDATE
# -----------------------------

async def update_role(member):

    score = points.get(member.id, 0)

    roles = member.guild.roles

    unprotected = discord.utils.get(
        roles,
        name="Unprotected"
    )

    protected = discord.utils.get(
        roles,
        name="Protected"
    )

    edictkill = discord.utils.get(
        roles,
        name="Edict's Kill"
    )


    if score < 0:

        await member.add_roles(edictkill)

        await member.remove_roles(
            unprotected,
            protected
        )


    elif score >= 100:

        await member.add_roles(protected)

        await member.remove_roles(
            unprotected,
            edictkill
        )


    else:

        await member.add_roles(unprotected)

        await member.remove_roles(
            protected,
            edictkill
        )


# -----------------------------
# BUTTON SYSTEM
# -----------------------------

@bot.command(name="points")
async def points_cmd(ctx):
    user_points = points.get(ctx.author.id, 0)
    try:
        await ctx.author.send(
            f"**THE EDICT RECORD**\n\nUser:\n{ctx.author}\n\nCurrent Edict Points:\n{user_points}"
        )
        await ctx.send("Your Edict record has been sent to your DMs.", delete_after=5)
    except discord.Forbidden:
        await ctx.send(
            f"Could not send a DM to {ctx.author.mention}. Please check your privacy settings!",
            delete_after=5,
        )


class PrescriptView(View):

    def __init__(self, user, prescript_text):

        super().__init__(
            timeout=None
        )

        self.user = user
        self.prescript_text = prescript_text
        self.message = None


    async def remove_message(self):

        if self.message:

            try:
                await self.message.delete()

            except discord.NotFound:
                pass



    @discord.ui.button(
        label="Accept Prescript",
        style=discord.ButtonStyle.green
    )

    async def accept(
        self,
        interaction: discord.Interaction,
        button: Button
    ):

        if interaction.user != self.user:
            await interaction.response.send_message(
                "This Prescript was not issued for you.",
                ephemeral=True
            )
            return

        points[self.user.id] = points.get(
            self.user.id,
            0
        ) + 10


        await update_role(self.user)


        await interaction.response.send_message(
            f"{self.user.mention} accepted the Prescript.\n+10 Edict Points.\n\n" + f"**Completed Prescript:**\n{self.prescript_text}\n\n",
            ephemeral=False
        )

        try:
            await interaction.message.delete()
        except discord.NotFound:
            pass



    @discord.ui.button(
        label="Decline Prescript",
        style=discord.ButtonStyle.red
    )

    async def decline(
        self,
        interaction: discord.Interaction,
        button: Button
    ):

        if interaction.user != self.user:
            await interaction.response.send_message(
                "This Prescript was not issued for you.",
                ephemeral=True
            )
            return


        points[self.user.id] = points.get(
            self.user.id,
            0
        ) - 20


        await update_role(self.user)


        await interaction.response.send_message(
            f"{self.user.mention} declined the Prescript.\n-20 Edict Points.\n\n" + f"**Completed Prescript:**\n{self.prescript_text}\n\n",
            ephemeral=False
        )

        try:
            await interaction.message.delete()
        except discord.NotFound:
            pass



# -----------------------------
# COMMANDS
# -----------------------------

@bot.command(name="addpoint")
async def addpoint(ctx, member: discord.Member, amount: int):
    bot_member = ctx.guild.get_member(bot.user.id)
    if ctx.author.top_role <= bot_member.top_role:
        await ctx.send(
            "You do not have a role higher than the bot to use this command."
        )
        return

    points[member.id] = points.get(member.id, 0) + amount
    await update_role(member)
    await ctx.send(
        f"Added {amount} Edict Points to {member.mention}. Total: {points[member.id]}"
    )


@bot.command(name="rmvpoint")
async def rmvpoint(ctx, member: discord.Member, amount: int):
    bot_member = ctx.guild.get_member(bot.user.id)
    if ctx.author.top_role <= bot_member.top_role:
        await ctx.send(
            "You do not have a role higher than the bot to use this command."
        )
        return

    points[member.id] = points.get(member.id, 0) - amount
    await update_role(member)
    await ctx.send(
        f"Removed {amount} Edict Points from {member.mention}. Total: {points[member.id]}"
    )



@bot.command()
@commands.cooldown(1, 300, commands.BucketType.user)
async def prescript(ctx):
    order = random.choice(prescripts)

    view = PrescriptView(ctx.author, order)

    msg = await ctx.send(
        "[[THE EDICT IS ALWAYS WATCHING YOU]].\n\n" + order,
        view=view
    )
    view.message = msg


@prescript.error
async def prescript_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(
            f"The Edict requires patience after {error.retry_after:.2f} seconds.",
            delete_after=5
        )
    else:
        raise error


@bot.command()
async def edict(ctx):

    score = points.get(
        ctx.author.id,
        0
    )


    if score < 0:
        status = "Edict's Kill"

    elif score >= 100:
        status = "Protected"

    else:
        status = "Unprotected"


    await ctx.send(
        f"""
**THE EDICT RECORD**

User:
{ctx.author}

Points:
{score}

Status:
{status}


Rules:

0-99 Points:
Unprotected

100+ Points:
Protected

Below 0:
Edict's Kill
"""
    )



@bot.event
async def on_ready():

    print(
        f"The Edict is online as {bot.user}"
    )



bot.run(TOKEN)