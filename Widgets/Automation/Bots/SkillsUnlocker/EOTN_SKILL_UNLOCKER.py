from __future__ import annotations

import os
from collections.abc import Callable
from typing import List, Tuple

import Py4GW
import PyImGui
from Py4GWCoreLib import Agent, GLOBAL_CACHE, ImGui, ModelID, Player
from Py4GWCoreLib.BottingTree import BottingTree
from Py4GWCoreLib.py4gwcorelib_src.BehaviorTree import BehaviorTree
from Py4GWCoreLib.routines_src.BehaviourTrees import BT as RoutinesBT
from Sources.ApoSource.ApoBottingLib import wrappers as BT


BOT_NAME = "Skills Unlocker"
MODULE_NAME = BOT_NAME

SKILLS_UNLOCKER_PATH = os.path.join(
    Py4GW.Console.get_projects_path(),
    "Widgets",
    "Automation",
    "Bots",
    "SkillsUnlocker",
)
TEXTURE = os.path.join(SKILLS_UNLOCKER_PATH, "skills_unlocker.png")
ICONS_PATH = os.path.join(SKILLS_UNLOCKER_PATH, "icons")

botting_tree: BottingTree | None = None
initialized = False
selected_skill_step = ""


def _action_tree(
    name: str,
    action_fn: Callable[[], object],
    aftercast_ms: int = 0,
) -> BehaviorTree:
    def _run() -> BehaviorTree.NodeState:
        action_fn()
        return BehaviorTree.NodeState.SUCCESS

    return BehaviorTree(
        BehaviorTree.ActionNode(
            name=name,
            action_fn=_run,
            aftercast_ms=max(0, int(aftercast_ms)),
        )
    )


def _runtime_combat_tree(pause_on_danger: bool) -> BehaviorTree:
    return BT.Subtree(
        name="Configure Skills Unlocker Combat",
        subtree_fn=lambda _node: ensure_botting_tree().Config.Aggressive(
            pause_on_danger=bool(pause_on_danger),
            account_isolation=True,
            multi_account=False,
            auto_loot=False,
            resurrection_scroll=False,
        ),
    )


def _profession_skillbar_tree() -> BehaviorTree:
    templates = {
        "Dervish": "OgSCU8pkcQZwnwWIAAAAAAAA",
        "Ritualist": "OASjUwHKIRyBlBfCbhAAAAAAAAA",
        "Warrior": "OQQTU4DHHaLUOoM4TAAAAAAAAAA",
        "Ranger": "OgQTU4DfHaLUOoM4TAAAAAAAAAA",
        "Necromancer": "OApCU8pkcQZwnwWIAAAAAAAA",
        "Elementalist": "OgRDU8x8QbhyBlBfCAAAAAAAAA",
        "Mesmer": "OQRDATxHTbhyBlBfCAAAAAAAAA",
        "Monk": "OwQTU4DDHaLUOoM4TAAAAAAAAAA",
        "Assassin": "OwRjUwH84QbhyBlBfCAAAAAAAAA",
        "Paragon": "OQSCU8pkcQZwnwWIAAAAAAAA",
    }

    def _build(_node: BehaviorTree.Node) -> BehaviorTree:
        profession, _ = Agent.GetProfessionNames(Player.GetAgentID())
        template = templates.get(str(profession), "")
        if not template:
            return BT.Failer(name=f"Unsupported profession: {profession}")
        return BT.LoadSkillbar(template=template, log=True)

    return BT.Subtree(
        name="Load Profession Skillbar",
        subtree_fn=_build,
    )


def _add_winds_heroes_tree() -> BehaviorTree:
    return BT.Sequence(
        name="Add Winds Heroes And Builds",
        children=[
            BT.LeaveParty(),
            BT.Wait(1_000),
            _action_tree("Add Gwen", lambda: GLOBAL_CACHE.Party.Heroes.AddHero(24), 250),
            _action_tree("Add Vekk", lambda: GLOBAL_CACHE.Party.Heroes.AddHero(26), 250),
            _action_tree("Add Ogden", lambda: GLOBAL_CACHE.Party.Heroes.AddHero(27), 250),
            BT.Wait(1_200),
            BT.LoadHeroSkillbar(1, "OQhkAsC8gFKCNkDT/QY6yQGcxA", log=True),
            BT.LoadHeroSkillbar(2, "OgljgwMpZO0iwBgWp5N0h14dMA", log=True),
            BT.LoadHeroSkillbar(3, "OwUTMwHD1ZMWP0iBkZSPIDsSAA", log=True),
        ],
    )


def _add_winds_henchmen_tree() -> BehaviorTree:
    return BT.Sequence(
        name="Add Winds Henchmen",
        children=[
            _action_tree(
                f"Add Henchman {henchman_id}",
                lambda henchman_id=henchman_id: GLOBAL_CACHE.Party.Henchmen.AddHenchman(henchman_id),
                250,
            )
            for henchman_id in range(1, 8)
        ],
    )


def Unlock_ebon_battle_standard_of_honor() -> BehaviorTree:
    return BT.Sequence(
        name='Unlock Ebon Battle Standard of Honor',
        children=[
            _runtime_combat_tree(True),
            BT.Travel(target_map_name="Longeyes Ledge", log=True),
            BT.Move((-21902, 12807), pause_on_combat=True, log=False),
            BT.Wait(5000),
            BT.MoveAndDialog((-21141.81, 12378.68), dialog_id=0x836003, pause_on_combat=True, log=True),
            BT.Wait(1000),
            BT.MoveAndDialog((-21141.81, 12378.68), dialog_id=0x836001, pause_on_combat=True, log=True),
            BT.Wait(1000),
            BT.Move(([
                    (-21593.0, 12517.0),
                    (-20064.0, 11212.0),
                    (-18659.0,  9768.0),
                    (-17352.0,  8246.0),
                    (-16126.0,  6640.0),
                    (-14663.0,  5256.0),
                    (-13347.0,  3732.0),
                    (-11993.0,  2247.0),
                    (-11088.0,   402.0),
                    ( -9414.0,  -699.0),
                    ( -7532.0,   132.0),
                    ( -5576.0,  -322.0),
                    ( -3621.0,  -814.0),
                    ( -1677.0, -1304.0),
                    (   177.0, -2140.0),
                    (  1759.0, -3373.0),
                    (  3730.0, -3747.0),
                    (  5650.0, -4349.0),
                    (  7421.0, -5292.0),
                    (  8547.0, -6957.0),
                    ( 10587.0, -6733.0),
                    ( 12591.0, -6583.0),
                    ( 14521.0, -7151.0),
                    ( 16095.0, -8448.0),
                    ( 17681.0, -9721.0),
                    ( 19282.0,-11005.0),
                    ( 20765.0,-12412.0),
                    ( 22538.0,-13411.0),
                    ( 23410.0,-13901.0),
                ]), pause_on_combat=True, log=False),
            BT.WaitUntilOutOfCombat(timeout_ms=120_000),
            BT.WaitForMapLoad(map_id=651, timeout_ms=45_000),
            BT.Move(([
                (-17861.0, 16317.0),
                (-16404.0, 14900.0),
                (-16459.0, 12851.0),
                (-17542.0, 11132.0),
                (-17939.0,  9166.0),
                (-16308.0,  7932.0),
                (-15150.0,  6294.0),
                (-14010.0,  4577.0),
                (-13622.0,  2552.0),
                (-13094.0,   598.0),
                (-11367.0,  -490.0),
                ( -9393.0,  -831.0),
                ( -7616.0, -1762.0),
                ( -5677.0, -2456.0),
                ( -4372.0, -4015.0),
                ( -3143.0, -5620.0),
                ( -2954.0, -7657.0),
                ( -2423.0, -9586.0),
                (  -593.0,-10426.0),
                (  1413.0,-10033.0),
                (  3432.0, -9958.0),
                (  4945.0, -8637.0),
                (  6962.0, -8362.0),
                (  8991.0, -8392.0),
                (  4471.0, -7294.0),
                (  6525.0, -7403.0),
                (  8415.0, -8062.0),
                ( 10082.0, -9228.0),
                ( 11715.0, -8045.0),
                ]), pause_on_combat=True, log=False),
            BT.WaitUntilOutOfCombat(timeout_ms=120_000),
            BT.Travel(target_map_id=650, log=True),
            BT.Move((-21902, 12807), pause_on_combat=True, log=False),
            BT.WaitForMapLoad(map_id=649, timeout_ms=45_000),
            BT.MoveAndDialog((-21141.81, 12378.68), dialog_id=0x836007, pause_on_combat=True, log=True),
        ],
    )

def Unlock_mental_block() -> BehaviorTree:
    return BT.Sequence(
        name='Unlock Mental Block',
        children=[
            _runtime_combat_tree(True),
            BT.Travel(target_map_id=641, log=True),
            BT.WaitForMapLoad(map_id=641, timeout_ms=45_000),
            BT.MoveAndDialog((25203, -10694), dialog_id=0x837701, pause_on_combat=True, log=True),
            BT.Travel(target_map_id=639, log=True),
            BT.WaitForMapLoad(map_id=639, timeout_ms=45_000),
            BT.Move((-22999, 6530), pause_on_combat=True, log=False),
            BT.WaitForMapLoad(map_id=566, timeout_ms=45_000),
            BT.Move((-9761, -8000), pause_on_combat=True, log=False),
            BT.Move((7833, -8293), pause_on_combat=True, log=False),
            BT.Move((11690, -6215), pause_on_combat=True, log=False),
            BT.Move((15918, -2667), pause_on_combat=True, log=False),
            BT.Wait(3000),
            BT.WaitUntilOutOfCombat(timeout_ms=120_000),
            BT.Resign(multi_account=False, log=True),
            BT.WaitForMapLoad(map_id=639, timeout_ms=45_000),
            BT.Travel(target_map_id=641, log=True),
            BT.WaitForMapLoad(map_id=641, timeout_ms=45_000),
            BT.MoveAndDialog((25203, -10694), dialog_id=0x837707, pause_on_combat=True, log=True),
        ],
    )

def Unlock_smooth_criminal() -> BehaviorTree:
    return BT.Sequence(
        name='Unlock Smooth Criminal',
        children=[
            _runtime_combat_tree(True),
            BT.Travel(target_map_id=641, log=True),
            BT.WaitForMapLoad(map_id=641, timeout_ms=45_000),
            BT.MoveAndDialog((25203, -10694), dialog_id=0x837C01, pause_on_combat=True, log=True),
            BT.Move((18781, -10477), pause_on_combat=True, log=False),
            BT.WaitForMapLoad(map_name="Alcazia Tangle", timeout_ms=45_000),
            BT.Move((17024, -600), pause_on_combat=True, log=False),
            BT.Move((18237, 6691), pause_on_combat=True, log=False),
            BT.Move((15518, 8375), pause_on_combat=True, log=False),
            BT.Move((13200, 15000), pause_on_combat=True, log=False),
            BT.Wait(3000),
            BT.WaitUntilOutOfCombat(timeout_ms=120_000),
            BT.Move((19516, 4686), pause_on_combat=True, log=False),
            BT.Move((12184, 370), pause_on_combat=True, log=False),
            BT.Move((4802, -4990), pause_on_combat=True, log=False),
            BT.Move((-8760, -3378), pause_on_combat=True, log=False),
            BT.Move((-5555, -2108), pause_on_combat=True, log=False),
            BT.Move((-6678, 6477), pause_on_combat=True, log=False),
            BT.Wait(3000),
            BT.WaitUntilOutOfCombat(timeout_ms=120_000),
            BT.Move((-8860, -3178), pause_on_combat=True, log=False),
            BT.Move((-11202, 758), pause_on_combat=True, log=False),
            BT.Wait(3000),
            BT.WaitUntilOutOfCombat(timeout_ms=120_000),
            BT.Resign(multi_account=False, log=True),
            BT.Wait(3000),
            BT.WaitForMapLoad(map_id=641, timeout_ms=45_000),
            BT.MoveAndDialog((25203, -10694), dialog_id=0x837C07, pause_on_combat=True, log=True),
        ],
    )

def Unlock_feel_no_pain() -> BehaviorTree:
    return BT.Sequence(
        name='Unlock Feel No Pain',
        children=[
            _runtime_combat_tree(True),
            BT.Travel(target_map_name="Olafstead", log=True),
            BT.MoveAndDialog((90.00, -749.00), dialog_id=0x835201, pause_on_combat=True, log=True),
            BT.MoveAndDialog((90.00, -749.00), dialog_id=0x84, pause_on_combat=True, log=True),
            BT.WaitForMapLoad(map_name="The Great Norn Alemoot", timeout_ms=45_000),
            BT.MoveAndDialog((12602.00, -6210.00), dialog_id=0x85, pause_on_combat=True, log=True),
            BT.MoveAndInteractWithGadget(pos=(12727.00, -6612.00), pause_on_combat=True, log=True),
            BT.MoveAndInteractWithGadget(pos=(12701.00, -6523.00), pause_on_combat=True, log=True),
            BT.MoveAndInteractWithGadget(pos=(10109.00, -8707.00), pause_on_combat=True, log=True),
            BT.Move((10750.13, -9616.31), pause_on_combat=True, log=False),
            BT.MoveAndInteractWithGadget(pos=(10109.00, -8707.00), pause_on_combat=True, log=True),
            BT.Move((10750.13, -9616.31), pause_on_combat=True, log=False),
            BT.MoveAndInteractWithGadget(pos=(10109.00, -8707.00), pause_on_combat=True, log=True),
            BT.Move((10750.13, -9616.31), pause_on_combat=True, log=False),
            BT.Move((12727.00, -6612.00), pause_on_combat=True, log=False),
            BT.MoveAndInteractWithGadget(pos=(12727.00, -6612.00), pause_on_combat=True, log=True),
            BT.MoveAndInteractWithGadget(pos=(12701.00, -6523.00), pause_on_combat=True, log=True),
            BT.Move(([
                (10699.6,-7143.7),
                (10860.8,-7346.0),
                (10995.1,-7550.1),
                (10929.0,-7752.8),
                (10732.7,-7956.7),
                (10595.6,-8161.1),
                (10663.2,-8364.8),
                (10866.8,-8382.3),
                (11069.9,-8278.6),
                (11270.6,-8175.8),
                (11474.9,-8166.0),
                (11509.5,-8370.6),
                (11339.8,-8570.8),
                (11165.9,-8776.2),
                (11122.3,-8977.3),
                (11324.1,-9149.3),
                (11524.2,-9087.1),
                (11726.6,-8891.3),
                (11928.8,-8749.9),
                (12128.9,-8825.3),
                (12133.3,-9030.4),
                (11989.0,-9233.9),
                (11841.6,-9434.0),
                (11752.0,-9636.7),
                (11954.8,-9805.3),
                (12156.2,-9668.8),
                (12237.3,-9466.5),
                (12349.3,-9265.1),
                (12905.82, -9617.43)]), pause_on_combat=True, log=False),
            BT.Move((12727.00, -6612.00), pause_on_combat=True, log=False),
            BT.MoveAndInteractWithGadget(pos=(12727.00, -6612.00), pause_on_combat=True, log=True),
            BT.MoveAndInteractWithGadget(pos=(12701.00, -6523.00), pause_on_combat=True, log=True),
            BT.MoveAndDialog((12602.00, -6210.00), dialog_id=0x835207, pause_on_combat=True, log=True),
        ],
    )

def Unlock_dwarven_stability() -> BehaviorTree:
    return BT.Sequence(
        name='Unlock Dwarven Stability',
        children=[
            _runtime_combat_tree(True),
            BT.Travel(target_map_name="Sifhalla", log=True),
            BT.WaitForMapLoad(map_id=643, timeout_ms=45_000),
            BT.MoveAndDialog((12009, 24726), dialog_id=0x837E03, pause_on_combat=True, log=True),
            BT.DialogAtXY((12009, 24726), dialog_id=0x837E01, log=True),
            BT.MoveAndExitMap((13583, 18781), target_map_id=513, log=True),
            BT.WaitForMapLoad(map_id=513, timeout_ms=45_000),
            BT.Move((15159, 12506), pause_on_combat=True, log=False),
            BT.WaitUntilOutOfCombat(timeout_ms=120_000),
            BT.Resign(multi_account=False, log=True),
            BT.Wait(3000),
            BT.WaitForMapToChange(map_id=643, timeout_ms=45_000),
            BT.MoveAndDialog((12009, 24726), dialog_id=0x837E07, pause_on_combat=True, log=True),
        ],
    )

def Unlock_deft_strike() -> BehaviorTree:
    return BT.Sequence(
        name='Unlock Deft Strike',
        children=[
            _runtime_combat_tree(True),
            BT.Travel(target_map_name="Eye of the North outpost", log=True),
            BT.MoveAndDialog((-1856.00, 3073.00), dialog_id=0x836401, pause_on_combat=True, log=True),
            BT.MoveAndDialog((-1856.00, 3073.00), dialog_id=0x836404, pause_on_combat=True, log=True),
            BT.MoveAndDialog((-1856.00, 3073.00), dialog_id=0x84, pause_on_combat=True, log=True),
            BT.WaitForMapLoad(map_name="Mano a Norn-o", timeout_ms=45_000),
            BT.Move((-1470.06, 2672), pause_on_combat=True, log=False),
            BT.MoveAndDialog((-1856.00, 3073.00), dialog_id=0x836407, pause_on_combat=True, log=True),
            BT.CancelSkillRewardWindow(),
        ],
    )

def Unlock_ebon_vanguard_assassin_support() -> BehaviorTree:
    return BT.Sequence(
        name='Unlock Ebon Vanguard Assassin Support',
        children=[
            _runtime_combat_tree(True),
            BT.Travel(target_map_name="Eye of the North outpost", log=True),
            BT.MoveAndDialog((-1856.00, 3073.00), dialog_id=0x836A01, pause_on_combat=True, log=True),
            BT.MoveAndDialog((-1856.00, 3073.00), dialog_id=0x836A04, pause_on_combat=True, log=True),
            BT.MoveAndDialog((-1856.00, 3073.00), dialog_id=0x86, pause_on_combat=True, log=True),
            BT.WaitForMapLoad(map_name="Service: Practice, Dummy", timeout_ms=45_000),
            BT.Move((-1856.00, 3073.00), pause_on_combat=True, log=False),
            BT.WaitForMapLoad(map_name="Eye of the North outpost", timeout_ms=45_000),
            BT.MoveAndDialog((-1856.00, 3073.00), dialog_id=0x836A07, pause_on_combat=True, log=True),
            BT.CancelSkillRewardWindow(),
        ],
    )

def Unlock_winds() -> BehaviorTree:
    return BT.Sequence(
        name='Unlock Winds',
        children=[
            _runtime_combat_tree(True),
            BT.Travel(target_map_name="Eye of the North outpost", log=True),
            BT.MoveAndDialog((-1856.00, 3073.00), dialog_id=0x835601, pause_on_combat=True, log=True),
            BT.Travel(target_map_name="Gunnar's Hold", log=True),
            _add_winds_heroes_tree(),
            BT.Wait(2000),
            _add_winds_henchmen_tree(),
            BT.MoveAndExitMap((15183.199218, -6381.958984), target_map_name="Norrhart Domains", log=True),
            BT.Move(([
                (14576.0,-6137.7),
                (14568.2,-5136.7),
                (14112.5,-4135.1),
                (13107.6,-3750.6),
                (12600.1,-2745.8),
                (12484.4,-1739.7),
                (12528.0,-732.3),
                (11619.6,313.6),
                (11527.4,1316.2),
                (10823.6,2318.0)]), pause_on_combat=True, log=False),
            BT.WaitUntilOutOfCombat(timeout_ms=120_000),
            BT.Travel(target_map_name="Eye of the North outpost", log=True),
            BT.MoveAndDialog((-1856.00, 3073.00), dialog_id=0x835607, pause_on_combat=True, log=True),
            BT.CancelSkillRewardWindow(),
        ],
    )

def Unlock_you_move_like_a_dwarf() -> BehaviorTree:
    return BT.Sequence(
        name='Unlock "You Move Like a Dwarf!"',
        children=[
            _runtime_combat_tree(True),
            BT.MoveAndDialog((14380, 23968), dialog_id=0x833A01, pause_on_combat=True, log=True),
            BT.MoveAndExitMap((8832, 23870), target_map_id=513, log=True),
            BT.WaitForMapLoad(map_id=513, timeout_ms=45_000),
            BT.Move((11434, 19708), pause_on_combat=True, log=False),
            BT.Move((14164, 2682), pause_on_combat=True, log=False),
            BT.Move((9435, -5806), pause_on_combat=True, log=False),
            BT.WaitUntilOutOfCombat(timeout_ms=120_000),
            BT.Move((1914, -6963), pause_on_combat=True, log=False),
            BT.WaitUntilOutOfCombat(timeout_ms=120_000),
            BT.Move((4735, -14202), pause_on_combat=True, log=False),
            BT.Move((5752, -15236), pause_on_combat=True, log=False),
            BT.Move((8924, -15922), pause_on_combat=True, log=False),
            BT.Move((14134, -16744), pause_on_combat=True, log=False),
            BT.Move((12581, -19343), pause_on_combat=True, log=False),
            BT.Move((12702, -23855), pause_on_combat=True, log=False),
            BT.Move((13952, -23063), pause_on_combat=True, log=False),
            BT.Wait(45000),
            BT.Resign(multi_account=False, log=True),
            BT.Wait(3000),
            BT.WaitForMapLoad(map_id=643, timeout_ms=45_000),
            BT.MoveAndDialog((14380, 23968), dialog_id=0x833A07, pause_on_combat=True, log=True),
            BT.CancelSkillRewardWindow(),
        ],
    )

def Unlock_i_am_unstoppable() -> BehaviorTree:
    return BT.Sequence(
        name='Unlock "I Am Unstoppable!"',
        children=[
            _runtime_combat_tree(True),
            BT.Travel(target_map_name="Sifhalla", log=True),
            BT.WaitForMapLoad(map_id=643, timeout_ms=45_000),
            BT.MoveAndDialog((14380, 23874), dialog_id=0x833E01, pause_on_combat=True, log=True),
            BT.Move((14682, 22900), pause_on_combat=True, log=False),
            BT.MoveAndExitMap((17000, 22872), target_map_id=546, log=True),
            BT.WaitForMapLoad(map_id=546, timeout_ms=45_000),
            BT.Move((-9431, -20124), pause_on_combat=True, log=False),
            BT.Move((-8441, -13685), pause_on_combat=True, log=False),
            BT.Move((-9743, -6744), pause_on_combat=True, log=False),
            BT.Move((-10672, 4815), pause_on_combat=True, log=False),
            BT.Move((-8464, 17239), pause_on_combat=True, log=False),
            BT.Move((-11700, 24101), pause_on_combat=True, log=False),
            BT.WaitUntilOutOfCombat(timeout_ms=120_000),
            BT.Move((-8464, 17239), pause_on_combat=True, log=False),
            BT.Move((-638, 17801), pause_on_combat=True, log=False),
            BT.Move((-933, 15368), pause_on_combat=True, log=False),
            BT.Wait(6000),
            BT.Move((-1339, 22089), pause_on_combat=True, log=False),
            BT.Wait(5000),
            BT.Resign(multi_account=False, log=True),
            BT.WaitForMapLoad(map_id=643, timeout_ms=45_000),
            BT.MoveAndExitMap((8832, 23870), target_map_id=513, log=True),
            BT.WaitForMapLoad(map_id=513, timeout_ms=45_000),
            BT.MoveAndDialog((-10926, 24732), dialog_id=0x832901, pause_on_combat=True, log=True),
            BT.MoveAndExitMap((-12138, 26829), target_map_id=628, log=True),
            BT.WaitForMapLoad(map_id=628, timeout_ms=45_000),
            BT.Move((-5343, -15773), pause_on_combat=True, log=False),
            BT.Move((-6237, -9310), pause_on_combat=True, log=False),
            BT.Move((-7512, -8414), pause_on_combat=True, log=False),
            BT.Move((-12804, 1066), pause_on_combat=True, log=False),
            BT.Wait(5000),
            BT.Resign(multi_account=False, log=True),
            BT.Wait(3000),
            BT.WaitForMapLoad(map_id=643, timeout_ms=45_000),
            BT.MoveAndDialog((14380, 23968), dialog_id=0x833E07, pause_on_combat=True, log=True),
            BT.Travel(target_map_name="Sifhalla", log=True),
            BT.WaitForMapLoad(map_id=643, timeout_ms=45_000),
            BT.SpawnBonusItems(log=True),
            BT.EquipItemByModelID(ModelID.Bonus_Nevermore_Flatbow.value, log=True),
            BT.EquipItemByModelID(6515, log=True),
            _profession_skillbar_tree(),
            BT.MoveAndDialog((14380, 23968), dialog_id=0x834401, pause_on_combat=True, log=True),
            BT.DialogAtXY((14380, 23968), dialog_id=0x85, log=True),
            BT.WaitForMapLoad(map_id=690, timeout_ms=45_000),
            BT.Wait(5000),
            BT.Move((14553, 23043), pause_on_combat=True, log=False),
            BT.Wait(2000),
            BT.CastSkillID(114, log=True),
            BT.WaitUntilOnCombat(timeout_ms=120_000),
            BT.WaitUntilOutOfCombat(timeout_ms=120_000),
            BT.Resign(multi_account=False, log=True),
            BT.Wait(20000),
            BT.WaitForMapLoad(map_id=643, timeout_ms=45_000),
            BT.MoveAndDialog((14380, 23968), dialog_id=0x834407, pause_on_combat=True, log=True),
        ],
    )


def Unlock_air_of_superiority() -> BehaviorTree:
    return BT.Sequence(
        name='Unlock Air of Superiority',
        children=[
            _runtime_combat_tree(True),
            Unlock_previous_skills(),
            BT.Travel(target_map_name="Tarnished Haven", log=True),
            BT.MoveAndDialog((25203, -10694), dialog_id=0x837D01, pause_on_combat=True, log=True),
            BT.Travel(target_map_name="Olafstead", log=True),
            BT.MoveAndExitMap((1440, 1147.00), target_map_name="Varajar Fells", log=True),
            BT.Move(([(-2584.1,515.4),
                (-3168.0,-985.5),
                (-3228.0,-2487.7),
                (-3424.8,-3989.7),
                (-4391.7,-2487.7),
                (-4291.6,-987.4),
                (-3990.1,512.9),
                (-3273.5,2013.5),
                (-2242.5,3515.2),
                (-975.6,5015.6),
                (527.6,5854.7),
                (2031.6,5378.3),
                (3536.6,5030.3),
                (5041.9,4768.3),
                (6545.9,5184.7),
                (8050.1,5978.9),
                (9552.6,6651.4),
                (11053.5,6855.5),
                (12558.9,7385.4),
                (14059.8,6908.5),
                (15561.8,6764.8),
                (17064.0,5965.7),
                (17953.4,4465.6),
                (19457.1,3896.6),
                (20957.5,3474.3),
                (23571.6,1778.8)]), pause_on_combat=True, log=False),
            BT.WaitUntilOutOfCombat(timeout_ms=120_000),
            BT.MoveAndDialog((22648.00, 1078.00), dialog_id=0x837D07, pause_on_combat=True, log=True),
            BT.CancelSkillRewardWindow(),
            BT.Resign(multi_account=False, log=True),
            BT.WaitForMapLoad(map_name="Olafstead", timeout_ms=45_000),
        ],
    )
     


def Unlock_asuran_scan() -> BehaviorTree:
    return BT.Sequence(
        name='Unlock Asuran Scan',
        children=[
            _runtime_combat_tree(True),
            BT.Travel(target_map_name="Tarnished Haven", log=True),
            BT.MoveAndDialog((25203, -10694), dialog_id=0x837901, pause_on_combat=True, log=True),
            BT.Travel(target_map_name="Gadd's Encampment", log=True),
            BT.MoveAndExitMap((-9690, -19524), target_map_name="Sparkfly Swamp", log=True),
            BT.Move(([(-11165.4,-18283.9),    (-11328.1,-17780.3),    (-11384.3,-17280.2),    (-11334.4,-16778.1),    (-11299.2,-16276.2),    (-11329.3,-15772.8),    (-11316.9,-15269.3),    (-11349.1,-14767.7),    (-11348.2,-14267.3),    (-11384.4,-13765.5),    (-11316.9,-13265.2),    (-11233.8,-12765.2),    (-11150.5,-12263.8),    (-11067.2,-11762.9),    (-10896.6,-11260.0),    (-10667.6,-10758.3),    (-10461.4,-10258.3),    (-10254.9,-9757.7),    (-10064.7,-9256.7),    (-9835.3,-8756.4),    (-9718.4,-8251.5),    (-9640.7,-7750.0),    (-9561.5,-7249.7),    (-9512.5,-6749.1),    (-9480.4,-6248.2),    (-9458.3,-5743.9),    (-9469.2,-5241.0),    (-9559.7,-4740.4),    (-9232.6,-4238.3),    (-8888.4,-3737.5),    (-8548.9,-3233.5),    (-8232.0,-2729.6),    (-8124.7,-2227.3),    (-8145.7,-1727.3),    (-8172.7,-1223.1),    (-8213.0,-718.8),    (-8263.4,-217.4),    (-8315.9,285.3),    (-8388.2,789.5),    (-8511.6,1292.5),    (-8647.4,1797.6),    (-8766.6,2301.6),    (-9177.1,2804.6),    (-9641.8,3305.0),    (-9964.5,3809.8),    (-9928.1,4311.3),    (-9428.2,4814.2),    (-8927.0,5191.5),    (-8443.6,5693.6),    (-7941.2,5822.0),    (-7440.0,5904.8),    (-6935.2,5990.9),    (-6431.5,6070.9),    (-5925.0,6133.0),    (-5422.3,6192.9),    (-4917.6,6210.4),    (-4415.9,6234.1),    (-3914.2,6258.1),    (-3413.2,6288.2),    (-2911.0,6320.1),    (-2406.6,6352.2),    (-1902.5,6292.1),    (-1401.4,6104.2),    (-898.4,5923.1),    (-396.5,5874.6),    (107.0,5793.2),    (607.5,5705.9),    (1111.0,5617.4),    (1612.5,5529.3),    (2114.7,5559.1),    (2616.7,5820.9),    (3119.0,6102.4),    (3620.1,6494.9),    (4121.1,6888.0),    (4623.3,7275.8),    (5124.6,7435.8),    (5626.4,7537.5),    (6080.2,7037.3),    (6438.3,6533.6),    (6795.6,6031.0),    (7296.8,5720.0),    (7797.8,5498.1),    (8299.2,5427.9),    (8799.6,5350.6),    (9300.5,5511.6),    (9802.5,5812.5),    (10346.69,8246.0),    (10808.6,6189.0),    (11311.0,6333.2),    (11302.6,5831.4),    (11248.2,5330.4),    (11210.3,4828.7),    (11132.2,4326.2),    (11034.8,3821.7),    (10937.3,3320.5),   (10839.4,2817.3),    (10741.8,2315.8),    (10644.0,1813.2),    (10530.5,1311.6),    (10410.4,807.9),    (10264.4,304.8),    (10117.4,-196.6),    (10220.3,-697.2),    (10295.1,-1198.7),    (9793.1,-1453.9),    (9289.4,-1546.0),    (8787.0,-1543.4),    (8286.1,-1480.6),    (7785.1,-1417.8),    (7285.0,-1355.1),    (6779.9,-1303.0),    (6276.2,-1185.9),    (5774.2,-1006.9),    (5272.1,-1011.6),    (4769.0,-1198.1),    (4264.9,-1441.2),    (3764.1,-1665.9),    (3823.0,-2168.4),    (4325.4,-2468.7),    (4828.8,-2117.9),    (5331.0,-1838.1),    (5833.0,-1559.3),    (6319.6,-1055.8),    (6395.2,-554.3),    (6346.1,-53.7),    (6292.7,447.5),    (6241.4,950.9),    (6140.5,1451.3),    (6090.1,1953.7),    (6039.9,2455.2),    (5728.8,2957.0),    (5271.5,3458.7),    (4767.9,3612.2),    (4350.9,3108.4),    (3865.1,2604.3),    (3657.0,2100.5),    (3460.4,1598.3),(3360.7,1463.1)]), pause_on_combat=True, log=False),
            BT.WaitUntilOutOfCombat(timeout_ms=120_000),
            BT.Wait(10000),
            BT.Resign(multi_account=False, log=True),
            BT.WaitForMapLoad(map_name="Gadd's Encampment", timeout_ms=45_000),
            BT.Travel(target_map_name="Tarnished Haven", log=True),
            BT.MoveAndDialog((25203, -10694), dialog_id=0x837907, pause_on_combat=True, log=True),
            BT.CancelSkillRewardWindow(),
        ],
    )

def Unlock_radiation_field() -> BehaviorTree:
    return BT.Sequence(
        name='Unlock Radiation Field',
        children=[
            _runtime_combat_tree(True),
            BT.Travel(target_map_name="Tarnished Haven", log=True),
            BT.MoveAndDialog((25203, -10694), dialog_id=0x837801, pause_on_combat=True, log=True),
            BT.Travel(target_map_name="Rata Sum", log=True),
            BT.MoveAndExitMap((20340, 16899), target_map_name="Riven Earth", log=True),
            BT.Move(([(-21603.1,8285.9),
                (-21798.3,9288.2),
                (-21789.4,10290.0),
                (-21909.8,11293.0),
                (-22083.2,12295.0),
                (-21079.4,12098.4),
                (-20077.3,11811.3),
                (-19076.9,11615.3),
                (-18075.5,11247.0),
                (-17073.4,10500.9),
                (-16247.2,9500.6),
                (-15282.3,8499.2),
                (-14280.3,7593.8),
                (-13275.6,7853.4),
                (-12272.0,8145.0),
                (-11268.3,8416.7),
                (-10266.5,7814.2),
                (-9364.5,6812.3),
                (-8361.9,6094.6),
                (-7359.9,6144.0),
                (-6355.5,6385.9),
                (-5405.8,7386.0),
                (-4936.1,8388.2),
                (-4396.1,9390.1),
                (-3394.9,9932.9),
                (-2391.5,9843.4),
                (-1391.0,9588.0),
                (1618.8,8503.5),
                (2311.4,11804.0),
                (3313.1,12027.4),
                (4316.5,11849.2),
                (5316.6,12024.3),
                (6318.5,11885.3),
                (7320.1,11537.4),
                (8321.1,11136.9),
                (9321.7,10593.2),
                (10324.7,10049.8),
                (11326.2,9505.4),
                (14718.8,5965.5),
                (15255.1,4964.5),
                (15921.5,3964.5),
                (16391.0,2962.0),
                (16474.3,1958.2),
                (17130.1,955.1),
                (17756.3,-45.2),
                (18257.8,-1046.1),
                (19065.4,-2046.7),
                (19437.0,-3050.3),
                (19807.5,-4051.0),
                (20178.1,-5052.2),
                (20671.6,-6054.6),
                (20041.9,-5054.5),
                (19039.5,-5913.2),
                (18158.3,-6913.3),
                (17246.3,-7913.5),
                (16287.2,-8914.5),
                (15287.1,-9047.3),
                (14284.6,-9227.9),
                (13283.0,-9408.5),
                (12281.7,-9672.8),
                (11281.3,-9987.0),
                (10280.3,-10117.4),
                (9278.4,-10264.2),
                (8278.3,-10399.0),
                (7275.8,-10447.3),
                (6274.1,-10469.4),
                (5271.4,-10193.3),
                (4270.0,-9822.4),
                (3268.8,-9567.0),
                (2265.5,-9244.4),
                (1263.1,-8930.2),
                (261.3,-8352.1),
                (-740.2,-7670.2),
                (-1556.0,-6669.4),
                (-2414.9,-5668.4),
                (-3224.1,-4665.7),
                (-4227.5,-3773.8),
                ]), pause_on_combat=True, log=False),
            BT.WaitUntilOutOfCombat(timeout_ms=120_000),
            BT.Move((-5226.4, -2772.8), pause_on_combat=True, log=False),
            BT.Wait(10000),
            BT.Resign(multi_account=False, log=True),
            BT.WaitUntilOutOfCombat(timeout_ms=120_000),
            BT.WaitForMapLoad(map_name="Rata Sum", timeout_ms=45_000),
            BT.Travel(target_map_name="Tarnished Haven", log=True),
            BT.MoveAndDialog((25203, -10694), dialog_id=0x837807, pause_on_combat=True, log=True),
            BT.CancelSkillRewardWindow(),
        ],
    )

def Unlock_mindbender() -> BehaviorTree:
    return _not_implemented_tree("Mindbender")


def Unlock_technobabble() -> BehaviorTree:
    return BT.Sequence(
        name='Unlock Technobabble',
        children=[
            _runtime_combat_tree(True),
            BT.Travel(target_map_name="Tarnished Haven", log=True),
            BT.MoveAndDialog((25203, -10694), dialog_id=0x837B01, pause_on_combat=True, log=True),
            BT.Travel(target_map_name="Rata Sum", log=True),
            BT.MoveAndExitMap((-6062, -2688), target_map_name="Magus Stones", log=True),
            BT.Move(([(16333.0,13134.0),
                (15831.3,12689.2),
                (14826.0,12244.9),
                (13819.6,11800.6),
                (12815.3,11338.3),
                (12323.8,10334.1),
                (11980.6,9332.0),
                (10972.8,8700.9),
                (9966.2,8792.9),
                (8965.1,9574.6),
                (7958.7,10437.8),
                (7435.5,11444.1),
                (6956.4,12448.6),
                (6460.2,13452.2),
                (5804.7,14341.9),
                (4799.9,14136.0),
                (3795.5,13944.2),
                (2793.6,13807.8),
                (1791.5,13711.2),
                (787.7,14183.2),
                (-214.4,13677.2),
                (-737.5,12676.2),
                (-1511.9,11673.6),
                (-2135.2,10670.0),
                (-2655.5,9665.3),
                (-3659.5,9939.1),
                (-4665.0,9846.3),
                (-5668.2,9829.6),
                (-6672.9,10007.4),
                (-7178.3,9004.0),
                (-7180.2,8000.7),
                (-7533.2,9006.4),
                (-8537.4,9423.0),
                (-9538.6,9947.0),
                (-10539.4,10902.5),
                (-10997.0,11906.4),
                (-10826.9,12910.9),
                (-10739.5,13913.7),
                (-10731.4,14918.5),
                (-11405.8,16127.1),
                (-12410.1,15642.0),
                (-13412.0,15177.1),
                (-14418.9,14726.5),
                (-15421.4,14567.4),
                (-16426.4,14590.7),
                (-17430.9,14742.7),
                (-17579.8,13740.1),
                (-18287.3,14623.7),]), pause_on_combat=True, log=False),
            BT.WaitUntilOutOfCombat(timeout_ms=120_000),
            BT.Move((list(reversed(([(16333.0,13134.0),
                (15831.3,12689.2),
                (14826.0,12244.9),
                (13819.6,11800.6),
                (12815.3,11338.3),
                (12323.8,10334.1),
                (11980.6,9332.0),
                (10972.8,8700.9),
                (9966.2,8792.9),
                (8965.1,9574.6),
                (7958.7,10437.8),
                (7435.5,11444.1),
                (6956.4,12448.6),
                (6460.2,13452.2),
                (5804.7,14341.9),
                (4799.9,14136.0),
                (3795.5,13944.2),
                (2793.6,13807.8),
                (1791.5,13711.2),
                (787.7,14183.2),
                (-214.4,13677.2),
                (-737.5,12676.2),
                (-1511.9,11673.6),
                (-2135.2,10670.0),
                (-2655.5,9665.3),
                (-3659.5,9939.1),
                (-4665.0,9846.3),
                (-5668.2,9829.6),
                (-6672.9,10007.4),
                (-7178.3,9004.0),
                (-7180.2,8000.7),
                (-7533.2,9006.4),
                (-8537.4,9423.0),
                (-9538.6,9947.0),
                (-10539.4,10902.5),
                (-10997.0,11906.4),
                (-10826.9,12910.9),
                (-10739.5,13913.7),
                (-10731.4,14918.5),
                (-11405.8,16127.1),
                (-12410.1,15642.0),
                (-13412.0,15177.1),
                (-14418.9,14726.5),
                (-15421.4,14567.4),
                (-16426.4,14590.7),
                (-17430.9,14742.7),
                (-17579.8,13740.1),
                (-18287.3,14623.7),])))), pause_on_combat=True, log=False),
            BT.WaitUntilOutOfCombat(timeout_ms=120_000),
            BT.Move(([(16029.7,12397.9),
                (15026.6,12140.9),
                (14025.6,11883.9),
                (13371.9,10881.3),
                (12902.8,9874.1),
                (12694.8,8871.6),
                (12506.1,7866.6),
                (11497.3,7588.6),
                (10484.8,7371.9),
                (9480.5,6952.3),
                (9145.1,7044.0),
                (9620.1,6039.9),
                (10161.9,5033.7),
                (10405.3,4027.2),
                (10317.9,3024.2),
                (9724.4,2022.1),
                (8833.3,1015.3),
                (7832.5,507.9),
                (6830.2,23.6),
                (5824.7,-490.1),
                (4822.4,-1027.4),
                (3941.5,-1783.5),
                (2951.3,-2653.6),
                (2170.4,-3524.7),
                (1746.0,-4528.3),
                (1487.5,-5532.6),
                (1182.3,-6537.0),
                (1026.8,-7039.6)]), pause_on_combat=True, log=False),
            BT.WaitUntilOutOfCombat(timeout_ms=120_000),
            BT.Wait(10000),
            BT.Resign(multi_account=False, log=True),
            BT.WaitForMapLoad(map_name="Rata Sum", timeout_ms=45_000),
            BT.Travel(target_map_name="Tarnished Haven", log=True),
            BT.MoveAndDialog((25203, -10694), dialog_id=0x837B07, pause_on_combat=True, log=True),
            BT.CancelSkillRewardWindow(),
        ],
    )


def Unlock_pain_inverter() -> BehaviorTree:
    return BT.Sequence(
        name='Unlock Pain Inverter',
        children=[
            _runtime_combat_tree(True),
            BT.Travel(target_map_name="Tarnished Haven", log=True),
            BT.MoveAndDialog((25203, -10694), dialog_id=0x837A01, pause_on_combat=True, log=True),
            BT.Travel(target_map_name="Vlox's Falls", log=True),
            BT.MoveAndExitMap((15505.38, 12460.59), target_map_name="Arbor Bay", log=True),
            BT.Move(([(14323.3,10846.0),
                    (12813.3,10172.5),
                    (12706.6,8670.7),
                    (12046.3,7170.5),
                    (11401.4,5666.6),
                    (11104.1,4165.7),
                    (12380.1,2655.5),
                    (13838.0,5496.0),                   #maybe need separe si point and add wait.fortime(5000) for the fight
                    (13645.2,2661.5),
                    (12136.8,1741.7),
                    (10629.4,1175.4),
                    (9118.9,404.5),
                    (7617.1,708.9),
                    (6114.2,1110.0),
                    (4613.7,1104.7),
                    (3324.0,2520.8),
                    (2059.3,1018.5),
                    (554.7,-202.7),                     #maybe need separe si point and add wait.fortime(5000) for the fight
                    (-947.4,-1268.4),
                    (-2451.0,-1768.3),
                    (-3292.4,-3271.8),
                    (-4334.0,-4776.2),
                    (-5233.3,-6280.5),
                    (-5660.5,-7790.6),
                    (-4604.2,-9290.9),
                    (-4368.7,-10796.7),
                    (-5871.9,-11996.5),
                    (-7377.8,-11568.5),
                    (-8885.3,-10854.7),
                    (-9333.4,-12357.6),                 #maybe need separe si point and add wait.fortime(5000) for the fight
                    (-452.2,-13283.1),
                    (371.6,-11782.2),
                    (-149.9,-10277.5),                  #maybe need separe si point and add wait.fortime(5000) for the fight
                    ]), pause_on_combat=True, log=False),
            BT.WaitUntilOutOfCombat(timeout_ms=120_000),
            BT.Wait(10000),
            BT.Resign(multi_account=False, log=True),
            BT.WaitForMapLoad(map_name="Vlox's Falls", timeout_ms=45_000),
            BT.Travel(target_map_name="Tarnished Haven", log=True),
            BT.MoveAndDialog((25203, -10694), dialog_id=0x837A07, pause_on_combat=True, log=True),
            BT.CancelSkillRewardWindow(),
        ],
    )

def Unlock_i_am_the_strongest() -> BehaviorTree:
    return _not_implemented_tree('"I Am the Strongest!"')

def Unlock_previous_skills() -> BehaviorTree:
    return BT.Sequence(
        name='Unlock Previous Skills',
        children=[
            _runtime_combat_tree(True),
            BT.Travel(target_map_id=641, log=True),
            BT.WaitForMapLoad(map_id=641, timeout_ms=45_000),
            BT.MoveAndDialog((25203, -10694), dialog_id=0x837C01, pause_on_combat=True, log=True),
            BT.Move((18781, -10477), pause_on_combat=True, log=False),
            BT.WaitForMapLoad(map_name="Alcazia Tangle", timeout_ms=45_000),
            BT.Move((17024, -600), pause_on_combat=True, log=False),
            BT.Move((18237, 6691), pause_on_combat=True, log=False),
            BT.Move((15518, 8375), pause_on_combat=True, log=False),
            BT.Move((13200, 15000), pause_on_combat=True, log=False),
            BT.Wait(3000),
            BT.WaitUntilOutOfCombat(timeout_ms=120_000),
            BT.Move((19516, 4686), pause_on_combat=True, log=False),
            BT.Move((12184, 370), pause_on_combat=True, log=False),
            BT.Move((4802, -4990), pause_on_combat=True, log=False),
            BT.Move((-8760, -3378), pause_on_combat=True, log=False),
            BT.Move((-5555, -2108), pause_on_combat=True, log=False),
            BT.Move((-6678, 6477), pause_on_combat=True, log=False),
            BT.Wait(3000),
            BT.WaitUntilOutOfCombat(timeout_ms=120_000),
            BT.Move((-8860, -3178), pause_on_combat=True, log=False),
            BT.Move((-11202, 758), pause_on_combat=True, log=False),
            BT.Wait(3000),
            BT.WaitUntilOutOfCombat(timeout_ms=120_000),
            BT.Resign(multi_account=False, log=True),
            BT.Wait(3000),
            BT.WaitForMapLoad(map_id=641, timeout_ms=45_000),
            BT.MoveAndDialog((25203, -10694), dialog_id=0x837C07, pause_on_combat=True, log=True),
            BT.CancelSkillRewardWindow(),
            BT.MoveAndDialog((25203, -10694), dialog_id=0x837701, pause_on_combat=True, log=True),
            BT.Travel(target_map_id=639, log=True),
            BT.Move((-22999, 6530), pause_on_combat=True, log=False),
            BT.WaitForMapLoad(map_id=566, timeout_ms=45_000),
            BT.Move((-9761, -8000), pause_on_combat=True, log=False),
            BT.Move((7622, -9747), pause_on_combat=True, log=False),
            BT.Move((11690, -6215), pause_on_combat=True, log=False),
            BT.Move((15918, -2667), pause_on_combat=True, log=False),
            BT.Wait(3000),
            BT.WaitUntilOutOfCombat(timeout_ms=120_000),
            BT.Resign(multi_account=False, log=True),
            BT.WaitForMapLoad(map_id=639, timeout_ms=45_000),
            BT.Travel(target_map_id=641, log=True),
            BT.MoveAndDialog((25203, -10694), dialog_id=0x837707, pause_on_combat=True, log=True),
            BT.CancelSkillRewardWindow(),
            BT.Travel(target_map_name="Tarnished Haven", log=True),
            BT.MoveAndDialog((25203, -10694), dialog_id=0x837801, pause_on_combat=True, log=True),
            BT.Travel(target_map_name="Rata Sum", log=True),
            BT.MoveAndExitMap((20340, 16899), target_map_name="Riven Earth", log=True),
            BT.Move(([(-21603.1,8285.9),
                (-21798.3,9288.2),
                (-21789.4,10290.0),
                (-21909.8,11293.0),
                (-22083.2,12295.0),
                (-21079.4,12098.4),
                (-20077.3,11811.3),
                (-19076.9,11615.3),
                (-18075.5,11247.0),
                (-17073.4,10500.9),
                (-16247.2,9500.6),
                (-15282.3,8499.2),
                (-14280.3,7593.8),
                (-13275.6,7853.4),
                (-12272.0,8145.0),
                (-11268.3,8416.7),
                (-10266.5,7814.2),
                (-9364.5,6812.3),
                (-8361.9,6094.6),
                (-7359.9,6144.0),
                (-6355.5,6385.9),
                (-5405.8,7386.0),
                (-4936.1,8388.2),
                (-4396.1,9390.1),
                (-3394.9,9932.9),
                (-2391.5,9843.4),
                (-1391.0,9588.0),
                (1618.8,8503.5),
                (2311.4,11804.0),
                (3313.1,12027.4),
                (4316.5,11849.2),
                (5316.6,12024.3),
                (6318.5,11885.3),
                (7320.1,11537.4),
                (8321.1,11136.9),
                (9321.7,10593.2),
                (10324.7,10049.8),
                (11326.2,9505.4),
                (14718.8,5965.5),
                (15255.1,4964.5),
                (15921.5,3964.5),
                (16391.0,2962.0),
                (16474.3,1958.2),
                (17130.1,955.1),
                (17756.3,-45.2),
                (18257.8,-1046.1),
                (19065.4,-2046.7),
                (19437.0,-3050.3),
                (19807.5,-4051.0),
                (20178.1,-5052.2),
                (20671.6,-6054.6),
                (20041.9,-5054.5),
                (19039.5,-5913.2),
                (18158.3,-6913.3),
                (17246.3,-7913.5),
                (16287.2,-8914.5),
                (15287.1,-9047.3),
                (14284.6,-9227.9),
                (13283.0,-9408.5),
                (12281.7,-9672.8),
                (11281.3,-9987.0),
                (10280.3,-10117.4),
                (9278.4,-10264.2),
                (8278.3,-10399.0),
                (7275.8,-10447.3),
                (6274.1,-10469.4),
                (5271.4,-10193.3),
                (4270.0,-9822.4),
                (3268.8,-9567.0),
                (2265.5,-9244.4),
                (1263.1,-8930.2),
                (261.3,-8352.1),
                (-740.2,-7670.2),
                (-1556.0,-6669.4),
                (-2414.9,-5668.4),
                (-3224.1,-4665.7),
                (-4227.5,-3773.8),
                ]), pause_on_combat=True, log=False),
            BT.WaitUntilOutOfCombat(timeout_ms=120_000),
            BT.Move((-5226.4, -2772.8), pause_on_combat=True, log=False),
            BT.Wait(10000),
            BT.Resign(multi_account=False, log=True),
            BT.WaitUntilOutOfCombat(timeout_ms=120_000),
            BT.WaitForMapLoad(map_name="Rata Sum", timeout_ms=45_000),
            BT.Travel(target_map_name="Tarnished Haven", log=True),
            BT.MoveAndDialog((25203, -10694), dialog_id=0x837807, pause_on_combat=True, log=True),
            BT.CancelSkillRewardWindow(),
            BT.Travel(target_map_name="Tarnished Haven", log=True),
            BT.MoveAndDialog((25203, -10694), dialog_id=0x837901, pause_on_combat=True, log=True),
            BT.Travel(target_map_name="Gadd's Encampment", log=True),
            BT.MoveAndExitMap((-9690, -19524), target_map_name="Sparkfly Swamp", log=True),
            BT.Move(([(-11165.4,-18283.9),    (-11328.1,-17780.3),    (-11384.3,-17280.2),    (-11334.4,-16778.1),    (-11299.2,-16276.2),    (-11329.3,-15772.8),    (-11316.9,-15269.3),    (-11349.1,-14767.7),    (-11348.2,-14267.3),    (-11384.4,-13765.5),    (-11316.9,-13265.2),    (-11233.8,-12765.2),    (-11150.5,-12263.8),    (-11067.2,-11762.9),    (-10896.6,-11260.0),    (-10667.6,-10758.3),    (-10461.4,-10258.3),    (-10254.9,-9757.7),    (-10064.7,-9256.7),    (-9835.3,-8756.4),    (-9718.4,-8251.5),    (-9640.7,-7750.0),    (-9561.5,-7249.7),    (-9512.5,-6749.1),    (-9480.4,-6248.2),    (-9458.3,-5743.9),    (-9469.2,-5241.0),    (-9559.7,-4740.4),    (-9232.6,-4238.3),    (-8888.4,-3737.5),    (-8548.9,-3233.5),    (-8232.0,-2729.6),    (-8124.7,-2227.3),    (-8145.7,-1727.3),    (-8172.7,-1223.1),    (-8213.0,-718.8),    (-8263.4,-217.4),    (-8315.9,285.3),    (-8388.2,789.5),    (-8511.6,1292.5),    (-8647.4,1797.6),    (-8766.6,2301.6),    (-9177.1,2804.6),    (-9641.8,3305.0),    (-9964.5,3809.8),    (-9928.1,4311.3),    (-9428.2,4814.2),    (-8927.0,5191.5),    (-8443.6,5693.6),    (-7941.2,5822.0),    (-7440.0,5904.8),    (-6935.2,5990.9),    (-6431.5,6070.9),    (-5925.0,6133.0),    (-5422.3,6192.9),    (-4917.6,6210.4),    (-4415.9,6234.1),    (-3914.2,6258.1),    (-3413.2,6288.2),    (-2911.0,6320.1),    (-2406.6,6352.2),    (-1902.5,6292.1),    (-1401.4,6104.2),    (-898.4,5923.1),    (-396.5,5874.6),    (107.0,5793.2),    (607.5,5705.9),    (1111.0,5617.4),    (1612.5,5529.3),    (2114.7,5559.1),    (2616.7,5820.9),    (3119.0,6102.4),    (3620.1,6494.9),    (4121.1,6888.0),    (4623.3,7275.8),    (5124.6,7435.8),    (5626.4,7537.5),    (6080.2,7037.3),    (6438.3,6533.6),    (6795.6,6031.0),    (7296.8,5720.0),    (7797.8,5498.1),    (8299.2,5427.9),    (8799.6,5350.6),    (9300.5,5511.6),    (9802.5,5812.5),    (10346.69,8246.0),    (10808.6,6189.0),    (11311.0,6333.2),    (11302.6,5831.4),    (11248.2,5330.4),    (11210.3,4828.7),    (11132.2,4326.2),    (11034.8,3821.7),    (10937.3,3320.5),   (10839.4,2817.3),    (10741.8,2315.8),    (10644.0,1813.2),    (10530.5,1311.6),    (10410.4,807.9),    (10264.4,304.8),    (10117.4,-196.6),    (10220.3,-697.2),    (10295.1,-1198.7),    (9793.1,-1453.9),    (9289.4,-1546.0),    (8787.0,-1543.4),    (8286.1,-1480.6),    (7785.1,-1417.8),    (7285.0,-1355.1),    (6779.9,-1303.0),    (6276.2,-1185.9),    (5774.2,-1006.9),    (5272.1,-1011.6),    (4769.0,-1198.1),    (4264.9,-1441.2),    (3764.1,-1665.9),    (3823.0,-2168.4),    (4325.4,-2468.7),    (4828.8,-2117.9),    (5331.0,-1838.1),    (5833.0,-1559.3),    (6319.6,-1055.8),    (6395.2,-554.3),    (6346.1,-53.7),    (6292.7,447.5),    (6241.4,950.9),    (6140.5,1451.3),    (6090.1,1953.7),    (6039.9,2455.2),    (5728.8,2957.0),    (5271.5,3458.7),    (4767.9,3612.2),    (4350.9,3108.4),    (3865.1,2604.3),    (3657.0,2100.5),    (3460.4,1598.3),(3360.7,1463.1)]), pause_on_combat=True, log=False),
            BT.WaitUntilOutOfCombat(timeout_ms=120_000),
            BT.Wait(10000),
            BT.Resign(multi_account=False, log=True),
            BT.WaitForMapLoad(map_name="Gadd's Encampment", timeout_ms=45_000),
            BT.Travel(target_map_name="Tarnished Haven", log=True),
            BT.MoveAndDialog((25203, -10694), dialog_id=0x837907, pause_on_combat=True, log=True),
            BT.CancelSkillRewardWindow(),
            BT.Travel(target_map_name="Tarnished Haven", log=True),
            BT.MoveAndDialog((25203, -10694), dialog_id=0x837B01, pause_on_combat=True, log=True),
            BT.Travel(target_map_name="Rata Sum", log=True),
            BT.MoveAndExitMap((-6062, -2688), target_map_name="Magus Stones", log=True),
            BT.Move(([(16333.0,13134.0),
                (15831.3,12689.2),
                (14826.0,12244.9),
                (13819.6,11800.6),
                (12815.3,11338.3),
                (12323.8,10334.1),
                (11980.6,9332.0),
                (10972.8,8700.9),
                (9966.2,8792.9),
                (8965.1,9574.6),
                (7958.7,10437.8),
                (7435.5,11444.1),
                (6956.4,12448.6),
                (6460.2,13452.2),
                (5804.7,14341.9),
                (4799.9,14136.0),
                (3795.5,13944.2),
                (2793.6,13807.8),
                (1791.5,13711.2),
                (787.7,14183.2),
                (-214.4,13677.2),
                (-737.5,12676.2),
                (-1511.9,11673.6),
                (-2135.2,10670.0),
                (-2655.5,9665.3),
                (-3659.5,9939.1),
                (-4665.0,9846.3),
                (-5668.2,9829.6),
                (-6672.9,10007.4),
                (-7178.3,9004.0),
                (-7180.2,8000.7),
                (-7533.2,9006.4),
                (-8537.4,9423.0),
                (-9538.6,9947.0),
                (-10539.4,10902.5),
                (-10997.0,11906.4),
                (-10826.9,12910.9),
                (-10739.5,13913.7),
                (-10731.4,14918.5),
                (-11405.8,16127.1),
                (-12410.1,15642.0),
                (-13412.0,15177.1),
                (-14418.9,14726.5),
                (-15421.4,14567.4),
                (-16426.4,14590.7),
                (-17430.9,14742.7),
                (-17579.8,13740.1),
                (-18287.3,14623.7),]), pause_on_combat=True, log=False),
            BT.WaitUntilOutOfCombat(timeout_ms=120_000),
            BT.Move((list(reversed(([(16333.0,13134.0),
                (15831.3,12689.2),
                (14826.0,12244.9),
                (13819.6,11800.6),
                (12815.3,11338.3),
                (12323.8,10334.1),
                (11980.6,9332.0),
                (10972.8,8700.9),
                (9966.2,8792.9),
                (8965.1,9574.6),
                (7958.7,10437.8),
                (7435.5,11444.1),
                (6956.4,12448.6),
                (6460.2,13452.2),
                (5804.7,14341.9),
                (4799.9,14136.0),
                (3795.5,13944.2),
                (2793.6,13807.8),
                (1791.5,13711.2),
                (787.7,14183.2),
                (-214.4,13677.2),
                (-737.5,12676.2),
                (-1511.9,11673.6),
                (-2135.2,10670.0),
                (-2655.5,9665.3),
                (-3659.5,9939.1),
                (-4665.0,9846.3),
                (-5668.2,9829.6),
                (-6672.9,10007.4),
                (-7178.3,9004.0),
                (-7180.2,8000.7),
                (-7533.2,9006.4),
                (-8537.4,9423.0),
                (-9538.6,9947.0),
                (-10539.4,10902.5),
                (-10997.0,11906.4),
                (-10826.9,12910.9),
                (-10739.5,13913.7),
                (-10731.4,14918.5),
                (-11405.8,16127.1),
                (-12410.1,15642.0),
                (-13412.0,15177.1),
                (-14418.9,14726.5),
                (-15421.4,14567.4),
                (-16426.4,14590.7),
                (-17430.9,14742.7),
                (-17579.8,13740.1),
                (-18287.3,14623.7),])))), pause_on_combat=True, log=False),
            BT.WaitUntilOutOfCombat(timeout_ms=120_000),
            BT.Move(([(16029.7,12397.9),
                (15026.6,12140.9),
                (14025.6,11883.9),
                (13371.9,10881.3),
                (12902.8,9874.1),
                (12694.8,8871.6),
                (12506.1,7866.6),
                (11497.3,7588.6),
                (10484.8,7371.9),
                (9480.5,6952.3),
                (9145.1,7044.0),
                (9620.1,6039.9),
                (10161.9,5033.7),
                (10405.3,4027.2),
                (10317.9,3024.2),
                (9724.4,2022.1),
                (8833.3,1015.3),
                (7832.5,507.9),
                (6830.2,23.6),
                (5824.7,-490.1),
                (4822.4,-1027.4),
                (3941.5,-1783.5),
                (2951.3,-2653.6),
                (2170.4,-3524.7),
                (1746.0,-4528.3),
                (1487.5,-5532.6),
                (1182.3,-6537.0),
                (1026.8,-7039.6)]), pause_on_combat=True, log=False),
            BT.WaitUntilOutOfCombat(timeout_ms=120_000),
            BT.Wait(10000),
            BT.Resign(multi_account=False, log=True),
            BT.WaitForMapLoad(map_name="Rata Sum", timeout_ms=45_000),
            BT.Travel(target_map_name="Tarnished Haven", log=True),
            BT.MoveAndDialog((25203, -10694), dialog_id=0x837B07, pause_on_combat=True, log=True),
            BT.CancelSkillRewardWindow(),
            BT.Travel(target_map_name="Tarnished Haven", log=True),
            BT.MoveAndDialog((25203, -10694), dialog_id=0x837A01, pause_on_combat=True, log=True),
            BT.Travel(target_map_name="Vlox's Falls", log=True),
            BT.MoveAndExitMap((15505.38, 12460.59), target_map_name="Arbor Bay", log=True),
            BT.Move(([(14323.3,10846.0),
                    (12813.3,10172.5),
                    (12706.6,8670.7),
                    (12046.3,7170.5),
                    (11401.4,5666.6),
                    (11104.1,4165.7),
                    (12380.1,2655.5),
                    (13838.0,5496.0),                   #maybe need separe si point and add wait.fortime(5000) for the fight
                    (13645.2,2661.5),
                    (12136.8,1741.7),
                    (10629.4,1175.4),
                    (9118.9,404.5),
                    (7617.1,708.9),
                    (6114.2,1110.0),
                    (4613.7,1104.7),
                    (3324.0,2520.8),
                    (2059.3,1018.5),
                    (554.7,-202.7),                     #maybe need separe si point and add wait.fortime(5000) for the fight
                    (-947.4,-1268.4),
                    (-2451.0,-1768.3),
                    (-3292.4,-3271.8),
                    (-4334.0,-4776.2),
                    (-5233.3,-6280.5),
                    (-5660.5,-7790.6),
                    (-4604.2,-9290.9),
                    (-4368.7,-10796.7),
                    (-5871.9,-11996.5),
                    (-7377.8,-11568.5),
                    (-8885.3,-10854.7),
                    (-9333.4,-12357.6),                 #maybe need separe si point and add wait.fortime(5000) for the fight
                    (-452.2,-13283.1),
                    (371.6,-11782.2),
                    (-149.9,-10277.5),                  #maybe need separe si point and add wait.fortime(5000) for the fight
                    ]), pause_on_combat=True, log=False),
            BT.WaitUntilOutOfCombat(timeout_ms=120_000),
            BT.Wait(10000),
            BT.Resign(multi_account=False, log=True),
            BT.WaitForMapLoad(map_name="Vlox's Falls", timeout_ms=45_000),
            BT.Travel(target_map_name="Tarnished Haven", log=True),
            BT.MoveAndDialog((25203, -10694), dialog_id=0x837A07, pause_on_combat=True, log=True),
            BT.CancelSkillRewardWindow(),
        ],
    )

# -------------------------
    # Skill registry
# -------------------------
RAW_SKILLS = [
    ('air_of_superiority', 'Air of Superiority', 'Asura', 'Unlock_air_of_superiority', 'Skill. (20...30 seconds). Gain a random Asura benefit every time you earn experience from killing an enemy.'),
    ('asuran_scan', 'Asuran Scan', 'Asura', 'Unlock_asuran_scan', 'Hex Spell. (9...12 seconds.) You cannot miss target foe. If you kill this foe, you lose 5% Death Penalty.'),
    ('Mental_Block', 'Mental Block', 'Asura', 'Unlock_mental_block', 'Enchantment Spell. (5...11 seconds.) You have a 50% chance to block. Renewal: every time an enemy hits you.'),
    ('mindbender', 'Mindbender', 'Asura', 'Unlock_mindbender', 'Enchantment Spell. (10...16 seconds.) You move 20...33% faster and cast Spells 20% faster.'),
    ('pain_inverter', 'Pain Inverter', 'Asura', 'Unlock_pain_inverter', 'Hex Spell. (6...10 seconds.) Deals 100...140% of the damage (maximum 80) back to target foe every time it does damage.'),
    ('radiation_field', 'Radiation Field', 'Asura', 'Unlock_radiation_field', 'Ward Spell. (5 seconds.) Causes -4...6 Health degeneration to foes in the area. End effect: inflicts Disease condition (12...20 seconds) to foes in the area.'),
    ('smooth_criminal', 'Smooth Criminal', 'Asura', 'Unlock_smooth_criminal', 'Spell. (10...20 seconds.) Disables one Spell. This skill becomes that Spell. You gain 5...10 Energy.'),
    ('summon_ice_imp', 'Summon Ice Imp', 'Asura', 'Unlock_summon_ice_imp', 'Spell. Summon a level 14...20 Ice Imp (40...60 lifespan) that has Ice Spikes. Only 1 Asura Summon can be active a time.'),
    ('summon_mursaat', 'Summon Mursaat', 'Asura', 'Unlock_summon_mursaat', 'Spell. Summon a level 14...20 Mursaat (40...60 lifespan) that has Enervating Charge. Only 1 Asura Summon can be active a time.'),
    ('summon_naga_shaman', 'Summon Naga Shaman', 'Asura', 'Unlock_summon_naga_shaman', 'Spell. Summon a level 14...20 Naga Shaman (40...60 lifespan) that has Stoning. Only 1 Asura Summon can be active a time.'),
    ('summon_ruby_djinn', 'Summon Ruby Djinn', 'Asura', 'Unlock_summon_ruby_djinn', 'Spell. Summon a level 14...20 Ruby Djinn (40...60 lifespan) that has Immolate. Only 1 Asura Summon can be active a time.'),
    ('technobabble', 'Technobabble', 'Asura', 'Unlock_technobabble', 'Spell. Deals 30...40 damage to target and adjacent foes. Inflicts Dazed condition (3...5 seconds) on these foes if target was not a boss.'),

    ('deft_strike', 'Deft Strike', 'Vanguard', 'Unlock_deft_strike', 'Ranged Attack. Deals 18...30 damage. Inflicts Bleeding condition (18...30 seconds) if target foe has Cracked Armor.'),
    ('ebon_battle_standard_of_courage', 'Ebon Battle Standard of Courage', 'Vanguard', 'Unlock_ebon_battle_standard_of_courage', 'Ward Spell. (14...20 seconds.) Allies in this ward have +24 armor and +24 more armor against Charr. Spirits are unaffected.'),
    ('ebon_battle_standard_of_honor', 'Ebon Battle Standard of Honor', 'Vanguard', 'Unlock_ebon_battle_standard_of_honor', 'Ward Spell. (14...20 seconds.) Allies in this ward deal +8...15 damage and +7...10 more damage against Charr. Spirits are unaffected.'),
    ('ebon_battle_standard_of_wisdom', 'Ebon Battle Standard of Wisdom', 'Vanguard', 'Unlock_ebon_battle_standard_of_wisdom', 'Ward Spell. (14...20 seconds.) Spells that allies in this ward cast have a 44...60% chance to recharge 50% faster. Spirits are unaffected.'),
    ('ebon_escape', 'Ebon Escape', 'Vanguard', 'Unlock_ebon_escape', 'Spell. Heals you and target ally for 70...110. Initial effect: Shadow Step to this ally. Cannot self-target.'),
    ('ebon_vanguard_assassin_support', 'Ebon Vanguard Assassin Support', 'Vanguard', 'Unlock_ebon_vanguard_assassin_support', 'Spell. Summon a level 14...20 assassin that has Iron Palm, Fox Fangs, and Nine Tail Strike; it Shadow Steps to this foe. If this foe is a Charr, the assassin lives for 24...30 seconds.'),
    ('ebon_vanguard_sniper_support', 'Ebon Vanguard Sniper Support', 'Vanguard', 'Unlock_ebon_vanguard_sniper_support', 'Spell. Deals 54...90 piercing damage and inflicts Bleeding condition (5...25 seconds). 10% chance of big bonus damage; more if target is a Charr.'),
    ('signet_of_infection', 'Signet of Infection', 'Vanguard', 'Unlock_signet_of_infection', 'Signet. Inflicts Diseased condition 13...20 seconds if target foe is Bleeding.'),
    ('sneak_attack', 'Sneak Attack', 'Vanguard', 'Unlock_sneak_attack', 'Melee Attack. Inflicts Blindness (5...8 seconds). Counts as a lead attack.'),
    ('tryptophan_signet', 'Tryptophan Signet', 'Vanguard', 'Unlock_tryptophan_signet', 'Signet. (14...20 seconds.) Target and adjacent foes move and attack 23...40% slower.'),
    ('weakness_trap', 'Weakness Trap', 'Vanguard', 'Unlock_weakness_trap', 'Trap. (90 seconds.) Affects nearby foes. Deals 24...50 lightning damage. Inflicts Weakness (10...20 seconds). Knocks-down Charr.'),
    ('winds', 'Winds', 'Vanguard', 'Unlock_winds', 'Ebon Vanguard Ritual. Creates a spirit (54...90 seconds). Affects foes within range. 15% chance to miss with ranged attacks.'),

    ('dodge_this', '"Dodge This!"', 'Norn', 'Unlock_dodge_this', 'Shout. (16...20 seconds.) Your next attack is unblockable and deals +14...20 damage.'),
    ('finish_him', '"Finish Him!"', 'Norn', 'Unlock_finish_him', 'Shout. Deals 44...80 damage and inflicts Cracked Armor and Deep Wound (12...20 seconds). No effect unless target < 50% HP.'),
    ('i_am_unstoppable', '"I Am Unstoppable!"', 'Norn', 'Unlock_i_am_unstoppable', 'Shout. (16...20 seconds.) You have +24 armor and cannot be knocked-down or Crippled.'),
    ('i_am_the_strongest', '"I Am the Strongest!"', 'Norn', 'Unlock_i_am_the_strongest', 'Shout. Your next 5...8 attacks deal +14...20 damage.'),
    ('you_are_all_weaklings', '"You Are All Weaklings!"', 'Norn', 'Unlock_you_are_all_weaklings', 'Shout. Inflicts Weakness (8...12 seconds). Also affects adjacent foes.'),
    ('you_move_like_a_dwarf', '"You Move Like a Dwarf!"', 'Norn', 'Unlock_you_move_like_a_dwarf', 'Shout. Deals 44...80 damage, knock-down, and inflicts Crippled (8...15 seconds).'),
    ('a_touch_of_guile', 'A Touch of Guile', 'Norn', 'Unlock_a_touch_of_guile', 'Touch Hex Spell. Deals 44...80 damage. Target cannot attack (5...8 seconds) if it was knocked-down.'),
    ('club_of_a_thousand_bears', 'Club of a Thousand Bears', 'Norn', 'Unlock_club_of_a_thousand_bears', 'Melee Attack. Deals +6...9 damage for each adjacent foe (max 60). Causes knock-down if target is non-human.'),
    ('feel_no_pain', 'Feel No Pain', 'Norn', 'Unlock_feel_no_pain', 'Skill. (30 seconds.) +2...3 regen. +200...300 max HP if drunk when activated.'),
    ('raven_blessing', 'Raven Blessing', 'Norn', 'Unlock_raven_blessing', 'Elite Form. Raven aspect (60 seconds). Attributes set to 0; replaces skills; 80 armor, ~660-700 HP.'),
    ('ursan_blessing', 'Ursan Blessing', 'Norn', 'Unlock_ursan_blessing', 'Elite Form. Bear aspect (60 seconds). Attributes set to 0; replaces skills; 100 armor, ~750-800 HP.'),
    ('volfen_blessing', 'Volfen Blessing', 'Norn', 'Unlock_volfen_blessing', 'Elite Form. Wolf aspect (60 seconds). Attributes set to 0; replaces skills; 80 armor, ~660-700 HP.'),

    ('by_urals_hammer', '"By Ural\'s Hammer!"', 'Deldrimor', 'Unlock_by_ural_s_hammer', 'Shout. (30 seconds.) Rez party in earshot with full HP/E. Party deals +25...33% dmg. They die when it ends (no DP).'),
    ('don_t_trip', '"Don\'t Trip!"', 'Deldrimor', 'Unlock_don_t_trip', 'Shout. (3...5 seconds.) Prevents knock-down; affects party within earshot.'),
    ('alkars_alchemical_acid', "Alkar's Alchemical Acid", 'Deldrimor', 'Unlock_alkar_s_alchemical_acid', 'Spell. Projectile: deals 40...50 damage. Deals extra vs Destroyers and inflicts Cracked Armor (14...20 seconds).'),
    ('black_powder_mine', 'Black Powder Mine', 'Deldrimor', 'Unlock_black_powder_mine', 'Trap. (90 seconds.) Deals 20...30 dmg. Inflicts Blindness and Bleeding (7...10 seconds).'),
    ('brawling_headbutt', 'Brawling Headbutt', 'Deldrimor', 'Unlock_brawling_headbutt', 'Touch Skill. Deals 45...70 damage; causes knock-down.'),
    ('breath_of_the_great_dwarf', 'Breath of the Great Dwarf', 'Deldrimor', 'Unlock_breath_of_the_great_dwarf', 'Spell. Removes burning and heals for 50...60 Health. Affects party members.'),
    ('drunken_master', 'Drunken Master', 'Deldrimor', 'Unlock_drunken_master', 'Stance. (72...90 seconds.) Move/attack faster; more if drunk.'),
    ('dwarven_stability', 'Dwarven Stability', 'Deldrimor', 'Unlock_dwarven_stability', 'Enchantment. (24...30 seconds.) Stances last longer. Cannot be knocked down if activated while drunk.'),
    ('ear_bite', 'Ear Bite', 'Deldrimor', 'Unlock_ear_bite', 'Touch. Deals 50...70 piercing dmg and inflicts Bleeding (15...25 seconds).'),
    ('great_dwarf_armor', 'Great Dwarf Armor', 'Deldrimor', 'Unlock_great_dwarf_armor', 'Enchantment. +24 armor and +60 max HP; extra vs Destroyers.'),
    ('great_dwarf_weapon', 'Great Dwarf Weapon', 'Deldrimor', 'Unlock_great_dwarf_weapon', 'Weapon Spell. +15...20 dmg and chance to KD. Cannot self-target.'),
    ('light_of_deldrimor', 'Light of Deldrimor', 'Deldrimor', 'Unlock_light_of_deldrimor', 'Spell. Holy dmg in area and pings hidden objects on compass.'),
    ('low_blow', 'Low Blow', 'Deldrimor', 'Unlock_low_blow', 'Touch. Deals 45...70 dmg. Extra dmg + Cracked Armor if target was knocked down.'),
    ('snow_storm', 'Snow Storm', 'Deldrimor', 'Unlock_snow_storm', "Spell. Deals cold damage each second (5 seconds). Hits foes adjacent to target's initial location."),
]


Skill = Tuple[
    str,
    str,
    str,
    str,
    Callable[[], BehaviorTree],
    str,
]


def _not_implemented_tree(label: str) -> BehaviorTree:
    def _log_warning() -> None:
        Py4GW.Console.Log(
            MODULE_NAME,
            f"{label}: routine not implemented yet.",
            Py4GW.Console.MessageType.Warning,
        )

    return BT.Sequence(
        name=f"{label} Not Implemented",
        children=[
            _action_tree(f"Log {label} Not Implemented", _log_warning),
            BT.Succeeder(name=f"Skip {label}"),
        ],
    )


def _resolve_unlock_fn(
    fn_name: str,
    label: str,
) -> Callable[[], BehaviorTree]:
    declaration = globals().get(fn_name)
    if callable(declaration):
        return declaration
    return lambda label=label: _not_implemented_tree(label)


def _build_skills() -> List[Skill]:
    return [
        (
            key,
            label,
            faction,
            f"SKILL:{faction}:{key}",
            _resolve_unlock_fn(fn_name, label),
            desc,
        )
        for key, label, faction, fn_name, desc in RAW_SKILLS
    ]


SKILLS: List[Skill] = _build_skills()
FACTIONS = ("Asura", "Vanguard", "Norn", "Deldrimor")


def InitializeBot() -> BehaviorTree:
    return BT.Sequence(
        name="Initialize Skills Unlocker",
        children=[
            _runtime_combat_tree(True),
            BT.LogMessage(
                message="Skills Unlocker BT ready.",
                module_name=MODULE_NAME,
            ),
        ],
    )


def _is_selected_skill(step_name: str, label: str) -> BehaviorTree:
    return BehaviorTree(
        BehaviorTree.ConditionNode(
            name=f"Selected Skill: {label}",
            condition_fn=lambda: selected_skill_step == step_name,
        )
    )


def RunSelectedSkill() -> BehaviorTree:
    return BT.Selector(
        name="Selected Skill Router",
        children=[
            BT.Sequence(
                name=f"Unlock {faction} - {label}",
                children=[
                    _is_selected_skill(step_name, label),
                    tree_builder(),
                ],
            )
            for _, label, faction, step_name, tree_builder, _ in SKILLS
        ],
    )


def get_execution_steps() -> list[tuple[str, Callable[[], BehaviorTree]]]:
    return [
        ("Initialize Bot", InitializeBot),
        ("Run Selected Skill", RunSelectedSkill),
    ]


def ensure_botting_tree() -> BottingTree:
    global botting_tree
    if botting_tree is None:
        botting_tree = BottingTree.Create(
            BOT_NAME,
            main_routine=get_execution_steps(),
            routine_name="SkillsUnlockerSequence",
            repeat=False,
            multi_account=False,
            configure_fn=lambda tree: tree.Config.ConfigureUpkeep(
                looting_enabled=False,
                resurrection_scroll=False,
                auto_inventory_handler_enabled=False,
                enable_party_wipe_recovery=False,
                heroai_state_logging=False,
            ),
        )
    return botting_tree


def _start_skill(step_name: str) -> None:
    global selected_skill_step
    selected = next((skill for skill in SKILLS if skill[3] == step_name), None)
    if selected is None:
        Py4GW.Console.Log(
            MODULE_NAME,
            f"Unknown skill step: {step_name}",
            Py4GW.Console.MessageType.Error,
        )
        return

    selected_skill_step = step_name
    tree = ensure_botting_tree()
    if tree.IsStarted():
        tree.Stop()
    tree.RestartFromNamedPlannerStep(
        "Run Selected Skill",
        auto_start=True,
    )


def draw_portal_ui() -> None:
    PyImGui.separator()
    PyImGui.text("Select Skill:")

    if PyImGui.begin_tab_bar("SU_Factions"):
        for faction in FACTIONS:
            if PyImGui.begin_tab_item(faction):
                _draw_skill_grid(faction)
                PyImGui.end_tab_item()
        PyImGui.end_tab_bar()


def _draw_skill_grid(faction: str) -> None:
    entries = [skill for skill in SKILLS if skill[2] == faction]
    if not entries:
        PyImGui.text("No Skill")
        return

    icon_size = 48
    columns = 4
    icon_count = 0

    for key, label, _faction, step_name, _tree_builder, desc in entries:
        icon_path = os.path.join(ICONS_PATH, f"{key}.png")
        has_icon = os.path.exists(icon_path)

        if has_icon:
            clicked = ImGui.ImageButton(
                f"##{key}",
                icon_path,
                icon_size,
                icon_size,
            )
        else:
            clicked = PyImGui.button(label, 260, 40)

        if clicked:
            _start_skill(step_name)

        if PyImGui.is_item_hovered():
            PyImGui.begin_tooltip()
            PyImGui.text(label)
            PyImGui.separator()
            PyImGui.text_wrapped(step_name)
            PyImGui.separator()
            PyImGui.text_wrapped(desc)
            PyImGui.end_tooltip()

        if has_icon:
            icon_count += 1
            if icon_count % columns != 0:
                PyImGui.same_line(0.0, -1.0)


def main() -> None:
    global initialized
    tree = ensure_botting_tree()
    initialized = True
    tree.tick()
    tree.UI.draw_window(
        icon_path=TEXTURE,
        main_child_dimensions=(350, 420),
        additional_ui=draw_portal_ui,
    )


if __name__ == "__main__":
    main()