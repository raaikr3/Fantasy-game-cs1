from drafter import *
from bakery import assert_equal
from dataclasses import dataclass, field

set_website_title("The Forgotten Kingdom")
set_site_information(
    author="Raaik Rayani",
    description="Fantasy Choose-your-own-Adventure Game",
    sources="Blockpy Textbook",
    planning=["plan.pdf", "design.pdf"],
    links=["https://github.com/raaikr3/Fantasy-game-cs1"]
)
hide_debug_information()
set_website_framed(False)

@dataclass
class Companion:
    """Represents a recruited companion in the guild"""
    name: str

@dataclass
class State:
    """The player's game state that tracks all their choices and progress"""
    name: str = "Arin"
    choose_destiny: str = ""
    guild_name: str = ""
    has_map: bool = False
    guild_members: list[Companion] = field(default_factory=list)
    guild_motto: str = " "
    
@route
def index(state: State) -> Page:
    """Shows game starting page and player inputs their name"""
    return Page(
        state=state,
        content=[
            "Welcome to the Realm of Legends! State your name...",
            "Try Arin, Nyx, Gareth, Selene, or Rowan for a surprise!",
            TextBox(name="name", kind="text", default_value=state.name),
            Button(text="Choose Destiny", url="/choose_destiny"),
        ],
    )

@route
def choose_destiny(state: State, name: str)->Page:
    """Lets the player choose their destiny, being a villager or adventurer"""
    state.name = name
    return Page(
        state=state,
        content=[
            "Choose your destiny!",
            Button(text="Villager", url="/villager"),
            Button(text="Adventurer", url="/adventurer")
        ]
    )
    
@route
def villager(state: State) ->Page:
    """Shows the path of being a villager, this also ends the gameplay"""
    state.choose_destiny = "Villager"
    return Page(
        state=state,
        content=["You live a peaceful life and watch the heroes pass through. A young mage seems to be making waves across the land.",
                 Button(text="Try again", url="/choose_destiny?name="+state.name),
                ],
    )
    
@route
def adventurer(state: State)->Page:
    """Shows the adventurer path giving the player to choose their guild name"""
    state.choose_destiny = "Adventurer"
    return Page(
        state=state,
        content=[
            "A guild needs a name...",
            TextBox(name="guild_name", kind="text", default_value="Silver Knights"),
            Button(text="Next", url="/guild_setup"),
        ],
    )
    
@route
def guild_setup(state: State, guild_name: str, guild_motto: str = "For Honor and Glory")-> Page:
    """Stores the user's guild name and motto to see"""
    state.guild_name = guild_name
    state.guild_motto = guild_motto
    return Page(
        state=state,
        content=[
            "The " + state.guild_name + " are ready for adventure!",
            "Every guild has a motto too, what's yours, leader?",
            TextArea(name="guild_motto", kind="text", default_value=state.guild_motto),
            Button(text="Continue", url="/recruit_members"),
        ],
    )
    
@route
def recruit_members(state: State)-> Page:
    """Checks the user's name to determine special companion"""
    companion_map = {
        "Arin": "Lyra the Wise",
        "Nyx": "Darius the Shadow",
        "Gareth": "Oren the Brave",
        "Selene": "Mira the Moonblade",
        "Rowan": "Thorne the Archer"
        }
    if state.name in companion_map:
        companion_name = companion_map[state.name]
        message = companion_name + " joins your guild as your trusted companion!"
    else:
        companion_name = "a wandering swordsman"
        message = "A wandering swordsman joins your guild."
        
    state.guild_members.append(Companion(name=companion_name))
    
    return Page(
        state=state,
        content=[
            message,
            Button(text="Continue", url="/choose_destination"),
            ],
        )

@route
def choose_destination(state: State)->Page:
    """Lets the player choose their next destination. The choice here matters"""
    
    
    member_names = []
    for member in state.guild_members:
        member_names.append(member.name)
        
    guild_list = "Guild Members: " + ", ".join(member_names) if member_names else "No guild members yet."
    
    return Page(
        state=state,
        content=[
            "You're a small guild, where to, leader?",
            "Guild name: " + state.guild_name,
            "Guild motto: " + state.guild_motto,
            guild_list,
            Button(text="Mountain Pass", url="/mountain_pass"),
            Button(text="Mysterious Forest", url="/mysterious_forest"),
        ],
    )
@route
def mountain_pass(state: State)->Page:
    """Player reaches a dangerous region and must choose what to do"""
    if state.has_map:
        return Page(
            state=state,
            content=[
                "Not bad, you made it to the Mountain Pass. But the monsters here are fierce. Where to now?",
                Button(text="Train", url="/train_up"),
                Button(text="Cross the Great Divide", url="/divide_fail"),
            ],
        )
    return Page(
        state=state,
        content=[
            "The twisting paths make it impossible to navigate. You aren't prepared yet.",
            Button(text="Go back", url="/choose_destination"),
        ],
    )

@route
def divide_fail(state: State)->Page:
    """Gives the game over sequence if the player comes here first"""
    return Page(
        state=state,
        content=[
            "You attempt to cross the Great Divide, but a colossal guardian blocks your path. With a single blow, it sends you crashing back down the mountain.",
            Button(text="Game Over", url="/index"),
            ],
        )

@route
def train_up(state: State)->Page:
    """The player trains here allowing them to progress"""
    state.has_power=True
    return Page(
        state=state,
        content=[
            "You travel to an ancient temple to train and unlock hidden powers.",
            Button(text="Cross the Great Divide", url="/divide_choice"),
            ],
        )

@route
def divide_choice(state: State)->Page:
    """Player faces a guardian and can choose to attack or flee"""
    return Page(
        state=state,
        content=[
            "You reach the Great Divide again, but the guardian rises to challenge you.",
            Button(text="Attack", url="/divide_attack"),
            Button(text="Retreat", url="/train_up"),
            ],
        )

@route
def divide_attack(state: State)->Page:
    """The player can block and counter to buy them enough time to survive"""
    return Page(
        state=state,
        content=[
            "It strikes, but you block and counter using your newfound powers. A distant commotion draws the guardian's attention, and you are allowed to pass.",
            Button(text="Cross the Great Divide", url="/win_page"),
            ],
        )

@route
def win_page(state: State)->Page:
    """The victory page after crossing into a new land."""
    return Page(
        state=state,
        content=[
            "You've crossed into the Forgotten Kingdom and earned a great reputation across the realm. Tales spread of Leader " + state.name + " of the " + state.guild_name + ".",
            Button(text="To Be Continued", url="/index"),
            ],
        )
        

    
@route
def mysterious_forest(state: State)->Page:
    """This handles the mysterious forest where the user gains the map to progress"""
    state.has_map = True
    return Page(
        state=state,
        content=[
            "You rescue a wounded ranger who, in gratitude, gives you a map that reveals the hidden paths of the Mountain Pass.",
            Button(text="Go back", url="/choose_destination"),
        ],
    )
                
    
state =  State()

page = index(state)
assert_equal(page.content[0], "Welcome to the Realm of Legends! State your name...")

page = choose_destiny(state, "Arin")
assert_equal(page.content[0], "Choose your destiny!")

page = villager(state)
assert_equal(page.content[0], "You live a peaceful life and watch the heroes pass through. A young mage seems to be making waves across the land.")

page = adventurer(state)
assert_equal(page.content[0], "A guild needs a name...")

page = guild_setup(state, "Silver Wolves", "For Honor and Glory")
assert_equal(state.guild_name, "Silver Wolves")
assert_equal(page.content[0], "The Silver Wolves are ready for adventure!")

page = recruit_members(state)
assert_equal(Companion(name="Lyra the Wise") in state.guild_members, True)
assert_equal(page.content[0], "Lyra the Wise joins your guild as your trusted companion!")

page = choose_destination(state)
assert_equal(page.content[0], "You're a small guild, where to, leader?")
assert_equal(page.content[1].startswith("Guild name:"), True)

page = mountain_pass(state)
assert_equal(page.content[0], "The twisting paths make it impossible to navigate. You aren't prepared yet.")

page = mysterious_forest(state)
assert_equal(state.has_map, True)
assert_equal(page.content[0], "You rescue a wounded ranger who, in gratitude, gives you a map that reveals the hidden paths of the Mountain Pass.")

page = mountain_pass(state)
assert_equal(page.content[0], "Not bad, you made it to the Mountain Pass. But the monsters here are fierce. Where to now?")

start_server(State())

